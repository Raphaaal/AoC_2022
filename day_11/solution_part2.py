# tr -d '\r' < input.txt | awk 'BEGIN {RS="";FS="\n"} ; {split($2, items, ":")} ; {split($3, op, "=")} ; {split($4, test, "by")} ; {split($5, true, "monkey")} ; {split($6, false, "monkey")} ; {print substr($1, 8, 1) ";" items[2] ";" op[2] ";" test[2] ";" true[2] ";" false[2]}' > input_awked.txt

from pprint import pprint
import copy


filename = "input_awked.txt"

# Parse the items
items = {}
with open(filename) as f:
     accumulator = 0
     for line in f:
          monkey = line.strip().split(";")

          # Create items
          for i in monkey[1].split(","):
               items[accumulator] = {
                    "id": accumulator,
                    "value": int(i),
                    "visited": {},
                    "old": [],
                    } 
               accumulator += 1

# Parse the monkeys
monkeys = {}
with open(filename) as f:
     accumulator = 0
     for line in f:
          monkey = line.strip().split(";")

          # Create monkeys
          monkeys[int(monkey[0])] = {
               "id": int(monkey[0]),
               "items": [
                    i + accumulator 
                    for i 
                    in range(len(monkey[1].split(",")))
                    ],
               "op": "lambda old :" + monkey[2],
               "type_op": monkey[2].split(" ")[2],
               "factor_op": monkey[2].split(" ")[3],
               "test": int(monkey[3]),
               "true": int(monkey[4]),
               "false": int(monkey[5]),
          }
          accumulator += len(monkeys[int(monkey[0])]["items"])

# Initialize the items
for i in items.values():
     val = i["value"]
     i["value"] = {k: val for k in monkeys.keys()}

# Initialize counters for monkey business
counters = {k:0 for k in monkeys.keys()}


# Run
for iteration in range(1, 10001):

     for idx, monkey in monkeys.items():

          while len(monkey["items"]) > 0:

               # Get item props
               i = monkey["items"].pop(0)
               item = items[i]

               # Increment items inspected
               counters[idx] += 1

               # Evaluate and reduce worry level
               for k, m in monkeys.items():
                    worry = eval(monkey["op"])(item["value"][k])
                    item["value"][k] = worry % m["test"]

               # Throw to another monkey
               test = (item["value"][idx] % monkey["test"]) == 0
               if test: 
                    monkeys[monkey["true"]]["items"].append(i)
               else:
                    monkeys[monkey["false"]]["items"].append(i)


# Compute monkey business
counts = list(counters.values())
top_1 = max(counts)
counts = [c for c in counts if c != top_1]
top_2 = max(counts)
print(top_1 * top_2)