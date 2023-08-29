from flask import Blueprint, Flask
import json
from .dao.database_dao import DatabaseDAO
from config import Config

app = Flask(__name__)
directory = Config()
database_manager = DatabaseDAO(directory.DATABASE)
database_blueprint = Blueprint("database_blueprint", __name__)


@database_blueprint.get("/movie/<title>")
def search_title_page(title):
    """Выводит данные про фильм"""
    response = database_manager.search_by_title(title=title)

    return app.response_class(response=json.dumps(response),
                              status=200,
                              mimetype='application/json')


@database_blueprint.get("/movie/<year1>/to/<year2>")
def search_date_page(year1, year2):
    """Выводит список картин в заданном диапазоне"""
    response = database_manager.search_by_date(year1=year1, year2=year2)

    return app.response_class(response=json.dumps(response),
                              status=200,
                              mimetype='application/json')


@database_blueprint.get("/rating/<rating>")
def search_rating_page(rating):
    """Выводит информацию о названии, рейтинге и описании картин, соответствующих заданному рейтингу"""
    response = database_manager.search_by_rating(rating=rating)

    return app.response_class(response=json.dumps(response),
                              status=200,
                              mimetype='application/json')


@database_blueprint.get("/genre/<listed_in>")
def search_genre_page(listed_in):
    """Возвращает 10 самых свежих фильмов в формате json, соответствующих заданному жанру"""
    response = database_manager.search_by_genre(listed_in=listed_in)

    return app.response_class(response=json.dumps(response),
                              status=200,
                              mimetype='application/json')
