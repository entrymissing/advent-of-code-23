from util import read_input

def solve_1(filename='input/test-01-1.txt'):
  lines = read_input(filename)
  
  res = 0
  for line in lines:
    digits = [int(c) for c in line if c.isdigit()]
    
    value = digits[0] * 10 + digits[-1]
    res += value
  return res

def solve_2(filename='input/test-01-2.txt'):
  lines = read_input(filename)
  convert = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

  res = 0
  for line in lines:
    line = line.strip()

    digits = []
    while(line):
      if line[0].isdigit():
        digits.append(int(line[0]))
        line = line[1:]
        continue
      
      found = False
      for i, digit_text in enumerate(convert):
        if line.startswith(digit_text):
          digits.append(i+1)
          line = line[1:]
          found = True
          continue
      if not found:
        line = line[1:]
    
    value = digits[0] * 10 + digits[-1]
    res += value
  return res

def test_results():
  assert solve_1() == 142
  assert solve_1('input/input-01.txt') == 54388
  assert solve_2() == 281
  assert solve_2('input/input-01.txt') == 53515

if __name__ == '__main__':
  print(solve_1('input/input-01.txt'))
  print(solve_2('input/input-01.txt'))
