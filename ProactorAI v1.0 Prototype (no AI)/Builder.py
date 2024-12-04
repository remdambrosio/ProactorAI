#
# Title: Builder.py  
# Authors: Sofiia Khutorna, Rem D'Ambrosio
# Created: 2024-11-15
# Description:  
# 

import json 
import os
import csv
import re

class Builder: 
    def __init__(self, path):
        self.path = path
        self.mins = {
            'ARES_latency' : float('inf'),
            'ARES_temp': float('inf'),
            'HESTIA_up_score': float('inf'),
            'HESTIA_down_score' : float('inf'),
            'NIKE_health_score': float('inf'),
            'jasper_mtd_usage_bytes': float('inf'),
            'star_mtd_usage_gb': float('inf')
        }
        self.maxs = {
            'ARES_latency' : 0,
            'ARES_temp' : 0,
            'HESTIA_up_score' : 0,
            'HESTIA_down_score' : 0,
            'NIKE_health_score' : 0,
            'jasper_mtd_usage_bytes' : 0,
            'star_mtd_usage_gb' : 0
        }
        with open(self.path+'Raw/devices&sites.json', 'r') as devices_sites:
            self.devices_sites = json.load(devices_sites)


    def create_site_folders(self): 
        sites_dir = self.path+"Sites/"
        try: 
            os.system(f'rm -r {sites_dir}')
        except:
            print("No site folders detected")
        os.mkdir(sites_dir)
        dev_types = ["Routers", "Switches", "APs", "Modems", "SeleneBoxes"]
        with open(self.path+"Raw/site_codes.csv", 'r') as file:
            reader = csv.reader(file)
            for row in reader:  
                folder_path = os.path.join(sites_dir, row[0])
                os.mkdir(folder_path)                                       # create a site folder
                for dev_type in dev_types:    
                    os.mkdir(os.path.join(folder_path, dev_type))    
        self.chmod_subfolders(sites_dir, 0o777)
        return


    def chmod_subfolders(self, directory, mode):
        os.chmod(directory, mode)
        for dirpath, dirnames, filenames in os.walk(directory):
            for dirname in dirnames:
                os.chmod(os.path.join(dirpath, dirname), mode)
            for filename in filenames:
                os.chmod(os.path.join(dirpath, filename), mode)
        return


    def build_routers(self): 
        routers = {}
        with open(self.path+'Raw/raw_ARES.json', 'r') as ARES_file:
            ARES_info = json.load(ARES_file)
        for name, info in ARES_info.items():
            if re.search(r'anon-regex', name):
                routers[name] = {}
                routers[name]['anon'] = name
                for key, val in info.items():
                    new_key = 'ARES_' + key
                    if new_key in self.mins and val:
                        val = float(val)
                        if val < self.mins[new_key]:
                            self.mins[new_key] = val
                        if val > self.maxs[new_key]:
                            self.maxs[new_key] = val
                    routers[name][new_key] = val
        with open(self.path+'Raw/raw_HESTIA.json', 'r') as HESTIA_file:
            HESTIA_info = json.load(HESTIA_file) 
            
        for name, info in HESTIA_info.items():
            if name not in routers:
                routers[name] = {}
                routers[name]['anon'] = name
            for key, val in info.items():
                    new_key = 'HESTIA_' + key
                    if new_key in self.mins:
                        if val < self.mins[new_key]:
                            self.mins[new_key] = val
                        if val > self.maxs[new_key]:
                            self.maxs[new_key] = val
                    routers[name][new_key] = val
        self.device_to_site("Routers", routers)
        return


    def build_switches(self):
        switches = {}
        with open(self.path+'Raw/raw_ARES.json', 'r') as ARES_file:
            ARES_info = json.load(ARES_file)
        for name, info in ARES_info.items():
            if re.search(r'anon-regex', name):
                switches[name] = {}
                switches[name]['anon'] = name
                for key, val in info.items():
                    new_key = 'ARES_' + key
                    if new_key in self.mins and val:
                        val = float(val)
                        if val < self.mins[new_key]:
                            self.mins[new_key] = val
                        if val > self.maxs[new_key]:
                            self.maxs[new_key] = val
                    switches[name][new_key] = val
        self.device_to_site("Switches", switches)
        return
        

    def build_aps(self): 
        aps = {}
        with open(self.path+'Raw/raw_ARES.json', 'r') as ARES_file:
            ARES_info = json.load(ARES_file)
        for name, info in ARES_info.items():
            if re.search(r'anon-regex', name):
                aps[name] = {}
                aps[name]['anon'] = name
                for key, val in info.items():
                    new_key = 'ARES_' + key
                    if new_key in self.mins and val:
                        val = float(val)
                        if val < self.mins[new_key]:
                            self.mins[new_key] = val
                        if val > self.maxs[new_key]:
                            self.maxs[new_key] = val
                    aps[name][new_key] = val
        self.device_to_site("APs", aps)
        return


    def build_modems(self):
        modems = {}
        with open(self.path+'Raw/raw_jasper.json', 'r') as jasper_file:
            jasper_info = json.load(jasper_file)
        for name, info in jasper_info.items():
            modems[name] = {}
            modems[name]['anon'] = name
            for key, val in info.items():
                new_key = 'jasper_'+key
                if new_key in self.mins:
                    if val < self.mins[new_key]:
                        self.mins[new_key] = val
                    if val > self.maxs[new_key]:
                        self.maxs[new_key] = val
                modems[name][new_key] = val
        
        with open(self.path+'Raw/raw_NIKE.json', 'r') as NIKE_file:
            NIKE_info = json.load(NIKE_file)
        for name, info in NIKE_info.items():
            if name not in modems:
                modems[name] = {}
            for key, val in info.items():
                new_key = 'NIKE_'+key
                if new_key in self.mins:
                    if val < self.mins[new_key]:
                        self.mins[new_key] = val
                    if val > self.maxs[new_key]:
                        self.maxs[new_key] = val
                modems[name][new_key] = val

        self.device_to_site("Modems", modems)
        return
    
    
    def build_seleneboxes(self):
        seleneboxes = {}
        with open(self.path+'Raw/raw_star.json', 'r') as star_file:
            star_info = json.load(star_file)
        for name, info in star_info.items():
            seleneboxes[name] = {}
            seleneboxes[name]['anon'] = name
            for key, val in info.items():
                new_key = 'star_'+key
                if new_key in self.mins:
                    if val < self.mins[new_key]:
                        self.mins[new_key] = val
                    if val > self.maxs[new_key]:
                        self.maxs[new_key] = val
                seleneboxes[name][new_key] = val

        self.device_to_site("SeleneBoxes", seleneboxes)
        return


    def device_to_site(self, device_type, devices):
        for name, info in devices.items():
            if name in self.devices_sites:
                site_name = self.devices_sites[name]
                device_name = name + '.json'
                filepath = os.path.join(self.path+"Sites/", site_name, device_type, device_name)
                self.to_json(filepath, info)
        return


    def save_range(self):
        self.to_json(self.path+"mins.json", self.mins)
        self.to_json(self.path+"maxs.json", self.maxs)


    def to_json(self, filepath, data):
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return