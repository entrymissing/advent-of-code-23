def read_input(filename):
  with open(filename) as fp:
    lines = fp.readlines()
    lines = [line.strip() for line in lines]
  return lines


def print_map(map):
  for row in map:
    print(''.join(row))


def get_pos(*args):
  if len(args) == 2:
    pos, map = args
    x, y = pos
  else:
    x, y, map = args

  if x < 0 or y < 0:
    return None
  if x > len(map[0])-1 or y > len(map)-1:
    return None
  return map[y][x]


def set_pos(*args):
  if len(args) == 3:
    pos, value, map = args
    x, y = pos
  else:
    x, y, value, map = args
  map[y][x] = value


def pos_plus_offset(pos, offset, multiplier=1):
  return (pos[0] + offset[0] * multiplier, pos[1] + offset[1] * multiplier)
  