import sys
import os
import collections
from datetime import datetime
try: import Queue as Q  # ver. < 3.0
except ImportError: import queue as Q


def update_dic(dic, key, val): 
    if key in dic:
        dic[key] += val
    else:
        dic[key] = val

        
# input: a dictionary where values are the integers
# output: a list of 10 items form this dictionary
# that have the maximum values sorted in descended order 
def get_top_ten(dic):
    top_ten = Q.PriorityQueue()
    count = 0
    for key, val in dic.items():
        top_ten.put((val, key))
        count +=1
        if count > 10: # we keep only 10 top items
            top_ten.get()       
    top_reverse = []
    while not top_ten.empty():
        top_reverse.append(top_ten.get())       
    return top_reverse


# input: two string in format "[%d/%b/%Y:%H:%M:%S"
# for example: [01/Jul/1995:00:00:01
# output: time difference in seconds
def get_time_diff(time1, time2):
    date_format = "[%d/%b/%Y:%H:%M:%S"
    diff = (datetime.strptime(time1, date_format) -
            datetime.strptime(time2, date_format)).seconds
    return diff


# to move the items that is older than one hour from a queue to a priority
# queue of the busiest 60 minutes periods.
# last_hour_queue is a queue of pairs (time, timezone)
# busiest_hours_pr_queue is a priority queue: item - (time, timezone),
# priority  - the number of requests during the next hour
def move_old_items(last_hour_queue, time, busiest_hours_pr_queue, flag):
    while len(last_hour_queue) != 0:
        diff = get_time_diff(time, last_hour_queue[0][0])
        
        # When we are done with reading, we still have the requests of the last
        # hour in hast_hour queue. We need to process them, but diff is less
        # than one hour, thus we increase the diff
        if flag == "end": 
            diff += 3601 
            
        if diff > 3600:
            current = last_hour_queue[0][0]
            req_count = len(last_hour_queue)

            #when a request is one hour old, we try to put its time in the
            #priority queue using the number of the request at this hour as
            #priority number
            busiest_hours_pr_queue.put((req_count, last_hour_queue.popleft()))

            # we keep only 10 best candidates
            if busiest_hours_pr_queue.qsize () > 10:
                busiest_hours_pr_queue.get()

            #now we need to remove the requests with the same time from the
            #last_hour_queue               
            while ((len(last_hour_queue) != 0) and
                               current == last_hour_queue[0][0]):
                last_hour_queue.popleft() 
        else:
            break

# to remove items that are older than time_interval from a queue.
# input: a queue of pairs (host, time), time as a string in format
# "[%d/%b/%Y:%H:%M:%S" , time interval as an integer in seconds
def remove_old(my_queue, time, time_interval):
    while not len(my_queue) == 0:
        diff = get_time_diff(time, my_queue[0][1])
        if diff > time_interval:
            my_queue.popleft()
        else:
            break
        
# input: reply code as a string, a queue of pairs (host, time),
# host as a string, time as a string in format "[%d/%b/%Y:%H:%M:%S",
# a queue blocked_for_5_min of pairs (host, time),
def update_last_20_sec_fails(reply_code, last_20_sec_fails, host, time,
                             blocked_for_5_min):
    if reply_code == "401":
        last_20_sec_fails.append((host, time))
                        
        #calculate the number of failed requests from this IP in the last 20sec:
        count = 0
        for i in range(len(last_20_sec_fails)):
            if host == last_20_sec_fails[i][0]:
                count += 1

        #we block this IP if the count is 3 or more                           
        if count >= 3:
            blocked_for_5_min.append((host, time))

    # since the login attempt is successful we need to remove the requests 
    # with the same host form last_20_sec_fails queue           
    else: 
        items_to_delite = []
        for i in last_20_sec_fails:
            if host == i[0]:
                items_to_delite.append(i)
        for item in items_to_delite:
            last_20_sec_fails.remove(item)
               
    
# input: name of out file, list of top hosts
def write_top_hosts(out_file, top_hosts):
    file_out  = open(out_file, "w")
    for i in reversed(top_hosts):
        file_out.write(i[1] + "," + str(i[0]) + "\n")
    file_out.close()

# input: name of out file, a priority queue
def write_busiest_hours(out_file, busiest_hours):
    hours_reverse = []
    while not busiest_hours.empty():
        hours_reverse.append(busiest_hours.get())
    file_out  = open(out_file, "w")
    for i in reversed(hours_reverse):
        file_out.write(str(i[1][0][1: ]) +" " +str(i[1][1][ :-1]) + ","
                        + str(i[0]) + "\n")
    file_out.close()

# input: name of out file, list of top resourses
def write_top_resourses(out_file, top_resourses):
    file_out  = open(out_file, "w")
    for i in reversed(top_resourses):       
        file_out.write(i[1] + "\n")
    file_out.close()

# input: name of out file, a list of requests
def write_list(out_file, my_list):
    file_out  = open(out_file, "w")
    for i in my_list:
        file_out.write(i)
    file_out.close()

# input: name of out file, list of the most dangerous hosts
def write_top_danger(out_file, top_danger):
    file_out  = open(out_file, "w")
    for i in reversed(top_danger):
        file_out.write(i[1] + "," + str(i[0]) + "\n")
    file_out.close()
    

def main():
    
    input_file = sys.argv[1] # ./log_input/log3.txt
    out_file1 = sys.argv[2] # ./log_output/hosts.txt
    out_file2 = sys.argv[3] # ./log_output/hours.txt
    out_file3 = sys.argv[4] # ./log_output/resources.txt
    out_file4 = sys.argv[5] # ./log_output/blocked.txt
    out_file5 = sys.argv[6] # ./log_output/dangerous_hosts.txt
    out_file6 = sys.argv[7] # ./log_output/missed_requests.txt

    if os.stat(input_file).st_size == 0:
        print (input_file, "is empty")
        
    
    line_count = 0
    print(datetime.now())
    
    host_count = {}
    bandwidth = {}
    busiest_hours = Q.PriorityQueue()
    last_hour = collections.deque()
    blocked = []
    last_20_sec_fails = collections.deque()
    blocked_for_5_min = collections.deque()
    most_dangerous = {} # for my additional feature

    missed_requests = [] # to keep the requests that are too short or too long

    with open(input_file, "rb") as infile:
        for line in infile:
            l = line.split()
            if len(l) < 9 or len(l) > 11:
                missed_requests.append(line)
                continue
            try:
                host = l[0]
                time = l[3]
                timezone = l[4]
                resource = l[6]
                reply_code = l[-2] 
                bites_numb = l[-1]
                if l[6] == "/" and l[7][0] != "H": #some of the requests have space 
                    l[6] = l[6] + l[7] # between "/" and the next part of the address
                if l[6][0] != "/":
                    missed_requests.append(line)
                    continue                   
                host = l[0]
                time = l[3]
                timezone = l[4]
                resource = l[6]
                reply_code = l[-2] 
                bites_numb = l[-1] 

                request_is_blocked = 0
                
                update_dic(host_count, host, 1)
                
                if bites_numb == "-":
                    bites_numb = "0"
                    
                update_dic(bandwidth, resource, int(bites_numb))
                move_old_items(last_hour, time, busiest_hours, flag = "loop")                        
                last_hour.append((time, timezone))

                #remove the restrictions that are older than 5 min:
                remove_old(blocked_for_5_min, time, 300)

                #remove the failed requests that are older than 20 seconds:
                remove_old(last_20_sec_fails, time, 20)
                
                # we need to check if the IP is blocked for 5 min
                for i in range(len(blocked_for_5_min)):
                    if host == blocked_for_5_min[i][0]:
                        blocked.append(line)
                        update_dic(most_dangerous, host, 1)
                        request_is_blocked = 1 # is blocked

                # when a request is not blocked: if it has reply_code "401",
                # we put it in the queue of failed requests, else we should
                # check if we had two failde requests from this IP in the
                # last 20 sec, we have to remove them from the queue of
                # failed requests
                if request_is_blocked == 0: # not blocked
                    update_last_20_sec_fails(reply_code, last_20_sec_fails,
                                host, time, blocked_for_5_min)
            except:
                missed_requests.append(line)
                
            #Statistics: print how many lines are done
            line_count += 1
            if line_count % 100000 == 0:
                print(line_count, " lines are done")           
                  
    infile.close()


    if len(last_hour) != 0:
        last_request_time = last_hour[-1][0]
        move_old_items(last_hour, last_request_time, busiest_hours, flag = "end")

    top_hosts = get_top_ten(host_count)
    top_resourses = get_top_ten(bandwidth)
    top_danger = get_top_ten(most_dangerous)

    write_top_hosts(out_file1, top_hosts)
    write_busiest_hours(out_file2, busiest_hours)
    write_top_resourses(out_file3, top_resourses)
    write_list(out_file4, blocked)
    write_top_danger(out_file5, top_danger)

    write_list(out_file6, missed_requests)
    
    print(datetime.now())
        
if __name__ == '__main__':
    main()
