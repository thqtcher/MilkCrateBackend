import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import random




def give_me_recs(playlist_id):

    # Set up the Spotify client credentials
    client_id = "c1f4309625494c848f3d90c0b3f96813"
    client_secret = "7b676d5c061c439389d95257530a0a76"
    client_credentials_manager = SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Initialize a list to store the results
    results = []

    # Make the initial API request
    response = sp.playlist_tracks(playlist_id=playlist_id)

    # Append the results to the list
    results.extend(response["items"])

    # Get the next page of results
    while response["next"]:
        response = sp.next(response)
        results.extend(response["items"])

    # parse through track IDs and names
    track_ids = []
    track_names = []

    for track in results:
        id = track["track"]["id"]
        name = track["track"]["name"]
        track_ids.append(id)
        track_names.append(name)

    # shuffle track ids to combat mass adding songs from same artist/album
    random.shuffle(track_ids)
    
    #if len(track_ids) > 100:
        #random.sample(track_ids, 100)
    # parse through track IDs and generate recommendations on each 5-song slice
    recommended_track_list = []

    for i in range(0, len(track_ids) - 1, 5):  # 20 x 20 = 400 rec
        # for i in range(0, len(track_ids) - 5, 1): # 20 x 95 = 1900 rec
        track_ids_slice = track_ids[i : i + 5]

        # Use the track IDs to get recommendations
        recommendations = sp.recommendations(seed_tracks=track_ids_slice)
        tracks = recommendations["tracks"]

        # build dictionary of recommendation information
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

    # turn rec information into a dataframe
    df = pd.DataFrame(recommended_track_list)
    # df is all recommendations, we want those that were recommended lots of times!

    # drop recommendations found anywhere else in playlist (so they don't get recommended songs they know)
    filtered = df.loc[df["track_name"].isin(track_names)]
    index = filtered.index
    df_trimmed = df.drop(index=index)

    # filter out duplicate recommendations (first one)
    duplicated = df_trimmed.duplicated()
    df_duplicated = df_trimmed[duplicated]

    # show all recs if no duplicate recs or if less than 10 dup recs
    if df_duplicated.empty or len(df_duplicated) < 10:
        df_trimmed = df
        df_final = df_trimmed.head(20)
        return df_final
    else:
        # sort by most recommended
        df_duplicated = (
            df_duplicated.groupby(["id", "track_name", "artist", "album"])["track_name"]
            .count()
            .reset_index(name="count")
            .sort_values(["count"], ascending=False)
        )

        # drop songs recommended more than once (so duplicates aren't shown on rec songs)
        trimmed_dups = df_duplicated.drop_duplicates()

        # cleaning final list
        df_final = trimmed_dups.drop(columns=["count"])
        df_final = df_final.head(20)

        return df_final


# print(give_me_recs(sys.argv[1]))
