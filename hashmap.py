
class HashMap():
    ## data structure representing a hash map. Uses closed addressing via python lists
    ## Variables:
    ##      items: lists of lists
    ##      items_len: length of item's list

    class Item():
        ## object that tracks an item's key/value pair
        ## Variables:
        ##      key: used to get item from hash-map, must be a string or a number
        ##      value: value associated with key
        def __init__(self, hash : str ="", value= None):
            self.key : str = str(hash)
            self.value : object = value
        def __str__(self):
            ## A string representation of an item
            ## Returns: "{ key, value }"
            return "{ "+ self.key + ", " + self.value + " }"
        
    def make_idx(self, hash : str):
        ## creates a hash-index to be used with the hash-map
        ## Parameters:
        ##      hash: the hash used to create the hash-index, must be string or a number
        ## Returns: The hashindex created as an Int     
        int_hash = 0
        if (str(hash).isalpha()):
            for h in hash:
                int_hash += ord(h)
        elif (str(hash).isnumeric()): int_hash = int(hash)
        return int_hash % self.items_len

    def __init__(self, len = 0):
        self.items : list[list] = [None]*len
        self.items_len : int = len

    def add(self, hash, value, throw_if_dupe = True):
        ## adds a key/value pair into the hash-map
        ## Parameters:
        ##      hash: used to get item from hash-map, must be string or a number
        ##      value: value associated with key
        ##      throw_if_dupe: if True, raises an exception if a matching key was found, otherwise replaces the found key with a new value, True by default
        ## Returns: Nothing
        idx = self.make_idx(hash)
        if (idx >= self.items_len): return
        if (self.items[idx] == None):
            self.items[idx] = []
        else:
            for it in self.items[idx]:
                if it.key == str(hash) and throw_if_dupe:
                    raise Exception("Hash must be unique")
                elif it.key == str(hash):
                    it = self.Item(hash, value)
                    return
        self.items[idx].insert(0,self.Item(hash, value))

    def remove(self, hash = None):
        ## removes a key/value pair from a hash-map and returns the value removed
        ## if a hash is not None, removes the key/value pair that matches the key with the hash
        ## otherwise, removes the first value found in the hash-map index
        ## Parameters:
        ##      hash: used to get item from hash-map, must be None, a string, or a number, None by default
        ## Returns: the value removed, or None if no value was removed
        value = None
        if hash == None:
            for items in self.items:
                if value != None: break
                if items == None: continue
                for i in range(len(items)):
                     value = items.pop(i).value 
                     break
        else:
            idx = self.make_idx(hash)
            sub_list = self.items[idx]
            length = len(sub_list)
            for i in range(length):
                if (str(hash) == sub_list[i].key):
                    value = sub_list.pop(i).value
                    break
        if (len(sub_list)== 0):
            self.items[idx] = None
        return value

    def find(self, hash = None):
        ## finds an item and returns a value. If a hash is not None, returns the key/value pair that matches the key with the hash. Otherwise, returns the first value found in the hashmap
        ## Parameters:
        ##      hash: used to get item from hash-map, must be None, a string, or a number, None by default
        ## Returns: the first value found, or None
        if hash == None:
            for items in self.items:
                if items == None: continue
                for i in range(len(items)):
                     return items[i].value 
        idx = self.make_idx(hash)
        sub_list = self.items[idx]
        if sub_list == None: return None
        length = len(sub_list)
        for i in range(length):
            if (str(hash) == sub_list[i].key):
                return sub_list[i].value
        return None
            
    def modify(self, hash, value):
        ## finds an item with the hash provided and changes the value that matches the key to the passed hash
        ## Parameters:
        ##      hash: used to get item from hash-map
        ##      value: the value to replace in the matching key/value pair
        ## Returns: the changed value, or None if no value was changed
        idx = self.make_idx(hash)
        sub_list = self.items[idx]
        length = len(sub_list)
        for i in range(length):
            if (str(hash) == sub_list[i].key):
                 sub_list[i].value = value
                 return sub_list[i].value
        return None
               
            
    def __str__(self):
        ## A string representation of the hashmap
        ## Returns: a string that shows the hashmap as the following:
        ##      index: [ { key, value } ] length
        ##      index: [ { key, value } ] length
        ##      index: [ { key, value } ] length
        ##      ...

        string = ""
        for i in range (self.items_len):
            string += (str(i) + ": ")
            if (self.items[i] != None):
                string += "[ "
                length = len(self.items[i])
                for j in range (length):
                    string += str(self.items[i][j])
                    if (j != length-1):
                        string += ", "
                string += " ] "
                string += str(length)
            else: string += "[]"
            string += "\n"
        return string
    
    def to_list(self):
        ## converts a HashMap into a list using each key/value pairs' values
        ## Returns: a list containing all values in the HashMap
        newList = []
        for items in self.items:
            if items == None: continue
            for item in items:
                newList.append(item.value)
        return newList

    @classmethod
    def convert_from_list(self,listObj: list, length: int = None, dict_key: str = None, throw_if_dupe = True):
        ## converts a list into a HashMap
        ## Parameters:
        ##      listObj: to list to convert
        ##      length: the length of the new HashMap, must be a positive number. If no length or None is passed, defaults to the length of the list. None by default
        ##      dict_key: if the list is a list of dicts, uses this parameter to set the dict's requested key's value as the hash(key) per element in the HashMap. If no dict_key or None is passed, uses a set of numbers to set the hash(key) per element in the HashMap instead. None by default
        ## throw_if_dupe: if True, raises an exception if a duplicate key was attempted to be added, if using dict_key; if not, modifies the requested key with the new value. True by default
        ## Returns: the resulting HashMap
        i = 0
        if length == None or length < 0: 
            length = len(listObj)
        map = HashMap(length)
        for l in listObj:
            if dict_key == None:
                map.add(i,l, throw_if_dupe)
                i += 1
            else: 
                try:
                    map.add(l[dict_key], l, throw_if_dupe)
                except:
                    map.add(i,l, throw_if_dupe)
                    i += 1
        return map



            
def test():
    ## Used to test the HashMap class
    map = HashMap(10)
    map.add("a", 'a')
    map.add("b", 'b')
    map.add("c", 'c')
    map.add("d", 'c')
    map.add("e", 'c')
    map.add("f", 'c')
    map.add("g", 'c')
    map.add("h", 'c')
    map.add("i", 'c')
    map.add("j", 'c')
    #map.add("j", 'd')
    print(str(map))
    popped = map.remove("a")
    print(str(map))
    print("popped: "+ str(popped))
    find = map.find("f")
    print("find: "+ str(find))
    map.modify("b", 'z')
    print(str(map))


#test()
    
