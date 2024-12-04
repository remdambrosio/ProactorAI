from Device import Device

class Modem(Device):
    allowed_attributes = Device.allowed_attributes | {'ZEUS_mtd_usage_bytes', 'NIKE_health_score'}
    
    def __init__(self, params): 
        super().__init__(params)
        raw_weights = {
            'ZEUS_mtd_usage_bytes': 1,
            'NIKE_health_score': 1
        }
        self.weights = super().normalize_dev_weights(raw_weights)

    def health_check(self, mins, maxs):
        health = 0

        if self.NIKE_health_score:
            health += super().normalize(self.NIKE_health_score, mins['NIKE_health_score'], maxs['NIKE_health_score']) * self.weights['NIKE_health_score']
        
        if self.ZEUS_mtd_usage_bytes:
            health += super().normalize(self.ZEUS_mtd_usage_bytes, mins['ZEUS_mtd_usage_bytes'], maxs['ZEUS_mtd_usage_bytes']) * self.weights['ZEUS_mtd_usage_bytes']

        return health