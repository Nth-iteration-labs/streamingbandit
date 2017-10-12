split = self.action['split']
discount = self.action['discount']
revenue = self.reward['revenue']
import time
self.log_data({
    "time" : int(time.time()),
    "split" : split,
    "discount" : discount,
    "revenue" : revenue,
    })