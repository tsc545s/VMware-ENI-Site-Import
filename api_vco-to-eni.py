#!/usr/bin/env python3
# author: vfrancadesou@vmware.com
# Simple Python Script that uses vmware sd-wan orchestrator api to create a csv file with edge list ready for ENI import

import os
import sys
import requests
import json
import csv

### VCO info and credentials
token = "Token %s" %(os.environ['VCO_TOKEN'])
vco_url = 'https://' + os.environ['VCO_HOSTNAME'] + '/portal/rest/'
headers = {"Content-Type": "application/json", "Authorization": token}
### VCO API METHODS
get_enterprise = vco_url + 'enterprise/getEnterprise'
get_edgelist = vco_url+'enterprise/getEnterpriseEdgeList'

######################### Main Program #####################
def main():
	enterprise = requests.post(get_enterprise, headers=headers, data='')
	ent_j = enterprise.json()
	eid=ent_j['id']
	ename=ent_j['name']
	enamenospace=ename.replace(" ", "")
	params = {'enterpriseId': eid, 'with': ['site', 'licenses']}
	edgesList = requests.post(get_edgelist, headers=headers, data=json.dumps(params))
	eList_dict=edgesList.json()
	site_array = []
	for edge in eList_dict:
            site_array.append({'name': edge['name'],
                                   'CrawlerIds': '',
                                   'ControllerIps': '',
                                   'Subnets': '',
                                   'APs': '',
                                   'Lat': edge['site']['lat'],
                                   'Lng': edge['site']['lon'],
                                   'Place name': '',
                                   'Ignore?': 'FALSE'})
            with open(f'edge_dump-{enamenospace}.csv', 'w') as f:
                writer = csv.DictWriter(f, fieldnames=site_array[0].keys())
                writer.writeheader()
                writer.writerows(site_array)
	print("CSV File Created")
if __name__ == "__main__":
        main()
