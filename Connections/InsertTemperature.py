import requests
import time 
import random
session = requests.Session()

var_url = 'https://9ks86gdmzd.execute-api.us-east-1.amazonaws.com/prod/var'
old_value = 33
id_number = 3
while True:
    #Put variables
    new_value = random.randint(240,320)/10
    body = {
        'value':old_value*0.8 + new_value*0.2,
        'var_name':'Temperature',
        'time':int(time.time())*1000,
        'var_id':id_number
    }
    putResponse = session.put(var_url,json=body)
    print(body, putResponse.text)

    id_number += 1
    time.sleep(600)