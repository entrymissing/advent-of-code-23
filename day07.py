import functools
import os
from collections import Counter

from util import read_input

card_values = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
card_values_with_wildcard = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']


def read_hands(lines):
  hands = []
  for line in lines:
    cards, bet = line.split()
    hands.append((list(cards), int(bet)))
  return hands


def parse_hand(hand):
  counts = Counter(hand)

  if counts.most_common(1)[0][1] == 5:
    return 0

  if counts.most_common(1)[0][1] == 4:
    return 1

  if counts.most_common(1)[0][1] == 3 and counts.most_common(2)[1][1] == 2:
    return 2

  if counts.most_common(1)[0][1] == 3:
    return 3

  if counts.most_common(1)[0][1] == 2 and counts.most_common(2)[1][1] == 2:
    return 4

  if counts.most_common(1)[0][1] == 2:
    return 5

  return 6


def test_parse_hand():
  assert parse_hand(['K', 'K', 'K', 'K', 'K']) == 0
  assert parse_hand(['K', 'Q', 'K', 'K', 'K']) == 1
  assert parse_hand(['Q', 'K', 'Q', 'K', 'K']) == 2
  assert parse_hand(['K', 'Q', 'K', 'K', 'Q']) == 2
  assert parse_hand(['K', 'Q', 'K', 'K', 'T']) == 3
  assert parse_hand(['Q', 'K', 'Q', 'K', 'T']) == 4
  assert parse_hand(['K', 'Q', 'K', 'T', 'Q']) == 4
  assert parse_hand(['K', 'K', '1', '2', '3']) == 5
  assert parse_hand(['K', 'Q', '1', '2', '3']) == 6


def compare_hand_and_bet(hand1, hand2):
  value_hand1 = parse_hand(hand1[0])
  value_hand2 = parse_hand(hand2[0])
  if value_hand1 < value_hand2:
    return -1

  if value_hand1 > value_hand2:
    return 1

  for card1, card2 in zip(hand1[0], hand2[0]):
    if card_values.index(card1) < card_values.index(card2):
      return -1
    if card_values.index(card1) > card_values.index(card2):
      return 1

  raise Exception(f'You should not be here: {hand1}, {hand2}')


def test_compare_hands():
  assert compare_hand_and_bet([['K', 'K', 'K', 'K', 'K'], 3], [['K', 'K', 'K', 'K', 'Q'], 6]) == -1
  assert compare_hand_and_bet([['K', 'K', '2', 'K', '1'], 4], [['K', 'K', 'K', 'K', 'Q'], 7]) == 1
  assert compare_hand_and_bet([['2', 'A', 'A', 'A', 'A'], 5], [['K', '2', '2', '2', '2'], 8]) == 1


def parse_hand_with_wildcards(hand):

  jack_count = hand.count('J')
  if jack_count == 0:
    return parse_hand(hand)

  # 4 or 5 jacks means we have 5 of a kind
  if jack_count >= 4:
    return 0

  hand = [h for h in hand if not h == 'J']
  counts = Counter(hand)

  # with 3 wildcards we have either 5 or 4 of a kind
  if jack_count == 3:
    if counts.most_common(1)[0][1] == 2:
      return 0
    return 1

  if jack_count == 2:
    if counts.most_common(1)[0][1] == 3:
      return 0
    if counts.most_common(1)[0][1] == 2:
      return 1
    # three of a kind
    return 3

  if jack_count == 1:
    if counts.most_common(1)[0][1] == 4:
      return 0
    if counts.most_common(1)[0][1] == 3:
      return 1
    if counts.most_common(1)[0][1] == 2 and counts.most_common(2)[1][1] == 2:
      return 2
    if counts.most_common(1)[0][1] == 2:
      return 3
    return 5

  raise Exception(f'You should not be here: {hand}, {jack_count}, {counts}')


def test_parse_hand_with_wildcards():
  assert parse_hand_with_wildcards(['K', 'K', 'K', 'K', 'K']) == 0
  assert parse_hand_with_wildcards(['K', 'K', 'J', 'K', 'K']) == 0
  assert parse_hand_with_wildcards(['K', 'J', 'J', 'K', 'K']) == 0
  assert parse_hand_with_wildcards(['K', 'J', 'J', 'J', 'J']) == 0
  assert parse_hand_with_wildcards(['J', 'J', 'J', 'J', 'J']) == 0

  assert parse_hand_with_wildcards(['J', 'J', 'K', 'J', '2']) == 1
  assert parse_hand_with_wildcards(['J', 'K', 'K', '2', 'J']) == 1
  assert parse_hand_with_wildcards(['K', 'K', 'K', 'J', '2']) == 1
  assert parse_hand_with_wildcards(['K', 'K', 'K', 'K', '2']) == 1

  assert parse_hand_with_wildcards(['K', 'K', '2', 'J', '2']) == 2
  assert parse_hand_with_wildcards(['K', 'K', '2', '2', '2']) == 2

  assert parse_hand_with_wildcards(['K', 'K', '2', 'J', '3']) == 3
  assert parse_hand_with_wildcards(['J', 'J', 'K', '2', '3']) == 3
  assert parse_hand_with_wildcards(['2', '2', 'K', '2', '3']) == 3

  assert parse_hand_with_wildcards(['J', 'J', 'K', '2', '3']) == 3
  assert parse_hand_with_wildcards(['K', 'K', 'K', '2', '3']) == 3

  assert parse_hand_with_wildcards(['2', '3', '4', '5', 'J']) == 5
  assert parse_hand_with_wildcards(['2', '3', '4', '5', '4']) == 5


def compare_hand_and_bet_with_wildcard(hand1, hand2):
  value_hand1 = parse_hand_with_wildcards(hand1[0])
  value_hand2 = parse_hand_with_wildcards(hand2[0])
  if value_hand1 < value_hand2:
    return -1

  if value_hand2 < value_hand1:
    return 1

  for card1, card2 in zip(hand1[0], hand2[0]):
    if card_values_with_wildcard.index(card1) < card_values_with_wildcard.index(card2):
      return -1
    if card_values_with_wildcard.index(card1) > card_values_with_wildcard.index(card2):
      return 1

  raise Exception(f'You should not be here: {hand1}, {hand2}')


def solve_1(filename='input/test-07.txt'):
  lines = read_input(filename)
  hand_and_bets = read_hands(lines)

  hand_and_bets.sort(key=functools.cmp_to_key(compare_hand_and_bet), reverse=True)

  winnings = 0
  for idx, hand_and_bet in enumerate(hand_and_bets):
    winnings += (idx+1) * hand_and_bet[1]
  return winnings


def solve_2(filename='input/test-07.txt'):
  lines = read_input(filename)
  hand_and_bets = read_hands(lines)

  hand_and_bets.sort(key=functools.cmp_to_key(compare_hand_and_bet_with_wildcard), reverse=True)

  winnings = 0
  for idx, hand_and_bet in enumerate(hand_and_bets):
    winnings += (idx+1) * hand_and_bet[1]
  return winnings


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 6440
    assert solve_1('input/input-07.txt') == 251927063
    assert solve_2() == 5905
    assert solve_2('input/input-07.txt') == 255632664


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-07.txt')) 
  print(solve_2())
  print(solve_2('input/input-07.txt')) 
