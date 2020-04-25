import os
import unittest
from datetime import datetime, timedelta, date
from flask import json
import sys
sys.path.append(".") # Adds higher directory to python modules path.

from extensions import db
from app import create_app
from config import TestConfig
from controllers.database.pandemic_whistle import PandemicWhistle

class ReportTests(unittest.TestCase):
    def setUp(self):
        app = create_app(TestConfig)
        app.app_context().push()
        self.client = app.test_client()
        db.create_all()
  
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def create_records(self):
        date1 = datetime(2020, 1, 1).timestamp()
        date2 = datetime(2020, 2, 1).timestamp()
        date3 = datetime(2020, 3, 1).timestamp()
        date4 = datetime(2020, 4, 1).timestamp()
        date5 = datetime(2020, 5, 1).timestamp()
        p1 = PandemicWhistle(hash='abc1', district_state='OH', district=1, reported_date=date1)
        p2 = PandemicWhistle(hash='abc2', district_state='OH', district=1, reported_date=date2)
        p3 = PandemicWhistle(hash='abc3', district_state='OH', district=1, reported_date=date3)
        p4 = PandemicWhistle(hash='abc4', district_state='OH', district=1, reported_date=date4)
        p5 = PandemicWhistle(hash='abc5', district_state='OH', district=1, reported_date=date5)
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.add(p5)
        db.session.commit()

    def test_no_data(self):
        response = self.client.get('/v1/reports', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_with_data(self):
        self.create_records()
        response = self.client.get('/v1/reports', follow_redirects=True)
        self.assertEqual(len(response.json), 5)
    
    def test_with_start_no_results(self):
        self.create_records()
        start_date = datetime(2020, 6, 1).timestamp()
        response = self.client.get('/v1/reports?start_date=' + str(start_date), follow_redirects=True)
        self.assertEqual(len(response.json), 0)
    
    def test_with_start_results(self):
        self.create_records()
        start_date = datetime(2020, 2, 1).timestamp()
        response = self.client.get('/v1/reports?start_date=' + str(start_date), follow_redirects=True)
        self.assertEqual(len(response.json), 4)

    def test_with_end_no_results(self):
        self.create_records()
        end_date = datetime(2020, 1, 1).timestamp()
        response = self.client.get('/v1/reports?end_date=' + str(end_date), follow_redirects=True)
        self.assertEqual(len(response.json), 0)

    def test_with_end_results(self):
        self.create_records()
        end_date = datetime(2020, 4, 1).timestamp()
        response = self.client.get('/v1/reports?end_date=' + str(end_date), follow_redirects=True)
        self.assertEqual(len(response.json), 3)

    def test_with_both_no_results(self):
        self.create_records()
        start_date = datetime(2020, 6, 1).timestamp()
        end_date = datetime(2020, 7, 1).timestamp()
        response = self.client.get('/v1/reports?start_date=' + str(start_date) + '&end_date=' + str(end_date), follow_redirects=True)
        self.assertEqual(len(response.json), 0)

    def test_with_both_results(self):
        self.create_records()
        start_date = datetime(2020, 2, 1).timestamp()
        end_date = datetime(2020, 5, 1).timestamp()
        response = self.client.get('/v1/reports?start_date=' + str(start_date) + '&end_date=' + str(end_date), follow_redirects=True)
        self.assertEqual(len(response.json), 3)

    def test_with_bad_start(self):
        self.create_records()
        response = self.client.get('/v1/reports?start_date=i_like_cheese', follow_redirects=True)
        self.assertEqual(response.json.get('message'), 'Invalid start_date')
        self.assertEqual(response.status_code, 400)

    def test_with_bad_end(self):
        self.create_records()
        response = self.client.get('/v1/reports?end_date=i_like_cheese', follow_redirects=True)
        self.assertEqual(response.json.get('message'), 'Invalid end_date')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()  