from re import A
from flask import Flask, request, jsonify, make_response
import urllib.request, json
from flask_caching import Cache 
from constants import ARTIST_DESCRIPTION, ARTIST_DISCOGRAPHY, FIELDS, ALBUM_FIELDS

app = Flask(__name__)
app.config.from_object('config.Config')  # Set the configuration variables to the flask application
cache = Cache(app)  # Initialize Cache

def parse_info(description, discography, fields, album_fields):
    """Parse the artist data into a dictionary

    :param description: The artist's description
    :type description: dict
    :param discography: The artist's discography
    :type discography: dict
    :param fields: Mapping the inputs fields names to output fileds of artist's characteristics
    :type fields: list of tuples
    :param fields: Mapping the inputs fields names to output fileds of artist's discography
    :type fields: list of tuples
    :returns: a dict with the artist's data
    :rtype: dict
    """
    result = {}
    description = description[0]
    for page_field, my_field in fields:
        if page_field in description.keys():
            result[my_field] = description[page_field]

    result['discography'] = []
    if discography['album']:
        for disc in discography['album']:
            aux_dict = {}
            for page_field, my_field in album_fields:
                aux_dict[my_field] = disc[page_field]
            result['discography'].append(aux_dict)
    return result

def get_artist_info(artist, artist_description, artist_discography, fields, album_fields):
    """Parse the artist data into a dictionary

    :param artist: The artist's name
    :type artist: string
    :param artist_description: The artist's description url
    :type artist_description: string
    :param artist_discography: The artist's discography url
    :type artist_discography: string
    :param fields: Mapping the inputs fields names to output fileds of artist's characteristics
    :type fields: list of tuples
    :param fields: Mapping the inputs fields names to output fileds of artist's discography
    :type fields: list of tuples
    :returns: a dict with the artist's data
    :rtype: dict
    """

    artist = artist.replace(' ', '') # delete spaces

    artist_description = artist_description.format(artist)

    artist_discography = artist_discography.format(artist)
    descrip = urllib.request.urlopen(artist_description)
    descrip = descrip.read()
    description = json.loads(descrip)['artists']

    discogr = urllib.request.urlopen(artist_discography)
    discogr = discogr.read()    
    discography = json.loads(discogr)

    if description is None:
        raise ValueError

    result = parse_info(description, discography, fields, album_fields)

    return result

@app.route('/artist')
@cache.cached(timeout=120, query_string=True)
def get_artist():
    
    artist = request.args.get('name', None)
    if artist is None:
        return make_response(jsonify({'message' : 'Route not found'}), 404)
    try:
        response = get_artist_info(artist, ARTIST_DESCRIPTION, ARTIST_DISCOGRAPHY, FIELDS, ALBUM_FIELDS)
    except ValueError:
        return make_response(jsonify({'message' : 'Route not found'}), 404)

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=False)