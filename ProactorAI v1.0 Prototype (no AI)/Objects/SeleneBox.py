from Device import Device

class SeleneBox(Device):
    allowed_attributes = Device.allowed_attributes | {'SELENE_mtd_usage_gb'}
    
    def __init__(self, params): 
        super().__init__(params)
        raw_weights = {
            'SELENE_mtd_usage_gb': 1
        }
        self.weights = super().normalize_dev_weights(raw_weights)

    def health_check(self, mins, maxs):
        health = 0
        health += super().normalize(self.SELENE_mtd_usage_gb, mins['SELENE_mtd_usage_gb'], maxs['SELENE_mtd_usage_gb']) * self.weights['SELENE_mtd_usage_gb']

        return health