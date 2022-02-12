import csv
import datetime


# open file and put the flights into tuples
try:
    with open('example/example0.csv', 'r') as read_obj:

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

                # allowed bagscount
                if  x == 7:
                    formatted_list_of_flights[i][x] = int(list_of_flights[i][x])

        # turning data into tuples...  does this make any sense with repeated bigger company size calculations?
        for i in range(len(formatted_list_of_flights)):
            formatted_list_of_flights[i] = tuple(formatted_list_of_flights[i])

        tuple_of_flights = tuple(formatted_list_of_flights)


finally:
    read_obj.close()
