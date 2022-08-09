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

#### Crawler Id file
crawler_id_file_name = os.environ['CRAWLER_ID_FILE_NAME'] if 'CRAWLER_ID_FILE_NAME' in os.environ else "crawlerId.json"

######################### Main Program #####################
def main():

	crawlerIds = {}
	if os.path.exists(crawler_id_file_name):
		with open(crawler_id_file_name) as json_file:
			input_json_value = json.load(json_file)
			if input_json_value and len(input_json_value) > 0:
				for crawler in input_json_value:
					if "name" in crawler and crawler["name"] and "crawlerId" and crawler["crawlerId"]: 
						crawlerIds[crawler["name"]] = crawler["crawlerId"]


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
                                   'CrawlerIds': crawlerIds[edge['name']] if edge['name'] in crawlerIds else '',
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
