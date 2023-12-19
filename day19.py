import os
from collections import namedtuple

from util import read_input


Rule = namedtuple('Rule', 'item condition value then')


def parse_input(lines):
  workflows = {}
  while lines[0]:
    line = lines.pop(0)

    id, line = line.split('{')
    line = line[:-1]
    raw_rules = line.split(',')
    rules = []
    for r in raw_rules[:-1]:
      item = r[0]
      cond = r[1]
      value = int(r[2:].split(':')[0])
      then = r[2:].split(':')[1]
      rules.append(Rule(item, cond, value, then))
    default = raw_rules[-1]
    workflows[id] = ((rules, default))

  lines.pop(0)

  ratings = []
  while lines and lines[0]:
    line = lines.pop(0)
    line = line[1:-1]
    rating = {}
    for values in line.split(','):
      item, value = values.split('=')
      rating[item] = int(value)
    ratings.append(rating)

  return workflows, ratings


def eval_workflow(rating, workflow):
  rules, default = workflow
  for rule in rules:
    if rule.condition == '<' and rating[rule.item] < rule.value:
      return rule.then
    if rule.condition == '>' and rating[rule.item] > rule.value:
      return rule.then
  return default


def solve_1(filename='input/test-19.txt'):
  lines = read_input(filename)
  workflows, ratings = parse_input(lines)

  resp = 0
  for rating in ratings:
    cur_id = 'in'
    while cur_id not in ['A', 'R']:
      cur_id = eval_workflow(rating, workflows[cur_id])
    if cur_id == 'A':
      for key in rating:
        resp += rating[key]
  return resp


def split_range(range, rule):
  unaffected_arm = range.copy()
  affected_arm = range.copy()

  item = rule.item

  if rule.condition == '>':
    # if the range starts after the condition the whole condition is affected
    if rule.value < range[item][0]:
      return range.copy(), rule.then, None

    # if the range ends before the condition nothing is affected
    if rule.value >= range[item][1]:
      return None, rule.then, range.copy()

    unaffected_arm[item] = (range[item][0], rule.value)
    affected_arm[item] = (rule.value + 1, range[item][1])
  else:
    # if the range starts after the condition the whole condition is unaffected
    if range[item][0] >= rule.value:
      return None, rule.then, range.copy()

    # if the range ends before the condition the whole range is affected
    if range[item][1] < rule.value:
      return range.copy(), rule.then, None

    affected_arm[item] = (range[item][0], rule.value - 1)
    unaffected_arm[item] = (rule.value, range[item][1])

  return affected_arm, rule.then, unaffected_arm


def eval_workflow_on_range(range, workflow):
  rules, default = workflow

  for rule in rules:
    split_range(range, rule)


def solve_2(filename='input/test-19.txt'):
  lines = read_input(filename)
  workflows, _ = parse_input(lines)

  accepted_ranges = []

  to_do = [('in', {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)})]
  while to_do:
    id, range = to_do.pop(0)
    rules, default = workflows[id]
    for rule in rules:
      affected_range, new_id, range = split_range(range, rule)
      # if nothing is affected or is in the rejected pile just move on to the next rule
      if not affected_range or new_id == 'R':
        continue

      # if we found an accepted range mark it
      if new_id == 'A':
        accepted_ranges.append(affected_range)
        continue

      # if we're still here we need to follow this affected range
      to_do.append((new_id, affected_range))

      # if the whole range was affected we need to stop processing
      if not range:
        break

    # if we default to accepting or rejecting we should do so
    if default == 'R':
      continue
    if default == 'A':
      accepted_ranges.append(range)
      continue

    to_do.append((default, range))
  resp = 0
  for ar in accepted_ranges:
    prod = 1
    for key in ar:
      prod *= (ar[key][1] - ar[key][0] + 1)
    resp += prod
  return resp
  print(accepted_ranges)


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 19114
    assert solve_1('input/input-19.txt') == 376008
    assert solve_2() == 167409079868000
    assert solve_2('input/input-19.txt') == 124078207789312


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-19.txt'))
  print(solve_2())
  print(solve_2('input/input-19.txt'))
