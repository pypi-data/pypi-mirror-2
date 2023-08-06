from pymongo import Connection
from pymongo.objectid import ObjectId

class Document(object):
    def __init__(self, object_dict):
        self.__dict__['_object_dict'] = object_dict
    
    def save(self):
        return self.__db__[self.__collection__].save(self._object_dict, safe=True)

    def delete(self):
        object_id = self._object_dict['_id']
        if object_id:
            self.__db__[self.__collection__].remove(object_id)
            del self._object_dict['_id']
            return True
        return False
    
    def __getattr__(self, name):
        try:
            return self.__dict__['_object_dict'][name]
        except:
            raise AttributeError()
    
    def __setattr__(self, name, value):
        if name not in ['_id', '__dict__', '_object_dict']:
        #    self._object_dict[name] = value
        #object.__setattr__(self, name, value)
            self.__dict__['_object_dict'][name] = value
    
    def __delattr__(self, name):
        del self.__dict__['_object_dict'][name]
    
    def __setitem__(self, name, value):
        self.__setattr__(name, value)
    
    def get_id(self):
        object_id = getattr(self, '_id', None)
        if object_id:
            return str(object_id)
    id = property(get_id)
    
    @classmethod
    def create(cls, dictionary):
        object_id = cls.__db__[cls.__collection__].insert(dictionary)
        return cls.get(str(object_id))
        #dictionary['_id'] = str(object_id)
    
    @classmethod
    def get(cls, object_id):
        object_dict = cls.__db__[cls.__collection__].find_one({'_id':ObjectId(object_id)})
        if object_dict:
            return cls(object_dict)
        return None
    
    @classmethod
    def find(cls, spec=None):
		#return cls.__db__[cls.__collection__].find(spec)
        for object_dict in cls.__db__[cls.__collection__].find(spec=spec):
            yield cls(object_dict)
    
    @classmethod
    def find_one(cls, spec=None):
        result =  cls(cls.__db__[cls.__collection__].find_one(spec))
        if result._object_dict:
            return result
        return None
		

class MongoObject(object):
    
    @classmethod
    def connection(cls, host='localhost', port=27017):
        if not hasattr(cls, '_connection'):
            cls._connection = Connection(host, port)
        return cls._connection
    
    @classmethod
    def db(cls, db_name='mongo_object', host='localhost', port=27017):
        return cls.connection(host, port)[db_name]
    
    @classmethod
    def factory(cls, collection_name, db_name='mongo_object', host='localhost', port=27017):
        items = {'__collection__': collection_name}
        items['__db__'] = cls.db(db_name=db_name, host=host, port=port)
        Klass = type(collection_name.capitalize(),(Document,), items)
        return Klass