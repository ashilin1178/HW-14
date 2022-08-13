import json
import sqlite3


def get_search_by_title(db_file, name_film):
    """
    поиск по названию в БД
    :param db_file:
    :param name_film:
    :return:
    """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        sql_qwery = f"""
                    SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE netflix.title = "{name_film}"
                    ORDER BY "release_year" DESC
                    LIMIT 1
                    """
        cursor.execute(sql_qwery)
        ex_qwery = cursor.fetchone()
        result = {
            "title": ex_qwery[0],
            "country": ex_qwery[1],
            "release_year": ex_qwery[2],
            "genre": ex_qwery[3],
            "description": ex_qwery[4]
        }
    return json.dumps(result, ensure_ascii=False, indent=4)


def get_search_between_years(db_file, from_year, before_year):
    """
    Возвращает фильмы в диапазоне указанных лет, включительно
    :param db_file:
    :param from_year:
    :param before_year:
    :return:
    """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        sql_qwery = f"""
                    SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {from_year} AND {before_year}
                    ORDER BY "release_year" ASC
                    LIMIT 100
                    """
        cursor.execute(sql_qwery)
        ex_qweryes = cursor.fetchall()
        result = []
        for ex_qwery in ex_qweryes:
            result.append({
                "title": ex_qwery[0],
                "release_year": ex_qwery[1],
            })

        return json.dumps(result, ensure_ascii=False, indent=4)


def get_search_by_rating(db_file, rating_group):
    """
    возвращает фильмы по возрастным группам
    :param db_file:
    :param rating_group:
    :return:
    """

    rating_family = ('G', 'PG', 'PG-13')
    rating_adult = ('R', 'NC-17')

    rating_ = ()

    if rating_group == 'children':
        sql_qwery = f"""
                            SELECT title, rating, description
                            FROM netflix
                            WHERE rating == 'G'
                            ORDER BY "release_year" DESC
                            LIMIT 100
                            """
    else:
        if rating_group == 'family':
            rating_ = rating_family
        elif rating_group == 'adult':
            rating_ = rating_adult

        sql_qwery = f"""
                        SELECT title, rating, description
                        FROM netflix
                        WHERE rating in {rating_}
                        ORDER BY "release_year" DESC
                        LIMIT 100
                        """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()

        cursor.execute(sql_qwery)
        ex_qweryes = cursor.fetchall()
        result = []
        for ex_qwery in ex_qweryes:
            result.append({
                "title": ex_qwery[0],
                "rating": ex_qwery[1],
                "description": ex_qwery[2]
            })

        return json.dumps(result, ensure_ascii=False, indent=4)


def get_fims_by_genre(db_file, genre):
    """
    возвращает 10 самых свежих фильмов в выбранном жанре
    :param db_file:
    :param genre:
    :return:
    """
    sql_qwery = f"""
                        SELECT title, description
                        FROM netflix
                        WHERE listed_in LIKE '%{genre}%'
                        ORDER BY "release_year" DESC 
                        LIMIT 10
                        """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute(sql_qwery)
        ex_qweryes = cursor.fetchall()
    result = []
    for ex_qwery in ex_qweryes:
        result.append({
            "title": ex_qwery[0],
            "description": ex_qwery[1]
        })

    return json.dumps(result, ensure_ascii=False, indent=4)


def get_actor_played_together(db_file, actor_one, actor_two):
    """
    возвращает список актеров, которые играли в более чем 2 фильмах совместно с actor_one и actor_two
    базу данных
    :param db_file: 
    :param actor_one: 
    :param actor_two: 
    :return: 
    """
    # формируем SQL запрос
    sql_qwery = f"""
                    SELECT netflix.cast
                    FROM netflix
                    WHERE title != ''
                    AND netflix.cast LIKE '%{actor_one}%'
                    AND netflix.cast LIKE '%{actor_two}%'
                """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute(sql_qwery)
        ex_qweryes = cursor.fetchall()
    result = []
    # преобразуем результат поиска в список
    for ex_qwery in ex_qweryes:
        result.append(
            ex_qwery[0]
        )
    # Создаем множество всех актеров, игравших в выбранных фильмах, исключаем из множества актеров из условий поиска
    actors = set()

    for item in result:
        actors.update(item.split(', '))

    actors.remove(actor_one)
    actors.remove(actor_two)
    # создаем словарь, где подсчитываем в скольких фильмах играл актер
    dict_result = dict()
    for item_actors in actors:
        number_film = 0
        for item_result in result:
            if item_actors in item_result:
                number_film += 1
        dict_result[item_actors] = number_film
    # создаем список с актерами, игравшими более 2 раз
    number_actor_played_together = []
    for k, v in dict_result.items():
        if v > 2:
            number_actor_played_together.append(k)

    return json.dumps(number_actor_played_together, ensure_ascii=False, indent=4)


def get_search_type_year_desc(db_file, type, release_year, genre):
    """
    возвращает список фильмов по типу, году, жанру
    :param db_file:
    :param type:
    :param release_year:
    :param genre:
    :return:
    """
    # формируем SQL запрос
    sql_qwery = f"""
                        SELECT type, listed_in, title, release_year, description
                        FROM netflix
                        WHERE title != ''
                        AND netflix.type LIKE '%{type}%'
                        AND release_year = {release_year}
                        AND listed_in LIKE '%{genre}%'
                        
                    """
    with sqlite3.connect(db_file) as connection:
        cursor = connection.cursor()
        cursor.execute(sql_qwery)
        ex_qweryes = cursor.fetchall()

    result = []

    # преобразуем результат поиска в список
    for ex_qwery in ex_qweryes:
        result.append(
            {'тип': ex_qwery[0],
             'жанр': ex_qwery[1],
             'название': ex_qwery[2],
             'год выхода': ex_qwery[3],
             'описание': ex_qwery[4]
             }
        )
    return json.dumps(result, ensure_ascii=False, indent=4)


print(get_search_type_year_desc('netflix.db', 'Movie', '2020', 'Sports'))
