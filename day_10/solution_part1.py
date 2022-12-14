filename = "input.txt"

x = 1
history = [x]


def cycle(command:tuple, history:list, x:int) -> tuple:
     if command[0] == "noop":
          history.append(x)

     # "Add" operation
     else:
          history.append(x)
          history.append(x)
          x = history[-1] + int(command[1])

     return history, x


with open(filename) as f:
     for line in f:
          history, x = cycle(line.strip().split(), history, x)

interesting_signals = [20, 60, 100, 140, 180, 220]
strength_sum = 0 
for signal in interesting_signals:
     strength_sum += (history[signal] * signal)

print(strength_sum)
