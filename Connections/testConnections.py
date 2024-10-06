import requests
import time 
session = requests.Session()
#%%
#Get Items
items = session.get('https://9ks86gdmzd.execute-api.us-east-1.amazonaws.com/prod/items')
print(items.json())

#%%
#Get Variables
var_url = 'https://9ks86gdmzd.execute-api.us-east-1.amazonaws.com/prod/var'
vars = session.get(var_url)
print(vars.json())
# %%
assert False
#Put variables
body = {
    'value':28.3,
    'var_name':'Temperature',
    'time':int(time.time())*1000,
    'var_id':1
}
putResponse = session.put(var_url,json=body)
print(putResponse.text)