class Device:
    allowed_attributes = {'name', 'site_code', 'device_health'}

    def __init__(self, params): 
        self.update_device(params)
         

    def update_device(self, params):

        for key in self.allowed_attributes:
            if key in params:
                setattr(self, key, params[key])
            else:
                setattr(self, key, None)

        return


    def normalize_dev_weights(self, weights):
        total = sum(weights.values())
        return {key: val / total for key, val in weights.items()}


    def normalize(self, x, x_min, x_max):
        return ((x - x_min) / (x_max - x_min))
