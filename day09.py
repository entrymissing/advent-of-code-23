import os

from util import read_input


def parse_input(lines):
  histories = []
  for line in lines:
    histories.append([int(step) for step in line.split()])
  return histories


def reduce_history(history):
  reduction = []
  cur_reduce = history
  while not all([v == 0 for v in cur_reduce]):
    reduction.append(cur_reduce)
    new_history = []
    for idx in range(len(cur_reduce)-1):
      new_history.append(cur_reduce[idx+1] - cur_reduce[idx])
    cur_reduce = new_history
  reduction.append(cur_reduce)
  return reduction


def predict_reduction(reduction):
  reduction[len(reduction)-1].append(0)

  for cur_layer in range(len(reduction)-2, -1, -1):
    difference = reduction[cur_layer+1][-1]
    new_value = reduction[cur_layer][-1] + difference
    reduction[cur_layer].append(new_value)
  return reduction


def solve_1(filename='input/test-09.txt'):
  lines = read_input(filename)
  histories = parse_input(lines)

  resp = 0

  for history in histories:
    reduction = reduce_history(history)
    predicted = predict_reduction(reduction)
    resp += predicted[0][-1]
  return resp


def predict_backward(reduction):
  reduction[len(reduction)-1].insert(0, 0)

  for cur_layer in range(len(reduction)-2, -1, -1):
    difference = reduction[cur_layer+1][0]
    new_value = reduction[cur_layer][0] - difference
    reduction[cur_layer].insert(0, new_value)
  return reduction


def solve_2(filename='input/test-09.txt'):
  lines = read_input(filename)
  histories = parse_input(lines)

  resp = 0

  for history in histories:
    reduction = reduce_history(history)
    predicted = predict_backward(reduction)
    resp += predicted[0][0]
  return resp


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 114
    assert solve_1('input/input-09.txt') == 1930746032
    assert solve_2() == 2
    assert solve_2('input/input-09.txt') == 1154


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-09.txt'))
  print(solve_2())
  print(solve_2('input/input-09.txt'))
