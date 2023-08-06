"""UserStore Interface

All backend stores for userdata should implement the UserStore interface
as defined here.

"""
class UserStore(object):
    """This is the interface for storing retrieved and normalized userdata"""
    def load_from_config(cls, config):
        """This method creates and returns a configured UserStore
        
        :param config: A dict of key/value's to use when
                       instantiating the UserStore. The key/value's accepted
                       from a config should be documented.
        :returns: A configured UserStore.
        :rtype: UserStore
        
        """
        raise NotImplementedError
    
    def retrieve(self, key):
        """This method retrieves the data for a key from the storage.
        
        The stored data is a pickled object, and should be unpickled before
        returning it.
        
        :param key: The key to retrieve. Keys are always ascii-safe strings.
        :returns: User information
        :rtype: dict
        
        """
        raise NotImplementedError
    
    def store(self, key, value, expires=None):
        """This method stores a users data dict in the storage.
        
        The supplied value will be a dict and should be pickled with the
        before being stored. 
        
        For backend's that don't automatically expire data, some record should
        be kept with the key's data marking when it should have expired so that
        :meth:`~velruse.store.interface.purge_expired` can properly purge
        old data.
        
        :param key: The key to store the value under.
        :param value: The userdata to store
        :param expires: Optional expiration time in seconds from now before the
                        stored data should be removed.
        :type value: dict
        :returns: True if the data was stored successfully, False otherwise.
        :rtype: boolean
        
        """
        raise NotImplementedError
    
    def delete(self, key):
        """This method deletes a users data dict from the storage
        
        :param key: The key of the data to be removed.
        
        :returns: True if the delete proceeded ok, regardless of if the key
                  actually existed or not.
        :rtype: boolean
        
        """
        raise NotImplementedError
    
    def purge_expired(self):
        """This method purges all expired data from the storage
        
        All expired data should be purged from the UserStore when this method
        is called. UserStore's that automatically expire old data must still
        implement this method, but can do nothing.
        
        """
        raise NotImplementedError
