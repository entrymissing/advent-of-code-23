from collections import defaultdict
import os

from util import read_input


def solve_1(filename='input/test-02.txt'):
  lines = read_input(filename)

  max_cubes = {'red': 12, 'green': 13, 'blue': 14}

  resp = 0

  for line in lines:
    game_id = int(line.split(':')[0][5:])
    draws = line.split(':')[1].split(';')

    game_possible = True
    for draw in draws:
      for cubes in draw.strip().split(','):
        count, color = cubes.split()
        if int(count) > max_cubes[color]:
          game_possible = False
    if game_possible:
      resp += game_id
  return resp


def solve_2(filename='input/test-02.txt'):
  lines = read_input(filename)

  resp = 0

  for line in lines:
    draws = line.split(':')[1].split(';')

    max_cubes = defaultdict(lambda: 0)

    for draw in draws:
      for cubes in draw.strip().split(','):
        count, color = cubes.split()
        max_cubes[color] = max(int(count), max_cubes[color])

    prod = 1
    for key in max_cubes:
      prod *= max_cubes[key]

    resp += prod
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 8
    assert solve_1('input/input-02.txt') == 2239
    assert solve_2() == 2286
    assert solve_2('input/input-02.txt') == 83435


if __name__ == '__main__':
  print(solve_1('input/input-02.txt'))
  print(solve_2('input/input-02.txt'))
