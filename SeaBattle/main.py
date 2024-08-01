from impl import *

number_players = int(input('Введите количество игроков: '))
N = 10  # размер стороны игрового поля
fields = init_fields(number_players, N)

draw_fields(fields)

# Заполняем игровые поля кораблями
fill_in_fields(fields, 1, 2, 3, 4)
print('\nКорабли готовы к бою.')
print('cheat code - абракадабра')
print('Для продолжения игры введите координаты выстрела.\nДля завершения игры введите СТОП\n')

draw_fields(fields)

start_game(fields, number_players)
