import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from itertools import chain


def give_me_recs():
    # Set up the Spotify client credentials
    client_id = "c1f4309625494c848f3d90c0b3f96813"
    client_secret = "7b676d5c061c439389d95257530a0a76"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Get the playlist ID
    playlist_id = "3rnUfkDDn2CUM8fsvz99Zl"
    # https://open.spotify.com/playlist/2mHUgJImW4zljkyFgLpCyB?si=19f43d342f204077
    # https://open.spotify.com/playlist/3WcxyS4KauVXjIb03g3v7R?si=39edd4ed1c7449a3
    # Get the tracks in the playlist
    results = sp.playlist_tracks(playlist_id=playlist_id)

    track_ids = []
    track_names = []
    for item in results["items"]:
        track = item["track"]
        id = track["id"]
        name = track["name"]
        track_ids.append(id)
        track_names.append(name)

    recommended_track_list = []

    # for i in range(0, len(track_ids) - 5, 1): # 20 x 95 = 1900 rec
    for i in range(0, len(track_ids) - 1, 5):  # 20 x 20 = 400 rec
        track_ids_slice = track_ids[i : i + 5]
        # Use the track IDs to get recommendations
        recommendations = sp.recommendations(seed_tracks=track_ids_slice)
        tracks = recommendations["tracks"]

        for track in tracks:
            id = track["id"]
            artist = track["artists"][0]["name"]
            track_name = track["name"]
            album = track["album"]["name"]
            recommended_track_info = []
            recommended_track_info = {
                "id": id,
                "artist": artist,
                "track_name": track_name,
                "album": album,
            }
            recommended_track_list.append(recommended_track_info)

    df = pd.DataFrame(recommended_track_list)
    # df is all recommendations, we want those that were recommended lots of times!

    # drop recommendations found earlier in playlist
    filtered = df.loc[df["track_name"].isin(track_names)]
    index = filtered.index
    df_trimmed = df.drop(index=index)

    # filter out duplicate recommendations (first one)
    duplicated = df_trimmed.duplicated()
    df_duplicated = df_trimmed[duplicated]

    if (
        df_duplicated.empty or len(df_duplicated) < 10
    ):  # show all recs if no duplicate recs or if less than 10 dup recs
        df_trimmed = df
        return df_trimmed
    else:
        # sort by most recommended
        df_duplicated = (
            df_duplicated.groupby(["id", "track_name", "artist", "album"])["track_name"]
            .count()
            .reset_index(name="count")
            .sort_values(["count"], ascending=False)
        )

        # drop songs recommended more than once
        trimmed_dups = df_duplicated.drop_duplicates()

        df_final = trimmed_dups.drop(columns=["count"])
        return df_final
