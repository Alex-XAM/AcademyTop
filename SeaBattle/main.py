from impl import *

number_players = int(input('Введите количество игроков: '))
N = 10  # размер стороны игрового поля
fields = init_fields(number_players, N)

draw_fields(fields)

# Заполняем игровые поля кораблями
fill_in_fields(fields, 4, 3, 2, 1)
print('\nКорабли готовы к бою.')
print('Для продолжения игры введите координаты выстрела.\nДля завершения игры введите СТОП\n')

# draw_fields(fields)  # Для отрисовки кораблей в impl.py функцию get_cell_symbol(value) переключить в режим "Глаз Бога"

start_game(fields, number_players)
