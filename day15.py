import os

from util import read_input


def compute_hash(text):
  val = 0
  for c in text:
    val += ord(c)
    val *= 17
    val %= 256
  return val


def test_compute_has():
  assert compute_hash('HASH') == 52
  assert compute_hash('rn') == 0
  assert compute_hash('cm') == 0
  assert compute_hash('pc') == 3


def solve_1(filename='input/test-15.txt'):
  line = read_input(filename)[0]
  parts = line.split(',')

  resp = 0
  for part in parts:
    resp += compute_hash(part)
  return resp


def parse_input(line):
  parts = line.split(',')
  parsed_parts = []
  for part in parts:
    for idx, val in enumerate(part):
      if val.isalpha():
        continue

      label = part[:idx]
      op = part[idx]
      if op == '=':
        focal = int(part[idx+1:])
      else:
        focal = -1

      parsed_parts.append((label, compute_hash(label), op, focal))
      break

  return parsed_parts


def compute_focusing_power(boxes):
  total = 0

  for idx, box in enumerate(boxes):
    for box_idx, val in enumerate(box):
      total += (idx + 1) * (box_idx+1) * val[1]

  return total


def solve_2(filename='input/test-15.txt'):
  line = read_input(filename)[0]
  parts = parse_input(line)

  boxes = []
  for _ in range(256):
    boxes.append([])

  for part in parts:
    label, hash, op, focal = part

    if op == '-':
      for lab, val in boxes[hash]:
        if lab == label:
          boxes[hash].remove((lab, val))

    if op == '=':
      found = False
      for idx, val in enumerate(boxes[hash]):
        if val[0] == label:
          boxes[hash][idx] = (label, focal)
          found = True
          break
      if not found:
        boxes[hash].append((label, focal))

  return compute_focusing_power(boxes)


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 1320
    assert solve_1('input/input-15.txt') == 509784
    assert solve_2() == 145
    assert solve_2('input/input-15.txt') == 230197


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-15.txt'))
  print(solve_2())
  print(solve_2('input/input-15.txt'))
