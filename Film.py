import json
from typing import Dict, List


def checking_input(txt: str, min_num: int = 1960, max_num: int = 2060) -> int:
    """
    Checking all choices in program. Returns result of user choice like digit
    """
    while True:
        num = input(txt)
        if num.isdigit():
            if min_num <= int(num) <= max_num:
                break
            else:
                print('\n- Неправильный ввод! -\n')
                continue
        else:
            print('\n- Необходимо ввести цифрами! -\n')
            continue
    return int(num)


def choice_genre(dict_genres: Dict[int, str]) -> str:
    """Returns the name of the genre"""
    print()
    for key, value in dict_genres.items():
        print(f'{key} - {value}')
    num_of_genre = checking_input('\nВыберите жанр >>> ', 1, 20)
    print(f'\nВыбранный жанр -> {dict_genres[num_of_genre]}')
    return dict_genres[num_of_genre]


def get_content(genre_: str, in_file: str = 'Непросмотренные.json') -> Dict[str, List]:
    """Gets content from json file or make new json file"""
    try:
        with open(in_file, 'r', encoding='utf-8-sig') as jsonfile:
            filling = json.load(jsonfile)
    except FileNotFoundError:
        with open(in_file, 'w', encoding='utf-8-sig') as jsonfile:
            filling = {genre_: []}
            json.dump(filling, jsonfile, indent=4, ensure_ascii=False)
    return filling


def checks_new_film(film_name: str, film_year: int,
                    content_: Dict[str, List]) -> bool:
    """Checks if the new film is in the json file"""
    flag = False
    try:
        for line in content_[genre]:
            if film_name == line['name'] and film_year == line['year']:
                print('\n- Есть такой фильм! -\n')
                flag = True
                available_film = [value for key, value in line.items()]
                print(genre, end=' : ')
                print(*available_film, sep=' | ', end='\n\n')
                break
    except KeyError:
        print('\nВозникла ошибка\n')
    return flag


def add_film(genre_: str, content_: Dict[str, List],
             file_: str = 'Непросмотренные.json') -> None:
    """Adds new film in json file (rewriting json file)"""
    while True:
        input_name = input('Введите название фильма >>> ')
        film_name = input_name.strip()
        film_year = checking_input('Введите год фильма >>> ')
        if checks_new_film(film_name, film_year, content_):
            break
        add_comment = checking_input('Добавить комментарий?: 1 - ДА ; 2 - НЕТ >>> ', 1, 2)
        if add_comment:
            film_comment = input('Напишите комментарий >>> ')
        else:
            film_comment = '-----'
        new_film = dict(name=film_name, year=film_year, comment=film_comment)
        content_[genre_].append(new_film)
        try:
            with open(file_, 'w', encoding='utf-8-sig') as out_file:
                json.dump(content_, out_file, indent=4, ensure_ascii=False)
            print('\n- ФИЛЬМ УДАЧНО ДОБАВЛЕН! -\n')
        except FileNotFoundError:
            print('\n- Произошла ошибка! -\n')
        break


def show_films(content_: Dict[str, List], genre_: str) -> None:
    """Show all films in chosen genre"""
    films_list = content_[genre_]
    print(separator)
    print(f'Фильмов в жанре "{genre_}" найдено {len(films_list)} :')
    print(separator)
    for n, kino in enumerate(films_list, 1):
        print(f'{n})', end=' ')
        show_list = ([f'{values}   |   ' for keys, values in kino.items()])
        print(*show_list)
    print(separator)


def delete_film(genre_: str, content_: Dict[str, List],
                file_: str = 'Непросмотренные.json') -> None:
    """Delete film from content and rewriting json file"""
    input_name = input('Введите название фильма >>> ')
    film_name = input_name.strip()
    film_year = checking_input('Введите год фильма >>> ')
    new_content = {genre_: []}
    try:
        for line in content_[genre_]:
            old_name = line['name'].strip()
            if film_name == old_name and film_year == line['year']:
                print('\n...Фильм найден...')
            else:
                new_content[genre_].append(line)
        if len(content_[genre_]) > len(new_content[genre_]):
            try:
                with open(file_, 'w', encoding='utf-8-sig') as out_file:
                    json.dump(new_content, out_file, indent=4, ensure_ascii=False)
                print('\n- ФИЛЬМ УДАЧНО УДАЛЁН! -\n')
            except FileNotFoundError:
                print('\n- Не удалось открыть файл для удаления! -\n')
        else:
            print('\n- Фильм НЕ НАЙДЕН! -\n')
    except KeyError:
        print('\n- Фильм НЕ НАЙДЕН! -\n')


def repeat_or_exit() -> bool:
    """Choose repeat or go to main menu"""
    exit_choice = ['Повторить действие', 'Выйти в главное меню']
    for i, value in enumerate(exit_choice, 1):
        print(f'{i} - {value}')
    answer = checking_input('\nВыберите действие >>> ', 1, 2)
    return answer == 1


def show_all(content_: Dict[str, List]) -> None:
    """This func just for file 'Непросмотренные'"""
    print(separator)
    for genre_, films in content_.items():
        first = genre_
        for film in films:
            print(first, end='  |  ')
            for key, value in film.items():
                print(value, end='   |   ')
            print()
    print(separator)


genres_dict = {
    1: "Боевики", 2: "Комедии", 3: "Фантастика", 4: "Ужасы", 5: "Мультфильмы",
    6: "Катастрофы", 7: "Супергерои", 8: "Фэнтези", 9: "Приключения",
    10: "Псевдодокументальные", 11: "Детективы", 12: "Про инопланетян",
    13: "Про демонов", 14: "Вампиры", 15: "Зомби", 16: "Космос",
    17: "Постапокалипсис", 18: "Сказки", 19: "Рождество", 20: "Достойные",
}
separator = ('\n' + ('*' * 50) + '\n')

print('\n Добро пожаловать! \n')
while True:
    with open('Main menu.txt', 'r', encoding='utf-8-sig') as file:
        menu = file.readlines()
        print(*menu)

    menu_choice = checking_input('\nВыберите действие >>> ', 1, 7)

    if menu_choice == 1:  # Show films from 'Непросмотренные'
        while True:
            choice_list = ['1 - Показать все фильмы', '2 - Выбрать по жанру\n']
            print(*(f'\n{s}' for s in choice_list))
            all_or_part = checking_input('Сделайте выбор >>> ', 1, 2)
            if all_or_part == 1:
                try:
                    with open('Непросмотренные.json', 'r', encoding='utf-8-sig') as file:
                        all_content = json.load(file)
                        show_all(all_content)
                except FileNotFoundError:
                    print('\n- Фильмов не найдено -\n')
            elif all_or_part == 2:
                genre = choice_genre(genres_dict)
                content = get_content(genre)
                try:
                    show_films(content, genre)
                except KeyError:
                    print('\n- Фильмов не найдено -\n')
                else:
                    print('\n- Фильмов не найдено -\n')
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 2:  # Show films from your catalog
        while True:
            genre = choice_genre(genres_dict)
            file = f'{genre}.json'
            content = get_content(genre, file)
            show_films(content, genre)
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 3:  # Add film to 'Непросмотренные'
        while True:
            genre = choice_genre(genres_dict)
            content = get_content(genre)
            add_film(genre, content)
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 4:  # Add film in catalog
        while True:
            genre = choice_genre(genres_dict)
            file = f'{genre}.json'
            content = get_content(genre, file)
            add_film(genre, content, file)
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 5:  # Delete film from 'Непросмотренные'
        while True:
            genre = choice_genre(genres_dict)
            content = get_content(genre)
            delete_film(genre, content)
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 6:  # Delete film from your catalogues
        while True:
            genre = choice_genre(genres_dict)
            file = f'{genre}.json'
            content = get_content(genre, file)
            delete_film(genre, content, file)
            if repeat_or_exit():
                continue
            else:
                print()
                break

    elif menu_choice == 7:  # close program
        break
