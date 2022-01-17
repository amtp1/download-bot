import sqlite3
import urllib.request
from pytube import YouTube

def get_video():
    yt = YouTube("https://www.youtube.com/watch?v=Vj4Y1c-DSM0")

    stream = yt.streams.get_by_itag(22)
    video = urllib.request.urlopen(stream.url).read()

def create_db():
    sql = sqlite3.connect("db.sqlite3")
    cursor = sql.cursor()

    cursor.execute("""
        CREATE TABLE users(id PRIMARY KEY,
            user_id INTEGER NOT NULL,
            username VARCHAR(255) NULL,
            first_name VARCHAR(255) NULL,
            last_name VARCHAR(255) NULL,
            joined DATETIME NOT NULL,
            download_count INTEGER NULL)
    """)

if __name__ == "__main__":
    create_db()