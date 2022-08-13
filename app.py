from flask import Flask

from utils import get_search_by_title, get_search_between_years, get_search_by_rating, get_fims_by_genre

app = Flask(__name__)

db_file = "netflix.db"


@app.route('/movie/<title>')
def page_search_title(title):
    """
    Страница поиска по названию
    :param title:
    :return:
    """
    result = get_search_by_title(db_file, title)
    return result


@app.route('/movie/<int:year_from>/to/<int:year_to>')
def page_search_years(year_from, year_to):
    """
    на странице выводится список фильмов созданных в диапазоне введенных лет
    :param year_from:
    :param year_to:
    :return:
    """
    result = get_search_between_years(db_file, year_from, year_to)
    return result


@app.route('/rating/<rating>')
def page_for_rating(rating):
    """
    на странице выводится список с фильмами по возрастным группам
    :param rating:
    :return:
    """
    result = get_search_by_rating(db_file, rating)
    return result


@app.route('/genre/<genre>')
def page_for_genre(genre):
    result = get_fims_by_genre(db_file, genre)
    return result


if __name__ == '__main__':
    app.run()
