import os

from util import read_input


def find_empty(map):
  empty_rows = []
  empty_columns = []

  for idx, row in enumerate(map):
    if all([r == '.' for r in row]):
      empty_rows.append(idx)

  for idx in range(len(map[0])):
    all_empty = True
    for row in map:
      if row[idx] != '.':
        all_empty = False
        break
    if all_empty:
      empty_columns.append(idx)

  return empty_rows, empty_columns


def find_galaxies(map):
  galaxies = []
  for row_idx, row in enumerate(map):
    for col_idx, v in enumerate(row):
      if v == '#':
        galaxies.append((col_idx, row_idx))
  return galaxies


def galaxy_distance(g1, g2, empty_x, empty_y, scaling_factor=1):
  from_x = min(g1[0], g2[0])
  to_x = max(g1[0], g2[0])
  from_y = min(g1[1], g2[1])
  to_y = max(g1[1], g2[1])

  x_steps = 0
  for ex in empty_x:
    if ex > from_x and ex < to_x:
      x_steps += scaling_factor
    if ex > to_x:
      break

  y_steps = 0
  for ey in empty_y:
    if ey > from_y and ey < to_y:
      y_steps += scaling_factor
    if ey > to_y:
      break

  return (to_x - from_x + x_steps) + (to_y - from_y + y_steps)


def solve_1(filename='input/test-11.txt'):
  map = read_input(filename)
  empty_y, empty_x = find_empty(map)
  galaxies = find_galaxies(map)

  resp = 0
  for gi1 in range(len(galaxies)):
    for gi2 in range(gi1+1, len(galaxies)):
      resp += galaxy_distance(galaxies[gi1], galaxies[gi2], empty_x, empty_y)
  return resp


def solve_2(filename='input/test-11.txt'):
  map = read_input(filename)
  empty_y, empty_x = find_empty(map)
  galaxies = find_galaxies(map)

  resp = 0
  for gi1 in range(len(galaxies)):
    for gi2 in range(gi1+1, len(galaxies)):
      resp += galaxy_distance(galaxies[gi1], galaxies[gi2], empty_x, empty_y, 999999)
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 374
    assert solve_1('input/input-11.txt') == 9684228
    assert solve_2() == 82000210
    assert solve_2('input/input-11.txt') == 483844716556


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-11.txt'))
  print(solve_2())
  print(solve_2('input/input-11.txt'))
