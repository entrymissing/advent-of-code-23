import os
import math

from util import read_input


def parse_input(lines):
  times = [int(t) for t in lines[0][7:].split() if t]
  distances = [int(d) for d in lines[1][11:].split() if d]
  return times, distances


def test_parse_input():
  lines = ['Time:        1  3     56  11  ', 'Distance:  33 65      1 2  ']
  times, distances = parse_input(lines)
  assert times == [1, 3, 56, 11]
  assert distances == [33, 65, 1, 2]


def solve_1(filename='input/test-06.txt'):
  lines = read_input(filename)
  times, distances = parse_input(lines)

  resp = 1
  for time, dist in zip(times, distances):
    win_count = 0
    for t in range(time):
      speed = t
      runtime = time-t
      if speed*runtime > dist:
        win_count += 1
    resp *= win_count
  return resp


def parse_input_2(lines):
  time = float(''.join([t for t in lines[0][7:].split() if t]))
  distance = float(''.join([t for t in lines[1][11:].split() if t]))
  return time, distance


def test_parse_input_2():
  lines = ['Time:        1  3     56  11  ', 'Distance: 33 65      1 2  ']
  time, distance = parse_input_2(lines)
  assert math.isclose(time, 135611.0)
  assert math.isclose(distance, 36512.0)


def solve_2(filename='input/test-06.txt'):
  lines = read_input(filename)
  time, distance = parse_input_2(lines)

  start = math.ceil(0.5 * (time - math.sqrt(time * time - 4*distance)))
  stop = math.floor(0.5 * (time + math.sqrt(time * time - 4*distance)))

  return stop-start+1


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 288
    assert solve_1('input/input-06.txt') == 625968
    assert solve_2() == 71503
    assert solve_2('input/input-06.txt') == 43663323


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-06.txt'))
  print(solve_2())
  print(solve_2('input/input-06.txt'))
