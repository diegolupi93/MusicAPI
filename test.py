import unittest
import json
from flask_caching import Cache
from unittest.mock import patch
from app import parse_info, get_artist_info, app
from constants import ARTIST_DESCRIPTION, ARTIST_DISCOGRAPHY, FIELDS, ALBUM_FIELDS

class TestApp(unittest.TestCase):
    
    def setUp(self):
        cache = Cache()
        cache.init_app(app, config={"CACHE_TYPE": "SimpleCache"})
        with app.app_context():
            cache.clear()

        self.app = app.test_client()

    def test_parse_info(self):
        fields = FIELDS
        album_fields = ALBUM_FIELDS
        description1 = [{"strArtist":"Coldplay",
                       "strStyle":"Rock/Pop",
                       "strMood":"Happy",
                       "strCountry":"London, UK",
                       "singer": "Palito ortega"}]
        description2 = [{"strArtist":"Coldplay",
                       "strStyle":None,
                       "strMood":3,
                       "strCountry":(2, 'es')}]
        discography1 = {'album':[{"strAlbum":"Higher Power","intYearReleased":"2021"},
                        {"strAlbum":"Music of the Spheres","intYearReleased":"2021"}]}
        discography2 = {"album":None}
        result1 = parse_info(description1, discography1, fields, album_fields)
        result2 = parse_info(description2, discography2, fields, album_fields)
        expected1 = {'artist':'Coldplay',
                     'style': 'Rock/Pop',
                     'mood': 'Happy',
                     'country': 'London, UK',
                     'discography': [
                        {'album':'Higher Power',
                         'year': '2021'
                        },
                        {'album': 'Music of the Spheres',
                         'year': '2021'
                        }
                     ]}
        expected2 = {'artist':'Coldplay',
                     'style': None,
                     'mood': 3,
                     'country': (2, 'es'),
                     'discography': []
                    }
        self.assertEqual(result1, expected1)
        self.assertEqual(result2, expected2)

    
    @patch('app.urllib.request.urlopen')
    def test_get_artist_info(self, mock_url_open):
        def get_api_responses():
            yield {'artists':[{"strArtist":"Coldplay",
                       "strStyle":"Rock/Pop",
                       "strMood":"Happy",
                       "strCountry":"London, UK",
                       "singer": "Palito ortega"}],
                       'other_field': 'key'}
            yield {'album':[{"strAlbum":"Higher Power","intYearReleased":"2021"},
                        {"strAlbum":"Music of the Spheres","intYearReleased":"2021"}]}
        responses = get_api_responses()
        fields = FIELDS
        artist = 'Coldplay'
        album_fields = ALBUM_FIELDS

        mock_url_open.return_value = mock_url_open
        mock_url_open.getcode.return_value = 200
        mock_url_open.read.side_effect = lambda: json.dumps(next(responses))
        result = get_artist_info(artist, ARTIST_DESCRIPTION, ARTIST_DISCOGRAPHY, fields, album_fields)
        expected = {'artist':'Coldplay',
                     'style': 'Rock/Pop',
                     'mood': 'Happy',
                     'country': 'London, UK',
                     'discography': [
                        {'album':'Higher Power',
                         'year': '2021'
                        },
                        {'album': 'Music of the Spheres',
                         'year': '2021'
                        }
                     ]}
        self.assertEqual(result, expected)

    @patch('app.get_artist_info')
    def test_get_artist(self, mock_get_artist_info):

        mock_get_artist_info.return_value = {'artist': 'Coldplay',
                                            'style': 'Rock/Pop',
                                            'mood': 'Happy',
                                            'country': 'London, UK',
                                            'discography': [
                                            {'album':'Higher Power',
                                            'year': '2021'
                                            },
                                            {'album': 'Music of the Spheres',
                                            'year': '2021'
                                            }
                                            ]}
                                    
        artist = self.app.get('/artist?name=Coldplay')

        expected = {'artist':'Coldplay',
                     'style': 'Rock/Pop',
                     'mood': 'Happy',
                     'country': 'London, UK',
                     'discography': [
                        {'album':'Higher Power',
                         'year': '2021'
                        },
                        {'album': 'Music of the Spheres',
                         'year': '2021'
                        }
                     ]}
                    
        self.assertEqual(artist.json, expected)
        self.assertEqual(artist.status_code, 200)
        self.assertEqual(artist.mimetype, 'application/json')
    
    @patch('app.get_artist_info')
    def test_get_artist_fail(self, mock_get_artist_info):

        mock_get_artist_info.side_effect = ValueError
        artist = self.app.get('/artist?name=Coldplay')
        expected = {'message' : 'Route not found'}      
        self.assertEqual(artist.json, expected)
        self.assertEqual(artist.status_code, 404)
        self.assertEqual(artist.mimetype, 'application/json')
        

if __name__ == '__main__':
    unittest.main()