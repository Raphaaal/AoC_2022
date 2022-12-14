filename = "input.txt"

x = 1
history = []


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


screen = [
     ["0" for i in range(40)]
     for j
     in range(6)
]
row = -1
for i, x in enumerate(history):
     print(i)
     col = i % 40
     if i % 40 == 0:
          row +=1
     print(col)
     print(row)
     if (col <= x+1) and (col >= x-1):
          screen[row][col] = "#"
     else:
          screen[row][col] = "."

for row in screen:
     print(" ".join(row + ["\n"]))
