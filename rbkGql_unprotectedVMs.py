#!/usr/bin/python3
#
# import our json module and our GraphQL client and transport methods
import json
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport as rht
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
#
# define our headers
header = {'Authorization': 'bearer {}'.format(api_key), 'Content-Type':'application/json'}
#
# build the API url endpoint - note that GQL API's will have a single endpoint for ALL queries and mutations
api_url = "https://amer2-rbk01.rubrikdemo.com/api/internal/graphql"
#
# build the request trandport - note that GQL will have single request trandport for all queries and mutations
transport = rht(url=api_url, verify=False, headers=header, use_json=True)
#
# create the client
client = Client(transport=transport, fetch_schema_from_transport=True)
#
# defube a function to get a count of unprotected VM's via GQL request
def get_unprotectedVM():
    #
    # execute the query and return the unprotected VM count to the user
    return client.execute(gql('''{vms{numUnprotected}}'''))
#
#
#
#
# pythonic code initiation point (execute our functions defined above)
if __name__ == "__main__":
    #
    # Execute a function call to obtain a count of our unprotected VM's
    data = get_unprotectedVM()
    #
    # do stuff with the results
    print("\n     The current number of discovered but unprotected VM's is: ", data['vms']['numUnprotected'],"\n")