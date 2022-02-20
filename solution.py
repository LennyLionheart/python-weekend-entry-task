import csv
import datetime
import sys
import argparse

#evaluate command-line inputs
parser = argparse.ArgumentParser(description = 'Flight comparing program.')
parser.add_argument('flightdata', metavar = 'F', type = str, help = 'filepath for the csv containing the flight data' )
parser.add_argument('origin', metavar = 'O', type = str, help = 'Origin airport code')
parser.add_argument('destination', metavar = 'D', type = str, help = 'Destination airport code')
parser.add_argument('--bags', type = int, default = 0, help = 'Number of requested bags')
parser.add_argument('--return', dest = 'returntrip', action = 'store_true', help = 'Is it a return flight?')

args = parser.parse_args()

#inputs
flightdata = args.flightdata
origin = args.origin
destination = args.destination
bagcount = args.bags
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

        tuple_of_flights = tuple(list_of_flights)

finally:
    read_obj.close()

# one_flight_trips = [dict for dict in tuple_of_flights if dict['origin'] == origin]
# flight_solutions.extend(one_flight_trips)

flight_solutions = []

one_flight_trips = []


for flight1 in tuple_of_flights:
    if flight1['origin'] == origin:
        if flight1['destination'] == destination:
            flight_solutions.append(flight1)
        else:
            # nondestination_one_flight_trips.append(flight1)
            for flight2 in tuple_of_flights:
                if (flight1['destination'] == flight2['origin'] and
                    flight2['departure'] - flight1['arrival'] > datetime.timedelta(hours = 1) and
                    flight2['departure'] - flight1['arrival'] < datetime.timedelta(hours = 6)):
                        if flight2['destination'] == destination:
                            flight_solutions.append([flight1, flight2])
                        else:
                            for flight3 in tuple_of_flights:
                                if (flight2['destination'] == flight3['origin'] and
                                    flight3['origin'] != origin and
                                    flight3['departure'] - flight2['arrival'] > datetime.timedelta(hours = 1) and
                                    flight3['departure'] - flight2['arrival'] < datetime.timedelta(hours = 6)):
                                    if flight3['destination'] == destination:
                                        flight_solutions.append([flight1, flight2, flight3])
                                    else:
                                        for flight4 in tuple_of_flights:
                                            if (flight3['destination'] == flight4['origin'] and
                                                flight3['origin'] != origin and
                                                flight4['origin'] != origin and
                                                flight4['origin'] != flight2['origin'] and
                                                flight4['departure'] - flight3['arrival'] > datetime.timedelta(hours = 1) and
                                                flight4['departure'] - flight3['arrival'] < datetime.timedelta(hours = 6)):
                                                if flight4['destination'] == destination:
                                                    flight_solutions.append([flight1, flight2, flight3, flight4])

print(tuple_of_flights[5]['arrival'])





#
#
#
#
#
#
#
#     for row in tuple_of_flights:
#         if (row['destination'] == destination and
#             dict['destination'] == row['origin'] and
#             row['departure'] - dict['arrival'] > datetime.timedelta(hours = 1) and
#             row['departure'] - dict['arrival'] < datetime.timedelta(hours = 6)):
#             two_flight_trips.append([dict, row])
#
# # print(one_flight_trips)
#
# two_flight_trips = []
#
# for dict in one_flight_trips:
#     for row in tuple_of_flights:
#         if (row['destination'] == destination and
#             dict['destination'] == row['origin'] and
#             row['departure'] - dict['arrival'] > datetime.timedelta(hours = 1) and
#             row['departure'] - dict['arrival'] < datetime.timedelta(hours = 6)):
#             two_flight_trips.append([dict, row])
#
#
# flight_solutions.extend(two_flight_trips)
#
# # print(two_flight_trips)
#
# three_flight_trips = []
#
# for i, [dict, dictfinal] in enumerate(two_flight_trips):
#     for row in tuple_of_flights:
#         print(dictfinal['destination'])
#         if (row['destination'] == destination and
#             dictfinal['destination'] == row['origin']):
#             #  and
#             # row['departure'] - dictfinal['arrival'] > datetime.timedelta(hours = 1) and
#             # row['departure'] - dictfinal['arrival'] < datetime.timedelta(hours = 6)):
#             three_flight_trips.append(1)
#             print("1")
#
# flight_solutions.extend(three_flight_trips)
#
# print(three_flight_trips)
#
# # print(flight_solutions)
# #
# # three_flight_trips = []
# #
# # for i,x in enumerate(two_flight_trips):
# #     for y in range(len(tuple_of_flights)):
# #         if (tuple_of_flights[x[1]][destination_column] == tuple_of_flights[y][origin_column] and
# #             tuple_of_flights[y][departure_column] - tuple_of_flights[x[1]][arrival_column] > datetime.timedelta(hours = 1) and
# #             (tuple_of_flights[y][departure_column] - tuple_of_flights[x[1]][arrival_column] < datetime.timedelta(hours = 6))):
# #             three_flight_trips.append(two_flight_trips[i] + [y])
# #
# # flight_solutions.extend(three_flight_trips)
# #
# # four_flight_trips = []
# #
# # for i,x in enumerate(three_flight_trips):
# #     for y in range(len(tuple_of_flights)):
# #         if (tuple_of_flights[x[2]][destination_column] == tuple_of_flights[y][origin_column] and
# #             tuple_of_flights[y][departure_column] - tuple_of_flights[x[2]][arrival_column] > datetime.timedelta(hours = 1) and
# #             (tuple_of_flights[y][departure_column] - tuple_of_flights[x[2]][arrival_column] < datetime.timedelta(hours = 6))):
# #             four_flight_trips.append(three_flight_trips[i] + [y])
# #
# # flight_solutions.extend(four_flight_trips)
# #
# #
# #
