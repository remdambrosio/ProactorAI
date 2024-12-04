#
# Title: Reporter.py 
# Authors: Sofiia Khutorna, Rem D'Ambrosio
# Created: 2024-11-22
# Description:

import csv
import json

class Reporter:
    def __init__(self, path):
        self.path = path
        with open(self.path+'/sites_health.json', 'r') as json_data:
            self.sites = json.load(json_data)


    def create_report(self):
        report = []
        for site_code, info in self.sites.items():
            simple_site = {
                "Site Name": site_code,
                "Site Health": info['health']
            }

            for dev_type, dev_list in info['devices'].items():
                dev_count = len(dev_list)
                if dev_count == 0:
                    simple_site[dev_type+' Count'] = 0
                    simple_site['Avg '+dev_type+' Health'] = None
                else:
                    simple_site[dev_type+' Count'] = dev_count
                    total_dev_health = sum([dev[1] for dev in dev_list])
                    avg_dev_health = total_dev_health / dev_count
                    simple_site['Avg '+dev_type+' Health'] = avg_dev_health

            report.append(simple_site)

        return report


    def to_csv(self, report):
        with open(self.path+'Output/report.csv', 'w', newline='') as file:
            fieldnames = ['Site Name', 'Site Health',
                            'Routers Count', 'Avg Routers Health',
                            'Switches Count', 'Avg Switches Health',
                            'APs Count', 'Avg APs Health',
                            'Modems Count', 'Avg Modems Health',
                            'SeleneBoxes Count', 'Avg SeleneBoxes Health']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for site in report:
                writer.writerow(site)