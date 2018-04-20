import csv

RESTAURANTS_FILE = 'restaurants.csv'
EVENTS_FILE = 'events.csv'
YELP_FILE = 'yelpdata.csv'

list_of_restaurants = []
list_of_events = []
list_of_yelp_data = []

def init_events(csv_file_name=EVENTS_FILE):
    global list_of_events
    with open(csv_file_name, encoding="utf8") as csvFile:
        csvReader = csv.reader(csvFile)
        next(csvReader)
        global list_of_events
        list_of_events = []
        for r in csvReader:
            r[0] = int(r[0])
            list_of_events.append(r)

def events_happening(sortby='time', sortorder='desc'):
    if sortby == 'time':
        sortcol = 3
    rev = (sortorder == 'asc')
    sorted_list = sorted(list_of_events, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list

def init_restaurants(csv_file_name2=RESTAURANTS_FILE):
    global list_of_restaurants
    with open(csv_file_name2, encoding="utf8") as csvFile2:
        csvReader2 = csv.reader(csvFile2)
        next(csvReader2)
        global list_of_restaurants
        list_of_restaurants = []
        for r in csvReader2:
            r[0] = int(r[0])
            r[2] = int(r[2])
            r[3] = float(r[3])
            list_of_restaurants.append(r)

def get_restaurants(sortby='price', sortorder='desc'):
    if sortby == 'price':
        sortcolumn = 2
    elif sortby == 'rating':
        sortcolumn = 3
    else:
        sortby = 0
    rev2 = (sortorder == 'desc')
    sorted_restaurants = sorted(list_of_restaurants, key=lambda row: row[sortcolumn], reverse=rev2)
    return sorted_restaurants

def init_yelp(csv_file_name3=YELP_FILE):
    global list_of_yelp_data
    with open(csv_file_name3, encoding="utf-8") as csvFile3:
        csvReader3 = csv.reader(csvFile3)
        global list_of_yelp_data
        list_of_yelp_data = []
        for r in csvReader3:
            r[1] = int(r[1])
            list_of_yelp_data.append(r)

def get_yelp(sortby='review_count', sortorder='desc'):
    if sortby == 'review_count':
        sortcol = 1
    rev3 = (sortorder == 'desc')
    sorted_yelp = sorted(list_of_yelp_data, key=lambda row:row[sortcol], reverse=rev3)
    return sorted_yelp
