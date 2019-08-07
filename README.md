# script_ticketmaster.py


script_ticketmaste.py mainly gets information from Ticketmaster API:

https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/

script_ticketmaster.py accepts these parameters:
  - **api_key**  (provided by ticketmaster API)
  - **date_start** (format needs to be like: 2019-08-21T00:00:00Z)  This is UTC time.
  - **date_end**   (format needs to be like: 2019-08-30T00:00:00Z)  This is UTC time.
  
  
Script pulls all events in the US with the classificationName “Musician” within the specified date range and
segments the events pulled above by US State and generates a CSV that contains:

 - The state name
 - The musician(s) with the most events in the state
 - The venue with the most events in the state
 - The most expensive ticket price of any event in the state
 - The event name of the event with the most expensive ticket price
 - The musician(s) of the event with the most expensive ticket price


The script parses all events that satisfy the criteria, and creates 2 dictionaries to maintain number of times something happen  (an artist plays or a venue hosts an event) for each state.

It also maintains a dictionary storing, for each state, information aboutthe event with most expensive ticket (price,  event_name and artists played on it). 

To keep track we check on every event, if the actual event's max_price is greater than the one stored in the dictionary. If so, we cahnge the stored values for the current ones.

After everything has been parsed, for each state, we get the artists with maximum number of events on that state. The same for the venues.

Finally we print, for each state the desired data.


## Install Instructions

This script was built for python3 and uses external [requests](https://2.python-requests.org/en/master/) module .

Make sure first to have python3 installed:

In Ubuntu Linux 18.04, you can check python version by typing python3 command:

```
$ python3 --version
Python 3.6.8
```

To install requests module on a Ubuntu Linux 18.04 LTS, you can use pip:

```
$ apt-get install python3-pip
$ pip3 install requests
```

To run the script you need to type:

```
$ python3 script_ticketmaster.py <api_key> <starting_date> <end_date>
```

To create a csv file for the output you just need to redirect standard output to a file. 
For example, this command will reate a file output.csv with the data:

```
$ python3 script_ticketmaster.py <api_key> 2019-08-01T00:00:00Z 2019-08-31T00:00:00Z  > output.csv
```

In case of any problem feel free to contact me to discuss it.
