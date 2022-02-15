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

        # format datatypes
        formatted_list_of_flights = list_of_flights

        for i in range(len(list_of_flights)):
            for x in range(i):
                # dates
                if x == 3 or x == 4:
                    formatted_list_of_flights[i][x] = datetime.datetime.strptime(list_of_flights[i][x],"%Y-%m-%dT%H:%M:%S")

                # prices
                if x == 5 or x == 6:
                    formatted_list_of_flights[i][x] = float(list_of_flights[i][x])

                # allowed bagcount
                if  x == 7:
                    formatted_list_of_flights[i][x] = int(list_of_flights[i][x])

        # turning data into tuples...  does this make any sense with repeated big company size calculations?
        for i in range(len(formatted_list_of_flights)):
            formatted_list_of_flights[i] = tuple(formatted_list_of_flights[i])

        tuple_of_flights = tuple(formatted_list_of_flights)


finally:
    read_obj.close()


print(flightdata)
print(origin)
print(destination)
print(bagcount)
print(returntrip)

print(tuple_of_flights)
