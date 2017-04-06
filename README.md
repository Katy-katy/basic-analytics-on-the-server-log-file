# Basic Analytics on The Server Log File

I was very exited to work on this challenge and I hope, I did it well. My main idea was to read the log file line by line and update all my data structure as needed. I used dictionaries, queue, and priority queues. Since I wanted to keep as less data as possible, I checked the oldest items in the queues and pop them when they were too old. The size of my priority queues was restricted by 10 items. I used a large log.txt file (about 4 500 000 lines) to test my programm and it took about 5 min to run on my machine. 
 

### Feature 1: 
List the top 10 most active host/IP addresses that have accessed the site.

I used dictionary to keep the count of requests from each IP address. After reading log file, I used a priority queue to choose 10 most active hosts. I put each  IP address in my priority queue using the count of the request as the priority. If the length of my priority queue was more than 10, I popped the item with the smallest count. Since my priority queue had only 10 items, and inserting takes a linear time,  I spent about 10 * number of IP address. Thus, Feature 1 takes O(n) time. 

### Feature 2: 
Identify the 10 resources that consume the most bandwidth on the site

As for the feature 1, I used a dictionary and a priority queue. Alsmost the same implementation as feature 1. 

### Feature 3:
List the top 10 busiest (or most frequently visited) 60-minute periods 

I used a queue to keep all requests for one hour. Then, when a request became too “old,” I used len() for queue to count how many requests we had for this hour. I popped the request time from one hour queue and pushed it in a priority queue using the number of request as its priority. The size of thus priority queue was also restricted by 10 items. I have found that len() of a queue takes O(1) time. Thus, this feature also take O(n) time.


### Feature 4: 
Detect patterns of three failed login attempts from the same IP address over 20 seconds so that all further attempts to the site can be blocked for 5 minutes. Log those possible security breaches.

I used two queues. One of them to keep the failed requests for 20 seconds. The second one to keep the IP that had three consecutive failed login attempts over 20 seconds. The IP from this queue must be blocked. Size of both queues were restricted by time - I removed old requests. This feature takes O(n * m * k ) where m is number of requests per 20 sec, and k is the number of IP that we are suppose to block.


### Optional features
### Feature 5:
List of the top 10 most dangerous hosts. The hosts that were blocked more often are in the dangerous_hosts.txt

As for feature 1 and 2 I used a dictionary and a priority queue. 

### Feature 6:

List of missed requests. Sometimes the requests have a strange formating or missing parts. 
Thus, I decided to put all requests that we can not prosess using this program in the missed_requests.txt. 
Now we can analyze them, too. 


***********************************************************************************
### Detailed Feature description form
https://github.com/InsightDataScience/fansite-analytics-challenge/blob/master/README.md#challenge-summary

### Feature 1 
List in descending order the top 10 most active hosts/IP addresses that have accessed the site.

Write to a file, named `hosts.txt`, the 10 most active hosts/IP addresses in descending order and how many times they have accessed any part of the site. There should be at most 10 lines in the file, and each line should include the host (or IP address) followed by a comma and then the number of times it accessed the site. 

e.g., `hosts.txt`:

    example.host.com,1000000
    another.example.net,800000
    31.41.59.26,600000
    …


### Feature 2 
Identify the top 10 resources on the site that consume the most bandwidth. Bandwidth consumption can be extrapolated from bytes sent over the network and the frequency by which they were accessed.

These most bandwidth-intensive resources, sorted in descending order and separated by a new line, should be written to a file called `resources.txt`


e.g., `resources.txt`:
    
    /images/USA-logosmall.gif
    /shuttle/resources/orbiters/discovery.html
    /shuttle/countdown/count.html
    …


### Feature 3 
List in descending order the site’s 10 busiest (i.e. most frequently visited) 60-minute period.

Write to a file named `hours.txt`, the start of each 60-minute window followed by the number of times the site was accessed during that time period. The file should contain at most 10 lines with each line containing the start of each 60-minute window, followed by a comma and then the number of times the site was accessed during those 60 minutes. The 10 lines should be listed in descending order with the busiest 60-minute window shown first. 

e.g., `hours.txt`:

    01/Jul/1995:00:00:01 -0400,100
    02/Jul/1995:13:00:00 -0400,22
    05/Jul/1995:09:05:02 -0400,10
    01/Jul/1995:12:30:05 -0400,8
    …

### Feature 4 
Your final task is to detect patterns of three consecutive failed login attempts over 20 seconds in order to block all further attempts to reach the site from the same IP address for the next 5 minutes. Each attempt that would have been blocked should be written to a log file named `blocked.txt`.

The site’s fictional owners don’t expect you to write the actual web server code to block the attempt, but rather want to gauge how much of a problem these potential security breaches represent. 

Detect three failed login attempts from the same IP address over a consecutive 20 seconds, and then write to the `blocked.txt` file any subsequent attempts to reach the site from the same IP address over the next 5 minutes. 

For example, if the third consecutive failed login attempt within a 20 second window occurred on `01/Aug/1995:00:00:08`, all access to the website for that IP address would be blocked for the next 5 minutes. Even if the same IP host attempted a login -- successful or not -- one minute later at `01/Aug/1995:00:01:08`, that attempt should be ignored and logged to the `blocked.txt` file. Access to the site from that IP address would be allowed to resume at `01/Aug/1995:00:05:09`.

If an IP address has not reached three failed login attempts during the 20 second window, a login attempt that succeeds during that time period should reset the failed login counter and 20-second clock. 

For example, if after two failed login attempts, a third login attempt is successful, full access should be allowed to resume immediately afterward. The next failed login attempt would be counted as 1, and the 20-second timer would begin there. In other words, this feature should only be triggered if an IP has  3 failed logins in a row, within a 20-second window.

e.g., `blocked.txt`

    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    …


## Download Data
You can download the data here: https://drive.google.com/file/d/0B7-XWjN4ezogbUh6bUl1cV82Tnc/view

## Description of Data

Assume you receive as input, a file, `log.txt`, in ASCII format with one line per request, containing the following columns:

* **host** making the request. A hostname when possible, otherwise the Internet address if the name could not be looked up.

* **timestamp** in the format `[DD/MON/YYYY:HH:MM:SS -0400]`, where DD is the day of the month, MON is the abbreviated name of the month, YYYY is the year, HH:MM:SS is the time of day using a 24-hour clock. The timezone is -0400.

* **request** given in quotes.

* **HTTP reply code**

* **bytes** in the reply. Some lines in the log file will list `-` in the bytes field. For the purposes of this challenge, that should be interpreted as 0 bytes.


e.g., `log.txt`

    in24.inetnebr.com - - [01/Aug/1995:00:00:01 -0400] "GET /shuttle/missions/sts-68/news/sts-68-mcc-05.txt HTTP/1.0" 200 1839
    208.271.69.50 - - [01/Aug/1995:00:00:02 -400] “POST /login HTTP/1.0” 401 1420
    208.271.69.50 - - [01/Aug/1995:00:00:04 -400] “POST /login HTTP/1.0” 200 1420
    uplherc.upl.com - - [01/Aug/1995:00:00:07 -0400] "GET / HTTP/1.0" 304 0
    uplherc.upl.com - - [01/Aug/1995:00:00:08 -0400] "GET /images/ksclogo-medium.gif HTTP/1.0" 304 0
    ...
    
In the above example, the 2nd line shows a failed login (HTTP reply code of 401) followed by a successful login (HTTP reply code of 200) two seconds later from the same IP address.


## My repo directory structure


    ├── README.md 
    ├── run.sh
    ├── src
    │   └── process_log.py
    ├── log_input
    │   └── log.txt
    ├── log_output
    |   └── hosts.txt
    |   └── hours.txt
    |   └── resources.txt
    |   └── blocked.txt
    |   └── dangerous_hosts.txt
    |   └── missed_requests.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_features
            |   ├── log_input
            |   │   └── log.txt
            |   |__ log_output
            |   │   └── hosts.txt
            |   │   └── hours.txt
            |   │   └── resources.txt
            |   │   └── blocked.txt   
            |   │   └── dangerous_hosts.txt
            |   │   └── missed_requests.txt
            ├── my_test
                ├── log_input
                │   └── your-own-log.txt
                |__ log_output
                    └── hosts.txt
                    └── hours.txt
                    └── resources.txt
                    └── blocked.txt
                    └── dangerous_hosts.txt
                    └── missed_requests.txt
