# This Python file uses the following encoding: utf-8
import os, sys
import json
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """

    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def valid_year(year):
  if year and year.isdigit():
    if int(year) >=1900 and int(year) <=2020:
      return True

def save_album(album_data):
    album = album_data["album"]
    artist = album_data["artist"]
    genre = album_data["genre"]
    year = album_data["year"]
            
    newAlbum = Album(
                    album = album,
                    artist = artist,
                    genre = genre,
                    year = year)

    session = connect_db()
    album = session.query(Album).filter(Album.album == album).all()
    if len(album) > 0 or not valid_year(year):
        return None
    else:
        session.add(newAlbum)   
    
    session.flush()
    return True

