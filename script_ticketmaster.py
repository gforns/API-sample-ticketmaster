#!/usr/bin/python3

import requests
import sys


if __name__ == "__main__":

    # Check if number arguments is fine. If not we exit.
    if len(sys.argv) != 4:
        print("Wrong arguments")
        print("You need to run:  python3", sys.argv[0] , "<API_key> <Start_Date(2019-08-01T00:00:00Z)> <End_Date(2019-08-31T00:00:00Z)>" )
        sys.exit()


    # Fill vars with provided arguments 
    # TODO: Check if arguments are correct
    api_key=sys.argv[1]
    start_date=sys.argv[2]
    end_date=sys.argv[3]


    # Fill a dictionary for initial paramters for the Web Service
    parameters = {}
    parameters["classificationName"] = "Musician"
    parameters["countryCode"] = "US"
    parameters["apikey"] = api_key
    parameters["startDateTime"] = start_date
    parameters["endDateTime"] = end_date
    parameters["page"] = 0
    parameters["size"] = 100
    
    

    # Initialization for the loop requesting the web service
    is_last_page = False

    # Initialization of dictionaries where we will keep track of the artists by state, venues by state, and expensive ticket by state
    count_artists = {}
    count_venues = {}
    expensive_ticket = {}
    

    # Loop to get all the pages from the web_service
    while (not is_last_page):
        # REST get from API with the parameters given above
        response = requests.get("http://app.ticketmaster.com/discovery/v2/events.json", params = parameters)


        # if HTTP code is not 200, we exit program
        if response.status_code != 200:
            print("Error receiving data from ticketmaster: " , response.status_code, response.json() )
            sys.exit()

        # Deserialization of json resonse in result.
        result = response.json()
        
        
        # If there are next pages,  keep requesting next page to web_service, otherewise we stop the loop
        if "next" in result["_links"].keys():
            parameters["page"] += 1
            
        else:
            is_last_page = True
        
        # API can only get 1000 embeded results:  'API Limits Exceeded: Max paging depth exceeded. (page * size) must be less than 1,000'
        if parameters["page"] * parameters["size"] >= 1000:
            print("----")
            print("WARNING: API Limits Exceeded: Max paging depth exceeded. (page * size) must be less than 1,000. Showing only first 1000")
            print("----")
            is_last_page = True


        # If no "_embedded" key, it means, nothing to show. So we exit.
        if "_embedded" not in result.keys():
            print("No events to show")
            sys.exit()


        # We parse embedded events.
        for event in result["_embedded"]["events"]:
            # initialization of a list of artists for the event
            atractions  = []

            # we get the event_name
            event_name = event["name"]

            # let's build a dictionary to count each venue by state, incrementing everytime we see the same venue on that state
            for venue in event["_embedded"]["venues"]:

                state_name = venue["state"]["name"]

                if state_name not in count_venues.keys():
                    count_venues[state_name] = {}
                    count_venues[state_name][venue["name"]] = 1
                else:
                    if venue["name"] not in count_venues[state_name].keys():
                        count_venues[state_name][venue["name"]] = 1
                    else:
                        count_venues[state_name][venue["name"]] += 1


            # build a dictionary of artists by state and incrementing everytime we see the same artist on the state
            for atraction in event["_embedded"]["attractions"]:

                # creation of a list of atractions of the event
                atractions.append(atraction["name"])

                # add state and artist in the dictionary of artists by state
                if state_name not in count_artists.keys():
                    count_artists[state_name] = {}
                    count_artists[state_name][atraction["name"]] = 1
                else:
                    if atraction["name"] not in count_artists[state_name].keys():
                        count_artists[state_name][atraction["name"]] = 1
                    else:
                        count_artists[state_name][atraction["name"]] += 1

                

            # Some events have no price information. We tet the max price or we keep as -1.
            max_price = -1
            if "priceRanges" in event.keys():
                for pricerange in event["priceRanges"]:
                    if "max" in pricerange.keys():
                        max_price = pricerange["max"]
                    

            if max_price >= 0:       
                # We keep a dictionary of max prices. On each state we will keep (max_price, event_name and list of artists)
                if state_name not in expensive_ticket.keys():
                    expensive_ticket[state_name] = [max_price, event_name, atractions]
            
                else:
                    # if actual max_price is greater than the one stored in the list, we update the dictionary with current values
                    if expensive_ticket[state_name][0] < max_price:
                        expensive_ticket[state_name] = [max_price, event_name, atractions]

        # End Parsing Events

    # End of the loop


    # At this point we have 3 dictionaries:
    #       - count_artists["state"]["artist"] stores number of times artist played in state.
    #       - count_venues["state"]["venue"]   stores number of times venue has a event in state.
    #       - expensive_tikcet["state"]        stores a list  [max_price, event_max_price, list_of_artists_of_event_max_price] for each state.

    
    # Visualizatiom of data for each state we will generate results. We sort the states
    for state in sorted(count_artists):
        max_artist_list = []
        max_venue_list = []
        max_ticket_price = ""
        event_max_price = ""
        artist_w_max_price = []


        # We get the maximum number of events done by artist and we select these artists to append to max_artist_list.
        max_number_artist = max(list(count_artists[state].values()))
        for artist, num in count_artists[state].items():
            if num == max_number_artist:
                max_artist_list.append(artist)


        # We get the maximum number of eventsdone by venue and we select these venues to append to max_venue_list.
        max_number_venue = max(list(count_venues[state].values()))
        for venue, num in count_venues[state].items():
            if num == max_number_venue:
                max_venue_list.append(venue)

            
        
        # We get the values for the expensive_ticket of the state (some states may not have information so we need to check if we have information before)
        if state in expensive_ticket.keys():
            max_ticket_price = expensive_ticket[state][0]
            event_max_price = expensive_ticket[state][1]
            artist_w_max_price = expensive_ticket[state][2]

            

        # We print on output the csv. Customer can create a file by redirecting the output
        # TODO: List needs to be transformed to string
        # TODO: Create file and write into the file as csv

        print(state + ";" + str(max_artist_list) + ";" + str(max_venue_list) + ";" + str(max_ticket_price) + ";" + event_max_price + ";" + str(artist_w_max_price) + ";")
    


