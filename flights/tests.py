from django.test import Client, TestCase
from django.db.models import Max

from .models import Airport, Flight

# Create your tests here.
class ModelTestCase(TestCase):

    def setUp(self):
        # Create airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create flights.
        Flight.objects.create(origin=a1, destination=a2, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=200)
        Flight.objects.create(origin=a2, destination=a1, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departures_count(self):
        ''' test departures count '''
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)
    
    def test_arrivals_count(self):
        ''' test arrivals count '''
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 2)

    def test_valid_flight(self):
        ''' test valid flight '''
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=100)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self):
        ''' test invalid flight '''
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_index(self):
        ''' test index view '''
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 4)

    def test_valid_flight_page(self):
        ''' test validity of flight page '''
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        
        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
    
    def test_invalid_flight_page(self):
        ''' test invalidity of flight page ''' 
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        c = Client()
        response = c.get(f"/{max_id + 1}")
        self.assertEqual(response.status_code, 404)
