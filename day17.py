import os
import pytest
from collections import defaultdict

from util import read_input


offset = {
  'E': (1, 0),
  'N': (0, -1),
  'W': (-1, 0),
  'S': (0, 1),
}


direction_orter = ('E', 'N', 'W', 'S')


def get_pos(x, y, map):
  if x < 0 or y < 0:
    return None
  if x > len(map[0])-1 or y > len(map)-1:
    return None
  return map[y][x]


def set_pos(x, y, value, map):
  map[y][x] = value


def prep_maps(map):
  dist_map = []
  cost_map = []

  max_dist = len(map) * len(map[0]) * 9

  for row in map:
    new_cost_row = []
    new_dist_row = []
    for v in row:
      new_dist_row.append(max_dist)
      new_cost_row.append(int(v))
    dist_map.append(new_dist_row)
    cost_map.append(new_cost_row)

  return dist_map, cost_map


def solve_1(filename='input/test-17.txt'):
  map = read_input(filename)
  _, cost_map = prep_maps(map)

  visited = defaultdict(list)

  # set_pos(0, 0, 0, dist_map)
  visited[(0, 0)] = [('W', 0), ('N', 0)]
  to_visit = [(get_pos(1, 0, cost_map), (1, 0), 'E'),
              (get_pos(0, 1, cost_map), (0, 1), 'S')]

  while to_visit:
    # Should really take distance to end into acoount here
    to_visit.sort()
    cur_dist, cur_pos, last_moves = to_visit.pop(0)

    if cur_pos[0] == len(map[0]) - 1 and cur_pos[1] == len(map) - 1:
      return cur_dist

    for next_dir in offset:
      # No going in the opposite direction
      if abs(direction_orter.index(next_dir) - direction_orter.index(last_moves[0])) == 2:
        continue
      new_pos = (cur_pos[0] + offset[next_dir][0], cur_pos[1] + offset[next_dir][1])
      if next_dir == last_moves[0]:
        if len(last_moves) > 2:
          continue
        new_moves = last_moves + next_dir
      else:
        new_moves = next_dir
      new_dist = get_pos(new_pos[0], new_pos[1], cost_map)
      if new_dist:
        new_cost = cur_dist + new_dist

        # Check the other ways of reaching this new position
        other_ways = visited[new_pos]

        is_new_way = True
        for prev_moves, prev_dist in other_ways:
          if prev_moves == new_moves:
            is_new_way = False
            if prev_dist > new_dist:
              visited[new_pos].remove((prev_moves, prev_dist))
              visited[new_pos].append((new_moves, new_dist))
              to_visit.append((new_cost, new_pos, new_moves))
              break
        if is_new_way:
          visited[new_pos].append((new_moves, new_dist))
          to_visit.append((new_cost, new_pos, new_moves))


def solve_2(filename='input/test-17.txt'):
  map = read_input(filename)
  _, cost_map = prep_maps(map)

  visited = defaultdict(list)

  # set_pos(0, 0, 0, dist_map)
  visited[(0, 0)] = [('W', 0), ('N', 0)]
  to_visit = [(get_pos(1, 0, cost_map), (1, 0), 'E'),
              (get_pos(0, 1, cost_map), (0, 1), 'S')]

  while to_visit:
    to_visit.sort()
    cur_dist, cur_pos, last_moves = to_visit.pop(0)

    if cur_pos[0] == len(map[0]) - 1 and cur_pos[1] == len(map) - 1:
      return cur_dist

    for next_dir in offset:
      # No going in the opposite direction
      if abs(direction_orter.index(next_dir) - direction_orter.index(last_moves[0])) == 2:
        continue

      # Need to go straight for at least 4 steps
      if next_dir != last_moves[0] and len(last_moves) < 4:
        continue

      new_pos = (cur_pos[0] + offset[next_dir][0], cur_pos[1] + offset[next_dir][1])
      if next_dir == last_moves[0]:
        if len(last_moves) > 9:
          continue
        new_moves = last_moves + next_dir
      else:
        new_moves = next_dir
      new_dist = get_pos(new_pos[0], new_pos[1], cost_map)
      if new_dist:
        new_cost = cur_dist + new_dist

        # Check the other ways of reaching this new position
        other_ways = visited[new_pos]

        is_new_way = True
        for prev_moves, prev_dist in other_ways:
          if prev_moves == new_moves:
            is_new_way = False
            if prev_dist > new_dist:
              visited[new_pos].remove((prev_moves, prev_dist))
              visited[new_pos].append((new_moves, new_dist))
              to_visit.append((new_cost, new_pos, new_moves))
              break
        if is_new_way:
          visited[new_pos].append((new_moves, new_dist))
          to_visit.append((new_cost, new_pos, new_moves))


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 102
    assert solve_2() == 94


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_1('input/input-17.txt') == 814
    assert solve_2('input/input-17.txt') == 974


if __name__ == '__main__':
  print(solve_1())
  # print(solve_1('input/input-17.txt'))
  print(solve_2())
  # print(solve_2('input/input-17.txt'))
