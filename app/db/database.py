import redis
import yaml

class Database:

    def __init__(self):
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        self.r_server = redis.Redis(settings['redis_ip'], settings['redis_port'], decode_responses=True)
        f.close()
        
    def set_theta(self, values, key_prefix, context = None, action=None, all_action=False, all_context=False):
        """ Set theta's
        """
        
        # Store the object fully nested:
        key = key_prefix + self.object_to_key(context) + self.object_to_key(action)
        self.r_server.hmset(key, values)  
        
        # Append to set of possible context and action combo's (basically create our own index)
        if all_action:
            key = key_prefix + self.object_to_key(context) + ":action:*"
            self.r_server.sadd(key, self.object_to_key(action)[1:])
        
        if all_context:
            key = key_prefix + self.object_to_key(action) + ":context:*"
            self.r_server.sadd(key, self.object_to_key(context)[1:])
        
        if all_action & all_context:
            key = key_prefix + ":context:*:action*"
            self.r_server.sadd(key, (self.object_to_key(context)+self.object_to_key(context))[1:])
        
        # should contain error checking:
        return True

    def get_theta(self, key_prefix, context = None, action=None, all_action=False, all_context=False, all_float=True):
        """ Retrieve theta's
        """
        #result = {}
        if not all_action and not all_context:
            key = key_prefix + self.object_to_key(context) + self.object_to_key(action) 
            result = self.r_server.hgetall(key)
        
        else:
            if all_action and not all_context:
                key = key_prefix + self.object_to_key(context) + ":action:*"
            if all_context and not all_action:
                key = key_prefix + self.object_to_key(action) + ":context:*"
            if all_action & all_context:
                key = key_prefix + ":context:*:action*"
            members = self.r_server.smembers(key)
            i = 0
            result = {}
            for member in members:
                result[member] = self.r_server.hgetall(key_prefix + ":" + member)
                i += 1
        
        if all_float:
            for i in result.keys():
                if(type(result[i])==dict):
                    for j in result[i].keys():
                        result[i][j] = float(result[i][j]) 
                else:
                    result[i] = float(result[i])
                
        return result
    
    def object_to_key(self, obj):   
        s = ""
        if obj != None:
            for key, value in sorted(obj.items()):
                s =  s + ":" + str(key) + ":" + str(value)
        return s

    def simple_query(self, querystr):
        return self.r_server.get(querystr)
    
    def experiment_properties(self, basestr, key):
        return self.r_server.hgetall(basestr)[key]
    
    ## ADMIN CALLS:
    def insert_experiment(self, obj, explistkey="admin:experiments"):
        # Find the length of the number of experiments:
        members = self.r_server.smembers(explistkey)
        exp_id = len(members) + 1
        
        # Add the experiment to the list of experiment:
        self.r_server.sadd(explistkey, exp_id)
 
        # Add the experiment to key exp:length++
        obj["active"] = 1  # Use for delete (never truly delete)
        self.r_server.hmset("exp:%s:properties" % exp_id, obj)
        
        # Return the ID of the experiment for future ref.
        return(exp_id)
    
    def edit_experiment(self, obj, exp_id,  explistkey="admin:experiments"):
        obj["active"] = 1
        self.r_server.hmset("exp:%s:properties" % exp_id, obj)
        return(exp_id)
        
    def get_all_experiments(self, explistkey="admin:experiments"):
        # This currently returns all the properties, we might change that:
        members = self.r_server.smembers(explistkey)
        i = 0         
        result = {}
        for member in members:
            result[member] = self.r_server.hgetall("exp:%s:properties" % (member))
            i += 1
        return result
        
    def get_one_experiment(self, exp_id, explistkey="admin:experiments"):   
        result = self.r_server.hgetall("exp:%s:properties" % (exp_id))
        return result
