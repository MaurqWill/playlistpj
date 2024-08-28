from flask import Flask, request, jsonify

app = Flask(__name__)


# Song class to encapsulate song attributes
class Song:
    def __init__(self, title, artist, genre):
        self.title = title
        self.artist = artist
        self.genre = genre

    def __str__(self):
        return f"{self.title} by {self.artist} ({self.genre})"


# Playlist class to manage songs
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, song):
        self.songs.append(song)

    def remove_song(self, song):
        self.songs.remove(song)

    def __str__(self):
        song_list = ", ".join(str(song) for song in self.songs)
        return f"Playlist: {self.name}\nSongs: {song_list}"


# Dictionary to manage multiple playlists
playlists = {}

# Function to create a playlist
def create_playlist(name):
    if name in playlists:
        print(f"Playlist {name} already exists!")
    else:
        playlists[name] = Playlist(name)
        print(f"Playlist {name} created.")

# Function to add a song to a playlist
def add_song_to_playlist(playlist_name, song):
    if playlist_name in playlists:
        playlists[playlist_name].add_song(song)
        print(f"Added {song} to {playlist_name}.")
    else:
        print(f"Playlist {playlist_name} does not exist!")

# Function to remove a song from a playlist
def remove_song_from_playlist(playlist_name, song=None, from_end=False):
    if playlist_name in playlists:
        playlist = playlists[playlist_name]
        if song:
            playlist.remove_song(song)
            print(f"Removed {song} from {playlist_name}.")
        elif from_end:
            removed_song = playlist.songs.pop()
            print(f"Removed {removed_song} from {playlist_name}.")
        else:
            removed_song = playlist.songs.pop(0)
            print(f"Removed {removed_song} from {playlist_name}.")
    else:
        print(f"Playlist {playlist_name} does not exist!")



# Binary search to find a song by title
def binary_search(songs, target_title):
    left, right = 0, len(songs) - 1
    while left <= right:
        mid = (left + right) // 2
        if songs[mid].title == target_title:
            return mid
        elif songs[mid].title < target_title:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Merge sort to sort songs by title, artist, or genre
def merge_sort(songs, key=lambda x: x.title):
    if len(songs) <= 1:
        return songs

    mid = len(songs) // 2
    left = merge_sort(songs[:mid], key)
    right = merge_sort(songs[mid:], key)

    return merge(left, right, key)

def merge(left, right, key):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

# Sort songs in a playlist
def sort_songs_in_playlist(playlist_name, by='title'):
    if playlist_name in playlists:
        playlist = playlists[playlist_name]
        if by == 'title':
            playlist.songs = merge_sort(playlist.songs, key=lambda x: x.title)
        elif by == 'artist':
            playlist.songs = merge_sort(playlist.songs, key=lambda x: x.artist)
        elif by == 'genre':
            playlist.songs = merge_sort(playlist.songs, key=lambda x: x.genre)
        print(f"Sorted songs in {playlist_name} by {by}.")
    else:
        print(f"Playlist {playlist_name} does not exist!")


@app.route('/songs', methods=['POST'])
def create_song():
    data = request.json
    song = Song(data['title'], data['artist'], data['genre'])
    return jsonify({'message': 'Song created', 'song': song.__dict__}), 201

@app.route('/playlists', methods=['POST'])
def create_playlist_api():
    data = request.json
    create_playlist(data['name'])
    return jsonify({'message': f"Playlist {data['name']} created."}), 201

@app.route('/playlists/<name>', methods=['GET'])
def get_playlist(name):
    if name in playlists:
        playlist = playlists[name]
        return jsonify({'playlist': playlist.name, 'songs': [song.__dict__ for song in playlist.songs]}), 200
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlists/<name>/songs', methods=['POST'])
def add_song_to_playlist_api(name):
    data = request.json
    song = Song(data['title'], data['artist'], data['genre'])
    add_song_to_playlist(name, song)
    return jsonify({'message': f"Song {song.title} added to {name}."}), 200

@app.route('/playlists/<name>/songs/<title>', methods=['DELETE'])
def remove_song_from_playlist_api(name, title):
    if name in playlists:
        playlist = playlists[name]
        song_index = binary_search(playlist.songs, title)
        if song_index != -1:
            removed_song = playlist.songs.pop(song_index)
            return jsonify({'message': f"Song {removed_song.title} removed from {name}."}), 200
        return jsonify({'error': 'Song not found'}), 404
    return jsonify({'error': 'Playlist not found'}), 404

@app.route('/playlists/<name>/songs/sort', methods=['POST'])
def sort_songs_in_playlist_api(name):
    data = request.json
    sort_songs_in_playlist(name, by=data.get('by', 'title'))
    return jsonify({'message': f"Songs in {name} sorted by {data.get('by', 'title')}."}), 200

if __name__ == '__main__':
    app.run(debug=True)



# Hip Hop Songs
hip_hop_songs = [
    Song("N.Y. State of Mind", "Nas", "Hip Hop"),
    Song("All of the Lights", "Kanye West", "Hip Hop"),
    Song("No Role Modelz", "J. Cole", "Hip Hop"),
    Song("Straight Outta Compton", "N.W.A", "Hip Hop"),
    Song("C.R.E.A.M.", "Wu-Tang Clan", "Hip Hop")
]

# Rap Songs
rap_songs = [
    Song("Big Poppa", "The Notorious B.I.G.", "Rap"),
    Song("HUMBLE.", "Kendrick Lamar", "Rap"),
    Song("Party Up (Up In Here)", "DMX", "Rap"),
    Song("Gold Digger", "Kanye West", "Rap"),
    Song("Lose Yourself", "Eminem", "Rap")
]

# R&B Songs
rnb_songs = [
    Song("Kiss of Life", "Mary J. Blige", "R&B"),
    Song("Pony", "Ginuwine", "R&B"),
    Song("Can We Talk", "Tevin Campbell", "R&B"),
    Song("Let’s Get It On", "Marvin Gaye", "R&B"),
    Song("No Scrubs", "TLC", "R&B")
]

# Create playlists
create_playlist("Hip Hop Essentials")
create_playlist("Classic Rap")
create_playlist("Timeless R&B")

# Add songs to playlists
for song in hip_hop_songs:
    add_song_to_playlist("Hip Hop Essentials", song)

for song in rap_songs:
    add_song_to_playlist("Classic Rap", song)

for song in rnb_songs:
    add_song_to_playlist("Timeless R&B", song)

# Print playlists
print(playlists["Hip Hop Essentials"])
print(playlists["Classic Rap"])
print(playlists["Timeless R&B"])
