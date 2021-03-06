import os
import json
import requests
import urllib


SPOTIFY_ACCESS_TOKEN = os.environ.get('SPOTIFY_ACCESS_TOKEN')
if not SPOTIFY_ACCESS_TOKEN:
    raise Exception('Spotify Access Token not available as an environment variable. Please set it before continuing.')
MOVIE_DB_KEY = os.environ.get('MOVIE_DB_KEY')
if not MOVIE_DB_KEY:
    raise Exception('Movie DB API key not available as an environment variable. Please set it before continuing.')


def get_all_movie_titles_for_genre(genre_id):
    movie_res = requests.get(
        'https://api.themoviedb.org/3/genre/{}/movies?api_key={}'.format(genre_id, MOVIE_DB_KEY)
    )
    movie_list = json.loads(movie_res.text).get('results')
    for movie in movie_list:
        yield movie.get('title')


def get_movie_soundtrack_popularity(movie):
    # this spotify access token will expire.
    headers = {
        'Authorization': 'Bearer {}'.format(SPOTIFY_ACCESS_TOKEN)
    }
    params = urllib.urlencode({'q': movie.encode('utf8'), 'type': 'album', 'limit': 1})

    # we're making a search for the album name by using the movie name. we're only asking for the first search result
    st_res = requests.get('https://api.spotify.com/v1/search', headers=headers, params=params)

    album_text = json.loads(st_res.text).get('albums')
    if not album_text:
        return 0

    album_items = album_text.get('items')
    if not album_items:
        return 0

    # we only asked for the first result in our api request so we know it's the first item and we've already checked
    # that the list exists
    album_id = album_items[0].get('id')
    album_res = requests.get('https://api.spotify.com/v1/albums/{}'.format(album_id), headers=headers)
    return json.loads(album_res.text).get('popularity')


def get_movie_soundtrack_popularity_avg_by_genre(genre_id):
    movie_titles = get_all_movie_titles_for_genre(genre_id)
    total_score = 0
    movie_count = 0

    for movie in movie_titles:
        pop_score = get_movie_soundtrack_popularity(movie)
        if not pop_score:
            continue
        total_score += pop_score
        movie_count += 1

    if movie_count == 0:
        return None

    return total_score / movie_count


def get_movie_music_popularity_scores():
    movie_music_list = []
    genre_reponse = requests.get(
        'https://api.themoviedb.org/3/genre/movie/list?api_key={}'.format(MOVIE_DB_KEY)
    )
    all_genre_list = json.loads(genre_reponse.text).get('genres')
    for genre_dict in all_genre_list:
        pop_score_avg = get_movie_soundtrack_popularity_avg_by_genre(genre_dict.get('id'))
        if not pop_score_avg:
            continue
        movie_music_list.append({
            'genre': genre_dict.get('name'),
            'popularity_avg': pop_score_avg
        })

    return movie_music_list


get_movie_music_popularity_scores()
