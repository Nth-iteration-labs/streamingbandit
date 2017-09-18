split = self.action['split']
y = self.action['y']
revenue = self.reward['revenue']

# Logging the data is very important now!
import time

self.log_data({
    "time" : int(time.time()),
    "split" : split,
    "y" : y,
    "revenue" : revenue
})
