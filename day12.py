import functools
import os

from util import read_input


def parse_input(lines, replicate=False):
  conditions = []
  counts = []

  for line in lines:
    cond = line.split()[0]
    count = tuple([int(v) for v in line.split()[1].split(',')])

    if replicate:
      cond = '?'.join([cond] * 5)
      count *= 5
    conditions.append(tuple(cond))
    counts.append(count)

  return conditions, counts


def test_parse_input():
  assert parse_input(['??? 1,2']) == ([tuple('???')], [(1, 2)], )
  assert parse_input(['X 1,2'], replicate=True) == ([tuple('X?X?X?X?X')], [(1, 2, 1, 2, 1, 2, 1, 2, 1, 2)], )


@functools.cache
def try_to_place(condition, to_place):
  # If there are no more symbols left, we're done
  if not condition:
    if to_place:
      return 0
    return 1

  # If we don't have anything to place anymore (but we still have some places to fill)
  if not to_place:
    if '#' in condition:
      return 0
    else:
      return 1

  # The length of stuff we have to place is more than we have space for
  if sum(to_place) + len(to_place) - 1 > len(condition):
    return 0

  next_to_place = to_place[0]

  # TODO: Can we skip this?
  if next_to_place > len(condition):
    return 0

  # We're trying to place a block of length next_to_place
  can_place = True

  # Check that the #next_to_place entries are all either ? or #
  for c in condition[:next_to_place]:
    if c not in ['?', '#']:
      can_place = False
      break

  # if there is something after this block it can't be a '#'#
  if len(condition) > (next_to_place + 1) and condition[next_to_place] == '#':
    can_place = False

  solution_count = 0
  if can_place:
    # compiling the prefix
    prefix_length = next_to_place
    # if the condition continues after we've placed the thing
    if len(condition) > (next_to_place + 1):
      prefix_length += 1

    solution_count += try_to_place(condition[prefix_length:], to_place[1:])

  # The other option is not to place anything
  if condition[0] == '?' or condition[0] == '.':
    solution_count += try_to_place(condition[1:], to_place)

  return solution_count


def test_try_to_place():
  assert try_to_place('.###.', (3,)) == 1
  assert try_to_place('.##.', (3,)) == 0
  assert try_to_place('.?##.', (3,)) == 1
  assert try_to_place('###.', (3,)) == 1
  assert try_to_place('.###', (3,)) == 1
  assert try_to_place('.?##', (3,)) == 1
  assert try_to_place('???', (3,)) == 1

  assert try_to_place('?...###', (1, 3,)) == 1
  assert try_to_place('??...###', (1, 3,)) == 2
  assert try_to_place('??...??', (1, 1,)) == 4
  assert try_to_place('.??..??.??.', (1, 1, 1)) == 8

  assert try_to_place('????.######..#####.', (1, 6, 5)) == 4


def solve_1(filename='input/test-12.txt'):
  lines = read_input(filename)
  conditions, counts = parse_input(lines)

  resp = 0
  for cond, count in zip(conditions, counts):
    resp += try_to_place(cond, count)
    try_to_place.cache_clear()
  return resp


def solve_2(filename='input/test-12.txt'):
  lines = read_input(filename)
  conditions, counts = parse_input(lines, replicate=True)

  resp = 0
  for cond, count in zip(conditions, counts):
    resp += try_to_place(cond, count)
    try_to_place.cache_clear()
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 21
    assert solve_1('input/input-12.txt') == 7236
    assert solve_2() == 525152
    assert solve_2('input/input-12.txt') == 11607695322318


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-12.txt'))
  print(solve_2())
  print(solve_2('input/input-12.txt'))
