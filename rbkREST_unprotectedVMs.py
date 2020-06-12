#!/usr/bin/python3
#
# import our json module and our requests client and transport methods
import requests
import json
#
# <LAB USE> import urllib to handle self-signed certificate errors/warnings
import urllib3
from urllib3.exceptions import InsecureRequestWarning
# <LAB USE> disable the warning to keep screen cluter to a minimum
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
# import our api keys
with open('/home/chad/apiKeys.json', 'r') as keys:
    api_key = json.loads(keys.read())['Rubrik']['amer2']
authorized = 'Bearer ' + api_key
#
# define our baseURL - note that RESTful API's will have mutliple differing endpoints for differing request types
baseURL = "https://amer2-rbk01.rubrikdemo.com/api/"
#
#
# define a helper function to retrieve the cluster ID so we do not misinterpret replicated datasets as unprotected VM's
def get_clusterID():
    #
    # define our headers - note that RESTful API's could have multiple headers and are defined alongside the json request
    header = {'Accept': 'application/json', 'Authorization': authorized}
    #
    # define our specific API url - will change based on REST endpoint
    API_URL = baseURL + "v1/cluster/me"
    #
    # build the request transport - note that RESTful API requests will differ based on methods (get, post, patch, delete) and additional pararms, configs, etc
    response = requests.get(API_URL,headers=header, verify=False)
    #
    # recieve the response data and store it in a variable
    clusterID = response.json()['id']
    #
    # return the dataset to the user/code for further processing
    return clusterID
#
#
# define a function to handle our REST api call for VM data, feed it the clusterID to limit the scope of returned data
def get_vmware_vm_data(cID):
    #
    # limit the scope of the data request so that we do not count replicated VM's as locally protected VMs
    # somtimes the datawe get back from a REST call is irrelevent to our actual query
    params = (('primary_cluster_id', cID),)
    #
    # define our headers - note that RESTful API's could have multiple headers and are defined alongside the json request
    header = {'Accept': 'application/json', 'Authorization': authorized}
    #
    # define our specific API url - will change based on REST endpoint
    API_URL = baseURL + "v1/vmware/vm"
    #
    # build the request transport - note that RESTful API requests will differ based on methods (get, post, patch, delete) and additional pararms, configs, etc
    response = requests.get(API_URL,headers=header, params=params, verify=False)
    #
    # recieve the response data and store it in a variable
    data = response.json()['data']
    #
    # return the dataset to the user/code for further processing
    return data
#
#
# define a helper function to process our collected VM data and give us the information (unprotected VM count) we care about)
def count_unprotectedVMs(vm_data):
    #
    # establish a variable to store the number of unprotected VM's we discover within the dataset
    count = 0
    #
    # establish a list of VM's which have been identified as unprotected
    protected_vms = []
    unprotected_vms = []
    #
    # iterate over our dataset and find all the known PROTECTED VM's
    for obj in vm_data:
        #
        # iterate over our dataset and identify all of the known protected VM's for later validation
        # with REST calls, sometimes you are getting datasets you dont expect (like VM's that have been deleted then recreated
        # with the same name but different moid's
        if obj['effectiveSlaDomainId'] != "UNPROTECTED":
            protected_vms.append(obj['name'])
    #
    # iterate over our datset again looking for unprotected VM's that are not know to actually be protected
    for obj in vm_data:
    #
    # run boolean logic to make sure our VM is truly a VM (not a relic) and truly unprotected, increment a counter if it is..
        if obj['effectiveSlaDomainId'] == "UNPROTECTED" and not obj['name'] in protected_vms and not obj['isRelic']:
        #
        # add the vm to a list of known unprotected VMs
            unprotected_vms.append(obj['name'])
            #
            # increment our counter variable when we do identify an unprotected VM
            count += 1
    #
    # return the unprotected VM count to the user
    return count
#
#
#
#
# pythonic code initiation point (execute our functions defined above)
if __name__ == "__main__":
    #
    # execute a funtion call to retrieve the local cluster ID and ensure our datasets are relivent.
    clusterID = get_clusterID()
    #
    # Execute a function call to obtain a dataset about known/discovered VM's from the local cluster
    required_vm_data = get_vmware_vm_data(clusterID)
    #
    # execute a second function call to process the collected data and provide us with what we actuall want
    unprotectedVM_count = count_unprotectedVMs(required_vm_data)
    #
    # do stuff with the results
    print("\n     The current number of discovered but unprotected VM's is: ", unprotectedVM_count, "\n")