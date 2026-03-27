
import psycopg2, psycopg, json


s
def cache(table, table_data):

  table_data = table_data[0][0]
  print(table)
  cache_json = {}

  # loop through the data ( the table data data is a list of dicts)
  for data in table_data:
    
    id = data.get("id")
    
    data.pop("id")
    
    cache_json.update( {id : data.copy()})
  
  # write the cache_file to the file

  
  
  with open("cache.json", "w") as cache_file:
    cache_file.write(json.dumps({table:cache_json}))

def check_cache(table):

  # open the cache file
  with open("cache.json", "r") as cache_file:

    # get data as dict
          
    cached_tabels = json.loads(str(*cache_file.readlines()))

    
    
    
    if cached_tabels.get(table) != None:

      
        
        return (cached_tabels.get(table), True)
      
    else:
      return (None, False)
  
 
# todo add a function to get a single user data for cache
