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


# open file and put the flights into tuples
try:
    with open(str(flightdata), 'r') as read_obj:

        csv_reader = csv.reader(read_obj)

        list_of_flights = list(map(list, csv_reader))

        # delete the header
        list_of_flights = list_of_flights[1:]

        #name the columns
        flight_no_column = 0
        origin_column = 1
        destination_column = 2
        departure_column = 3
        arrival_column = 4
        base_price_column = 5
        bag_price_column = 6
        bags_allowed_column = 7

        # format datatypes
        formatted_list_of_flights = list_of_flights

        for i in range(len(list_of_flights)):
            for x in range(len(list_of_flights[0])):
                # dates
                if x == departure_column or x == arrival_column:
                    formatted_list_of_flights[i][x] = datetime.datetime.strptime(list_of_flights[i][x],"%Y-%m-%dT%H:%M:%S")

                # prices
                if x == base_price_column or x == bags_allowed_column:
                    formatted_list_of_flights[i][x] = float(list_of_flights[i][x])

                # allowed bagcount
                if  x == bags_allowed_column:
                    formatted_list_of_flights[i][x] = int(list_of_flights[i][x])

        # turning data into tuples...  does this make any sense with repeated big company size calculations?
        formatted_list_of_flights = [tuple(formatted_list_of_flights[i]) for i in range(len(formatted_list_of_flights))]

        tuple_of_flights = tuple(formatted_list_of_flights)

finally:
    read_obj.close()


one_flight_trips = [i for i in range(len(tuple_of_flights)) if tuple_of_flights[i][origin_column] == origin]

# print(one_flight_trips)

flight_solutions = []

flight_solutions.extend(one_flight_trips)

two_flight_trips = []

for i in one_flight_trips:
    for x in range(len(tuple_of_flights)):
        if (tuple_of_flights[i][destination_column] == tuple_of_flights[x][origin_column] and
        tuple_of_flights[x][departure_column] - tuple_of_flights[i][arrival_column] > datetime.timedelta(hours = 1) and
        (tuple_of_flights[x][departure_column] - tuple_of_flights[i][arrival_column] < datetime.timedelta(hours = 6))):
            two_flight_trips.append([i, x])

flight_solutions.extend(two_flight_trips)

# print(flight_solutions)

three_flight_trips = []

for i,x in enumerate(two_flight_trips):
    for y in range(len(tuple_of_flights)):
        if (tuple_of_flights[x[1]][destination_column] == tuple_of_flights[y][origin_column] and
            tuple_of_flights[y][departure_column] - tuple_of_flights[x[1]][arrival_column] > datetime.timedelta(hours = 1) and
            (tuple_of_flights[y][departure_column] - tuple_of_flights[x[1]][arrival_column] < datetime.timedelta(hours = 6))):
            three_flight_trips.append(two_flight_trips[i] + [y])

flight_solutions.extend(three_flight_trips)

four_flight_trips = []

for i,x in enumerate(three_flight_trips):
    for y in range(len(tuple_of_flights)):
        if (tuple_of_flights[x[2]][destination_column] == tuple_of_flights[y][origin_column] and
            tuple_of_flights[y][departure_column] - tuple_of_flights[x[2]][arrival_column] > datetime.timedelta(hours = 1) and
            (tuple_of_flights[y][departure_column] - tuple_of_flights[x[2]][arrival_column] < datetime.timedelta(hours = 6))):
            four_flight_trips.append(three_flight_trips[i] + [y])

flight_solutions.extend(four_flight_trips)
