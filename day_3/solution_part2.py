import string

filename = "input.txt"

PRIORITIES = {
     k: v 
     for (k, v) 
     in zip(
          list(string.ascii_lowercase) + list(string.ascii_uppercase), 
          range(1, 26*2+1)
          )
}

counter = 0 

with open(filename) as f:

     group = []

     for line in f:

          # Parse each group
          if len(group) < 3:
               group.append(line.strip())

          # Find common item
          if len(group) == 3:
               elf_1 = set(list(group[0]))
               elf_2 = set(list(group[1]))
               elf_3 = set(list(group[2]))

               common = elf_1.intersection(elf_2).intersection(elf_3).pop()

               # Accumulate priorities
               counter += PRIORITIES[common]

               # Start new group
               group = []

print(f"Total = {counter}")