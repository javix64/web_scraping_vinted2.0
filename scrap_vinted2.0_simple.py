import requests, json, time,csv,os
import pandas as pd
web = requests.session()
web.get('https://www.vinted.es/vetements?catalog[]=1&page=1')
session = requests.session()
with open('cookie.txt', 'w') as f:
    json.dump(requests.utils.dict_from_cookiejar(web.cookies), f)
with open('cookie.txt', 'r') as f:
    cookies = requests.utils.cookiejar_from_dict(json.load(f))
    session.cookies.update(cookies)
    end_page = 105+1
    output = 'data.csv'
    data_file = open(output, 'w') 
    writer = csv.writer(data_file)
    writer.writerow(['Usuario','City','User items','Item title','Item description', 'Item views','Size','Brand','Status','Price','Color','Likes'])
    main_url='https://www.vinted.es/api/v2/items?per_page=96&page='
    
    for i in range(1,end_page):
        vinted_json = web.get(main_url+str(i)).json()
        print('Page: '+main_url+str(i))
        for value in vinted_json["items"]:
            writer.writerow(
            [value["user"]["login"],
            value["user"]["city"],
            value["user"]["item_count"],
            value["title"],
            value["description"],
            value["view_count"],
            value["size"],
            value["brand"],
            value["status"],
            value["price"],
            value["color1_id"],
            value["favourite_count"]
            ])