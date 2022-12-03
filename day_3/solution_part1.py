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
     for line in f:

          # Parse
          line = list(line.strip())
          half = int(len(line)/2)
          compartment_1 = set(line[:half])
          compartment_2 = set(line[half:])

          # Find common item
          common = compartment_1.intersection(compartment_2).pop()
          
          # Accumulate priorities
          counter += PRIORITIES[common]

print(f"Total = {counter}")