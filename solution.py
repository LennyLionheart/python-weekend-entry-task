import csv
import datetime
import sys
import argparse
import json

# evaluate command-line inputs
parser = argparse.ArgumentParser(description = 'Flight comparing program.')
parser.add_argument('flightdata', metavar = 'F', type = str, help = 'filepath for the csv containing the flight data' )
parser.add_argument('origin', metavar = 'O', type = str, help = 'Origin airport code')
parser.add_argument('destination', metavar = 'D', type = str, help = 'Destination airport code')
parser.add_argument('--bags', type = int, default = 0, help = 'Number of requested bags')
# parser.add_argument('--return', dest = 'returntrip', action = 'store_true', help = 'Is it a return flight?')

args = parser.parse_args()

# inputs
flightdata = args.flightdata
origin = args.origin
destination = args.destination
bags_count = args.bags
# returntrip = args.returntrip


# open file and put the flight into a tuple of dictionaries

with open(str(flightdata), 'r') as read_obj:

    list_of_flights = []

    csv_reader = csv.DictReader(read_obj)
    for line in csv_reader:
        list_of_flights.append(line)

    for flight in list_of_flights:
        flight['departure'] = datetime.datetime.strptime(flight['departure'],'%Y-%m-%dT%H:%M:%S')
        flight['arrival'] = datetime.datetime.strptime(flight['arrival'],'%Y-%m-%dT%H:%M:%S')
        flight['base_price'] = float(flight['base_price'])
        flight['bag_price'] = float(flight['bag_price'])
        flight['bags_allowed'] = int(flight['bags_allowed'])

    # dropping low baggage flights if necessary
    if bags_count == 2:

        two_bag_list_of_flights = [flight for flight in list_of_flights if flight['bags_allowed'] == 2]
        list_of_flights = two_bag_list_of_flights



tuple_of_flights = tuple(list_of_flights)

def flightsearchloop(*flightcheck): # function for assembling the right flight solutions

    global flight_solutions
    global destination

    # filtering for no repeating airports
    repeating_airport_condition = "False"
    origin_list = []

    for x in range(len(flightcheck)):
        origin_list.append(flightcheck[x]['origin'])

    if len(origin_list) == len(set(origin_list)):
            repeating_airport_condition = "True"


    if (flightcheck[-2]['destination'] == flightcheck[-1]['origin'] and
        repeating_airport_condition == "True" and
        flightcheck[-1]['departure'] - flightcheck[-2]['arrival'] > datetime.timedelta(hours = 1) and # filtering the layover times
        flightcheck[-1]['departure'] - flightcheck[-2]['arrival'] < datetime.timedelta(hours = 6)): # filtering the layover times

              if flightcheck[-1]['destination'] == destination:

                  to_append = []

                  for i in flightcheck:
                      to_append.append(i)

                  flight_solutions.append(to_append)
                  return True
              else:
                  return False

    else:
        return True

flight_solutions = []
# one flight permutations
for flight1 in tuple_of_flights:

    if flight1['origin'] == origin:

        if flight1['destination'] == destination:
            flight_solutions.append([flight1])
        else:
            # two flight permutations of the not direct flights
            for flight2 in tuple_of_flights:

                if flightsearchloop(flight1, flight2):
                    pass
                else:
                    # three flight permutations of the not direct two flight permutations
                    for flight3 in tuple_of_flights:

                        if flightsearchloop(flight1, flight2, flight3):
                            pass
                        else:
                            # four flight permutations of the not direct three flight permutations
                            for flight4 in tuple_of_flights:

                                if flightsearchloop(flight1, flight2, flight3, flight4):
                                    pass
                                else:
                                    # five flight permutations of the not direct three flight permutations
                                    for flight5 in tuple_of_flights:

                                        if flightsearchloop(flight1, flight2, flight3, flight4, flight5):
                                            pass
                                        else:
                                            # six flight permutations of the not direct three flight permutations
                                            for flight6 in tuple_of_flights:

                                                if flightsearchloop(flight1, flight2, flight3, flight4, flight5, flight6):
                                                    pass
                                                else:
                                                    # seven flight permutations of the not direct three flight permutations
                                                    for flight7 in tuple_of_flights:
                                                        flightsearchloop(flight1, flight2, flight3, flight4, flight5, flight6, flight7)



jsonlist = []
# building the output
for flight in flight_solutions:

    travel_time = flight[-1]['arrival'] - flight[0]['departure']
    travel_time = str(travel_time)
    bags_allowed = 2
    total_price = 0

    for i in range(len(flight)):

        total_price += flight[i]['base_price'] + bags_count * flight[i]['bag_price']

        if flight[i]['bags_allowed'] == 1: # filtering for baggage limits
            bags_allowed = 1

    jsonlist.append({
                        'flights' : flight,
                        'bags_allowed' : bags_allowed,
                        'bags_count' : bags_count,
                        'destination' : destination,
                        'origin' : origin,
                        'total_price' : total_price,
                        'travel_time' : travel_time,
                    })

# sorting based on price
jsonlist.sort(key = lambda x: x.get('total_price'))

json_string = json.dumps(jsonlist, indent = 4, default = str)

print(json_string)
print(len(flight_solutions))
