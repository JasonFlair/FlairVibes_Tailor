#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)

if __name__ == '__main__':
    """gets the song details from user and works using the details"""
    song_name, artist = input("Enter song name and title")
