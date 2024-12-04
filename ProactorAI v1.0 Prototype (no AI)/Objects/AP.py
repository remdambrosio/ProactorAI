from Device import Device

class AP(Device):  
    allowed_attributes = Device.allowed_attributes | {'ARES_ping', 'ARES_latency'}

    def __init__(self, params): 
        super().__init__(params)
        raw_weights = {
            'ARES_ping': 1, 
            'ARES_latency': 1
        }
        self.weights = super().normalize_dev_weights(raw_weights)


    def health_check(self, mins, maxs):
        health = 0

        if self.ARES_ping and self.ARES_ping == 'up':
            health += self.weights['ARES_ping']

        if self.ARES_latency and self.ARES_latency != 0:
            health += self.weights['ARES_latency'] - (super().normalize(self.ARES_latency, mins['ARES_latency'], maxs['ARES_latency']) * self.weights['ARES_latency'])
    
        return health