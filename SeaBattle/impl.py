from random import randint, choice

EMPTY = 0  # Пустая ячейка
SHIP = 1  # Ячейка с кораблём
MISS = 5  # Удар мимо
HIT = 6  # Попадание в корабль
NEAR = 7  # Окресность корабля


def init_fields(fields_number, side):
    """Создаёт два игровых поля и заполняет все ячейки нулями.

    :param fields_number: Количество игровых полей
    :param side: Размер стороны в игровом поле
    :return: Список игровых полей
    """
    fields = []
    for k in range(fields_number):
        fields.append([])
        for i in range(side):
            fields[k].append([])
            for j in range(side):
                fields[k][i].append(0)
    return fields


def get_cell_symbol(value):
    """Возвращает значение, которое будет отображаться на игровом поле

    :param value: Значение из ячейки игрового поля
    :return: Значение, которое будет принимать ячейка игрового поля
    """
    return chr(183) if type(value) == int else value  # Режим невидимки
    # return chr(183) if value == 0 else value  # Режим "Глаз Бога"


def draw_fields(fields):
    """Рисует в консоли игровые поля

    :param fields: Список игровых полей
    :return: Ничего не возвращает
    """
    SPACE_FIELDS = 7  # Зазор между игровыми полями по горизонтали
    CHARACTERS_IN_CELLS = 3  # Количество символов, которое занимает ячейка поля
    N = len(fields[0])
    print()

    for p in range(1, len(fields) + 1):
        player = f'player {p}'
        print(f'{player:^{CHARACTERS_IN_CELLS * (N + 1)}}', end='')
        print(end=' ' * SPACE_FIELDS if p <= len(fields) - 1 else '\n')

    for k in range(len(fields)):
        print(' ' * CHARACTERS_IN_CELLS, end='')
        for j in range(N):
            print(f'{j + 1:^{CHARACTERS_IN_CELLS}}', end='')
        print(end=' ' * SPACE_FIELDS if k < len(fields) - 1 else '')
    print()

    for i in range(N):
        for k in range(len(fields)):
            vert, _ = coord_atou(i, 0)
            print(f'{vert:^{CHARACTERS_IN_CELLS}}', end='')
            for j in range(N):
                print(f'{get_cell_symbol(fields[k][i][j]):^{CHARACTERS_IN_CELLS}}', end='')
            print(end=' '*SPACE_FIELDS if k < len(fields) - 1 else '')
        print()
    print()


def get_alphabet():
    """ Создаёт список букв русского алфавита в верхнем регистре, кроме букв Ё и Й

    :return: Список букв русского алфавита
    """
    alphabet = [chr(i) for i in range(ord('А'), ord('А') + 32)]
    alphabet.remove('Й')
    return alphabet


def coord_utoa(vert, horiz):
    """Преобразует координаты пользовательского вида в координаты массива

    :param vert: Координата по вертикали (буква русского алфавита в верхнем регистре: А, Б, В... )
    :param horiz: Координата по горизонтали (цифра: 1, 2, 3...)
    :return: Возвращает положение координаты в массиве в виде кортежа (2, 1)
    """
    tmp = {key: value for value, key in enumerate(get_alphabet())}
    i = tmp[vert]
    j = horiz - 1
    return i, j


def coord_atou(i, j):
    """Преобразует координаты массива в координаты пользовательского вида

    :param i: Координата по вертикали (цифра: 0, 1, 2...)
    :param j: Координата по горизонтали (цифра: 0, 1, 2...)
    :return: Возвращает положение координат пользовательского вида на игровом поле в виде кортежа ("Б", 5)
    """
    return get_alphabet()[i], j + 1


def is_on_field(field: list, i, j):
    """ Проверяет, находится ли клетка с координатами (i, j) в пределах игрового поля

    :return:
    """
    return True


def get_near_coords(i, j) -> list:
    """ Возвращает список кортежей координат ячеек в окресности заданной ячейки"""
    return [(i-1, j-1), (), (), (), (), (), (), ()]


def add_ship(field: list, ship_len: int, head_coord: tuple, is_horizontal: bool) -> bool:
    """Добавляет корабль на игровое поле, если функция выполнилась успешно.

    :param field: Игровое поле, на котором создаёт корабль
    :param ship_len: Количество клеток, которое занимает корабль
    :param head_coord: Начальная координата корабля
    :param is_horizontal: Горизонтальный или вертикальный корабль (True, False)
    :return: True или False (успех или неудача создания корабля)
    """
    i, j = coord_utoa(*head_coord)
    ship_stern = j + ship_len if is_horizontal else i + ship_len
    N = len(field)
    if ship_stern > N:
        # print('Неудача! Корабль вышел за пределы игрового поля.')
        return False
    else:
        ship_coord = {}
        for _ in range(ship_len):
            lst_contact_coord = []
            for n in range(i - 1, i + 2):
                for m in range(j - 1, j + 2):
                    if (n, m) != (i, j) and 0 <= n < N and 0 <= m < N:
                        lst_contact_coord.append((n, m))
            for n, m in lst_contact_coord:
                if field[n][m] != 0:
                    # print('Неудача! Корабли не могут соприкасаться.')
                    return False
            ship_coord[(i, j)] = ship_len
            if is_horizontal:
                j += 1
            else:
                i += 1
    for coord, ship_type in ship_coord.items():
        i, j = coord
        field[i][j] = ship_type
    return True


def fill_in_field(field: list, four_cells: int, three_cells: int, two_cells: int, one_cell: int):
    """ Заполняет игровое поле кораблями

    :param field: Игровое поле, которое будет заполнено кораблями
    :param four_cells: Количество кораблей из четырёх клеток
    :param three_cells: Количество кораблей из трёх клеток
    :param two_cells: Количество кораблей из двух клеток
    :param one_cell: Количество кораблей из одной клетки
    :return: True поле заполнено кораблями
    """
    ships = {4: four_cells,  3: three_cells, 2: two_cells, 1: one_cell}
    for ship_len, number_ships in ships.items():
        while number_ships:
            N = len(field)
            i_coord = randint(0, N - 1)
            j_coord = randint(0, N - 1)
            is_horizontal = bool(randint(0, 1))
            if add_ship(field, ship_len, coord_atou(i_coord, j_coord), is_horizontal):
                number_ships -= 1
    return True


def fill_in_fields(fields: list, four_cells: int, three_cells: int, two_cells: int, one_cell: int):
    """ Заполняет все игровые поля кораблями

    :param fields: Список игровых полей
    :param four_cells: Количество кораблей из четырёх клеток
    :param three_cells: Количество кораблей из трёх клеток
    :param two_cells: Количество кораблей из двух клеток
    :param one_cell: Количество кораблей из одной клетки
    :return:
    """
    N = len(fields)
    for i in range(N):
        fill_in_field(fields[i], four_cells, three_cells, two_cells, one_cell)


def shot(field: list, coord: tuple):
    """Проверяет выстрел на попадание и сохраняет результат выстрела в игровом поле

    :param field: Игровое поле по которому стреляют
    :param coord: Координата выстрела
    :return: True или False (Попадание или Промах)
    """
    i_coord, j_coord = coord_utoa(*coord)
    result_shot = field[i_coord][j_coord] in [1, 2, 3, 4, 'X']
    if field[i_coord][j_coord] == 'X':
        print('\nА говорят, что в одну воронку снаряд не попадает дважды!')
    field[i_coord][j_coord] = 'X' if result_shot else chr(664)
    return result_shot


def coordinate_processing(field: list, coord: tuple):
    """Проверка валидации координат введённые пользователем

    :param field: Игровое поле текущего игрока
    :param coord: Координаты введённые игроком
    :return: True или False (Валидные ли координаты)
    """
    if len(coord) == 2 and coord[0].isalpha() and coord[0] in get_alphabet()[:len(field)]:
        if coord[1].isdigit() and 1 <= int(coord[1]) <= len(field):
            return True
    else:
        return False


def presence_enemy(field: list):
    """ Проверка наличия врага на игровом поле

    :param field: Текущее игровое поле
    :return: True или False (наличие врага на поле)
    """
    count = 0
    for row in field:
        for item in row:
            if item in [1, 2, 3, 4]:
                count += 1
                break
    return bool(count)


def wounding_enemy(field: list, coord: tuple):
    """ Проверка ранения или уничтожения врага

    :param field: Текущее игровое поле
    :param coord: Координаты выстрела
    :return: True или False (ранен или убит)
    """
    i_coord, j_coord = coord_utoa(*coord)
    N = len(field)
    tmp = []
    for i in (i_coord - 1, i_coord + 1):
        if 0 <= i < N:
            tmp.append((i, j_coord))
    for j in (j_coord - 1, j_coord + 1):
        if 0 <= j < N:
            tmp.append((i_coord, j))
    for item in tmp:
        i, j = item
        if field[i][j] in [1, 2, 3, 4]:
            return True
    return False


def start_game(fields: list, players: int):
    """ Старт игры. Игроки поочерёдно вводят координаты выстрелов. Функция проверяет попадание в противника

    :param fields: Список игровых полей
    :param players: Количество игроков
    :return: Ничего не возвращает
    """
    while True:
        for p in range(players):
            while True:
                coord = tuple(input(f'player {p+1}\nВведите координаты выстрела. Например: А 2: ').split())
                if coord[0].lower() == 'стоп':
                    print('Игра остановлена.')
                    return False
                if coordinate_processing(fields[p], coord):
                    break
                print('\nВведите корректные координаты.\n')
            i_coord, j_coord = coord
            coord = (i_coord, int(j_coord))
            shot_player = shot(fields[p], coord)
            if shot_player:
                print('\n' + choice(['Попадание!', 'Враг в огне.', 'Меткий выстрел.']))

                # Проверка на ранение или уничтожение корабля
                print('Корабль подбит.' if wounding_enemy(fields[p], coord) else 'Корабль уничтожен')

                # Проверка, все ли корабли уничтожены
                if not presence_enemy(fields[p]):
                    draw_fields(fields)
                    print('Враг уничтожен! Игра окончена.')
                    return False

            else:
                print('\n' + choice(['Мимо.', 'Промах.', 'В следующий раз целься лучше.']))
            draw_fields(fields)
