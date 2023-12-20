from collections import defaultdict
import math
import os
import pytest

from util import read_input


def parse_input(lines):
  modules = {}
  for line in lines:
    mod_string = line.split('->')[0].strip()
    if mod_string == 'broadcaster':
      module_type = mod_string
      module_id = mod_string
    else:
      module_type = mod_string[0]
      module_id = mod_string[1:]

    out_string = line.split('->')[1].strip()
    out_modules = [mod_id.strip() for mod_id in out_string.split(',')]
    modules[module_id] = (module_type, out_modules)

  return modules


def test_parse_input():
  assert parse_input(['broadcaster -> a, b, c']) == {'broadcaster': ('broadcaster', ['a', 'b', 'c'])}
  assert parse_input(['%xx -> a, b']) == {'xx': ('%', ['a', 'b'])}
  assert parse_input(['%xx -> a, b', '&yy -> x, b']) == {'xx': ('%', ['a', 'b']), 'yy': ('&', ['x', 'b'])}


def send_pulse(input, from_module_name, module_name, module, state):
  module_type, out_modules = module
  match module_type:
    case 'button' | 'broadcaster':
      return (input, out_modules, state)

    case '%':
      if input == 'high':
        return (None, [], state)

      state[module_name] = (state[module_name] + 1) % 2
      if state[module_name] == 1:
        return ('high', out_modules, state)
      else:
        return ('low', out_modules, state)

    case '&':
      state[module_name][from_module_name] = input
      for fm in state[module_name]:
        if state[module_name][fm] == 'low':
          return ('high', out_modules, state)
      return ('low', out_modules, state)

  print(f'You should not be here {input}, {module}')


def test_send_pulse():
  modules = {'xx': ('%', ['yy']), 'yy': ('&', ['aa'])}

  state = init_state(modules)
  new_input, new_module_names, new_state = send_pulse('low', 'xx', 'yy', modules['yy'], state)
  assert new_input == 'high'
  assert new_module_names == ['aa']
  assert new_state == {'xx': 0, 'yy': defaultdict(dict, {'xx': 'low'}), 'aa': defaultdict(dict, {'yy': 'low'})}

  state = init_state(modules)
  new_input, new_module_names, new_state = send_pulse('high', 'yy', 'xx', modules['xx'], state)
  assert not new_input
  assert new_module_names == []
  assert new_state == {'xx': 0, 'yy': defaultdict(dict, {'xx': 'low'}), 'aa': defaultdict(dict, {'yy': 'low'})}

  state = init_state(modules)
  new_input, new_module_names, new_state = send_pulse('low', 'yy', 'xx', modules['xx'], state)
  assert new_input == 'high'
  assert new_module_names == ['yy']
  assert new_state == {'xx': 1, 'yy': defaultdict(dict, {'xx': 'low'}), 'aa': defaultdict(dict, {'yy': 'low'})}
  new_input, new_module_names, new_state = send_pulse('low', 'yy', 'xx', modules['xx'], new_state)
  assert new_input == 'low'
  assert new_module_names == ['yy']
  assert new_state == {'xx': 0, 'yy': defaultdict(dict, {'xx': 'low'}), 'aa': defaultdict(dict, {'yy': 'low'})}

  modules = {'xx': ('%', ['yy']), 'zz': ('%', ['yy']), 'yy': ('&', ['aa'])}
  state = init_state(modules)
  assert state['yy'] == defaultdict(dict, {'xx': 'low', 'zz': 'low'})
  new_input, _, state = send_pulse('high', 'xx', 'yy', modules['yy'], state)
  assert new_input == 'high'
  new_input, _, state = send_pulse('high', 'zz', 'yy', modules['yy'], state)
  assert new_input == 'low'


def init_state(modules):
  state = defaultdict(dict)

  # In a first pass we add the backlinks for the &
  for module_name in modules:
    for connected_module in modules[module_name][1]:
      state[connected_module][module_name] = 'low'

  # In a second pass we overwrite the backlinks with 0 for %
  for module_name in modules:
    match modules[module_name][0]:
      case '%':
        state[module_name] = 0
  return state


def test_init_state():
  modules = {'xx': ('%', ['a', 'yy']), 'yy': ('&', ['xx', 'a']), 'c': ('%', ('xx',))}
  state = init_state(modules)
  print(state)
  assert state['a'] == {'xx': 'low', 'yy': 'low'}
  assert state['xx'] == 0
  assert state['c'] == 0


def solve_1(filename='input/test-20.txt'):
  lines = read_input(filename)
  modules = parse_input(lines)
  modules['button'] = ('button', ['broadcaster'])
  state = init_state(modules)

  count_high = 0
  count_low = 0
  for _ in range(1000):
    to_send = [('low', 'button', 'broadcaster')]
    while to_send:
      input, from_module_name, to_module_name = to_send.pop(0)
      if input == 'high':
        count_high += 1
      else:
        count_low += 1

      if to_module_name not in modules:
        continue

      new_input, new_module_names, state = send_pulse(input,
                                                      from_module_name,
                                                      to_module_name,
                                                      modules[to_module_name],
                                                      state)

      for new_module_name in new_module_names:
        to_send.append((new_input, to_module_name, new_module_name))

  return count_high*count_low


def solve_2(filename='input/test-20.txt'):
  lines = read_input(filename)
  modules = parse_input(lines)
  modules['button'] = ('button', ['broadcaster'])
  state = init_state(modules)

  press_count = 0
  kr = []
  zs = []
  kf = []
  qk = []
  for _ in range(15000):
    press_count += 1
    to_send = [('low', 'button', 'broadcaster')]
    while to_send:
      input, from_module_name, to_module_name = to_send.pop(0)

      if state['gf']['kr'] == 'high':
        kr.append(press_count)
      if state['gf']['zs'] == 'high':
        zs.append(press_count)
      if state['gf']['kf'] == 'high':
        kf.append(press_count)
      if state['gf']['qk'] == 'high':
        qk.append(press_count)

      if to_module_name not in modules:
        continue

      new_input, new_module_names, state = send_pulse(input,
                                                      from_module_name,
                                                      to_module_name,
                                                      modules[to_module_name],
                                                      state)

      for new_module_name in new_module_names:
        to_send.append((new_input, to_module_name, new_module_name))

  kr = sorted(list(set(kr)))
  zs = sorted(list(set(zs)))
  kf = sorted(list(set(kf)))
  qk = sorted(list(set(qk)))

  return math.lcm(kr[0], zs[0], kf[0], qk[0])


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 32000000
    assert solve_1('input/test-20-2.txt') == 11687500
    assert solve_1('input/input-20.txt') == 739960225


# Calculating the result for solve_2 takes several seconds which is annoying
@pytest.mark.longrun
def test_result_long():
  if os.path.exists('input'):
    assert solve_2('input/input-20.txt') == 231897990075517


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/test-20-2.txt'))
  print(solve_1('input/input-20.txt'))
  print(solve_2('input/input-20.txt'))
