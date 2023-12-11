import os
import pytest

from util import read_input

pipes = {
  '|': ((0, 1), (0, -1)),
  '-': ((1, 0), (-1, 0)),
  'L': ((1, 0), (0, -1)),
  'J': ((-1, 0), (0, -1)),
  '7': ((-1, 0), (0, 1)),
  'F': ((1, 0), (0, 1)),
  }


def get_pos(x, y, map):
  if x < 0 or y < 0:
    return None
  if x > len(map[0])-1 or y > len(map)-1:
    return None
  return map[y][x]


def set_pos(x, y, map, v):
  map[y][x] = v


def find_start(map):
  for col, line in enumerate(map):
    for row, symbol in enumerate(line):
      if symbol == 'S':
        return row, col


def test_find_start():
  map = read_input('input/test-10-1.txt')
  assert find_start(map) == (1, 1)
  map = read_input('input/test-10-2.txt')
  assert find_start(map) == (0, 2)


def find_connected_neighbors(x, y, map):
  connected = []
  max_x = len(map[0])-1
  max_y = len(map)-1

  # TODO: use pipes{} to look this up instead of if
  if x > 0 and get_pos(x-1, y, map) in ('-', 'L', 'F'):
    connected.append((x-1, y))

  if x < max_x and get_pos(x+1, y, map) in ('-', '7', 'J'):
    connected.append((x+1, y))

  if y > 0 and get_pos(x, y-1, map) in ('|', 'F', '7'):
    connected.append((x, y-1))

  if y < max_y and get_pos(x, y+1, map) in ('|', 'L', 'J'):
    connected.append((x, y+1))

  return connected


def find_next_tiles(x, y, map):
  connected_positions = []
  for delta in pipes[get_pos(x, y, map)]:
    connected_positions.append((x+delta[0], y+delta[1]))
  return connected_positions


def get_path(map):
  x, y = find_start(map)
  next_step, _ = find_connected_neighbors(x, y, map)

  path = [(x, y)]

  while next_step != path[0]:
    connected = find_next_tiles(next_step[0], next_step[1], map)

    for conn in connected:
      if conn == path[-1]:
        continue

      path.append(next_step)
      next_step = conn
      break
  return path


def solve_1(filename='input/test-10-1.txt'):
  map = read_input(filename)
  path = get_path(map)

  return int(len(path)/2)


paint_map = {
    'S': ('.*.', '***', '.*.'),
    '|': ('.*.', '.*.', '.*.'),
    '-': ('...', '***', '...'),
    'L': ('.*.', '.**', '...'),
    'J': ('.*.', '**.', '...'),
    '7': ('...', '**.', '.*.'),
    'F': ('...', '.**', '.*.'),
}


def zoom_and_enhance(map, path):
  new_map = [['.']*len(map)*3 for _ in range(len(map)*3)]

  for row_idx, row in enumerate(map):
    for col_idx, v in enumerate(row):
      new_row_idx = row_idx * 3
      new_col_idx = col_idx * 3

      if (col_idx, row_idx) not in path:
        v = '.'
      if v not in paint_map:
        continue
      for paint_row in range(3):
        symbols = paint_map[v][paint_row]
        for i, s in enumerate(symbols):
          new_map[new_row_idx+paint_row][new_col_idx+i] = s

  return new_map


def flood_fill(map):
  map[0][0] = 'O'
  to_visit = [(1, 0), (0, 1)]
  visited = set()

  marked = 1

  while to_visit:
    x, y = to_visit.pop(0)
    if (x, y) in visited:
      continue
    visited.add((x, y))
    v = get_pos(x, y, map)
    if v == '.':
      set_pos(x, y, map, 'O')
      marked += 1

    if (x-1, y) not in visited and get_pos(x-1, y, map) == '.':
      to_visit.append((x-1, y))
    if (x+1, y) not in visited and get_pos(x+1, y, map) == '.':
      to_visit.append((x+1, y))
    if (x, y-1) not in visited and get_pos(x, y-1, map) == '.':
      to_visit.append((x, y-1))
    if (x, y+1) not in visited and get_pos(x, y+1, map) == '.':
      to_visit.append((x, y+1))


def solve_2(filename='input/test-10-2.txt'):
  map = read_input(filename)
  path = get_path(map)

  new_map = zoom_and_enhance(map, path)

  flood_fill(new_map)

  resp = 0
  for x in range(1, len(new_map), 3):
    for y in range(1, len(new_map[0]), 3):
      if get_pos(x, y, new_map) == '.':
        resp += 1
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 4
    assert solve_1('input/test-10-2.txt') == 8
    assert solve_1('input/input-10.txt') == 6714
    assert solve_2() == 1
    assert solve_2('input/test-10-3.txt') == 4


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_2('input/input-10.txt') == 429


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/test-10-2.txt'))
  print(solve_1('input/input-10.txt'))
  print(solve_2())
  print(solve_2('input/test-10-3.txt'))
  print(solve_2('input/input-10.txt'))
