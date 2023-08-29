import json
import sqlite3


class DatabaseDAO:

    def __init__(self, path):
        self.path = path

    def get_title_from_bd(self, sql):
        """Принимает sql-запрос и распаковывает данные из таблицы"""
        with sqlite3.connect(self.path) as connect:
            connect.row_factory = sqlite3.Row
            result = connect.execute(sql).fetchall()

            return result

    def search_by_title(self, title):
        """Принимает title и возвращает title, country, listed_in, description"""
        for film in self.get_title_from_bd(sql=f"""
                SELECT title, country, listed_in, description
                FROM netflix
                WHERE title = '{title}'
                ORDER BY release_year DESC 
                LIMIT 1
                """):

            return dict(film)

    def search_by_date(self, year1, year2):
        """Принимает два года и возвращает картины, выпущенные в этом диапазоне"""
        response = self.get_title_from_bd(sql=f"""
                        SELECT title, release_year
                        FROM netflix
                        WHERE release_year BETWEEN {year1} AND {year2}
                        ORDER BY release_year
                        LIMIT 100
                        """)
        films_list = []
        for film in response:
            films_list.append(dict(film))

        return films_list

    def search_by_rating(self, rating):
        """Реализует поиск по рейтингу. Выводит картины, которые имеют рейтинг соответствующий запросу"""
        rating_dict = {
            "children": ["G"],
            "family": ["G", "PG", "PG-13"],
            "adult": ["R", "NC-17"]
        }

        if len(rating_dict[rating]) < 2:
            response = self.get_title_from_bd(sql=f"""
                                            SELECT title, rating, description
                                            FROM netflix
                                            WHERE rating = ('{rating_dict[rating][0]}')
                                            """)
        else:
            response = self.get_title_from_bd(sql=f"""
                                            SELECT title, rating, description
                                            FROM netflix
                                            WHERE rating IN {tuple(rating_dict[rating])}
                                            """)

        films_list = []
        for film in response:
            films_list.append(dict(film))

        return films_list

    def search_by_genre(self, listed_in):
        """Принимает название жанра и возвращает данные в формате: [{"название", "описание"}]"""
        response = self.get_title_from_bd(sql=f"""
                                        SELECT title, description
                                        FROM netflix n 
                                        WHERE listed_in LIKE '%{listed_in}%'
                                        ORDER BY release_year DESC
                                        LIMIT 10
                                        """)
        films_list = []
        for film in response:
            films_list.append(dict(film))

        return films_list

    def get_actors(self, actor1, actor2):
        """Получает в качестве аргумента имена двух актеров, сохраняет всех актеров из колонки cast и возвращает список
        тех, кто играет с ними в паре больше 2 раз"""
        response = self.get_title_from_bd(sql=f"""
                                        SELECT netflix.cast
                                        FROM netflix
                                        WHERE netflix.cast LIKE '%{actor1}%' 
                                        AND netflix.cast LIKE '%{actor2}%'
                                        """)
        actors_list = []
        collaborate_list = []
        for actor in response:
            names_lists = dict(actor).get("cast").split(", ")
            for name in names_lists:
                actors_list.append(name)
        names = set(actors_list) - {actor1, actor2}

        for name in names:
            collaborate_count = 0
            for actor in response:
                if name in dict(actor).get("cast").split(", "):
                    collaborate_count += 1
            if collaborate_count > 2:
                collaborate_list.append(name)

        return collaborate_list

    def get_title_by_options(self, type_film, release_year, genre):
        """Принимает тип картины (фильм или сериал), год выпуска и ее жанр и возвращает список названий картин
         с их описаниями в JSON"""
        response = self.get_title_from_bd(sql=f"""
                                        SELECT title, description 
                                        FROM netflix
                                        WHERE netflix.type = '{type_film}'
                                        AND release_year = '{release_year}'
                                        AND listed_in LIKE '%{genre}%'
                                        """)
        title_list = []
        for title in response:
            title_list.append(dict(title))

        return json.dumps(title_list, indent=4)
