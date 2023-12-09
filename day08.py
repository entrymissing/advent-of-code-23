import math
import numpy as np
import os
import pytest

from util import read_input


def parse_map(lines):
  moves = [0 if move == 'L' else 1 for move in list(lines[0])]
  lines = lines[2:]

  map = {}
  for line in lines:
    node = line.split('=')[0].strip()
    left = line[7:10]
    right = line[12:15]
    map[node] = (left, right)

  return moves, map


def test_parse_map():
  moves, map = parse_map(['LLLRRRLR', '', 'ABC = (123, ABC)', 'DEF = (321, XZZ)'])
  assert moves == [0, 0, 0, 1, 1, 1, 0, 1]
  assert map['ABC'] == ('123', 'ABC')
  assert map['DEF'] == ('321', 'XZZ')

  if os.path.exists('input'):
    lines = read_input('input/input-08.txt')
    moves, map = parse_map(lines)
    assert len(map) == len(lines) - 2

    # Same number of starts as ends
    assert len([n for n in map if n[2] == 'A']) == len([n for n in map if n[2] == 'Z'])

    # each map node and direction is 3 chars long
    for node in map:
      assert len(node) == 3
      assert len(map[node][0]) == 3
      assert len(map[node][1]) == 3

      for idx in range(3):
        assert node[idx].isalpha()
        assert map[node][0][idx].isalpha()
        assert map[node][0][idx].isalpha()


def solve_1(filename='input/test-08-1.txt'):
  lines = read_input(filename)
  moves, map = parse_map(lines)

  curPos = 'AAA'
  move_count = 0

  while curPos != 'ZZZ':
    curDir = moves[move_count % len(moves)]
    curPos = map[curPos][curDir]
    move_count += 1

  return move_count


def has_arrived(positions):
  return all([pos[2] == 'Z' for pos in positions])


def test_has_arrived():
  assert not has_arrived(['AZX', 'BBB', 'ZZZ'])
  assert has_arrived(['AXZ', 'BZZ', 'ZZZ'])
  assert not has_arrived(['BZB'])
  assert has_arrived(['BBZ'])


def get_loop(cur_position, moves, map):
  steps = []
  offset = 0
  move_count = 0
  while (cur_position, move_count % len(moves)) not in steps:
    steps.append((cur_position, move_count % len(moves)))
    if not offset and move_count % len(moves) == 0 and cur_position.endswith('Z'):
      offset = move_count
    curDir = moves[move_count % len(moves)]
    cur_position = map[cur_position][curDir]
    move_count += 1
  start_offset = steps.index((cur_position, move_count % len(moves)))
  loop_length = len(steps) - start_offset
  return steps, offset, loop_length


def test_get_loop():
  map = {'AAA': ('BBB', 'XXX'), 'BBB': ('CCZ', 'YYY'), 'CCZ': ('BBB', 'ZZZ')}
  steps, offset, loop_length = get_loop('AAA', [0, 0, 0], map)
  assert offset == 6
  assert loop_length == 6
  assert steps == [('AAA', 0), ('BBB', 1), ('CCZ', 2), ('BBB', 0), ('CCZ', 1), ('BBB', 2), ('CCZ', 0)]


def do_n_steps(start, n, moves, map):
  cur_pos = start
  move_count = 0
  for idx in range(n):
    curDir = moves[move_count % len(moves)]
    cur_pos = map[cur_pos][curDir]
    move_count += 1
  return cur_pos


def test_arrive_at_z():
  if not os.path.exists('input'):
    return

  lines = read_input('input/test-08-3.txt')
  moves, map = parse_map(lines)

  starting_positions = [pos for pos in map if pos[2] == 'A']
  starting_positions = starting_positions[:2]

  for cur_position in starting_positions:
    _, o, ll = get_loop(cur_position, moves, map)
    final = do_n_steps(cur_position, o, moves, map)
    assert final.endswith('Z')

    _, o, ll = get_loop(cur_position, moves, map)
    final = do_n_steps(cur_position, o + ll, moves, map)
    assert final.endswith('Z')


def solve_2(filename='input/test-08-3.txt'):
  lines = read_input(filename)
  moves, map = parse_map(lines)

  starting_positions = [pos for pos in map if pos.endswith('A')]

  offsets = []
  loop_lengths = []
  for cur_position in starting_positions:
    _, o, ll = get_loop(cur_position, moves, map)
    offsets.append(o)
    loop_lengths.append(ll)

  cur_step_count = offsets

  while not all(s == cur_step_count[0] for s in cur_step_count[1:]):
    min_steps = min(cur_step_count)

    indices = [idx for idx, val in enumerate(cur_step_count) if val == min_steps]
    lengths = [loop_lengths[idx] for idx in indices]
    step_length = np.lcm.reduce(np.array(lengths))

    second_lowest = sorted(cur_step_count)[len(indices)]

    min_ground_to_cover = second_lowest - min_steps
    step_length = step_length * math.ceil(min_ground_to_cover/step_length)

    for idx in indices:
      cur_step_count[idx] += step_length

  return cur_step_count[0]


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 2
    assert solve_1('input/test-08-2.txt') == 6
    assert solve_1('input/input-08.txt') == 19099
    assert solve_2() == 6


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_2('input/input-08.txt') == 17099847107071


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-08.txt'))
  print(solve_2())
  print(solve_2('input/input-08.txt'))
