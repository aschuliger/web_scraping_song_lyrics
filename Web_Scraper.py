import requests
from bs4 import BeautifulSoup
import String_Parser as strp

class Web_Scraper:

    URL_BASE = "https://www.azlyrics.com/"

    def __init__(self, artist, writers):
        self.artist = artist
        self.writers = [writer.lower() for writer in writers]
        self.artist_query = Web_Scraper.create_artist_query(artist)
        self.lyrics_query = Web_Scraper.create_lyrics_query(artist)
        self.current_page = None
        pass

    @staticmethod
    def create_artist_query(artist):
        artist_query = strp.convert_string_to_query(artist)
        return artist_query[0] + "/" + artist_query + ".html"

    @staticmethod
    def create_lyrics_query(artist):
        artist_query = strp.convert_string_to_query(artist)
        return "lyrics/" + artist_query + "/.html"

    def get_response(self, song=None):
        URL = None
        if song == None:
            URL = self.URL_BASE + self.artist_query
        else:
            song = strp.convert_string_to_query(song)
            print(song)
            index = self.lyrics_query.index(".html")
            song_query = self.lyrics_query[0:index] + song + ".html"
            URL = self.URL_BASE + song_query
        page = requests.get(URL)
        return BeautifulSoup(page.content, "html.parser")

    def get_songs(self):
        page_content = self.get_response()
        song_container = page_content.find(id="listAlbum")
        song_results = song_container.find_all("div", class_="listalbum-item")
        songs = list()
        for song in song_results:
            title = song.find_all("a")
            songs.append(title[0].text)
        return songs

    def get_lyrics(self, song):
        page_content = self.get_response(song)
        lyrics_container = page_content.find_all("div", class_="container main-page")[0]
        lyrics_response = lyrics_container.text
        self.current_page = lyrics_response
        
        if self.has_correct_writers():
            return self.extract_lyrics_from_html(lyrics_response, song)
        return -1

    def extract_lyrics_from_html(self, response, song):
        first_index = response.index("\"" + song + "\"\n") + len(song) + 2
        last_index = response.index("Submit Corrections")
        lyrics = response[first_index:last_index]

        first_index = strp.index_letter(lyrics)
        last_index = strp.rindex_letter(lyrics)+1
        return lyrics[first_index:last_index]

    def extract_album(self, song, album_content=None):
        if self.current_page == None:
            page_content = self.get_response(song)
            lyrics_container = page_content.find_all("div", class_="container main-page")[0]
            self.current_page = lyrics_container.text
        if album_content == None:
            album_content = self.get_album_content()
        
        if album_content != -1:
            first_quote = album_content.index("\"")
            album = album_content[first_quote+1:len(album_content)]
            return album[0:album.index("\"")]
        return "N/A"

    def extract_release_date(self, song):
        if self.current_page == None:
            self.current_page = self.get_response(song)
        album_content = self.get_album_content()
        
        if album_content != -1:
            album = self.extract_album(song, album_content=album_content)
            album_index = album_content.index(album)
            temp = album_content[album_index+len(album)+1:len(album_content)]
            return temp[temp.index("(")+1:temp.index(")")]
        return "N/A"

    def get_album_content(self):
        album_index = self.current_page.find('album:')
        if album_index > -1:
            return self.current_page[album_index:len(self.current_page)]
        return -1

    def has_correct_writers(self):
        page_content = self.current_page
        writer_index = page_content.find("Writer(s):")
        if writer_index > -1:
            temp = page_content[writer_index:len(page_content)]
            temp = temp[temp.index(" ")+1:temp.index("\n")]
            writers = temp.split(", ")
            for writer in writers:
                if writer.lower() in self.writers:
                    return True
        return False

    def remove_duplicate_songs(self):
        # Check for duplicate songs
        # Remove non-Taylor Swift Original Songs using the writers section on the lyrics tab
        pass