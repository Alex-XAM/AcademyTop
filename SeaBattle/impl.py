from random import randint, choice

EMPTY = 0  # Пустая ячейка
SHIP = 1  # Ячейка с кораблём
MISS = 5  # Удар мимо
HIT = 6  # Попадание в корабль
NEAR = 7  # Окрестность корабля
cheat_code = False


def init_fields(fields_number, side) -> list:
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
    cell_display = None
    if value in (EMPTY, NEAR):
        cell_display = chr(183)
    elif value == SHIP and cheat_code:
        cell_display = '#'
    elif value == SHIP:
        cell_display = chr(183)
    elif value == MISS:
        cell_display = chr(664)
    elif value == HIT:
        cell_display = 'X'
    return cell_display


def draw_fields(fields):
    """Рисует в консоли игровые поля

    :param fields: Список игровых полей
    :return: Ничего не возвращает
    """
    SPACE_FIELDS = 7  # Зазор между игровыми полями по горизонтали
    CHARACTERS_IN_CELLS = 3  # Количество символов, которое занимает ячейка поля
    n = len(fields[0])
    print()

    for p in range(1, len(fields) + 1):
        player = f'player {p}'
        print(f'{player:^{CHARACTERS_IN_CELLS * (n + 1)}}', end='')
        print(end=' ' * SPACE_FIELDS if p <= len(fields) - 1 else '\n')

    for k in range(len(fields)):
        print(' ' * CHARACTERS_IN_CELLS, end='')
        for j in range(n):
            print(f'{j + 1:^{CHARACTERS_IN_CELLS}}', end='')
        print(end=' ' * SPACE_FIELDS if k < len(fields) - 1 else '')
    print()

    for i in range(n):
        for k in range(len(fields)):
            vert, _ = coord_atou(i, 0)
            print(f'{vert:^{CHARACTERS_IN_CELLS}}', end='')
            for j in range(n):
                print(f'{get_cell_symbol(fields[k][i][j]):^{CHARACTERS_IN_CELLS}}', end='')
            print(end=' '*SPACE_FIELDS if k < len(fields) - 1 else '')
        print()
    print()


def get_alphabet() -> list:
    """Создаёт список букв русского алфавита в верхнем регистре, кроме букв Ё и Й

    :return: Список букв русского алфавита
    """
    alphabet = [chr(i) for i in range(ord('А'), ord('А') + 32)]
    alphabet.remove('Й')
    return alphabet


def coord_utoa(vert, horiz) -> tuple:
    """Преобразует координаты пользовательского вида в координаты массива

    :param vert: Координата по вертикали (буква русского алфавита в верхнем регистре: А, Б, В... )
    :param horiz: Координата по горизонтали (цифра: 1, 2, 3...)
    :return: Возвращает положение координаты в массиве в виде кортежа (2, 1)
    """
    tmp = {key: value for value, key in enumerate(get_alphabet())}
    i = tmp[vert]
    j = horiz - 1
    return i, j


def coord_atou(i, j) -> tuple:
    """Преобразует координаты массива в координаты пользовательского вида

    :param i: Координата по вертикали (цифра: 0, 1, 2...)
    :param j: Координата по горизонтали (цифра: 0, 1, 2...)
    :return: Возвращает положение координат пользовательского вида на игровом поле в виде кортежа ("Б", 5)
    """
    return get_alphabet()[i], j + 1


def is_on_field(field: list, i, j) -> bool:
    """Проверяет, находится ли клетка с координатами (i, j) в пределах игрового поля

    :return: True, если клетка в поле
    """
    i, j = coord_utoa(i, j) if isinstance(i, str) else (i, j)
    return 0 <= i < len(field) and 0 <= j < len(field)


def get_near_coords(i, j) -> list:
    """Возвращает список кортежей координат ячеек в окрестности проверяемой ячейки"""
    return [(i-1, j-1), (i-1, j), (i-1, j+1), (i, j-1), (i, j+1), (i+1, j-1), (i+1, j), (i+1, j+1)]


def add_ship(field: list, ship_len: int, head_coord: tuple, is_horizontal: bool) -> bool:
    """Добавляет корабль на игровое поле, если функция выполнилась успешно.

    :param field: Игровое поле, на котором создаёт корабль
    :param ship_len: Количество клеток, которое занимает корабль
    :param head_coord: Начальная координата корабля
    :param is_horizontal: Горизонтальный или вертикальный корабль (True, False)
    :return: True или False (успех или неудача создания корабля)
    """
    i, j = coord_utoa(*head_coord)
    tmp_ship = []

    # Сохраняем координаты клеток корабля во временном списке tmp_ship, если они не выходят за пределы поля
    for k in range(ship_len):
        i_cell, j_cell = (i, j+k) if is_horizontal else (i+k, j)
        if is_on_field(field, i_cell, j_cell) and field[i_cell][j_cell] != SHIP and field[i_cell][j_cell] != NEAR:
            tmp_ship.append((i_cell, j_cell))
        else:
            return False

    # Добавление корабля в игровое поле
    for i, j in tmp_ship:
        field[i][j] = SHIP

    # Добавление окрестности вокруг корабля
    for i, j in tmp_ship:
        for n, m in get_near_coords(i, j):
            if is_on_field(field, n, m) and field[n][m] == EMPTY:
                field[n][m] = NEAR
    return True


def fill_in_field(field: list, four_cells: int, three_cells: int, two_cells: int, one_cell: int) -> bool:
    """Заполняет игровое поле кораблями

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
            n = len(field)
            i_coord = randint(0, n - 1)
            j_coord = randint(0, n - 1)
            is_horizontal = bool(randint(0, 1))
            if add_ship(field, ship_len, coord_atou(i_coord, j_coord), is_horizontal):
                number_ships -= 1
    return True


def fill_in_fields(fields: list, four_cells: int, three_cells: int, two_cells: int, one_cell: int):
    """Заполняет все игровые поля кораблями

    :param fields: Список игровых полей
    :param four_cells: Количество кораблей из четырёх клеток
    :param three_cells: Количество кораблей из трёх клеток
    :param two_cells: Количество кораблей из двух клеток
    :param one_cell: Количество кораблей из одной клетки
    :return:
    """
    n = len(fields)
    for i in range(n):
        fill_in_field(fields[i], four_cells, three_cells, two_cells, one_cell)


def shot(field: list, coord: tuple) -> bool:
    """Проверяет выстрел на попадание и сохраняет результат выстрела в игровом поле

    :param field: Игровое поле по которому стреляют
    :param coord: Координата выстрела
    :return: True или False (Попадание или Промах)
    """
    i_coord, j_coord = coord_utoa(*coord)
    result_shot = field[i_coord][j_coord] == SHIP
    if field[i_coord][j_coord] == HIT:
        print('\nА говорят, что в одну воронку снаряд не попадает дважды!')
    field[i_coord][j_coord] = HIT if result_shot or field[i_coord][j_coord] == HIT else MISS
    return result_shot


def checking_validity_of_coord(field: list, coord: str) -> bool:
    """Проверка валидности координат введённых пользователем

    :param field: Игровое поле текущего игрока
    :param coord: Координаты введённые игроком
    :return: True или False (Валидные ли координаты)
    """
    if coord[0].isalpha() and coord[0] in get_alphabet()[:len(field)]:
        if coord[1:].isdigit() and 1 <= int(coord[1:]) <= len(field):
            return True
    else:
        return False


def presence_enemy(field: list) -> bool:
    """Проверка наличия врага на игровом поле

    :param field: Текущее игровое поле
    :return: True или False (наличие врага на поле)
    """
    count = 0
    for row in field:
        for item in row:
            if item == SHIP:
                count += 1
                break
    return bool(count)


def wounding_enemy(field: list, coord: tuple) -> bool:
    """Проверка ранения или уничтожения врага

    :param field: Текущее игровое поле
    :param coord: Координаты выстрела
    :return: True или False (ранен или убит)
    """
    i, j = coord_utoa(*coord)
    n = len(field)
    tmp_coords = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
    for i_cell, j_cell in tmp_coords:
        if is_on_field(field, i_cell, j_cell) and field[i_cell][j_cell] == SHIP:
            return True
    return False


def input_coord(fields: list, player: int) -> str:
    """Принимает от игрока строку, проверяет на cheat_code, на СТОП игры и на соответствие координатам

    :param fields: Список игровых полей
    :param player: Номер игрока
    :return: Пустую строку или строку с координатами
    """
    global cheat_code
    while True:
        coord = input(f'player {player + 1}\nВведите координаты выстрела. Например: А2: ')
        if coord.lower() == 'абракадабра':
            cheat_code = True
            print('\nВключен режим "Глаз Бога"')
            draw_fields(fields)
            continue
        if coord.lower() == 'стоп':
            print('Игра остановлена.')
            return ''
        if checking_validity_of_coord(fields[player], coord):
            return coord
        print('\nВведите корректные координаты.\n')


def start_game(fields: list, players: int):
    """Старт игры. Игроки поочерёдно вводят координаты выстрелов. Функция проверяет попадание в противника

    :param fields: Список игровых полей
    :param players: Количество игроков
    :return: Ничего не возвращает
    """
    while True:
        for p in range(players):

            # Получение координат выстрела
            str_coord = input_coord(fields, p)
            if not str_coord:
                return False  # Игра остановлена
            coord = (str_coord[0], int(str_coord[1:]))

            # Получение результата выстрела
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
