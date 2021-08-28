from Web_Scraper import Web_Scraper
import pandas as pd
import random
import time

COLUMNS = ["Artist", "Album", "Title", "Release Date", "Lyric", "Position", "Sentiment"]

def collect_data(artist, writers):
    scraper = Web_Scraper(artist, writers)
    song_data_lines = pd.DataFrame(columns=COLUMNS)
    song_data_blocks = pd.DataFrame(columns=COLUMNS)

    songs = scraper.get_songs()
    random.shuffle(songs)
    print(len(songs))
    for song in songs:
        print(song)
        lyrics = scraper.get_lyrics(song)

        if lyrics != -1:
            album = scraper.extract_album(song)
            release_date = scraper.extract_release_date(song)
            song_data_lines = add_lyrics_by_line(song_data_lines, lyrics, artist, song, album, release_date)
            song_data_blocks = add_lyrics_by_block(song_data_blocks, lyrics, artist, song, album, release_date)
        wait_time = random.randint(5,30)
        time.sleep(wait_time)

    song_data_lines.to_csv(artist+" Data By Line.csv",index=False)
    song_data_blocks.to_csv(artist+" Data By Block.csv",index=False)
    return song_data_lines, song_data_blocks


def add_lyrics_by_line(df, lyrics, artist, song, album, release_date):
    lines = lyrics.split('\n')
    lines = [line for line in lines if line != '']
    return add_lyrics_to_df(df, artist, album, song, release_date, lines)

def add_lyrics_by_block(df, lyrics, artist, song, album, release_date):
    blocks = lyrics.split('\n\n')
    blocks = [block.replace('\n', " ") for block in blocks]
    return add_lyrics_to_df(df, artist, album, song, release_date, blocks)

def add_lyrics_to_df(df, artist, album, title, date, lyrics):
    num_of_lyrics = len(lyrics)
    artists = [artist] * num_of_lyrics
    titles = [title] * num_of_lyrics
    albums = [album] * num_of_lyrics
    dates = [date] * num_of_lyrics
    positions = [*range(1, num_of_lyrics+1)]
    sentiments = [0] * num_of_lyrics 
    data_list = list(zip(artists, albums, titles, dates, lyrics, positions, sentiments))
    new_data = pd.DataFrame(data_list, columns=COLUMNS)
    return df.append(new_data)