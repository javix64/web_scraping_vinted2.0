import requests, json, time,csv,os, threading, time, math

# Just preparation work
web = requests.session()
web.get('https://www.vinted.es/vetements?catalog[]=1&page=1')
session = requests.session()
#open the url that allow us to save the cookie
with open('cookie.txt', 'w') as f:
    json.dump(requests.utils.dict_from_cookiejar(web.cookies), f)
#load the cookie

# Function needs to be on top
# Define the function that will do the magic inside
def request_thread(start_page, middle_end_page, results_array, lock):
    print('I am thread number %s'%(threading.current_thread().name))

    lock.acquire()
    #Here we put our code
    # we want the thread to get the 27 pages and returns the results into a variable, last thread will get less
    thread_name = threading.current_thread().name
    # page request
    #go into loop for scrap all json pages
    for i in range(start_page,middle_end_page):
        vinted_json = web.get(main_url+str(i)).json()
        try:
            #getting the data from json and saving into csv
            for value in vinted_json["items"]:

              res = []
              res.append(str(value["id"]))
              res.append(str(value["title"]))
              res.append(str(value["brand_id"]))
              res.append(str(value["size_id"]))
              res.append(str(value["status_id"]))
              res.append(str(value["disposal_conditions"]))
              res.append(str(value["user_id"]))

              results_array.append(res)
        except:
             mamon=1
    print("Length is: " + str(len(results_array)))
    lock.release()

with open('cookie.txt', 'r') as f:
    cookies = requests.utils.cookiejar_from_dict(json.load(f))
    session.cookies.update(cookies)
    end_page = 105+1
    output = 'data.csv'
    data_file = open(output, 'w', newline='',encoding='utf-8')
    writer = csv.writer(data_file)
    #write the csv index
    writer.writerow(['id','title','brand_id','size_id','status_id','disposal_conditions','user_id'])
    main_url='https://www.vinted.es/api/v2/items?per_page=96&page='

    # Here comes the crazy part
    num_threads = 16
    results_thread = []
    threads = []
    locks = []
    for i in range(num_threads):
        results_thread.append([])
        # create a locker to control the thread
        locks.append(threading.Lock())
        # create the threads
        call_start_page = (math.floor(end_page/num_threads)*i)+1
        call_end_page = (math.floor(end_page/num_threads)*(i+1))+1
        if i == num_threads-1:
            call_end_page = end_page
        threads.append(threading.Thread(target=request_thread, args=(call_start_page, call_end_page, results_thread[i], locks[i],)))
        print(" " + str(call_start_page) + "," + str(call_end_page))

    # start the thread
    start = time.time()
    for t in threads: t.start()
    for t in threads: t.join()
    end = time.time()
    timing = end - start
    print(timing)

    #for t in threads:
    #    print(results_thread[i])

    for i in range(len(results_thread)):
        #print(str(i))
        for j in range(len(results_thread[i])):
            print(results_thread[i][j])
            writer.writerow(results_thread[i][j])
