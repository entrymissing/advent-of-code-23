def read_input(filename):
  with open(filename) as fp:
    lines = fp.readlines()
    lines = [line.strip() for line in lines]
  return lines