#
# Title: Checker.py 
# Authors: Sofiia Khutorna, Rem D'Ambrosio
# Created: 2024-11-22
# Description:  
# 
import sys
import os
import json

sys.path.append(os.path.abspath('/anon/path'))
from Site import Site

class Checker:
    def __init__(self, path):
        self.path = path
        with open(self.path+'/mins.json', 'r') as devices_sites:
            self.mins = json.load(devices_sites)
        with open(self.path+'/maxs.json', 'r') as devices_sites:
            self.maxs = json.load(devices_sites)


    def build_sites(self):
        sites_path = self.path + "Sites"
        sites = {} 
        for subfolder in os.listdir(sites_path):
            site_path = os.path.join(sites_path, subfolder)
            name = subfolder
            site = Site(site_path, self.mins, self.maxs)
            sites[name] = {'health':site.health, 'devices':site.devices}
   
        return sites

    def to_json(self, data):
        filepath = self.path + "Output/sites_health.json"
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return