import json
import requests
import urllib

genre_list = []

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
# "Authorization: Bearer BQBKTvUytqIIyuz7mULGu-dILUb4qf-xXWDRMcUOiV7Q-6ViHrlfbgkQHGYwTZ5W-5q6rj9PPnE-AocpWc44E_hlaP5Nnqd9J3tcxZ5CjKE2dLNfGGXbxgGJzbvxT3mSEdFHZrQy6H8"
	headers = {
		'Authorization': 'Bearer BQBKTvUytqIIyuz7mULGu-dILUb4qf-xXWDRMcUOiV7Q-6ViHrlfbgkQHGYwTZ5W-5q6rj9PPnE-AocpWc44E_hlaP5Nnqd9J3tcxZ5CjKE2dLNfGGXbxgGJzbvxT3mSEdFHZrQy6H8'
	}
	params = urllib.urlencode({'q': movie, 'type': 'album', 'limit': 1})

	st_res = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

	album_text = json.load(st_res.text).get('album')

	if not album_text:
		continue

	album_items = album_text.get('items')

	if not album_items:
		continue

	album_id = album_items[0].get('id')

	

	

