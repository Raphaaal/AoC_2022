# cat input.txt | awk 'BEGIN {RS="";FS="\n"}; {split($2, items, ":")} ; {split($3, op, "=")} ; {split($4, test, "by")} ; {split($5, true, "monkey")} ; {split($6, false, "monkey")} ; {print substr($1, 8, 1) ";" items[2] ";" op[2] ";" test[2] ";" true[2] ";" false[2]}' > input_awked.txt

from pprint import pprint


filename = "input_awked.txt"
monkeys = {}

with open(filename) as f:
     for line in f:

          # Parse
          monkey = line.strip().split(";")
          monkeys[int(monkey[0])] = {
               "items": [int(i) for i in monkey[1].split(",")],
               "op": "lambda old :" + monkey[2],
               "test": int(monkey[3]),
               "true": int(monkey[4]),
               "false": int(monkey[5]),
          }

counters = {
     k:0 
     for k 
     in monkeys.keys()
     }

divisors = [v["test"] for v in monkeys.values()]
print(divisors)

for i in range(1, 21):

     for idx, data in monkeys.items():

          for item in data["items"]:

               # Count items inspected
               counters[idx] += 1

               # Evaluate worry level
               worry = eval(data["op"])(item)
               worry = int(worry / 3)

               # Throw to another monkey
               test = worry % data["test"] == 0 

               if test:
                    # if idx == 0:
                    #      if not (worry % 13 == 0):
                    #           worry = worry % 13
                    # if idx == 1:
                    #      if not (worry % 13 == 0):
                    #           worry = worry % 13
                    # if idx == 3:
                    #      if (
                    #           ((worry*19) % 23 == 0) and
                    #           not ((worry*19) % 13 == 0)
                    #           ):
                    #                worry = (worry*19) % 13

                    monkeys[data["true"]]["items"].extend([worry])

               else:

                    monkeys[data["false"]]["items"].extend([worry])

               # Update current list of items
               if len(data["items"]) > 1:
                    data["items"] = data["items"][1:]
               else:
                    data["items"] = []

     if i in [1, 20, 1000, 2000, 3000, 4000, 5000, 10000]:
          print(i)
          pprint(counters)
          # pprint(monkeys)

# Compute monkey business
counts = list(counters.values())
top_1 = max(counts)
counts = [c for c in counts if c != top_1]
top_2 = max(counts)

print(top_1 * top_2)
