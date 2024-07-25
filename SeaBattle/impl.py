def init_fields(fields_number, side):
    fields = []
    for k in range(fields_number):
        fields.append([])
        for i in range(side):
            fields[k].append([])
            for j in range(side):
                fields[k][i].append(0)
    return fields


def get_cell_symbol(value):
    return '.' if value == 0 else value


def draw_fields(fields):
    SPACE_FIELDS = 7  # Зазор между игровыми полями по горизонтали
    SPACE_CELLS = 2   # Зазор между элементами
    N = len(fields[0])

    print((' ' + ' ' * SPACE_CELLS), end='')

    for k in range(len(fields)):
        for j in range(N):
            print(j + 1, end=' '*SPACE_CELLS if j < N - 1 else '')
        print(end=' ' * (SPACE_FIELDS + 2) if k < len(fields) - 1 else '')
    print()

    for i in range(N):
        for k in range(len(fields)):
            vert, _ = coord_atou(i, 0)
            print(vert, end='  ')
            for j in range(N):
                print(get_cell_symbol(fields[k][i][j]), end=' '*SPACE_CELLS if j < N - 1 else '')
            print(end=' '*SPACE_FIELDS if k < len(fields) - 1 else '')
        print()
    print()


def coord_utoa(vert, horiz):
    tmp = {'А': 0, 'Б': 1, 'В': 2, 'Г': 3, 'Д': 4, 'Е': 5, 'Ж': 6, 'З': 7, 'И': 8, 'К': 9}
    i = tmp[vert]
    j = horiz - 1
    return i, j


def coord_atou(i, j):
    return 'АБВГДЕЖЗИК'[i], j + 1


def add_ship(field: list, ship_len: int, head_coord: tuple, is_horizontal: bool) -> bool:
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
