from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        
        self.client = app.test_client()
        app.config['TESTING'] = True
    
    def test_home(self):
        '''make sure home page shows html markup and game board'''
        with self.client:
            
            response = self.client.get('/')
            self.assertIn(b'<p>High Score:',response.data)
            self.assertIn('board',session)

    def test_valid_word(self):
        '''create a table and test if a word on board returns a valid word''' 
        with self.client as client:
            with client.session_transaction() as session:
                session['board'] = [['H','O','T'],
                                    ['H','O','T'],
                                    ['H','O','T']]
            response = self.client.get('/word-check?word=hot')
            self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        '''test words that are not on the board or not real words'''
        self.client.get('/')
        response = self.client.get('/word-check?word=pbsqsf')
        self.assertEqual(response.json['result'], 'not-word')
        
        response = self.client.get('/word-check?word=leg')
        self.assertEqual(response.json['result'], 'not-on-board')
        


