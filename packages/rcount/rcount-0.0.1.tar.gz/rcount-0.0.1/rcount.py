"""
rcount: Redis-powered Counting, Ranking and Comparing

"""

__author__ = 'Ted Nyman'
__version__ = '0.0.1'
__license__ = 'MIT'

import redis
from operator import itemgetter

redis = redis.Redis()

### The Counter object. All else depends upon it. ###

class Counter(object):
    """A counter object"""
    def __init__(self, name):
        """One required argument: a name for the counter object"""
        #Create a unique global ID for the new counter object
        global_id = redis.incr("global_space")
        global_id_name = "global:%s" %global_id
        #Create a counter-specific (local) ID
        local_id = redis.incr("counter_space")
        id_name = "counter:%s:%s" %(local_id, name)
        self.id_name = id_name
        #Set the counter at 0
        redis.set(id_name, 0)

    def increase(self):
        """Increase the counter by one"""
        id_name = self.id_name
        increase = redis.incr(id_name)
        return increase

    def decrease(self):
        """Decrease the counter by one"""
        id_name = self.id_name
        decrease = redis.decr(id_name)
        return decrease

    def read(self):
        """Return the current value of the counter"""
        id_name = self.id_name
        read = redis.get(id_name)
        if read == None:
            return read
        else: 
            read = int(read)
            return read

    def delete(self):
        """Delete the counter"""
        id_name = self.id_name
        delete = redis.delete(id_name)
        return delete 

###Compare and rank your counter objects 

class Comparison(object):
    """An abstract comparison object. Allows queries against two existing counter objects."""
    def __init__(self, name, object1, object2):
        """Three required arguments: a name for the comparison, and the two objects to be 
        compared"""
        #Create a unique global ID for the new comparison object
        global_id = redis.incr("global_space")
        global_id_name = "global:%s" %global_id
        #Create a comparison-specific (local) ID
        local_id = redis.incr("comparison_space")
        id_name = "comparison:%s:%s" %(local_id, name)
        #The two counter objects
        self.id_name = id_name
        self.object1 = object1
        self.object2 = object2

    def compare(self):
        """Returns a string representation of the relationship between
        object 1 and object 2 ('equal', 'greater than', 'less than')"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read() 
        if object1_size == object2_size:
             return "Equal"
        elif object1_size > object2_size:
             return "Greater than"
        elif object1_size < object1_size:
             return "Less than"
        else:
             pass

    def difference(self):
        """Return the numberic difference between object 1 and object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read()
        difference = object1_size-object2_size
        return difference

    def equal(self):
        """Check if the value of object 1 is equal to the value of object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read()
        if object1_size == object2_size:
             return True
        else:
             return False
   
    def greater_than(self):
        """Check if the value of object 1 is greater than the value of object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read()
        if object1_size > object2_size:
             return True
        else:
             return False     

    def less_than(self):
        """Check if the value of object 1 is less than the value of object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read() 
        if object1_size < object2_size:
             return True
        else:
             return False

    def greater_than_or_equal(self):
        """Check if the value of object 1 is greater than or equal to the value of object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read() 
        if object1_size >= object2_size:
             return True
        else:
             return False     

    def less_than_or_equal(self):
        """Check if the value of object 1 is less than or equal to the value of object 2"""
        object1 = self.object1
        object2 = self.object2
        object1_size = object1.read()
        object2_size = object2.read() 
        if object1_size <= object2_size:
             return True
        else:
             return False

class Ranking(object):
    """A ranking object. Instatiate with any number of exsting 
    counter objects (passsed via keyword arguments)"""
    def __init__(self, name, *kwargs):
        #Create a unique global ID for the new ranking object
        global_id = redis.incr("global_space")
        global_id_name = "global:%s" %global_id
        #Create a ranking-specific (local) ID
        local_id = redis.incr("ranking_space")
        id_name = "ranking:%s:%s" %(local_id, name)
        self.id_name = id_name
        self.kwargs = kwargs  
 
    def rank(self):
        """Rank by integer size (greatest to smallest) and return a list of the ranking""" 
        id_name = self.id_name
        kwargs = self.kwargs
        object_dict = {}
        for object in kwargs:
            object_name = object.id_name
            value = object.read()
            object_dict[object_name] = value
        rank = sorted(object_dict.iteritems(), key=itemgetter(1))
        rank.reverse()
        return rank

    def reverse_rank(self):
        """Rank by integer size (smallest to greatest) and return a list of the ranking""" 
        id_name = self.id_name
        kwargs = self.kwargs
        object_dict = {}
        for object in kwargs:
            object_name = object.id_name
            value = object.read()
            object_dict[object_name] = value
        rank = sorted(object_dict.iteritems(), key=itemgetter(1))
        return rank


