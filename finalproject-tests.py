import unittest
import finalproject as finalproject
import sqlite3
DBNAME = 'restaurants.db'

class TestTables(unittest.TestCase):
    def test_restaurants_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM Restaurants'
        results = cur.execute(sql)
        list_of_results = results.fetchall()
        self.assertIn(('Vinology',), list_of_results)
        self.assertEqual(len(list_of_results), 60)

        sql = 'SELECT * FROM Restaurants ORDER BY Rating DESC'
        result = cur.execute(sql)
        list_of_results = result.fetchall()
        self.assertEqual(list_of_results[1][1], 'The Lunch Room')
        self.assertEqual(list_of_results[0][3], 4.7)

        conn.close()

    def test_details_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Name FROM RestaurantDetails'
        results = cur.execute(sql)
        list_of_results = results.fetchall()
        self.assertIn(('Aventura',), list_of_results)

        sql = 'SELECT COUNT(*) FROM RestaurantDetails'
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 66)

        conn.close()

class TestTableJoins(unittest.TestCase):
    def test_joins(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT RestaurantDetails.Name
            FROM Restaurants
                JOIN RestaurantDetails
                ON Restaurants.Id = RestaurantDetails.RestaurauntId
            WHERE Price='3'
        '''
        results = cur.execute(sql)
        list_of_results = results.fetchall()
        self.assertIn(('Amadeus',), list_of_results)
        self.assertEqual(len(list_of_results), 7)
        conn.close()

class TestAPIs(unittest.TestCase):
    def testGoogleAPI(self):
        googles = finalproject.get_google_restaurants()
        self.assertTrue(len(googles) > 0)

class TestClasses(unittest.TestCase):
    def testUmichConstructor(self):
        e1 = finalproject.UmichEvents()
        e2 = finalproject.UmichEvents('Theresa Project', '10:00 PM', 'North Quad', 'SI 206', 'The final project demo')

        self.assertEqual(e1.title, 'No Title')
        self.assertEqual(e2.title, 'Theresa Project')
        self.assertEqual(e2.time, '10:00 PM')

    def testGoogleConstructor(self):
        g1 = finalproject.GoogleRestaurants()
        g2 = finalproject.GoogleRestaurants('The Restaurant', '12 Rest Way', 1, 3.3, 'Brunch', '345', 'Open Everyday', '123456789')

        self.assertEqual(g1.name, 'No Name')
        self.assertEqual(g1.phone,'No Phone')
        self.assertEqual(g2.address, '12 Rest Way')
        self.assertEqual(g2.rating, 3.3)
        self.assertEqual(g2.__str__(), 'The Restaurant')

    def testYelpConstructor(self):
        y1 = finalproject.YelpBusinesses()
        y2 = finalproject.YelpBusinesses('Best Bar', 5, 'www.bestbar.com')

        self.assertEqual(y1.review_count, 0)
        self.assertEqual(y2.url, 'www.bestbar.com')

if __name__ == "__main__":
	unittest.main(verbosity=2)
