# This Python file uses the following encoding: utf-8
import os, sys
from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find(artist)
    if not albums_list:
        message = "Альбомов {0} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
        result = "Total {0}: ".format(len(albums_list))
        result += "Список альбомов {0}: ".format(artist)
        result += ", ".join(album_names)
    return result

@route("/create", method="POST")
def create():
    album_data = {
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album"),
        "year": request.forms.get("year")
    }
    resource_path = album.save_album(album_data)
    if resource_path is None:
        message = "Альбом уже есть в базе данных"
        result = HTTPError(409, message)
    else:
        result = "Альбом успешно сохранен"
    
    return result
    

if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)