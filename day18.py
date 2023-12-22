import os
import pytest
from collections import defaultdict

from util import read_input, set_pos, get_pos

offset = {
  'R': (1, 0),
  'U': (0, -1),
  'L': (-1, 0),
  'D': (0, 1),
}


def pos_plus_offset(pos, offset, multiplier=1):
  return (pos[0] + offset[0] * multiplier, pos[1] + offset[1] * multiplier)


def parse_input(lines, use_colors=False):
  dirs = []
  counts = []
  colors = []
  for line in lines:
    dir, count, color = line.split()
    dirs.append(dir)
    counts.append(int(count))
    colors.append(color[2:-1])

  # Use for part 2
  if use_colors:
    dirs, counts = decode_path(colors)

  return dirs, counts, colors


def decode_path(encoded_dir):
  dir_mapping = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U',
  }
  dirs = []
  counts = []
  for segment in encoded_dir:
    dirs.append(dir_mapping[segment[-1]])
    counts.append(int(segment[0:-1], 16))
  return dirs, counts


def flood_fill(map, x, y, wall='#', fill_with='#'):
  to_fill = [(x, y)]

  while to_fill:
    cur_x, cur_y = to_fill.pop()
    set_pos(cur_x, cur_y, fill_with, map)

    for o in offset:
      new_pos = pos_plus_offset((cur_x, cur_y), offset[o])
      val = get_pos(new_pos[0], new_pos[1], map)
      if val and val != wall:
        to_fill.append(new_pos)


def solve_1(filename='input/test-18.txt'):
  lines = read_input(filename)
  dirs, counts, colors = parse_input(lines)

  path = [(0, 0)]
  cur_pos = (0, 0)
  min_x, min_y = 0, 0
  max_x, max_y = 0, 0
  for cur_dir, count, _ in zip(dirs, counts, colors):
    for _ in range(count):
      cur_pos = pos_plus_offset(cur_pos, offset[cur_dir])
      min_x = min(min_x, cur_pos[0])
      min_y = min(min_y, cur_pos[1])

      max_x = max(max_x, cur_pos[0])
      max_y = max(max_y, cur_pos[1])
      path.append(cur_pos)

  path = [(p[0]-min_x, p[1]-min_y) for p in path]

  map = []
  for y in range(max_y - min_y + 1):
    cur_row = []
    for x in range(max_x - min_x + 1):
      if (x, y) in path:
        cur_row.append('#')
      else:
        cur_row.append('.')
    map.append(cur_row)

  resp = 0
  for row in map:
    resp += row.count('#')

  return resp


def poi_type(poi):
  poi = ''.join(sorted(poi))
  match poi:
    case 'horizontal_startvertical_start':
      return 'F'
    case 'horizontal_startvertical_end':
      return 'L'
    case 'horizontal_endvertical_start':
      return '7'
    case 'horizontal_endvertical_end':
      return 'J'
    case 'crossing':
      return '|'

  print(f'You should not be here: {poi}')


def test_poi_type():
  assert poi_type(['horizontal_start', 'vertical_start']) == 'F'
  assert poi_type(['horizontal_end', 'vertical_start']) == '7'
  assert poi_type(['horizontal_start', 'vertical_end']) == 'L'
  assert poi_type(['horizontal_end', 'vertical_end']) == 'J'
  assert poi_type(['crossing']) == '|'


def pois_to_counts(pois):
  is_open = False

  num_sections = 0
  last_x = sorted(pois.keys())[0]
  width_going_down = 0
  width_this_row = 0

  for x in sorted(pois.keys()):
    poi_type = pois[x]
    match poi_type:
      case '|':
        if is_open:
          is_open = False
          num_sections += 1
          width_going_down += (x - last_x) + 1
          width_this_row += (x - last_x) + 1
        else:
          is_open = True

      case 'F':
        if is_open:
          is_open = False
          width_going_down += (x - last_x) + 1
          width_this_row += (x - last_x)
          num_sections += 1
        else:
          is_open = True

      case '7':
        if is_open:
          is_open = False
          width_going_down += (x - last_x) + 1
          width_this_row += (x - last_x) + 1
          num_sections += 1
        else:
          width_this_row += (x - last_x)
          is_open = True

      case 'L':
        if is_open:
          width_going_down += (x - last_x)
          width_this_row += (x - last_x)

      case 'J':
        if is_open:
          width_going_down += (x - last_x)
          width_this_row += (x - last_x)
        else:
          width_this_row += (x - last_x) + 1
          num_sections += 1

    last_x = x

  return width_going_down, width_this_row


def test_pois_to_couts():
  assert pois_to_counts({0: 'F', 6: '7'}) == (7, 7)
  assert pois_to_counts({0: 'F', 2: '7', 4: '|', 6: '|'}) == (6, 6)
  assert pois_to_counts({0: 'L', 6: 'J'}) == (0, 7)
  assert pois_to_counts({0: 'L', 2: 'J', 4: '|', 6: '|'}) == (3, 6)

  assert pois_to_counts({0: 'L', 2: '7', 6: '|'}) == (5, 7)
  assert pois_to_counts({0: 'L', 2: 'J', 4: 'L', 6: 'J'}) == (0, 6)

  assert pois_to_counts({0: 'L', 1: '7', 4: 'L', 6: '7'}) == (6, 7)
  assert pois_to_counts({0: 'F', 2: 'J', 4: 'F', 6: 'J'}) == (5, 7)

  # Negative numbers should work the same
  assert pois_to_counts({-7: 'L', -5: 'J', -3: 'L', -1: 'J'}) == (0, 6)


def solve_2(filename='input/test-18.txt'):
  lines = read_input(filename)
  dirs, counts, colors = parse_input(lines, True)
  # dirs, counts = decode_path(encoded_dirs)

  segments = []
  x, y = 0, 0
  for dir, count in zip(dirs, counts):
    end_x, end_y = pos_plus_offset((x, y), offset[dir], count)
    # For horizontal lines we want the smaller x to be first
    if end_y == y:
      if x < end_x:
        segments.append((x, y, end_x, end_y))
      else:
        segments.append((end_x, end_y, x, y))
    # For veritcal lines we want the smaller y coordinate first
    else:
      if y < end_y:
        segments.append((x, y, end_x, end_y))
      else:
        segments.append((end_x, end_y, x, y))
    x, y = end_x, end_y

  all_y = list({y: True for (_, y, _, _) in segments}.keys())
  all_y.sort()

  resp = 0
  last_width = None
  last_y = None
  for y in all_y:
    pois = defaultdict(list)
    for x1, y1, x2, y2 in segments:
      # Horizontal at this y
      if y == y1 == y2:
        pois[x1].append('horizontal_start')
        pois[x2].append('horizontal_end')
        continue

      # If the vertical line ends at this y level (segments always have  the higher y at the end)
      if y == y2:
        pois[x1].append('vertical_end')
        continue

      # If the vertical line starts at this y level (segments always have  the higher y at the end)
      if y == y1:
        pois[x1].append('vertical_start')
        continue

      # No matching start or end points but maybe the segment is crossing
      if x1 == x2 and y1 < y and y2 > y:
        pois[x1].append('crossing')
        continue

    # Convert pois
    for x in pois:
      pois[x] = poi_type(pois[x])

    continued_width, this_width = pois_to_counts(pois)

    # This row we calculate specially and add it verbatim
    resp += this_width

    # If this isn't the first row we add the last_width times the number of rows we moved
    if last_width:
      resp += last_width * (y - last_y - 1)

    # Copy stuff over
    last_width = continued_width
    last_y = y

  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 38
    assert solve_2() == 952408144115
    assert solve_2('input/input-18.txt') == 127844509405501


# Solution 1 uses the unoptimized version and is slow on the bigger input
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_1('input/input-18.txt') == 4808


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-18.txt'))
  print(solve_2())
  print(solve_2('input/input-18.txt'))
