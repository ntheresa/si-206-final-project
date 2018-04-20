SI 206 Final Project

My program aims to provide the user a fun weekend in Ann Arbor. My program will allow the user to see upcoming events happening at Michigan for the day as well as aggregation of top restaurants in Ann Arbor for a good outing with friends. First, I present data from the Happening @ Michigan (https://events.umich.edu/feeds) page for that day, which is already in json format. Then the user is presented with restaurants in Ann Arbor from Google Places API (https://developers.google.com/places/web-service/search#PlaceSearchResponses), which requires setting up an account and retrieving and API key. Then the user can choose to get more info about a restaurant from Yelp - using the phone number of the restaurant returned from Google API - (https://www.yelp.com/developers/documentation/v3/business_search), which requires making an account to get an API key as well as including headers. Make sure you put your API keys from Google and Yelp into a secrets.py file and import secrets into the main program to hide your API keys.

Please install all modules listed in requirements.txt to run the program successfully.
The program has 3 main functions to get data:
- get_umich_events(): retrieves event data for the current day from the Happening @ Michigan page which is then saved as instances in the UmichEvents class.
- get_google_restaurants(): retrieves Ann Arbor restaurants from Google Places API which is saved in GoogleRestaurants class to be used to populate the Restaurants database.
- create_yelp_table(): creates relation between Restaurants table and RestaurantDetails table in database by populating data from Yelp API using the phone number of the restaurant from the Restaurants table.

Brief user guide, including how to run the program and how to choose presentation options.
To run the program, simply run the file finalproject.py. When prompted with the question "Would you like the next Google results page? ", enter yes. (This is to not cause an error because Google delays the data collection by a couple seconds). You will see these lines:
  - Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
  - Restarting with stat
  - Debugger is active!
  - Debugger PIN: 324-859-096


Copy the url(http://127.0.0.1:5000/) and paste it into your browser. You will be on the home page! From there, you can choose to explore events at Michigan, or see Ann Arbor Restaurants. On the Ann Arbor Restaurants page, you can choose to sort the restaurants by rating or price. If you want to read reviews about a restaurant, simply click on the link that says "Go To Yelp Pages." Find the name of the restaurant you want, and copy and paste the Yelp URL into your browser.
Happy exploring!
