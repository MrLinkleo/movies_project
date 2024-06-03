import json
from typing import Dict, Union, List



# отсортировать по рейтингу и по году
# поиск
def write_movies(movies: List[Dict[str, Union[str, int, float]]]) -> str:
    try:
        with open("movies.json", 'w', encoding='UTF-8') as fp:
            fp.write(json.dumps(movies, indent=4))
        return f"Данные обновлены."
    except Exception as e:
        return f"{e}"
    

def read_movies_from_file() -> List[Dict[str, Union[str, int, float]]]:
    try:
        with open("movies.json", "r", encoding="UTF-8") as fp:
            movies = json.load(fp)
            return movies
    except Exception as e:
        print(e)


def get_movie(name: str) -> Dict[str, Union[str, int, float]]:
    movies = read_movies_from_file()
    for movie in movies:
        if movie["name"].lower() == name:
            return movie


def get_average_rating(movie):
    return sum(movie["rating"]) / len(movie["rating"])


def add_movie() -> str:
    new_movie = {}
    name = input("Введите название фильма: ").lower().strip()
    movie = get_movie(name)
    if movie:
        print("Такой фильм уже есть.")
        return
    movies = read_movies_from_file()
    year = int(input("Введите год выхода: "))
    genre = input("Жанр фильма: ").strip()
    new_movie["name"] = name
    new_movie["year"] = year
    new_movie["genre"] = genre
    new_movie["rating"] = [5]
    movies.append(new_movie)
    write_movies(movies)
    print("Фильм добавлен.")
    

def delete_movie() -> str:
    name = input("Введите название фильма: ").lower().strip()
    movie = get_movie(name)
    if movie:
        movies = read_movies_from_file()
        movies.remove(movie)
        print("Фильм удален.")
    print("Такого фильма нет..")


def add_rating() -> str:
    name = input("Введите название фильма: ").lower().strip()
    movie = get_movie(name)
    if movie:
        print(f'Рейтинг фильма: {get_average_rating(movie)}')
        new_rating = int(input("Введите оценку от 0 до 10: "))
        movie["rating"].append(new_rating)
        print(f'Рейтинг фильма: {get_average_rating(movie)}')
    else:
        print(f"Такого фильма нет..")
        question = int(input("1-добавить фильм, 0-нет"))
        if not question:
            print("Меню")
        add_movie()


def get_movies_list() -> str:
    print(f"{''*36}Список фильмов{''*36}")
    #print("Название фильма", ""*10, "Год выпуска", ""10, "Жанр", ""*10, "Рейтинг")
    movies = read_movies_from_file()
    for movie in movies:
        if movie['rating']:
            average_rating = get_average_rating(movie)
        else:
            average_rating = f"Нет оценок"
        print(f"{movie.get('name', 'Нет данных')} {movie.get('year', 'Нет данных')} {movie.get('genre', 'Нет данных')} {average_rating}")
    print("*" * 86)


def search_movie():
    name = input("Введите название фильма: ").lower().strip()
    movie = get_movie(name)
    if not movie:
        print("Такого фильма нет")
        return
    print(movie.get('name', ''))
    print(movie.get('year', ''))
    print(get_average_rating(movie))
    print(movie.get('genre', ''))


def get_sorted_rating_movies():
    print(f"{'*'*36}Список фильмов{''*36}")
    #print("Название фильма", "*"*10, "Год выпуска", "*"10, "Жанр", "*"*10, "Рейтинг")
    movies = read_movies_from_file()
    sorted_movies = sorted(movies, key=get_average_rating, reverse=True)
    for movie in sorted_movies:
        if movie['rating']:
            average_rating = get_average_rating(movie)
        else:
            average_rating = f"Нет оценок"
        print(f"{movie.get('name', 'Нет данных')} {movie.get('year', 'Нет данных')} {movie.get('genre', 'Нет данных')} {average_rating}")
    print("*" * 86)


def get_genres():
    genres = []
    counter_index = 0
    text_menu = ''
    movies = read_movies_from_file()
    for movie in movies:
        genres.append(movie['genre'])
    genres = list(set(genres))
    for genre in genres:
        counter_index += 1
        text_menu += f'{counter_index}-{genre}\n'
    return genres, text_menu


def get_sorted_genre_movies():
    movies = read_movies_from_file()
    genres, text_menu = get_genres()
    print(genres)
    print(text_menu)
    genre_name = input(text_menu)
    if int(genre_name) > len(genres) or int(genre_name) < 1:
        print("Введите правильную команду")
        return
    for movie in movies:
        if genres[int(genre_name) - 1] == movie["genre"]:
                print(movie.get('name', ''))
                print(movie.get('year', ''))
                print(get_average_rating(movie))
                print(movie.get('genre', ''))

command_menu = {
    '1': add_movie,
    '2': delete_movie,
    '3': add_rating,
    '4': get_movies_list,
    '5': search_movie,
    '6': get_sorted_rating_movies,
    '7': get_sorted_genre_movies
}


menu_text = '''1-добавить
2-удалить
3-добавить рейтинг
4-список фильмов
5-поиск фильма
6-отсортировать по рейтингу
7-сортировка по жанру
0-выход
'''

def main() -> None:
    menu = input(menu_text).strip()
    while menu != '0':
        if menu not in command_menu:
            print(f"Нет такой команды")
        else:
            command_menu[menu]()
        menu = input(menu_text).strip()

try:
    main()
except ValueError:
    print("Вводите корректные данные")
    main()