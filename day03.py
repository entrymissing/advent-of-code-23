from collections import defaultdict
import os

from util import read_input


def get_numbers_in_line(line):
  res = []
  num_started = False
  digits = []
  start_idx = 0
  for idx, c in enumerate(line):
    if num_started:
      if c.isnumeric():
        digits.append(c)
      else:
        res.append((int(''.join(digits)), start_idx))
        num_started = False
      continue

    if c.isnumeric():
      num_started = True
      digits = [c]
      start_idx = idx

  if num_started:
    res.append((int(''.join(digits)), start_idx))
  return res


def has_symbols(row, col, length, lines):
  row_start = max(0, row-1)
  row_end = min(len(lines[0]), row+length+1)

  for c in range(max(0, col-1), min(len(lines[0]), col+2)):
    inp = lines[c][row_start:row_end]
    inp = inp.strip('0123456789.')
    if inp:
      return True
  return False


def solve_1(filename='input/test-03.txt'):
  lines = read_input(filename)

  resp = 0
  for col_idx, line in enumerate(lines):
    numbers = get_numbers_in_line(line)

    for number, row_idx in numbers:
      if has_symbols(row_idx, col_idx, len(str(number)), lines):
        resp += number

  return resp


def get_gears(row, col, length, lines):
  row_start = max(0, row-1)
  row_end = min(len(lines[0]), row+length+1)

  gears = []

  for c in range(max(0, col-1), min(len(lines[0]), col+2)):
    inp = lines[c][row_start:row_end]
    for idx, symb in enumerate(inp):
      if symb == '*':
        gears.append((c, idx+row_start))
  return gears


def solve_2(filename='input/test-03.txt'):
  lines = read_input(filename)

  gear_connections = defaultdict(list)

  for col_idx, line in enumerate(lines):
    numbers = get_numbers_in_line(line)

    for number, row_idx in numbers:
      gears = get_gears(row_idx, col_idx, len(str(number)), lines)
      for gear in gears:
        gear_connections[gear].append(number)

  resp = 0
  for gear in gear_connections:
    if len(gear_connections[gear]) == 2:
      resp += gear_connections[gear][0] * gear_connections[gear][1]
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 4361
    assert solve_1('input/input-03.txt') == 544664
    assert solve_2() == 467835
    assert solve_2('input/input-03.txt') == 84495585


if __name__ == '__main__':
  print(solve_1('input/input-03.txt'))
  print(solve_2('input/input-03.txt'))
