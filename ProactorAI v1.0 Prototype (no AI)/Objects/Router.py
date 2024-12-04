from Device import Device

class Router(Device):
    allowed_attributes = Device.allowed_attributes | {
        'HESTIA_mtd_usage_bytes', 'HESTIA_up_score', 'HESTIA_down_score', 'HESTIA_state', 
        'ARES_ping', 'ARES_snmp', 'ARES_latency'
        }

 
    def __init__(self, params):
        super().__init__(params) 
        raw_weights = {
            'HESTIA_mtd_usage_bytes': 1,
            'HESTIA_up_score': 1,
            'HESTIA_down_score': 1,
            'HESTIA_state': 1,         
            'ARES_ping': 1,
            'ARES_snmp': 1,
            'ARES_latency': 1
        }
        self.weights = super().normalize_dev_weights(raw_weights)


    def health_check(self, mins, maxs):
        health = 0

        if self.HESTIA_state == 'CONNECTED':
            health += self.weights['HESTIA_state']
        if self.ARES_ping == 'up':
            health += self.weights['ARES_ping']
        if self.ARES_snmp == 'up':
            health += self.weights['ARES_snmp']
        if self.HESTIA_mtd_usage_bytes != 0:
            health += self.weights['HESTIA_mtd_usage_bytes']

        if self.ARES_latency and self.ARES_latency != 0:
            health += self.weights['ARES_latency'] - (super().normalize(self.ARES_latency, mins['ARES_latency'], maxs['ARES_latency']) * self.weights['ARES_latency'])
            
        health += super().normalize(self.HESTIA_up_score, mins['HESTIA_up_score'], maxs['HESTIA_up_score']) * self.weights['HESTIA_up_score']
        health += super().normalize(self.HESTIA_down_score, mins['HESTIA_down_score'], maxs['HESTIA_down_score']) * self.weights['HESTIA_down_score']
       
        return health
