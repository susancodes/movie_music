import json
import requests
import urllib

genre_reponse = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=eb90ad0ff308c0b16691816876d0f9f4')
genre_text = json.loads(genre_reponse.text).get('genres')

genre_ids = [item.get('id') for item in genre_text]


def get_all_movie_titles(genre_ids):
	all_movie_titles = []

	# grabbing all movies' titles
	for genre_id in genre_ids:
		movie_res = requests.get('https://api.themoviedb.org/3/genre/{}/movies?api_key=eb90ad0ff308c0b16691816876d0f9f4'.format(genre_id))
		movie_list = json.loads(movie_res.text).get('results')
		all_movie_titles.extend(item.get('title') for item in movie_list)

	return all_movie_titles


# grab all of the soundtrack popularity for each movie
for movie in all_movie_titles:

def get_movie_soundtrack_popularity(movie):

	# this spotify access token will expire.
	headers = {
		'Authorization': 'Bearer BQCs32Pkj7wyEKF6wWZMq6F8dJon5814D2IFaTZPoQ7Gdl2sYcCitDVgxTS0z9GW3CTZ2QPRBlnilqvur_UvTA'
	}
	params = urllib.urlencode({'q': movie, 'type': 'album', 'limit': 1})

	# we're making a search for the album name by using the movie name. we're only asking for the first search result
	st_res = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

	album_text = json.loads(st_res.text).get('albums')

	if not album_text:
		continue

	album_items = album_text.get('items')

	if not album_items:
		continue

	# we only asked for the first result in our api request so we know it's the first item and we've already checked that the list exists
	album_id = album_items[0].get('id')

	album_res = requests.get('https://api.spotify.com/v1/albums/{}'.format(album_id), headers=headers)
	return json.loads(album_res.text).get('popularity')
