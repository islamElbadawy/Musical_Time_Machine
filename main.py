import  requests
from bs4 import BeautifulSoup
import lxml
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint


CLIENT_ID = "5965afb6fd624041aa9501d242529e8b"
CLIENT_SECRET = "5dd182be41a842ad8d107607795af34a"


date = input("what year you would like to travel to ? in YYY-MM-DD format : ")

url = "https://www.billboard.com/charts/hot-100"

page = requests.get(f"{url}/{date}").text

soup = BeautifulSoup(page, "lxml")

songs_rows = [song for song in soup.find_all(name="ul", class_="o-chart-results-list-row")]

songs = [song.find(name="h3").getText().strip() for song in songs_rows]


for song in songs:
    print(song)

scope = "playlist-modify-private"


sp = spotipy.Spotify(
        auth_manager= SpotifyOAuth(
                        client_id=CLIENT_ID,
                        client_secret=CLIENT_SECRET,
                        scope= scope,
                        redirect_uri= 'https://developer.spotify.com/dashboard/applications/',
                        show_dialog=True,
                        cache_path="token.txt"
                        )
)

user_id = sp.current_user()["id"]
print(user_id)




results = []
year = date.split('-')[0]


for song in songs[:20]:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        results.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id,name="best songs", public=False)
playlist_id = playlist["id"]
sp.playlist_add_items(playlist_id=playlist_id, items=results)





