import pytest
import os

from copy import deepcopy
from collections import defaultdict

from util import read_input


class Brick(object):
  def __init__(self, config, id):
    self.id = id
    from_pos, to_pos = config.split('~')
    self.from_pos = [int(v) for v in from_pos.split(',')]
    self.to_pos = [int(v) for v in to_pos.split(',')]

    # assert that from xyz is always lower than to xyz
    for idx in range(3):
      assert self.from_pos[idx] <= self.to_pos[idx]

    self.update_all_cubes()

  def update_all_cubes(self):
    self.all_cubes = []
    for x in range(self.from_pos[0], self.to_pos[0] + 1):
      for y in range(self.from_pos[1], self.to_pos[1] + 1):
        for z in range(self.from_pos[2], self.to_pos[2] + 1):
          self.all_cubes.append([x, y, z])

    if not self.all_cubes:
      self.all_cubes.append(self.from_pos)

  def move_brick_down(self):
    self.from_pos[2] -= 1
    self.to_pos[2] -= 1
    self.update_all_cubes()

  def get_highest_z(self):
    return self.to_pos[2]

  def get_lowest_z(self):
    return self.from_pos[2]


def test_brick():
  brick = Brick('1,0,1~1,2,1', 123)
  assert brick.all_cubes == [[1, 0, 1], [1, 1, 1], [1, 2, 1]]
  assert brick.id == 123
  brick.move_brick_down()
  assert brick.all_cubes == [[1, 0, 0], [1, 1, 0], [1, 2, 0]]
  assert brick.id == 123

  brick = Brick('1,0,1~1,0,1', 234)
  assert brick.all_cubes == [[1, 0, 1]]
  brick.move_brick_down()
  assert brick.all_cubes == [[1, 0, 0]]


def test_input_parsable_and_conforming():
  if not os.path.exists('input'):
    return

  lines = read_input('input/test-22.txt')
  bricks = parse_blocks(lines)
  for idx, brick in enumerate(bricks):
    assert idx == brick.id

  lines = read_input('input/input-22.txt')
  bricks = parse_blocks(lines)
  for idx, brick in enumerate(bricks):
    assert idx == brick.id


def parse_blocks(lines):
  bricks = []
  for idx, line in enumerate(lines):
    brick = Brick(line, idx)
    bricks.append(brick)
  return bricks


def get_high_z(bricks):
  brick_z = defaultdict(list)
  for brick in bricks:
    brick_z[brick.get_highest_z()].append(brick.id)
  return brick_z


def get_low_z(bricks):
  brick_z = defaultdict(list)
  for brick in bricks:
    brick_z[brick.get_lowest_z()].append(brick.id)
  return brick_z


def get_brick_supports(brick, bricks, brick_z):
  all_supports = set()

  for pos in brick.all_cubes:
    cube_z = pos[2]
    # If the cube is at bedrock it can't move down
    if cube_z == 1:
      return ['bedrock']

    # If there are no bricks below this cube continue
    if (cube_z - 1) not in brick_z:
      continue

    # if there are we need to check each cube of each brick below
    for brick_id_below in brick_z[pos[2]-1]:
      brick_below = bricks[brick_id_below]
      for cube_below in brick_below.all_cubes:
        if cube_below[2] == cube_z - 1 and cube_below[0] == pos[0] and cube_below[1] == pos[1]:
          all_supports.add(brick_id_below)
          continue

  return list(all_supports)


def test_get_brick_supports():
  if not os.path.exists('input'):
    return

  lines = read_input('input/test-22.txt')
  bricks = parse_blocks(lines)
  brick_z = get_high_z(bricks)
  support = get_brick_supports(bricks[0], bricks, brick_z)
  assert support == ['bedrock']

  support = get_brick_supports(bricks[1], bricks, brick_z)
  assert support == [0]

  support = get_brick_supports(bricks[2], bricks, brick_z)
  assert support == []


def get_bricks_above(brick, bricks, brick_z):
  all_above = set()

  for pos in brick.all_cubes:
    cube_z = pos[2]

    # If there are no bricks below this cube continue
    if (cube_z + 1) not in brick_z:
      continue

    # if there are we need to check each cube of each brick below
    for brick_id_above in brick_z[pos[2]+1]:
      brick_above = bricks[brick_id_above]
      for cube_below in brick_above.all_cubes:
        if cube_below[2] == cube_z + 1 and cube_below[0] == pos[0] and cube_below[1] == pos[1]:
          all_above.add(brick_id_above)
          continue

  return list(all_above)


def test_get_bricks_above():
  if not os.path.exists('input'):
    return

  lines = read_input('input/test-22.txt')
  bricks = parse_blocks(lines)
  brick_z = get_low_z(bricks)
  above = get_bricks_above(bricks[0], bricks, brick_z)
  assert above == [1]

  above = get_bricks_above(bricks[1], bricks, brick_z)
  assert above == []


def move_brick_down(brick, brick_z):
  cur_brick_z = brick.get_highest_z()
  brick.move_brick_down()
  brick_z[cur_brick_z].remove(brick.id)
  brick_z[cur_brick_z - 1].append(brick.id)


def can_disintegrate(brick, bricks, brick_z):
  for pos in brick.all_cubes:
    cube_z = pos[2]

    # If there are no bricks above this cube continue
    if (cube_z + 1) not in brick_z:
      continue

    # if there are we need to check each cube of each brick below
    for brick_id_below in brick_z[pos[2]+1]:
      brick_below = bricks[brick_id_below]
      for cube_below in brick_below.all_cubes:
        if cube_below[2] == cube_z + 1 and cube_below[0] == pos[0] and cube_below[1] == pos[1]:
          return False

  return True


def solve_1(filename='input/test-22.txt', max_dist=6):
  lines = read_input(filename)
  bricks = parse_blocks(lines)

  brick_z = get_high_z(bricks)
  # Move bricks down
  still_moving = True
  count = 0
  while still_moving:
    count += 1
    if count % 1000 == 0:
      s = 0
      for h in brick_z.keys():
        s += len(brick_z[h]) * h
      print(count, s, sorted(list(brick_z.keys()))[-1])
    still_moving = False
    for brick in bricks:
      supports = get_brick_supports(brick, bricks, brick_z)
      if not supports:
        move_brick_down(brick, brick_z)
        still_moving = True

  all_supports = {}
  for brick in bricks:
    all_supports[brick.id] = get_brick_supports(brick, bricks, brick_z)

  brick_z = get_low_z(bricks)
  removable_bricks = []
  for brick in bricks:
    bricks_above = get_bricks_above(brick, bricks, brick_z)
    if not bricks_above:
      removable_bricks.append(brick.id)
      continue

    for brick_above in bricks_above:
      # if this is the only brick supporting the one above it can't be removed
      if len(all_supports[brick_above]) == 1:
        break
    # if all bricks above are supported by at least 2 bricks this one can be removed
    else:
      removable_bricks.append(brick.id)

  return len(removable_bricks)


def solve_2(filename='input/test-22.txt', max_dist=6):
  lines = read_input(filename)
  bricks = parse_blocks(lines)

  brick_z = get_high_z(bricks)
  # Move bricks down
  still_moving = True
  count = 0
  while still_moving:
    count += 1
    if count % 1000 == 0:
      s = 0
      for h in brick_z.keys():
        s += len(brick_z[h]) * h
      print(count, s, sorted(list(brick_z.keys()))[-1])
    still_moving = False
    for brick in bricks:
      supports = get_brick_supports(brick, bricks, brick_z)
      if not supports:
        move_brick_down(brick, brick_z)
        still_moving = True

  all_supports = {}
  for brick in bricks:
    all_supports[brick.id] = get_brick_supports(brick, bricks, brick_z)

  brick_z = get_low_z(bricks)
  removable_bricks = []
  for brick in bricks:
    bricks_above = get_bricks_above(brick, bricks, brick_z)
    if not bricks_above:
      removable_bricks.append(brick.id)
      continue

    for brick_above in bricks_above:
      # if this is the only brick supporting the one above it can't be removed
      if len(all_supports[brick_above]) == 1:
        break
    # if all bricks above are supported by at least 2 bricks this one can be removed
    else:
      removable_bricks.append(brick.id)

  resp = 0
  original_bricks = deepcopy(bricks)
  for c, cur_brick in enumerate(original_bricks):
    print(c, len(original_bricks))
    if cur_brick.id in removable_bricks:
      continue

    # Recalculate the condition
    bricks = deepcopy(original_bricks)
    bricks.pop(cur_brick.id)
    for idx, brick in enumerate(bricks):
      brick.id = idx
    brick_z = get_high_z(bricks)

    bricks_that_moved = set()
    still_moving = True
    while still_moving:
      still_moving = False
      bricks_in_flight = len(bricks_that_moved)
      for brick in bricks:
        supports = get_brick_supports(brick, bricks, brick_z)
        if not supports:
          move_brick_down(brick, brick_z)
          bricks_that_moved.add(brick.id)
          still_moving = True
      if bricks_in_flight == len(bricks_that_moved):
        break

    resp += len(bricks_that_moved)

  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 5
    assert solve_2() == 7


# Calculating the full results takes too long to run quickly
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_1('input/input-22.txt') == 437
    assert solve_2('input/input-22.txt') == 42561


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-22.txt'))
  print(solve_2())
  print(solve_2('input/input-22.txt'))
