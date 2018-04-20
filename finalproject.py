import requests
import json
import sqlite3
import secrets
from flask import Flask, render_template, request
import model


app = Flask(__name__)

# Google key
google_key = secrets.google_api_key
# YELP keys
client_id = secrets.yelp_id
yelp_key = secrets.yelp_api_key
bearer_token = 'Bearer ' + yelp_key

DBNAME = 'restaurants.db'
def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print('Error creating database')

    statement0 = '''
        DROP TABLE IF EXISTS 'Events';
    '''
    cur.execute(statement0)
    conn.commit()

    statement00 = '''
        DROP TABLE IF EXISTS 'Restaurants';
    '''
    cur.execute(statement00)
    conn.commit()

    statement000 = '''
        DROP TABLE IF EXISTS 'RestaurantDetails';
    '''
    cur.execute(statement000)
    conn.commit()

    statement1 = '''
        CREATE TABLE 'Events' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'Type' TEXT NOT NULL,
            'Time' TEXT NOT NULL,
            'Location' TEXT NOT NULL,
            'Description' TEXT NOT NULL
        );
    '''
    cur.execute(statement1)
    statement2 = '''
        CREATE TABLE 'Restaurants' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT NOT NULL,
                'Price' INTEGER,
                'Rating' REAL,
                'Types' TEXT,
                'Hours' TEXT,
                'Address' TEXT NOT NULL,
                'Phone' TEXT );
    '''
    cur.execute(statement2)
    statement3 = '''
        CREATE TABLE 'RestaurantDetails' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT,
                'ReviewCount' INTEGER,
                'URL' TEXT,
                'RestaurauntId' INTEGER);
    '''
    cur.execute(statement3)
    conn.commit()
    conn.close()

UMICHJSON = 'umich_cache_file.json'
try:
    cache_file = open(UMICHJSON, 'r')
    cache_contents = cache_file.read()
    UMICH_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    UMICH_DICTION = {}
def make_umich_request_using_cache(baseurl, params):
    resp = requests.get(baseurl, params)
    dumped_json_cache = json.dumps(resp.text)
    fw = open(UMICHJSON,"w")
    fw.write(dumped_json_cache)
    fw.close()
    return UMICH_DICTION

class UmichEvents:
    def __init__(self, title = 'No Title', time = 'No Time', location = 'No Location', type = 'No Type', description = 'No Desc'):
        self.title = title
        self.time = time
        self.location = location
        self.type = type
        self.description = description
    def __str__(self):
        return '{} ({}) \n Time: {} \n Location: {} \n About: {}'.format(self.title, self.type, self.time, self.location, self.description)

def get_umich_events():
    events_list = []
    baseurl = 'https://events.umich.edu/day/json'
    umich_params = {'filter': '3,6,8,9,10,15,21', 'filter': 'show:new' }
    results = make_umich_request_using_cache(baseurl, params = umich_params)
    results_dict = json.loads(results)
    for event in results_dict:
        event_info = results_dict[event]
        title = event_info['event_title']
        time = event_info['time_start']
        location = event_info['location_name']
        type = event_info['event_type']
        description = event_info['description']
        umich_instance = UmichEvents(title, time, location, type, description)
        events_list.append(umich_instance)
    return events_list

def insert_events_data():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print('Error creating database')
    baseurl = 'https://events.umich.edu/day/json'
    umich_params = {'filter': '3,6,8,9,10,15,21', 'filter': 'show:new'}
    results = make_umich_request_using_cache(baseurl, params = umich_params)
    results_dict = json.loads(results)
    for event in results_dict:
        event_info = results_dict[event]
        title = event_info['event_title']
        time = event_info['time_start'][:5]
        location = event_info['location_name']
        type = event_info['event_type']
        description = event_info['description']
        insertion = (None, title, type, time, location, description)
        statement = 'INSERT INTO "Events" '
        statement += 'VALUES (?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

GOOGLEJSON = 'google_cache.json'
try:
    cache_file = open(GOOGLEJSON, 'r')
    cache_contents = cache_file.read()
    GOOGLE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    GOOGLE_DICTION = {}

def get_unique_key2(baseurl, params):
	alphabetized_keys= sorted(params.keys())
	lis = []
	for k in alphabetized_keys:
		lis.append("{}-{}".format(k, params[k]))
	return baseurl + "_".join(lis)

def make_google_request_using_cache(baseurl, params):
	unique_ident = get_unique_key2(baseurl, params)
	if unique_ident in GOOGLE_DICTION:
		return GOOGLE_DICTION[unique_ident]

	else:
		resp = requests.get(baseurl, params)
		GOOGLE_DICTION[unique_ident] = resp.text
		dumped_json_cache = json.dumps(GOOGLE_DICTION)
		fw = open(GOOGLEJSON,"w")
		fw.write(dumped_json_cache)
		fw.close()
		return GOOGLE_DICTION[unique_ident]

class GoogleRestaurants:
    def __init__(self, name = 'No Name', address = 'No Address', price = 0, rating = 0.0,
            types = 'No Types', id = 'No Id', days = 'No Days', phone = 'No Phone'):
        self.name = name
        self.address = address
        self.price = price
        self.rating = rating
        self.types = types
        self.id = id
        self.days = days
        self.phone = phone
    def __str__(self):
        return self.name

def get_google_restaurants():
    restaurants = []
    term = 'restaurants in Ann Arbor'
    baseurl = 'https://maps.googleapis.com/maps/api/place/textsearch/json?'
    google_params = {'query': term, 'key': google_key}
    results = make_google_request_using_cache(baseurl, params=google_params)
    results_dict = json.loads(results)
    next_page = str(results_dict['next_page_token'])
    data = results_dict['results']
    for place in data:
        name = place['name']
        address = place['formatted_address']
        try:
            price = place['price_level']
        except:
            None
        rating = place['rating']
        types = str(place['types'])
        id = place['place_id']

        place_id = str(id)
        baseurl2 = 'https://maps.googleapis.com/maps/api/place/details/json?'
        google_params2 = {'key': google_key, 'placeid': place_id}
        results2 = make_google_request_using_cache(baseurl2, params=google_params2)
        results_dict2 = json.loads(results2)['result']
        days = str(results_dict2['opening_hours']['weekday_text'])
        phone = results_dict2['international_phone_number'].replace('-', '').replace(" ", "")
        google_instance = GoogleRestaurants(name, address, price, rating, types, id, days, phone)
        restaurants.append(google_instance)

    user = input('Would you like the next Google results page? ')
    if user == 'yes':
        params2 = {'pagetoken': next_page, 'key': google_key}
        results2 = make_google_request_using_cache(baseurl, params2)
        results_dict2 = json.loads(results2)
        next_page = str(results_dict2['next_page_token'])
        data = results_dict2['results']
        for place in data:
            name = place['name']
            address = place['formatted_address']
            try:
                price = place['price_level']
            except:
                None
            try:
                rating = place['rating']
            except:
                None
            types = str(place['types'])
            id = place['place_id']

            place_id = str(id)
            baseurl3 = 'https://maps.googleapis.com/maps/api/place/details/json?'
            google_params3 = {'key': google_key, 'placeid': place_id}
            results3 = make_google_request_using_cache(baseurl2, params=google_params3)
            results_dict3 = json.loads(results3)['result']
            try:
                days = str(results_dict3['opening_hours']['weekday_text'])
            except:
                None
            phone = results_dict3['international_phone_number'].replace('-', '').replace(" ", "")
            google_instance = GoogleRestaurants(name, address, price, rating, types, id, days,phone)
            restaurants.append(google_instance)
    user = input('Would you like the next Google results page? ')
    if user == 'yes':
        params4 = {'pagetoken': next_page, 'key': google_key}
        results4 = make_google_request_using_cache(baseurl, params=params4)
        results_dict4 = json.loads(results4)
        data = results_dict4['results']
        for place in data:
            name = place['name']
            address = place['formatted_address']
            try:
                price = place['price_level']
            except:
                None
            try:
                rating = place['rating']
            except:
                None
            types = str(place['types'])
            id = place['place_id']

            place_id = str(id)
            baseurl5 = 'https://maps.googleapis.com/maps/api/place/details/json?'
            google_params5 = {'key': google_key, 'placeid': place_id}
            results5 = make_google_request_using_cache(baseurl5, params=google_params5)
            results_dict5 = json.loads(results5)['result']
            try:
                days = str(results_dict5['opening_hours']['weekday_text'])
            except:
                None
            phone = results_dict5['international_phone_number'].replace('-', '').replace(" ", "")
            google_instance = GoogleRestaurants(name, address, price, rating, types, id, days,phone)
            restaurants.append(google_instance)
    return restaurants

def insert_google_data():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print('Error creating database')
    all_restaurants = get_google_restaurants()
    for restaurant in all_restaurants:
        insertion = (None, restaurant.name, restaurant.price, restaurant.rating,
        restaurant.types, restaurant.days, restaurant.address, restaurant.phone)
        statement =  'INSERT INTO "Restaurants" '
        statement += 'VALUES (?,?,?,?,?,?,?,?)'
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

YELPJSON = 'yelp_cache.json'
try:
    cache_file = open(YELPJSON, 'r')
    cache_contents = cache_file.read()
    YELP_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    YELP_DICTION = {}
def get_unique_key2(baseurl, params):
    alphabetized_keys= sorted(params.keys())
    lis = []
    for k in alphabetized_keys:
        lis.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(lis)

def make_yelp_request_using_cache(baseurl, params):
    unique_ident = get_unique_key2(baseurl, params)
    if unique_ident in YELP_DICTION:
        return YELP_DICTION[unique_ident]
    else:
        headers = {'Authorization' : bearer_token}
        resp = requests.get(baseurl, params=params, headers=headers)
        YELP_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(YELP_DICTION)
        fw = open(YELPJSON,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return YELP_DICTION[unique_ident]

class YelpBusinesses:
    def __init__(self, name = 'No Name', review_count = 0, url= 'No URL'):
        self.name = name
        self.review_count = review_count
        self.url = url
def create_yelp_table():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except Error as e:
        print('Error creating database')
    statement = '''SELECT Phone, Id FROM Restaurants '''
    all_phones = cur.execute(statement).fetchall()
    for phone in all_phones:
        baseurl = 'https://api.yelp.com/v3/businesses/search/phone'
        params = {'phone': phone[0]}
        resp = make_yelp_request_using_cache(baseurl, params)
        results_dict = json.loads(resp)
        data = results_dict['businesses']
        for x in data:
            name = x['name']
            review_count = x['review_count']
            url = x['url']
            insertion = (None, name, review_count, url, phone[1])
            statement = 'INSERT INTO "RestaurantDetails" '
            statement += 'VALUES (?,?,?,?,?)'
            cur.execute(statement, insertion)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return '''
        <h1> Welcome to Theresa's Final Project!</h1>
        <h2> Are you ready to explore the University of Michigan?</h2>
        <img src="https://media.giphy.com/media/jzaZ23z45UxK8/giphy.gif" height="100px" width="200px"/>
        <ul>
            <li><a href="/events"> Explore Events happening at Michigan </a></li>
            <li><a href="/restaurants"> Explore Ann Arbor Restaurants </a></li>
        </ul>
    '''

@app.route('/events')
def events():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        events = model.events_happening(sortby, sortorder)
    else:
        events = model.events_happening()
    return render_template("events.html", events=events)

@app.route('/restaurants', methods=['GET', 'POST'])
def restaurants():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        restaurants = model.get_restaurants(sortby, sortorder)
    else:
        restaurants = model.get_restaurants()
    return render_template("restaurants.html", restaurants=restaurants)

@app.route('/yelp', methods=['GET', 'POST'])
def yelp():
    if request.method == 'POST':
        sortby = request.form['sortby']
        sortorder = request.form['sortorder']
        yelp = model.get_yelp(sortby, sortorder)
    else:
        yelp = model.get_yelp()
    return render_template("yelpdata.html", yelp=yelp)

if __name__=="__main__":
    init_db()
    insert_events_data()
    insert_google_data()
    create_yelp_table()
    model.init_events()
    model.init_restaurants()
    model.init_yelp()
    app.run(debug=True)
