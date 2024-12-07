from util import read_input, get_pos, pos_plus_offset
import os


offset = {
  'R': (1, 0),
  'U': (0, -1),
  'L': (-1, 0),
  'D': (0, 1),
}

opposing_dir = {
  'R': 'L',
  'L': 'R',
  'D': 'U',
  'U': 'D',
}


def test_map():
  if not os.path.exists('input'):
    return
  for input_file in ('input/test-23.txt', 'input/input-23.txt'):
    map = read_input(input_file)
    start_and_ends = 0
    for y, row in enumerate(map):
      for x, v in enumerate(row):
        # We're only interested in walkable places
        if v != '.':
          continue

        # count start and end points to make sure that is just one each
        if x == 0 or x == len(row)-1 or y == 0 or y == len(map)-1:
          start_and_ends += 1
          continue

        # Tests from before we adapted the next_sep function
        # for dir in offset:
        #   if get_pos(x, y, map) == '#':
        #     continue
        #   if x == 0 or x == len(row)-1 or y == 0 or y == len(map)-1:
        #     continue
        #   paths, slopes = get_next_steps((x, y), dir, map)
        #   # There are never more than 2 paths leaving a spot
        #   assert len(paths) < 3

    assert start_and_ends == 2


def get_next_steps(pos, prev_dir, map):
  slopes = []
  path = None

  for dir in offset:
    if dir == opposing_dir[prev_dir]:
      continue
    neighbor = pos_plus_offset(pos, offset[dir])
    symb = get_pos(neighbor, map)
    if symb == '#':
      continue
    if symb == '.':
      if path:
        print(f'You should not be here {pos} {prev_dir} {dir}')
      path = dir
      continue
    if symb in ['^', '>', 'v', '<']:
      slopes.append((dir, symb))
  return path, slopes


def test_get_next_steps():
  if os.path.exists('input'):
    map = read_input('input/test-23.txt')

    path, slopes = get_next_steps((1, 1), 'D', map)
    assert path == 'R'
    assert slopes == []

    paths, slopes = get_next_steps((11, 3), 'R', map)
    assert paths is None
    assert slopes == [('R', '>'), ('D', 'v')]


def solve_1(filename='input/test-23.txt'):
  map = read_input(filename)
  print(map)


if __name__ == '__main__':
  print(solve_1())
