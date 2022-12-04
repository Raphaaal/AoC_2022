filename = "input.txt"

counter = 0 

with open(filename) as f:

     for line in f:

          # Parse
          line = line.strip().split(",")
          elf_1 = [int(i) for i in line[0].split("-")]
          elf_2 = [int(i) for i in line[1].split("-")]

          # Test for non overlap
          if elf_1[0] < elf_2[0]:
               if elf_1[1] < elf_2[0]:
                    continue
          elif elf_2[0] < elf_1[0]:
               if elf_2[1] < elf_1[0]:
                    continue

          # Accumulate in counter
          counter += 1

print(f"Total = {counter}")