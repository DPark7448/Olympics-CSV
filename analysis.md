# Data Structure Description

The majority of the program uses the built-in python lists in combination with python dicts to process each record in the file. Each dict's key was mapped to each field located in the first record of the file (the header file). For instance, the `athlete_id` data in the athletes file in the first record would become the key, and so on. This was used to merge the paris data with the olympics data and to clean the data in the athletes file.

When adding the age to the event results and generating the medal summary, it was initially taking more than half an hour to process all the data. We were motivated enough to create a new data structure that would handle this data faster. We decided that using hash-maps was an appropriate solution to the problem. This reduced the runtime of running both functions (adding age and generating the medal tally) from over minutes to at least under 20 seconds.

In the applicable methods, we would convert a list to a hash-map before data-processing. Because of how hash-map's worked, instead of searching through the data each time in a list, the hashmap can just directly get the index using the passed in hash and retrieve the value there. A note that in the way the hashindex is created, it would check if the hash passed is a whole number: if not (assuming its a string), for each character in the string, it would convert it to its ASCII code and add them all together as an integer. So the runtime of creating a hashindex would at most be $O(n)$ based on the length of the string, however, it is still significantly faster than searching through a list each time, since the id of a record would not be as long as 1000000 records in a list. If each id is even all at a set length, well, that's even better.

Also a note that the hash-map uses _closed addressing_, so each filled part of a hash-map would be a list that's able to store values that has the same hashindex, but different hashes. If the hash-map was initialized properly (the length of the hash-map isn't smaller than that of all the added values), the act of retrieving from the file itself should be $O(1)$ at best, $O(n)$ at worst. This doesn't include the act of creating a hash-index itself, which should be taken into account.

# Assumptions and Decisions Made

For cleaning the data, we listed some of the most common formats seen in the original bio data and assumed those as the valid formats to standardize them. To handle two-digit years like 10-Apr-99 / 10-Apr-45 that were greater than the current year, we assumed them to be in the 1900s to prevent dates from being misread as future events. We also stored an empty string in cleaned dataset for empty and invalid formats.

In addition, the `add_age_column` assumes that the field that contains the athlete's birth data is formatted like how the clean_data function formats it. (DD-MMM-YYYY). Adding the ages wouldn't really work correctly if the date formats in the athletes_data folder were all mismatched, like how it was previously. Of course sometimes there are records that contain missing birthdays; for that it just inserts `-1` in the age field.

# How Data Is Processed (in general)

Data is first processed via using the DictReader and DictWriter classes to read data and write data respectively. With each record comes a dict, and each dict is stored into a list, where further processing will occur, depending in the function.

Sometimes, a record needs to be referenced from a list of dicts repeatedly, and searching one by one can take time, so we convert some lists to our custom HashMap data structure. More details about how this data is converted can be found in the Data Structure Description section.

# Runtime Analysis

## `clean_paris_data`

    let n represent the number of records in the olympic_athlete_events_results file
    let a represent the number of records in the olympic_athlete_bio file

    import csv                      # 1
    import ParisMerge               # 1
    from datetime import datetime   # 1
    from hashmap import HashMap     # 1

    #format "born" column
    def format_born_date(str_date, comp_year: int = -1): # 1
        # empty/missing dates
        if not str_date or not str(str_date).strip():    # 2
            return ""                                    # 1                      
    
        # convert date to string and remove whitespaces
        str_date = str(str_date).strip()                 # 3
    
        # list expected formats
        formats = [                                      # 1
            '%d-%b-%y', # 10-Apr-99
            '%d-%b-%Y', # 10-Apr-1999
            '%d %B %Y', # 10 April 1999
            '%Y',       # 1999
            '%B %Y',    # April 1999
        ]
    
        # parsing using each expected format
        for fmt in formats:                              # 5 (fixed number of expected formats)
            try:
                dt = datetime.strptime(str_date, fmt)    # 1 (5)
                # handle 2 digit years (past or future) 
                # by comparing to the current year
                y = dt.year                              # 1 (5)
                if dt.year > datetime.now().year:        # 1 (5)
                    y = dt.year - 100                    # 2 (5)
                comp_num = comp_year - y                 # 2 (5)
                # compares if the year chosen is bigger than the olympic year if passed
                # adjusts if needed
                if (comp_year > -1 and comp_num< 0):     # 2 (5)
                    y = y - 100                          # 2 (5)
                dt = dt.replace(year=y)                  # 1 (5)
                # return date with the correct format
                return dt.strftime('%d-%b-%Y')           # 1 (5)
            # if fail, try the next format
            except ValueError:                           # 1 (5)
                continue                                 # 1 (5)
        # return empty if all formats failed
        return ""                                        # 1 (5)

        T(n) = 4 + 1 + 2 + 1 + 3 + 1 + 5 (1 + 1 + 1 + 2 + 2 + 2 + 2 + 4)
        T(n) = 12 + 5 (15)
            = 87
        Therefore, T(n) is O(1).

    let n represent the number of records in the olympic_athlete_events_results file
    let a represent the number of records in the olympic_athlete_bio file

    #open data to clean and write result to a results file
    def clean_data(input_file, output_file, events : list = None):                              # 1

        if (events is None):                                                                    # 1
            events = ParisMerge.read_csv("olympic_athlete_event_results.csv")                   # O(n) + 1 + 1
        events = HashMap.convert_from_list(events, None, "athlete_id", False)                   # O(n)
        # open file for reading (with column headers)
        with open(input_file, mode='r', encoding='utf-8') as infile:                            # 1
            reader = csv.DictReader(infile)                                                     # 1
            fieldnames = reader.fieldnames                                                      # 1
            rows = list(reader)                                                                 # O(a)
    
        # clean each row from the data using the function format_born_date for formatting
        for row in rows:                                                                        # a
            # tries to compare an olympic year to athlete loaded year for validation
            e = events.find(row["athlete_id"])                                                  # 1 (a)
            e_year = e["\ufeffedition"].split(" ")[0]                                           # 2 (a)
            row['born'] = format_born_date(row['born'], int(e_year))                            # 1 (a)
    
        # open file to write the results
        with open(output_file, mode='w', encoding='utf-8', newline='') as outfile:              # 1
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)                             # 1
            writer.writeheader()                                                                # 1
            writer.writerows(rows)                                                              # O(a)

    #define the files
    input_file = "olympic_athlete_bio.csv"                                                      # 1
    output_file = "new_olympic_athlete_bio.csv"                                                 # 1
    #execute the cleaning function
    clean_data(input_file, output_file)

        T(n, a) = 1 + 1 + n + 2 + n + 3 + a + a (1 + 2 + 1) + 3 + a + 2
            = 2n + 6a + 12
        Therefore, T(n, a) is O(n + a).

## `merge_data`

```python
#a: The number of records in the "olympic_athlete_bio.csv"
#p: The number of records in the "paris/athletes.csv"
#k: The number of new Paris athletes after filtering
#M: The number of records in the dataset passed to write_csv


import csv  # 1

def read_csv(file_name):
    data_set = []  # 1
    with open(file_name, mode='r', encoding="utf-8") as file:  # 1
        reader = csv.DictReader(file)  # 1 + 1
        for row in reader:  # 1 per row: n * 1
            data_set.append(row)  # 1 per row: n * 1
    return data_set  # 1

def write_csv(file_name, data_set):
    if not data_set:  # 1
        return
    with open(file_name, mode='w', newline='', encoding="utf-8") as file:  # 1
        fieldnames = data_set[0].keys()  # 1 + 1
        writer = csv.DictWriter(file, fieldnames=fieldnames)  # 1 + 1
        writer.writeheader()  # 1 + 1
        for row in data_set:  # 1 per row: M * 1
            writer.writerow(row)  # 1 per row: M * 1

# Read CSV files
original_bio = read_csv("olympic_athlete_bio.csv")  # O(a): 1+1+n
paris_bio_raw = read_csv("paris/athletes.csv")  # O(p): 1+1+p

# Build set of existing athletes from original_bio
existing_athletes = set()  # 1
for athlete in original_bio:  # a iterations: a * (loop overhead)
    # athlete['name'] (1) + .strip() (1) + .upper() (1) + athlete['born'] (1) + .strip() (1) + tuple creation (1) = 6
    identifier = (athlete['name'].strip().upper(), athlete['born'].strip())  # 6
    existing_athletes.add(identifier)  # 1

# Filter new Paris athletes
new_paris_athletes = []  # 1
for athlete in paris_bio_raw:  # p iterations
    # Similar tuple: 6 operations (using 'birth_date' instead of 'born')
    identifier = (athlete['name'].strip().upper(), athlete['birth_date'].strip())  # 6
    if identifier not in existing_athletes:  # 1 check
        new_paris_athletes.append(athlete)  # 1

# Find max athlete_id in original_bio and assign new IDs
# 3 per athlete in original_bio (check, conversion, etc.)
max_id = max(int(a['athlete_id']) for a in original_bio if a['athlete_id'].isdigit())
for i, athlete in enumerate(new_paris_athletes, start=1):  # k iterations (k ≤ p)
    # addition (1) + str() conversion (1) + assignment (1) = 3
    athlete['athlete_id'] = str(max_id + i)  # 3

def reformat_paris(athlete):
    # accesses field 8 times + dict creation (1) = 9
    return {
        'athlete_id': athlete['athlete_id'],  # 1
        'name': athlete['name'],              # 1
        'sex': athlete['gender'],             # 1
        'born': athlete['birth_date'],        # 1
        'height': athlete['height'],          # 1
        'weight': athlete['weight'],          # 1
        'country': athlete['country'],        # 1
        'country_noc': athlete['country_code'],  # 1
    }

formatted_paris = [reformat_paris(a) for a in new_paris_athletes]  # k * 9 ops
merged_athlete_bio = original_bio + formatted_paris  # 2(a + k): copying a + k items
write_csv("new_olympic_athlete_bio.csv", merged_athlete_bio)  # 2(a + k)
# formatting takes 9k operations
# Merging requires 2(a+k)
# Writing csv file requires 2(a+k)
# Total operations count for the three steps results in: 9k + 2(a + k) + 2(a + k) = 9k + 4a + 4k = 13k + 4a
# In conclusion O(a + k) where k ≤ p and a is the number of records in the original bio file. Meaning the cost of the merge is
# linear in the number of records in the original bio file and the number of new Paris athletes after filtering.
```

## `generate_medal_summary`

```python

## utils.py
def generate_medal_summary(medal_results : list, country_list: list):
    # let n represent the number of records in the olympic_athlete_events_results file via the medal results list

    # let c represent the number of records in the olympics_country file via the country_list... list

    # let h represent the length of the string used to create the hash

    # let m represent the length of the hash string used to find a medal tally
    # let a represent the length of the hash string used to find an athlete
    # let o represent the length of the hash string used to find a country

    # let T(n, c) represent the total number of operations

    id = "" # 1
    country_list : HashMap = HashMap.convert_from_list(country_list, None, dict_key="noc") # 1 + (oc)
    medal_list = HashMap(len(medal_results)) # 1 + n + 1 (medal_list will most likely have smaller values than expected so consider it as properly initialized)
    athlete_history = HashMap(len(medal_results)) # 1 + n + 1 (athlete_history will most likely have smaller values than expected so consider it as properly initialized)
    dict= {
            "metal_results_id": id,
            "edition": "",
            "edition_id": -1,
            "country_noc": "",
            "country": "",
            "athletes_num": 0,
            "gold_num": 0,
            "silver_num":0,
            "bronze_num": 0,
            "total_num": 0
              } # 1 + 10
    for item in medal_results: # 1 + n
            found_ath = None # 1n
            id = str(item["edition_id"]) + str(item["country_noc"])  # (1 + 1 + 1 + 1)n (assume both are already strings)
            dupe_item = medal_list.find(id) # (1 + m)n (assume the hashmap is properly initialized)
            country = country_list.find(item["country_noc"]) # (1 + o)n
            if (dupe_item == None): # 1n
                dict = {
                "metal_results_id": id,
                "edition": item["\ufeffedition"],
                "edition_id": item["edition_id"],
                "country_noc": item["country_noc"],
                "country": "" if country == None else country["country"],
                "athletes_num":0,
                "gold_num": 0,
                "silver_num": 0,
                "bronze_num": 0,
                "total_num": 0
                } # (1 + 10 + 2)n (extra 2 for the if/else statement)
                medal_list.add(id,dict) # (1 + m)n (assume the hashmap is properly initialized)
            else: dict = dupe_item # 1n
            found_ath = athlete_history.find(item["athlete_id"]) # (1 + a)n
            if found_ath == None: # 1n
                dict["athletes_num"] += 1 # 2n
                athlete_history.add(item["athlete_id"], item["athlete"]) # an
            if (str(item["medal"]) == "Bronze"): # 1n
                dict["bronze_num"] += 1 # 2n
                dict["total_num"] += 1 # 2n
            if (str(item["medal"]) == "Silver"): # 1n
                dict["silver_num"] += 1 # 2n
                dict["total_num"] += 1 # 2n
            if (str(item["medal"]) == "Gold"): # 1n
                dict["gold_num"] += 1 # 2n
                dict["total_num"] += 1 # 2n

    ParisMerge.write_csv("new_medal_tally.csv",medal_list.to_list()) # n + n (assume the hashmap is initialized properly)
    return medal_list # 1

    # T(n, c) = 1 + 1 + oc + 1 + n + 1 + 1 + n + 1 + 1 + 10 + 1 + n + n + 4n + (1+m)n + (1+o)n + n + 13n + (1+m)n + n + (1+a)n + n + 2n + an + 1n + 2n + 2n + 1n + 2n + 2n + 1n + 2n + 2n + vn + n + 1
    # T(n, c) = 19 + oc + 43n + (1+m)n + (1+o)n + (1+m)n + (1+a)n + an
    # T(n, c) = 19 + oc + 43n + n + mn + n + on + n + mn + m + an + an
    # T(n, c) = 19 + oc + 46n + 2mn + on + m + 2an
    # runtime: O(oc + mn + an)

## HashMap.py

class HashMap():

    class Item():
        def __init__(self, hash ="", value= None):
            # let h be the length of the hash given
            self.key : str = str(hash) # 1 (assume the hash is already a string)
            self.value : object = value # 1
            ## runtime is O(1) if hash is already a string, otherwise O(h)

    def make_idx(self, hash : str): # with letters
        # let h be the length of the hash given (assume hash is already a string)
        int_hash = 0 # 1
        if (str(hash).isalpha()): # 1 + h
            for h in hash: # 1 + h
                int_hash += ord(h) # (2 + 1)h
        elif (str(hash).isnumeric()): int_hash = int(hash) # 1 + 0 (assume hash has letters)
        return int_hash % self.items_len # 1 + 1
        ## T(h) = 1 + 1 + h + 1 + h + (2-1)h + 1 + 1 + 1
        ## T(h) = 3h + 6
        ## runtime: O(n)

    def make_idx(self, hash : str): # with numbers
        # let h be the length of the hash given (assume hash is already a string)
        int_hash = 0 # 1
        if (str(hash).isalpha()): # 1 + h (assume hash only has numbers)
            for h in hash: # 0
                int_hash += ord(h) # 0
        elif (str(hash).isnumeric()): int_hash = int(hash) # 1 + (1+h)
        return int_hash % self.items_len # 1 + 1
        ## T(h) = 1 + 1 + h + 1 + 1 + h + 1 + 1
        ## T(h) = 2h + 6
        ## runtime: O(n)

    def __init__(self, len = 0):
        # let l be the length given through len
        self.items : list[list] = [None]*len # 1+1+l (assignment + multiply operator + number of times None is added)
        self.items_len : int = len # 1
        ## T(l) = 1 + 1 + l + 1
        ## T(l) = l + 3
        ## runtime is O(l)

    def add(self, hash, value, throw_if_dupe = True):
        # let h be the length of the hash given (assume hash is already a string)
        # let l be the length of the selected index (as a list)
        idx = self.make_idx(hash) # 1 + h
        if (idx >= self.items_len): return # 0 (assume this won't happen)
        if (self.items[idx] == None): # 1
            self.items[idx] = [] # 0 (assume there is a value in the index)
        else: # 1
            for it in self.items[idx]: # 1 + l
                if it.key == str(hash) and throw_if_dupe: # l(1 + 1 + 1)
                    raise Exception("Hash must be unique") # 0 (assume all hashed passed are unique)
                elif it.key == str(hash): # (1 + 1)l
                    it = self.Item(hash, value) # 0 (assume all hashed passed are unique)
                    return # 0 (assume all hashed passed are unique)
        self.items[idx].insert(0,self.Item(hash, value)) # 1 + 1
        ## T(h) = 1 + h + 1 + 1 + 1 + l + l(1+1+1) + l(1+1) + 1 + 1 + 1
        ## T(h) = 4 + h + l + 3l + 2l + 3
        ## T(h) = 7 + h + 6l
        # Note: If the hashmap is initialized properly, l would normally be 1. Therefore, the best case would run O(h). However, if chaining were to occur, then best case would be O(l + h).

    def find(self, hash = None):
        # let h be the length of the hash
        # let l be the length of the selected index (as a list)
        if hash == None: # 1
            for items in self.items: # 0 (assume hash will be passed)
                if items == None: continue # 0 (assume hash will be passed)
                for i in range(len(items)): # 0 (assume hash will be passed)
                     return items[i].value # 0 (assume hash will be passed)
        idx = self.make_idx(hash) # 1 + h
        sub_list = self.items[idx] # 1
        if sub_list == None: return None # 1 + 0 (assume the index is filled)
        length = len(sub_list) # 1 + 1
        for i in range(length): # 1 + l
            if (str(hash) == sub_list[i].key): # (1 + 1)l (assume the hash is already a string)
                return sub_list[i].value # 1 (if value is found, will instantly return)
        return None # 0 (assume a value will be found)
        ## T(h) = 1 + 1 + h + 1 + 1 + 1 + 1 + 1 + l + (1+1)l + 1
        ## T(h) = 8 + h + 3l
        # Note: If the hashmap is initialized properly, l would normally be 1. Therefore, the best case would run O(h). However, if chaining were to occur, then best case would be O(l + h).



    def to_list(self):
        ## let n be the length of the HashMap
        ## let l be the length of each index list
        newList = [] # 1
        for items in self.items: # 1 + n
            if items == None: continue # 1n + 0 (assume all indexes are filled)
            for item in items: # (1 + l)n
                newList.append(item.value) # 1ln
        return newList # 1
        ## T(n) = 1 + 1 + n + n + (1 + l)n + ln
        ## T(n) = 2 + 3n + 2ln
        # Note: If the hashmap is initialized properly, l would normally be 1. Therefore, the best case would run O(n). However, if chaining were to exist at any part in the loop, then best case would be O(ln).

    @classmethod
    def convert_from_list(self,listObj: list, length: int = None, dict_key: str = None, throw_if_dupe = True):
        ## let n be the length passed with listObj
        ## lst h be the length of the string value taken from each record using dict_key
        i = 0 # 1
        if length == None or length < 0: # 1
            length = len(listObj) # 1 + 1 (assignment + len)
        map = HashMap(length) # 1 + n
        for l in listObj: # 1 + n
            if dict_key == None: # 1n
                map.add(i,l, throw_if_dupe) # 0 (dict_key won't be None)
                i += 1 # 0 (dict_key won't be None)
            else: # 1n
                try:
                    map.add(l[dict_key], l, throw_if_dupe) # hn
                except:
                    map.add(i,l, throw_if_dupe) # 0 (assume no exceptions will occur)
                    i += 1 # 0 (assume no exceptions will occur)
        return map # 1
        ## T(n) = 1 + 1 + 1 + 1 + n + 1 + n + n + n + hn + 1
        ## T(n) = 6 + 4n + hn
        ## Runtime is O(hn)

```
