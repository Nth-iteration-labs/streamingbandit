import redis
import yaml
import random

class Database:
    """ This database is written in Redis. If other types of database are used,
    they should at least contain the same functions and functionality as the
    functions in this class.
    """
    def __init__(self):
        f = open("config.cfg",'r')
        settings = yaml.load(f)
        self.r_server = redis.Redis(settings['redis_ip'], settings['redis_port'], decode_responses=True)
        f.close()
        
    def set_theta(self, thetas, key):
        """ Set theta's in the database

        :param dict values: The values of the theta to be stored.
        :param string key_prefix: The key prefix for the stored theta.
        Typically this is something as: "exp:1:theta"
        :param dict context: The context for this specific theta.
        :param dict action: The action for this specific theta.
        :param bool all_action: If true, the theta that is saved with the
        specific context in the name of the key will be retrieved.
        :param bool all_context: If true, the theta that is saved with the
        specific action in the name of the key will be retrieved.
        :param bool all_float: If true, all parameters will be returned as a
        float.

        :returns bool: True if succeeded (perhaps needs better error handling).
        """
        # Store the object fully nested:
        self.r_server.hmset(key, thetas)  
        # should contain error checking:
        return True

    def get_theta(self, key, all_values = False, all_float = False):
        """ Retrieve theta's from the database

        :param string key_prefix: The key prefix for the stored theta.
        Typically this is something as: "exp:1:theta"
        :param dict context: The context for this specific theta.
        :param dict action: The action for this specific theta.
        :param bool all_action: If true, the theta that is saved with the
        specific context in the name of the key will be retrieved.
        :param bool all_context: If true, the theta that is saved with the
        specific action in the name of the key will be retrieved.
        :param bool all_float: If true, all parameters will be returned as a
        float.

        :returns dict result: A dictionary with all the paramaters.
        For example:
        {
            A : 1.23,
            B : 4.56
        }
        """
        result = {}
        if all_values == False:
            result = self.r_server.hgetall(key)
        else:
            number_of_keys = 0
            for obj in self.r_server.scan_iter(key + "*"):
                number_of_keys += 1
            if number_of_keys > 1:
                for obj in self.r_server.scan_iter(key + "*"):
                    final_key = obj[len(key)+1:]
                    result[final_key] = self.r_server.hgetall(obj)
            else:
                result = self.r_server.hgetall(key)
        
        if all_float: #check
            for i in result.keys():
                if(type(result[i])==dict):
                    for j in result[i].keys():
                        result[i][j] = float(result[i][j]) 
                else:
                    result[i] = float(result[i])
                
        return result
    
    def delete_theta(self, key):
        count = 0
        key = key + '*'
        for k in self.r_server.scan_iter(key):
            self.r_server.delete(k)
            count += 1
        return count
        #return True

    def object_to_key(self, obj):   
        """ Converts an object to a redis key-style string.

        :param dict obj: Dictionary with the objects.

        Example: If dict is context and looks like:
        {
            age : 20,
            gender : "male"
            country : "NL"
            language : "EN"
        }

        The output will look as follows:
        age:20:gender:male:country:NL:language:EN
        """
        s = ""
        if obj != None:
            for key, value in sorted(obj.items()):
                s =  s + ":" + str(key) + ":" + str(value)
        return s

    def simple_query(self, querystr):
        return self.r_server.get(querystr)
    
    def experiment_properties(self, basestr, key):
        return self.r_server.hgetall(basestr)[key]
   
   
   ########################################################
   ## ADMIN CALLS:
   ########################################################
   
    def insert_experiment(self, obj, explistkey="admin:experiments"):
        """ Inserts a new experiment, in both the administrative list and a
        properties list.

        :param dict obj:
        :param string explistkey: 
        :return int exp_id: Returns the exp_id that now belongs to this
        experiment.
        """
        members = self.r_server.smembers(explistkey)
        exp_id = hex(random.getrandbits(42))[2:-1]
        self.r_server.sadd(explistkey, exp_id)
        self.r_server.hmset("exp:%s:properties" % exp_id, obj)
        return(exp_id)
    
    def edit_experiment(self, obj, exp_id,  explistkey="admin:experiments"):
        """ Re-adds the experiment and the properties.
        
        :param dict obj: The objects of the properties of the experiment (such
        as key and code).
        :param int exp_id: The concerning experiment id.
        :param string explistkey: Set to standarda value. Typically redundant.
        :returns int exp_id: Simply returns the exp_id as a sort of "true"
        statement.
        """
        obj["active"] = 1
        self.r_server.hmset("exp:%s:properties" % exp_id, obj)
        return(exp_id)
        
    def delete_experiment(self, exp_id, explistkey="admin:experiments"):
        """ Delete an experiment from the list and delete the properties.

        :param int exp_id: The id of the experiment that will be deleted.
        :param string explistkey: Set to standard value. Typically redundant.
        :returns int exp_id: Simply returns the exp_id as a sort of "true"
        statement.
        """
        self.r_server.srem(explistkey, exp_id)
        self.r_server.delete("exp:%s:properties" % exp_id)
        return(exp_id)
        
    def get_all_experiments(self, user_id, explistkey="admin:experiments"):
        """ Returns a dict of experiment properties, so a dict of dicts.

        :param string explistkey: Set to standard value. Typically redundant.
        :return dict: A dict of dict of all experiment properties
        """
        # This currently returns all the properties, we might change that:
        members = self.r_server.smembers(explistkey)
        result = {}
        for member in members:
            tmp_result = self.r_server.hgetall("exp:%s:properties" % (member))
            if int(tmp_result['user_id']) == user_id:
                result[member] = tmp_result.copy()
        return result
        
    def get_one_experiment(self, exp_id, explistkey="admin:experiments"):   
        """ Returns the properties of one experiment

        :param int exp_id: The experiment id of which the properties are
        wanted.
        :param string explistkey: Set to standard value. Typically redundant.
        :returns dict: A dictionary of all the properties (such as the code,
        keys et cetera.
        """
        result = self.r_server.hgetall("exp:%s:properties" % (exp_id))
        return result

    def get_experiment_ids(self, explistkey="admin:experiments"):
        """ Returns a list with experiment ids

        :param string explistkey: Set to standard value. If set to something
        different this can be changed, but mostly is redundant.
        """
        return self.r_server.smembers(explistkey)
