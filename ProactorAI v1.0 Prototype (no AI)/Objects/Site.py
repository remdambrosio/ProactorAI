import json
import sys
import os 

sys.path.append(os.path.abspath('/anon/path'))
from Router import Router 
from Switch import Switch
from AP import AP
from Modem import Modem
from SeleneBox import SeleneBox


class Site:
    def __init__(self, path, mins, maxs):
        self.path = path
        self.mins = mins
        self.maxs = maxs
        raw_weights = {
            'Routers': 3,
            'Switches': 3,
            'APs': 1,
            'Modems': 2,
            'Starlinks': 2
        }
        self.devices = self.build_devices()
        self.weights = self.normalize_weights(raw_weights)
        self.health = self.health_check()


    def normalize_weights(self, weights):
        for device_type, devices in self.devices.items():
            if not devices:
                weights.pop(device_type)
        total = sum(weights.values())
        return {key: val / total for key, val in weights.items()}


    def build_devices(self):
        device_types = ['Routers', 'Switches', 'APs', 'Modems', 'SeleneBoxes']
        devices = {}
        for device_type in device_types:
            devices[device_type] = []
            device_type_path = os.path.join(self.path, device_type)
            for subfolder in os.listdir(device_type_path):
                device_path = os.path.join(device_type_path, subfolder)
                with open(device_path, 'r') as data:
                    params = json.load(data)
                device = None
                if device_type == 'Routers':
                    device = Router(params)
                elif device_type == 'Switches':
                    device = Switch(params)
                elif device_type == 'APs':
                    device = AP(params)
                elif device_type == 'Modems':
                    device = Modem(params)
                elif device_type == 'SeleneBoxes':
                    device = SeleneBox(params)
                device_health = device.health_check(self.mins, self.maxs)
                devices[device_type].append((device.name, device_health))
        return devices 


    def health_check(self):
        health = 0
        for device_type, device_list in self.devices.items():
            if device_list:
                device_type_health_total = 0                                            # get avg health for device type
                for device in device_list:
                    device_type_health_total += device[1]
                device_type_health_avg = device_type_health_total / len(device_list)
                health += device_type_health_avg * self.weights[device_type]            # weight it
        return health
