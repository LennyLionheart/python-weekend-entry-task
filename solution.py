import csv
import datetime
import sys
import argparse
import json

#evaluate command-line inputs
parser = argparse.ArgumentParser(description = 'Flight comparing program.')
parser.add_argument('flightdata', metavar = 'F', type = str, help = 'filepath for the csv containing the flight data' )
parser.add_argument('origin', metavar = 'O', type = str, help = 'Origin airport code')
parser.add_argument('destination', metavar = 'D', type = str, help = 'Destination airport code')
parser.add_argument('--bags', type = int, default = 0, help = 'Number of requested bags')
# parser.add_argument('--return', dest = 'returntrip', action = 'store_true', help = 'Is it a return flight?')

args = parser.parse_args()

#inputs
flightdata = args.flightdata
origin = args.origin
destination = args.destination
bags_count = args.bags
returntrip = args.returntrip


# open file and put the flight into a tuple of dictionaries
try:
    with open(str(flightdata), 'r') as read_obj:

        list_of_flights = []

        csv_reader = csv.DictReader(read_obj)
        for line in csv_reader:
            list_of_flights.append(line)

        for dict in list_of_flights:
            dict['departure'] = datetime.datetime.strptime(dict['departure'],'%Y-%m-%dT%H:%M:%S')
            dict['arrival'] = datetime.datetime.strptime(dict['arrival'],'%Y-%m-%dT%H:%M:%S')
            dict['base_price'] = float(dict['base_price'])
            dict['bag_price'] = float(dict['bag_price'])
            dict['bags_allowed'] = int(dict['bags_allowed'])

        # dropping low baggage flights if necessecery
        if bags_count == 2:

            two_bag_list_of_flights = [dict for dict in list_of_flights if dict['bags_allowed'] == 2]
            list_of_flights = two_bag_list_of_flights



        tuple_of_flights = tuple(list_of_flights)

finally:
    read_obj.close()

flight_solutions = []
# one flight permutations
for flight1 in tuple_of_flights:

    if flight1['origin'] == origin:

        if flight1['destination'] == destination:
            flight_solutions.append([flight1])

        else:
            # two flight permutations of the not direct flights
            for flight2 in tuple_of_flights:

                if (flight1['destination'] == flight2['origin'] and
                    flight2['departure'] - flight1['arrival'] > datetime.timedelta(hours = 1) and # filtering the layover times
                    flight2['departure'] - flight1['arrival'] < datetime.timedelta(hours = 6)): # filtering the layover times

                        if flight2['destination'] == destination:
                            flight_solutions.append([flight1, flight2])

                        else:
                            # three flight permutations of the not direct two flight permutations
                            for flight3 in tuple_of_flights:

                                if (flight2['destination'] == flight3['origin'] and
                                    flight3['origin'] != origin and # no airport repetition
                                    flight3['departure'] - flight2['arrival'] > datetime.timedelta(hours = 1) and # filtering the layover times
                                    flight3['departure'] - flight2['arrival'] < datetime.timedelta(hours = 6)): # filtering the layover times

                                    if flight3['destination'] == destination:
                                        flight_solutions.append([flight1, flight2, flight3])

                                    else:
                                        # four flight permutations of the not direct three flight permutations
                                        for flight4 in tuple_of_flights:

                                            if (flight3['destination'] == flight4['origin'] and
                                                flight3['origin'] != origin and # no airport repetition
                                                flight4['origin'] != origin and # no airport repetition
                                                flight4['origin'] != flight2['origin'] and # no airport repetition
                                                flight4['departure'] - flight3['arrival'] > datetime.timedelta(hours = 1) and # filtering the layover times
                                                flight4['departure'] - flight3['arrival'] < datetime.timedelta(hours = 6)): # filtering the layover times

                                                if flight4['destination'] == destination:
                                                    flight_solutions.append([flight1, flight2, flight3, flight4])



jsonlist = []
# building the output
for flight in flight_solutions:

    travel_time = flight[-1]['arrival'] - flight[0]['departure']
    travel_time = str(travel_time)
    bags_allowed = 2
    total_price = 0

    for i in range(len(flight)):

        total_price += flight[i]['base_price'] + bags_count * flight[i]['bag_price']

        if flight[i]['bags_allowed'] == 1: #filtering for baggage limits
            bags_allowed = 1

    jsonlist.append({
                        'flights' : flight,
                        'bags_allowed' : bags_allowed,
                        'bags_count' : bags_count,
                        'destination' : destination,
                        'origin' : origin,
                        'total_price' : total_price,
                        'travel_time' : travel_time
                    })

# sorting based on price
jsonlist.sort(key = lambda x: x.get('total_price'))

json_string = json.dumps(jsonlist, indent = 4, default = str)

print(json_string)
