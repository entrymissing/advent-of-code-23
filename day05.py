import os

from util import read_input


def parse_mapping_input(lines):
  map_names = []
  mapping = []
  cur_mapping = []

  for line in lines:
    if not line:
      continue

    if not line[0].isdigit():
      line = line.split()[0]
      map_from, _, map_to = line.split('-')
      map_names.append((map_from, map_to))
      if cur_mapping:
        cur_mapping = sorted(cur_mapping, key=lambda x: x[1])
        mapping.append(cur_mapping)
      cur_mapping = []

      continue

    dest_start, source_start, range_length = line.split()
    cur_mapping.append((int(dest_start), int(source_start), int(range_length)))

  cur_mapping = sorted(cur_mapping, key=lambda x: x[1])
  mapping.append(cur_mapping)
  return map_names, mapping


def parse_input_ranges(lines):
  seed_numbers = [int(s) for s in lines[0][7:].split()]
  seed_ranges = []
  for idx in range(0, len(seed_numbers), 2):
    seed_ranges.append((seed_numbers[idx], seed_numbers[idx+1]))
  lines = lines[2:]

  map_names, mapping = parse_mapping_input(lines)
  return seed_ranges, map_names, mapping


def parse_input(lines):
  seeds = [int(s) for s in lines[0][7:].split()]
  lines = lines[2:]

  map_names, mapping = parse_mapping_input(lines)
  return seeds, map_names, mapping


def propagate_seed(seed, map_step):
  for cur_map in map_step:
    dest_start, source_start, range_length = cur_map

    if seed >= source_start and seed < (source_start + range_length):
      return dest_start + (seed - source_start)
  return seed


def propagate_seeds(seeds, map_step):
  new_seeds = []
  for seed in seeds:
    new_seeds.append(propagate_seed(seed, map_step))
  return new_seeds


def solve_1(filename='input/test-05.txt'):
  lines = read_input(filename)

  seeds, map_names, mapping = parse_input(lines)

  for cur_map in mapping:
    seeds = propagate_seeds(seeds, cur_map)
  return min(seeds)


def propagate_seed_range(seed_range, map_step):
  to_do = [seed_range]
  new_seed_ranges = []

  while to_do:
    cur_range = to_do.pop(0)
    seed_start = cur_range[0]
    seed_end = cur_range[0] + cur_range[1]

    found_match = False
    for cur_map in map_step:
      dest_start, source_start, range_length = cur_map
      dest_end = dest_start + range_length
      source_end = source_start + range_length

      # not touching the current block
      if seed_start > source_end or seed_end < source_start:
        continue

      # fully in the current block
      if seed_start >= source_start and seed_end <= source_end:
        new_seed_start = dest_start + (seed_start - source_start)
        new_seed_ranges.append((new_seed_start, seed_end - seed_start))
        found_match = True
        break

      # MMM-OOO-SSS
      if seed_start >= source_start and seed_start < source_end:
        # Map the overlapping part
        new_range_start = dest_start + (seed_start - source_start)
        new_range_end = dest_end
        new_seed_ranges.append((new_range_start, new_range_end - new_range_start))

        # create a todo for the block after the overlap
        to_do.append((source_end, seed_end - source_end))
        found_match = True
        break

      # SSS-OOO-MMM or SSS-OOO-SSS
      if seed_start < source_start and seed_end > source_start:
        # create a todo for the block before and after the overlap
        to_do.append((seed_start, source_start - seed_start))
        to_do.append((source_start, seed_end - source_start))

        found_match = True
        break

    # If we didn't match anything we just propagate
    if not found_match:
      new_seed_ranges.append((seed_start, seed_end - seed_start))
  return new_seed_ranges


def test_propagate_seed_range():
  # Fully within
  assert propagate_seed_range([10, 10], [[100, 5, 20]]) == [(105, 10)]
  assert propagate_seed_range([10, 10], [[100, 10, 10]]) == [(100, 10)]
  assert propagate_seed_range([11, 9], [[100, 10, 10]]) == [(101, 9)]
  assert propagate_seed_range([10, 9], [[100, 10, 10]]) == [(100, 9)]

  # Fully without
  assert propagate_seed_range([10, 10], [[100, 50, 20]]) == [(10, 10)]
  assert propagate_seed_range([10, 10], [[100, 20, 20]]) == [(10, 10)]
  assert propagate_seed_range([40, 10], [[100, 20, 20]]) == [(40, 10)]

  # Start overlap
  assert sorted(propagate_seed_range([5, 10], [[100, 10, 10]])) == sorted([(5, 5), (100, 5)])
  assert sorted(propagate_seed_range([5, 10], [[100, 14, 10]])) == sorted([(5, 9), (100, 1)])

  # End overlap
  assert sorted(propagate_seed_range([15, 10], [[100, 10, 10]])) == sorted([(20, 5), (105, 5)])
  assert sorted(propagate_seed_range([19, 10], [[100, 10, 10]])) == sorted([(20, 9), (109, 1)])

  # End to end overlap
  assert sorted(propagate_seed_range([4, 22], [[100, 10, 10]])) == sorted([(4, 6), (20, 6), (100, 10)])
  assert sorted(propagate_seed_range([9, 12], [[100, 10, 10]])) == sorted([(9, 1), (20, 1), (100, 10)])

  # Two cut points
  assert (sorted(propagate_seed_range([4, 32], [[100, 10, 5], [200, 20, 5]])) ==
          sorted([(4, 6), (15, 5), (25, 11), (100, 5), (200, 5)]))


def propagate_seed_ranges(seed_ranges, map_step):
  new_seed_ranges = []
  for seed_range in seed_ranges:
    new_seed_ranges.extend(propagate_seed_range(seed_range, map_step))
  return new_seed_ranges


def solve_2(filename='input/test-05.txt'):
  lines = read_input(filename)
  seed_ranges, map_names, mapping = parse_input_ranges(lines)
  for cur_map in mapping:
    seed_ranges = propagate_seed_ranges(seed_ranges, cur_map)

  return min([r[0] for r in seed_ranges])


def test_results():
  if os.path.exists('input'):
    assert solve_1() == 35
    assert solve_1('input/input-05.txt') == 51580674
    assert solve_2() == 46
    assert solve_2('input/input-05.txt') == 99751240


if __name__ == '__main__':
  print(solve_1())
  print(solve_1('input/input-05.txt'))
  print(solve_2())
  print(solve_2('input/input-05.txt'))
