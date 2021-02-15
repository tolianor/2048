import random
import copy


def pretty_print(mass):
    print("-" * 10)
    for row in mass:
        print(*row)
    print("-" * 10)


def empty_list(mass):
    empty = []
    for i in range(4):
        for j in range(4):
            if mass[i][j] == 0:
                num = get_number_from_index(i, j)
                empty.append(num)
    return empty


def get_number_from_index(i, j):
    return i * 4 + j + 1


def get_index_from_number(num):
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def insert_2_or_4(mass, x, y):
    if random.random() <= 0.8:
        mass[x][y] = 2
    else:
        mass[x][y] = 4
    return mass


def is_zero_in_mas(mass):
    for row in mass:
        if 0 in row:
            return True
    return False


def move_left(mass):
    origins = copy.deepcopy(mass)
    delta = 0
    for row in mass:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mass[i][j] == mass[i][j + 1] and mass[i][j] != 0:
                mass[i][j] *= 2
                delta += mass[i][j]
                mass[i].pop(j + 1)
                mass[i].append(0)
    return mass, delta, not origins == mass, origins


def move_right(mass):
    origins = copy.deepcopy(mass)
    delta = 0
    for row in mass:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mass[i][j] == mass[i][j - 1] and mass[i][j] != 0:
                mass[i][j] *= 2
                delta += mass[i][j]
                mass[i].pop(j - 1)
                mass[i].insert(0, 0)
    return mass, delta, not origins == mass, origins


def move_up(mass):
    origins = copy.deepcopy(mass)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if mass[i][j] != 0:
                column.append(mass[i][j])
        while len(column) != 4:
            column.append(0)
        for i in range(3):
            if column[i] == column[i + 1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i + 1)
                column.append(0)
        for i in range(4):
            mass[i][j] = column[i]
    return mass, delta, not origins == mass, origins


def move_down(mass):
    origins = copy.deepcopy(mass)
    delta = 0
    for j in range(4):
        column = []
        for i in range(4):
            if mass[i][j] != 0:
                column.append(mass[i][j])
        while len(column) != 4:
            column.insert(0, 0)
        for i in range(3, 0, -1):
            if column[i] == column[i - 1] and column[i] != 0:
                column[i] *= 2
                delta += column[i]
                column.pop(i - 1)
                column.insert(0, 0)
        for i in range(4):
            mass[i][j] = column[i]
    return mass, delta, not origins == mass, origins


def can_move(mass):
    for i in range(3):
        for j in range(3):
            if mass[i][j] == mass[i][j + 1] or mass[i][j] == mass[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mass[i][j] == mass[i][j - 1] or mass[i][j] == mass[i - 1][j]:
                return True
    return False
