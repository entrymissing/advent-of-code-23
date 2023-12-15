import os
import pytest

from collections import defaultdict

from util import read_input


def print_map(map):
  for row in map:
    print(''.join(row))


def rotate_map(map, n=1):
  for i in range(n):
    map = list(zip(*map[::-1]))
  return map


def fall_left(map):
  new_map = []
  for line in map:
    line = list(line)
    fall_to = 0
    for idx, val in enumerate(line):
      if val == 'O':
        if fall_to == idx:
          fall_to += 1
          continue
        line[fall_to] = 'O'
        line[idx] = '.'
        fall_to += 1
        continue
      if val == '#':
        fall_to = idx + 1
        continue
    new_map.append(line)
  return new_map


def count_weight(map):
  weight = 0
  for line in map:
    for idx, val in enumerate(line):
      if val == 'O':
        weight += (len(line)-idx)
  return weight


def solve_1(filename='input/test-14.txt'):
  map = read_input(filename)
  map = rotate_map(map, 3)

  map = fall_left(map)

  weight = count_weight(map)
  return weight


def fingerprint_map(map):
  return ''.join([x for xs in map for x in xs])


def solve_2(filename='input/test-14.txt'):
  map = read_input(filename)
  map = rotate_map(map, 3)

  repeats = defaultdict(list)

  for r in range(250):
    for i in range(4):
      map = fall_left(map)
      map = rotate_map(map, 1)
    weight = count_weight(map)
    fingerprint = fingerprint_map(map)
    repeats[(fingerprint, weight)].append((r+1))

  for key in repeats:
    if len(repeats[key]) < 2:
      continue
    r1 = repeats[key][0]
    r2 = repeats[key][1]
    cycle = r2 - r1
    if (1000000000 - r1) % cycle == 0:
      return key[1]
  return 0


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 136
    assert solve_1('input/input-14.txt') == 113486
    assert solve_2() == 64


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_2('input/input-14.txt') == 104409


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-14.txt'))

  print(solve_2())
  print(solve_2('input/input-14.txt'))
