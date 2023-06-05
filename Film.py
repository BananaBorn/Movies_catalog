import json


# Checking all choices in program. Returns result of user choice like digit
def checking_input(txt, min_num=1960, max_num=2060):
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


# returns the name of the genre
def choice_genre(dict_genres):
    print()
    for key, value in dict_genres.items():
        print(f'{key} - {value}')
    num_of_genre = checking_input(
        '\nВыберите жанр >>> ', min_num=1, max_num=20)
    print(f'\nВыбранный жанр -> {dict_genres[num_of_genre]}')
    return dict_genres[num_of_genre]


# Gets content from json file or make new json file
def get_content(genre, in_file='Непросмотренные.json'):
    try:
        with open(in_file, 'r', encoding='utf-8-sig') as jsonfile:
            content = json.load(jsonfile)
    except:
        with open(in_file, 'w', encoding='utf-8-sig') as jsonfile:
            content = {genre: []}
            json.dump(content, jsonfile, indent=4, ensure_ascii=False)
    return content


# Checks if the new film is in the json file
def checks_new_film(film_name, film_year, content):
    flag = False
    try:
        for line in content[genre]:
            if film_name == line['name'] and film_year == line['year']:
                print('\n- Есть такой фильм! -\n')
                flag = True
                available_film = [value for key, value in line.items()]
                print(genre, end=' : ')
                print(*available_film, sep=' | ', end='\n\n')
                break
    except KeyError:
        content[genre] = []
    return flag


# Adds new film in json file (rewriting json file)
def add_film(genre, content, file='Непросмотренные.json'):
    while True:
        input_name = input('Введите название фильма >>> ')
        film_name = input_name.strip()
        film_year = checking_input('Введите год фильма >>> ')
        if checks_new_film(film_name, film_year, content):
            break
        add_comment = checking_input(
            'Добавить комментарий?: 1 - ДА ; 2 - НЕТ >>> ',
            min_num=1, max_num=2)
        if add_comment == 1:
            film_comment = input('Напишите комментарий >>> ')
        elif add_comment == 2:
            film_comment = '-----'
        new_film = dict(name=film_name, year=film_year,
                        comment=film_comment)
        content[genre].append(new_film)
        try:
            with open(file, 'w', encoding='utf-8-sig') as out_file:
                json.dump(content, out_file, indent=4,
                          ensure_ascii=False)
            print('\n- ФИЛЬМ УДАЧНО ДОБАВЛЕН! -\n')
        except:
            print('\n- Произошла ошибка! -\n')
        break


# Show all films in chosen genre
def show_films(content, genre):
    films_list = content[genre]
    print(separator)
    print(f'Фильмов в жанре "{genre}" найдено {len(films_list)} :')
    print(separator)
    for n, kino in enumerate(films_list, 1):
        print(f'{n})', end=' ')
        show_list = ([f'{values}   |   ' for keys,
        values in kino.items()])
        print(*show_list)
    print(separator)


# Delete film from content and rewriting json file
def delete_film(genre, content, file='Непросмотренные.json'):
    input_name = input('Введите название фильма >>> ')
    film_name = input_name.strip()
    film_year = checking_input('Введите год фильма >>> ')
    new_content = {genre: []}
    try:
        for line in content[genre]:
            old_name = line['name'].strip()
            if film_name == old_name and film_year == line['year']:
                print('\n...Фильм найден...')
            else:
                new_content[genre].append(line)
        if len(content[genre]) > len(new_content[genre]):
            try:
                with open(file, 'w', encoding='utf-8-sig') as out_file:
                    json.dump(new_content, out_file, indent=4,
                              ensure_ascii=False)
                print('\n- ФИЛЬМ УДАЧНО УДАЛЁН! -\n')
            except:
                print('\n- Не удалось открыть файл для удаления! -\n')
        else:
            print('\n- Фильм НЕ НАЙДЕН! -\n')
    except:
        print('\n- Фильм НЕ НАЙДЕН! -\n')


# Func for choose repeat or go to main menu
def repeat_or_exit():
    exit_choice = ['Повторить действие', 'Выйти в главное меню']
    for i, value in enumerate(exit_choice, 1):
        print(f'{i} - {value}')
    answer = checking_input('\nВыберите действие >>> ',
                            min_num=1, max_num=2)
    if answer == 1:  # repeat
        return True
    elif answer == 2:  # main menu
        return False


# This func just for file 'Непросмотренные'
def show_all(content):
    print(separator)
    for genre, films in content.items():
        first = genre
        for film in films:
            print(first, end='  |  ')
            for key, value in film.items():
                print(value, end='   |   ')
            print()
    print(separator)


genres_dict = {
    1: "Боевики", 2: "Комедии", 3: "Фантастика",
    4: "Ужасы", 5: "Мультфильмы", 6: "Катастрофы",
    7: "Супергерои", 8: "Фэнтези", 9: "Приключения",
    10: "Псевдодокументальные", 11: "Детективы",
    12: "Про инопланетян", 13: "Про демонов", 14: "Вампиры",
    15: "Зомби", 16: "Космос", 17: "Постапокалипсис",
    18: "Сказки", 19: "Рождество", 20: "Достойные",
}
separator = ('\n' + ('*' * 50) + '\n')

print('\n Добро пожаловать! \n')
while True:
    with open('Main menu.txt', 'r', encoding='utf-8-sig') as file:
        menu = file.readlines()
        print(*menu)

    menu_choice = checking_input('\nВыберите действие >>> ',
                                 min_num=1, max_num=7)

    if menu_choice == 1:  # Show films from 'Непросмотренные'
        while True:
            choice_list = ['1 - Показать все фильмы',
                           '2 - Выбрать по жанру\n']
            print(*[f'\n{s}' for s in choice_list])
            all_or_part = checking_input('Сделайте выбор >>> ',
                                         min_num=1, max_num=2)
            if all_or_part == 1:
                file = 'Непросмотренные.json'
                try:
                    with open(file, 'r', encoding='utf-8-sig') as file:
                        all_content = json.load(file)
                        show_all(all_content)
                except:
                    print('\n- Фильмов не найдено -\n')
            elif all_or_part == 2:
                genre = choice_genre(genres_dict)
                content = get_content(genre)
                try:
                    show_films(content, genre)
                except:
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

    elif menu_choice == 3:  # Add film in 'Непросмотренные'
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
