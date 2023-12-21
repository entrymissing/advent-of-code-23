import functools
import os

from util import read_input, get_pos, set_pos, pos_plus_offset


offset = {
  'E': (1, 0),
  'N': (0, -1),
  'W': (-1, 0),
  'S': (0, 1),
}


def find_start(map):
  for y, row in enumerate(map):
    for x, v in enumerate(row):
      if v == 'S':
        return (x, y)


@functools.cache
def path_through_map(start, hashable_map, max_dist):
  map = [list(row) for row in hashable_map]
  to_visit = [(start, 0)]

  leaving_map = {}

  while to_visit:
    pos, dist = to_visit.pop(0)

    # If we're past the maximum number of steps we can stop
    if dist > max_dist:
      continue

    spot = get_pos(pos, map)

    if not spot:
      if pos[0] < 0 and 'W' not in leaving_map:
        leaving_map['W'] = (pos, dist)
      if pos[1] < 0 and 'N' not in leaving_map:
        leaving_map['N'] = (pos, dist)
      if pos[0] >= len(map[0]) and 'E' not in leaving_map:
        leaving_map['E'] = (pos, dist)
      if pos[1] >= len(map) and 'S' not in leaving_map:
        leaving_map['S'] = (pos, dist)
      continue

    if spot != '.':
      continue

    set_pos(pos, dist, map)
    for cur_dir in offset:
      new_pos = pos_plus_offset(pos, offset[cur_dir])
      to_visit.append((new_pos, dist + 1))

  count_even = 0
  count_odd = 0
  for y, row in enumerate(map):
    for x, value in enumerate(row):
      if isinstance(value, int):
        if value % 2 == 0:
          count_even += 1
        else:
          count_odd += 1

  return count_even, count_odd, leaving_map


def test_path_through_map():
  map = ('...', '...', '...')
  count_even, count_odd, leaving_map = path_through_map((1, 1), map, 1)
  # Technically incorrcect because after 1 step we can't actually reach the starting position
  # but it will be correct for every number of steps except 1
  assert count_even == 1
  assert count_odd == 4
  assert leaving_map == {}

  # Going way past the boundaries
  count_even, count_odd, leaving_map = path_through_map((1, 1), map, 5)
  assert count_even == 5
  assert count_odd == 4
  assert leaving_map['N'] == ((1, -1), 2)
  assert leaving_map['E'] == ((3, 1), 2)
  assert leaving_map['S'] == ((1, 3), 2)
  assert leaving_map['W'] == ((-1, 1), 2)


def solve_1(filename='input/test-21.txt', max_dist=6):
  map = read_input(filename)

  # Prep the map
  map = [list(row) for row in map]
  start = find_start(map)
  set_pos(start, '.', map)

  # Make it hashable
  map = (''.join(row) for row in map)

  count_even, _, _ = path_through_map(start, map, max_dist)
  return count_even


def test_map_symetry():
  if not os.path.exists('input'):
    return
  map = read_input('input/input-21.txt')

  # Prep the map
  map = [list(row) for row in map]
  start = find_start(map)
  set_pos(start, '.', map)

  # Make it hashable
  map = tuple([''.join(row) for row in map])

  count_even = {}
  count_odd = {}
  map_exits = {}
  count_even['Start'], count_odd['Start'], map_exits['Start'] = path_through_map(start, map, 1000)

  # Verify that south exit stays at the same x as start
  # print((map_exits['Start']['S'][0][0], 0))
  count_even['S'], count_odd['S'], map_exits['S'] = path_through_map((map_exits['Start']['S'][0][0], 0), map, 1000)
  count_even['N'], count_odd['N'], map_exits['N'] = path_through_map((map_exits['Start']['N'][0][0], len(map)-1),
                                                                     map, 1000)
  count_even['E'], count_odd['E'], map_exits['E'] = path_through_map((0, map_exits['Start']['E'][0][1]), map, 1000)
  count_even['W'], count_odd['W'], map_exits['W'] = path_through_map((len(map[0]) - 1, map_exits['Start']['W'][0][1]),
                                                                     map, 1000)

  for direction in offset:
    assert map_exits['Start'][direction][0][0] == map_exits[direction][direction][0][0]
    assert map_exits['S']['S'][1] == map_exits[direction][direction][1]


def solve_2_old(filename='input/input-21.txt', max_dist=6):
  map = read_input(filename)

  # Prep the map
  map = [list(row) for row in map]
  start = find_start(map)
  set_pos(start, '.', map)

  # Make it hashable
  map = tuple([''.join(row) for row in map])

  count_even = {}
  count_odd = {}
  map_exits = {}
  count_even['Start'], count_odd['Start'], map_exits['Start'] = path_through_map(start, map, 1000)
  count_even['S'], count_odd['S'], map_exits['S'] = path_through_map((map_exits['Start']['S'][0][0], 0), map, 1000)
  count_even['N'], count_odd['N'], map_exits['N'] = path_through_map((map_exits['Start']['N'][0][0], len(map)-1),
                                                                     map, 1000)
  count_even['E'], count_odd['E'], map_exits['E'] = path_through_map((0, map_exits['Start']['E'][0][1]), map, 1000)
  count_even['W'], count_odd['W'], map_exits['W'] = path_through_map((len(map[0]) - 1, map_exits['Start']['W'][0][1]),
                                                                     map, 1000)

  count_even['NE'], count_odd['NE'], map_exits['NE'] = path_through_map((0, len(map)), map, 1000)
  count_even['NW'], count_odd['NW'], map_exits['NW'] = path_through_map((len(map[0]), len(map)), map, 1000)
  count_even['SE'], count_odd['SE'], map_exits['SE'] = path_through_map((len(map[0]), 0), map, 1000)
  count_even['SW'], count_odd['SW'], map_exits['SW'] = path_through_map((0, 0), map, 1000)

  # We test above that they are all the same
  distance_per_tile = map_exits['S']['S'][1]

  # going east
  print(map_exits['Start']['E'][1])

  print(26501365 / distance_per_tile)


def solve_2(filename='input/test-21.txt', max_dist=6):
  map = read_input(filename)

  expand_factor = 3

  # Prep the map
  map = [list(row) for row in map]
  start = find_start(map)
  set_pos(start, '.', map)

  map = [list(row)*(2*expand_factor+1) for row in map]*(2*expand_factor+1)

  # Make it hashable
  map = tuple([''.join(row) for row in map])

  c = int((len(map) - 1) / 2)
  start = (c, c)

  stuff = path_through_map(start, map, 65)
  print(stuff)
  stuff = path_through_map(start, map, 196)
  print(stuff)
  stuff = path_through_map(start, map, 327)
  print(stuff)
  stuff = path_through_map(start, map, 458)
  print(stuff)

  print('3740 - 15054 n + 15173 n^2 for n =202301')
  print('I needed a hint on the repeating pattern and quadratic equation from Wolfram alpha')

  return 620962518745459


if __name__ == '__main__':
  # print(solve_1())
  # print(solve_1('input/input-21.txt', 64))

  print(solve_2('input/input-21.txt'))
