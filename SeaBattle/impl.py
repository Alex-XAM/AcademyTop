from random import randint


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
    return chr(183) if value == 0 else value


def draw_fields(fields):
    """Рисует в консоли игровые поля

    :param fields: Список игровых полей
    :return: Ничего не возвращает
    """
    SPACE_FIELDS = 7  # Зазор между игровыми полями по горизонтали
    CHARACTERS_IN_CELLS = 3  # Количество символов, которое занимает ячейка поля
    N = len(fields[0])

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
        print('Неудача! Корабль вышел за пределы игрового поля.')
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
                    print('Неудача! Корабли не могут соприкасаться.')
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


def fill_in_field(field: list, one_cell: int, two_cells: int, three_cells: int, four_cells: int):
    """ Заполняет игровое поле кораблями

    :param field: Игровое поле, которое будет заполнено кораблями
    :param one_cell: Количество кораблей из одной клетки
    :param two_cells: Количество кораблей из двух клеток
    :param three_cells: Количество кораблей из трёх клеток
    :param four_cells: Количество кораблей из четырёх клеток
    :return:
    """
    ships = {1: one_cell, 2: two_cells, 3: three_cells, 4: four_cells}
    for ship_len, number_ships in ships.items():
        while number_ships:
            N = len(field)
            i_coord = randint(0, N - 1)
            j_coord = randint(0, N - 1)
            is_horizontal = bool(randint(0, 1))
            if add_ship(field, ship_len, coord_atou(i_coord, j_coord), is_horizontal):
                number_ships -= 1
    return True


def shot(field: list, coord: tuple):
    i_coord, j_coord = coord_utoa(*coord)
    return field[i_coord][j_coord] in [1, 2, 3, 4]
