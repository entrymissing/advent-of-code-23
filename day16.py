import os
from collections import defaultdict
import pytest

from util import read_input


offset = {
  'E': (1, 0),
  'W': (-1, 0),
  'N': (0, -1),
  'S': (0, 1),
}


def prep_moves_map():
  moves = {}
  for dir in ['N', 'E', 'S', 'W']:
    moves[dir+'.'] = (dir,)

  # Running into wrong side of splitter
  moves['N|'] = ('N',)
  moves['S|'] = ('S',)
  moves['W-'] = ('W',)
  moves['E-'] = ('E',)

  # Being reflected
  moves['E/'] = ('N',)
  moves['E\\'] = ('S',)
  moves['W/'] = ('S',)
  moves['W\\'] = ('N',)

  moves['S/'] = ('W',)
  moves['S\\'] = ('E',)
  moves['N/'] = ('E',)
  moves['N\\'] = ('W',)

  # Splitters
  moves['E|'] = ('N', 'S')
  moves['W|'] = ('N', 'S')
  moves['S-'] = ('E', 'W')
  moves['N-'] = ('E', 'W')

  return moves


def get_map(pos, map):
  return map[pos[1]][pos[0]]


def move(pos, direction, map):
  new_pos = (pos[0] + offset[direction][0], pos[1] + offset[direction][1])
  if new_pos[0] < 0 or new_pos[0] >= len(map[0]):
    return False, False

  if new_pos[1] < 0 or new_pos[1] >= len(map):
    return False, False

  return new_pos, get_map(new_pos, map)


def count_visited(start_pos, start_dir, map):
  moves = prep_moves_map()

  to_go = [(start_pos, start_dir)]
  visited = defaultdict(lambda: False)

  while to_go:
    cur_pos, cur_dir = to_go.pop(0)
    if visited[(cur_pos, cur_dir)]:
      continue
    visited[(cur_pos, cur_dir)] = True
    cur_pos, cur_tile = move(cur_pos, cur_dir, map)

    if cur_pos:
      new_dirs = moves[cur_dir + cur_tile]
      for nd in new_dirs:
        to_go.append((cur_pos, nd))

  visited_pos = {key[0]: True for key in visited.keys()}
  # We're enquing (-1,0) as starting point, so -1
  return len(visited_pos.keys()) - 1


def solve_1(filename='input/test-16.txt'):
  map = read_input(filename)
  return count_visited((-1, 0), 'E', map)


def solve_2(filename='input/test-16.txt'):
  map = read_input(filename)
  max_illuminated = 0
  for i in range(len(map)):
    max_illuminated = max(max_illuminated,
                          count_visited((-1, i), 'E', map))
    max_illuminated = max(max_illuminated,
                          count_visited((len(map), i), 'W', map))
    max_illuminated = max(max_illuminated,
                          count_visited((i, -1), 'S', map))
    max_illuminated = max(max_illuminated,
                          count_visited((i, len(map)), 'N', map))

  return max_illuminated


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 46
    assert solve_1('input/input-16.txt') == 7111
    assert solve_2() == 51


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_2('input/input-16.txt') == 7831


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-16.txt'))
  print(solve_2())
  print(solve_2('input/input-16.txt'))
