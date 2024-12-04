#
# Title: Puller.py
# Authors: Sofiia Khutorna, Rem D'Ambrosio
#

import sys
import os 
import json
import re
import csv

sys.path.append(os.path.abspath('/anon/path/for/APIwrappers'))
from ARESAPI import ARESAPI 
from NIKEAPI import NIKEAPI
from HESTIAAPI import HESTIAAPI
from SELENEAPI import SELENEAPI 
from ZEUSAPI import ZEUSAPI 


class Puller:
    def __init__(self, path):
        self.path = path + 'Raw'

    
    def pull_datariver(self):

        return

        
    def pull_api_data(self, processes):
        num_processes = processes
        pids = []
        for i in range(0, num_processes):
            pid = os.fork()
            if pid == 0:
                if i == 0:
                    self.pull_ARES_data()
                    print("...Pulled ARES...")
                elif i == 1:
                    self.pull_NIKE_data()
                    print("...Pulled NIKE...")
                elif i == 2:
                    self.pull_HESTIA_data()
                    print("...Pulled HESTIA...")
                elif i == 3:
                    self.pull_ZEUS_data()
                    print("...Pulled ZEUS...")
                elif i == 4:
                    self.pull_star_data()
                    print("...Pulled SELENE...")
                os._exit(0)
            else:
                pids.append(pid)
        
        for pid in pids:
            os.waitpid(pid, 0)
            
        return


    def pull_ARES_data(self):
        """
        Pulls data from ARES and saves it as (name: site_code, pin, snmp, temp etc) json
        """
        filepath = self.path + "/raw_ARES.json"
        ARES = ARESAPI()
        calc_function = "anon api call"
        get_function = "anon api call"
        queries = [calc_function, get_function]
        ARES_dict = {}
        for i, function in enumerate(queries):
            response = ARES.web_adb(function)
            reader = csv.reader(response.split('\n'), delimiter=',')
            for row in reader:
                if len(row) < 5: continue                       # if row is missing values, skip to the next loop
                match = re.search(r'anon-regex', row[0])
                if not match: continue                     

                name = match.group(1).upper()
                if name not in ARES_dict:
                    ARES_dict[name] = {}
                    ARES_dict[name]['site_code'] = match.group(2).upper()
                
                category = row[2]
                if re.search(r'anon', category): 
                    ARES_dict[name]["anon"] = row[5] 
                elif re.search(r'anon', category):
                    ARES_dict[name]["anon"] = row[5] 
                elif re.search(r'anon', category) or re.search(r'anon', category):
                    ARES_dict[name]["anon"] = row[4] 
                elif re.search(r'anon', category) and row[4]:
                    ARES_dict[name]["anon"] = row[4] 
                
        self.to_json(filepath, ARES_dict)
        
        return


    def pull_NIKE_data(self):
        """
        Pulls data from NIKE and saves it as dict with (modem_name: health_score)  
        """
        filepath = self.path + "/raw_NIKE.json"
        nc_data = {}
        NIKE = NIKEAPI()
        net_devices = NIKE.pull_net_devices()
        for device in net_devices.values():
            nc_name = device['anon']
            device_name = self.check_for_router_name(nc_name)
            if device_name and device['anon'] != 'anon':
                nc_id = device['anon']
                health_response = NIKE.pull_net_device_health(nc_id)
                health_result = health_response['anon']
                if health_result:
                    health_score = health_result[0]['anon']
                    nc_data['anon' + device_name] = {'anon':health_score}
        self.to_json(filepath, nc_data)
        return


    def pull_ZEUS_data(self):
        """
        Pulls data from ZEUS and saves it as dict with (modem_name: lte usage from the beginning of cur month)  
        """
        filepath = self.path + "/raw_ZEUS.json"
        ZEUS_data = {}
        ZEUS = ZEUSAPI()
        devices = ZEUS.pull_recent()

        for iccid in devices.keys():
            device_info = ZEUS.pull_device_info(iccid)
            ZEUS_name = device_info['anon']
            device_name = self.check_for_router_name(ZEUS_name)
            if device_name:
                usage_data = ZEUS.pull_current_usage(iccid)
                usage = usage_data['anon']
                ZEUS_data['anon' + device_name] = {'anon':usage}
                
        self.to_json(filepath, ZEUS_data)
        return


    def pull_star_data(self):
        """
        Pulls data from SELENE and saves it as dict with (star_name: usage in GB from the beginning of cur month to cur time)  
        """
        filepath = self.path + "/raw_star.json"
        star = SELENEAPI()
        star_data = {}

        page = 0
        last_page = False
        star_usage = {}
        while not last_page:
            response = star.get_data_usage_cycles(0, page)
            for result in response['anon']['anon']:
                sln = result['anon']
                cycle = result['anon'][0]
                usage = cycle['anon'] + cycle['anon'] + cycle['anon'] + cycle['anon']
                star_usage[sln] = {'anon':usage}
                if response['anon']['anon']:
                    last_page = True
            page += 1

        page = 0
        last_page = False
        while not last_page:
            lines = star.get_service_lines(page)
            for line in lines['anon']['anon']:
                if line['anon']:
                    sln = line['anon']
                    star_nickname = line['anon']
                    router_name = self.check_for_router_name(star_nickname)
                    if sln and router_name and (sln in star_usage):
                        star_data['anon' + router_name] = star_usage[sln]
            last_page = lines['anon']['anon']
            page += 1

        self.to_json(filepath, star_data)
        return


    def pull_HESTIA_data(self):
        filepath = self.path + "/raw_HESTIA.json"
        HESTIA = HESTIAAPI()
        HESTIA_data = {}

        routers = HESTIA.pull_routers()
        for router in routers:
            HESTIA_name = router['anon']
            router_name = self.check_for_router_name(HESTIA_name)
            if router_name:
                state = router['anon']
                id = router['anon']
                metrics = HESTIA.pull_mtd_metrics(id)
                if metrics and metrics[0]:
                    traffic = metrics[0]['anon']
                    up_score = metrics[0]['anon']
                    down_score = metrics[0]['anon']
                    HESTIA_data[router_name] = {'anon1':state, 'anon2':traffic,
                                              'anon3':up_score, 'anon4':down_score}

        self.to_json(filepath, HESTIA_data)
        return
        
 
    def check_for_router_name(self, string):
        """
        Checks if a string contains a valid router name
        Output: the router name (uppercase, excluding any other elements of input string), if it exists
        """
        if not string:
            return None

        input = string.upper()
        pattern = r'anon-regex'
        match = re.search(pattern, input)
        
        if match:
            return match.group(1)
        else:
            return None


    def to_file(self, filepath, data):
        file = open(filepath, "w")
        file.write(data)
        file.close()
        return


    def to_json(self, filepath, data):
        with open(filepath, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        return
