import os

from util import read_input


def read_card(line):
  card_number = int(line.split(':')[0][5:])

  numbers = line.split(':')[1]
  winning_numbers = [int(n.strip()) for n in numbers.split('|')[0].strip().split(' ') if n]
  picked_numbers = [int(n.strip()) for n in numbers.split('|')[1].strip().split(' ') if n]

  return card_number, winning_numbers, picked_numbers


def solve_1(filename='input/test-04.txt'):
  lines = read_input(filename)

  resp = 0

  for line in lines:
    card_number, winning_numbers, picked_numbers = read_card(line)
    my_winners = set(winning_numbers).intersection(set(picked_numbers))
    if len(my_winners):
      payout = 2 ** (len(my_winners)-1)
      resp += payout
  return resp


def solve_2(filename='input/test-04.txt'):
  lines = read_input(filename)

  num_tickets = [1]*len(lines)

  for idx, line in enumerate(lines):
    card_number, winning_numbers, picked_numbers = read_card(line)
    num_winners = len(set(winning_numbers).intersection(set(picked_numbers)))
    cur_tickets = num_tickets[idx]
    for offset in range(num_winners):
      num_tickets[idx+1+offset] += cur_tickets

  return sum(num_tickets)


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 13
    assert solve_1('input/input-04.txt') == 20407
    assert solve_2() == 30
    assert solve_2('input/input-04.txt') == 23806951


if __name__ == '__main__':
  print(solve_1('input/input-04.txt'))
  print(solve_2('input/input-04.txt'))
