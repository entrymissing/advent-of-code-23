import os

from util import read_input


def parse_input(lines):
  maps = []

  new_map = []
  for line in lines:
    if line:
      new_map.append(line)
    else:
      maps.append(new_map.copy())
      new_map = []
  maps.append(new_map.copy())
  return maps


def print_map(map):
  for row in map:
    print(row)


def find_row_reflection(map):
  for reflection_idx in range(len(map)-1):
    is_reflection = True

    for offset in range(len(map)):
      top_row_idx = reflection_idx - offset
      bott_row_idx = reflection_idx + 1 + offset

      if top_row_idx < 0 or bott_row_idx >= len(map):
        break

      if map[top_row_idx] != map[bott_row_idx]:
        is_reflection = False
        break

    if is_reflection:
      return reflection_idx

  return -1


def diff_between_string(str1, str2):
  diff_count = 0
  for a, b in zip(str1, str2):
    if a != b:
      diff_count += 1
  return diff_count


def find_single_diff_reflection(map):
  for reflection_idx in range(len(map)-1):
    diff_count = 0

    for offset in range(len(map)):
      top_row_idx = reflection_idx - offset
      bott_row_idx = reflection_idx + 1 + offset

      if top_row_idx < 0 or bott_row_idx >= len(map):
        break

      diff_count += diff_between_string(map[top_row_idx], map[bott_row_idx])
      if diff_count > 1:
        break

    if diff_count == 1:
      return reflection_idx

  return -1


def solve_1(filename='input/test-13.txt'):
  lines = read_input(filename)
  maps = parse_input(lines)

  resp = 0
  for cur_map in maps:
    reflection = find_row_reflection(cur_map)
    if reflection >= 0:
      resp += (reflection + 1) * 100

    cur_map = [''.join(list(i)) for i in zip(*cur_map)]

    reflection = find_row_reflection(cur_map)
    if reflection >= 0:
      resp += reflection + 1
  return resp


def solve_2(filename='input/test-13.txt'):
  lines = read_input(filename)
  maps = parse_input(lines)

  resp = 0
  for cur_map in maps:
    reflection = find_single_diff_reflection(cur_map)
    if reflection >= 0:
      resp += (reflection + 1) * 100

    cur_map = [''.join(list(i)) for i in zip(*cur_map)]

    reflection = find_single_diff_reflection(cur_map)
    if reflection >= 0:
      resp += reflection + 1
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 405
    assert solve_1('input/input-13.txt') == 35521
    assert solve_2() == 400
    assert solve_2('input/input-13.txt') == 34795


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-13.txt'))
  print(solve_2())
  print(solve_2('input/input-13.txt'))
