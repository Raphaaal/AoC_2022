# cat input.txt | awk 'BEGIN {RS="";FS="\n"}; {split($2, items, ":")} ; {split($3, op, "=")} ; {split($4, test, "by")} ; {split($5, true, "monkey")} ; {split($6, false, "monkey")} ; {print substr($1, 8, 1) ";" items[2] ";" op[2] ";" test[2] ";" true[2] ";" false[2]}' > input_awked.txt

from pprint import pprint
import copy


filename = "input_awked.txt"

# Create the items
items = {}
with open(filename) as f:

     accumulator = 0

     for line in f:

          # Parse
          monkey = line.strip().split(";")

          # Create items
          for i in monkey[1].split(","):
               items[accumulator] = {
                    "id": accumulator,
                    "start": int(i),
                    "current": int(i),
                    "remainders": {},
                    "visited": {},
                    "old": [],
                    } 
               accumulator += 1

# Create the monkeys
monkeys = {}
with open(filename) as f:
    
     accumulator = 0

     for line in f:

          # Parse
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

counters = {
     k:0 
     for k 
     in monkeys.keys()
     }

print(monkeys)

for i in range(1, 21):

     for idx, monkey in monkeys.items():

          while len(monkey["items"]) > 0:

               item_id = monkey["items"].pop(0)
               item = items[item_id]

               # Update visit history
               for k in monkeys.keys():
                    if k in items[item_id]["visited"]:
                         items[item_id]["visited"][k].append(idx)
                    else:
                         items[item_id]["visited"][k] = [idx]

               # Count items inspected
               counters[idx] += 1

               # Evaluate worry level
               worry = eval(monkey["op"])(item["current"])

               # Update item
               if monkey["factor_op"] == "old":
                    items[item_id]["old"].append(item["current"])
               items[item_id]["current"] = worry

               # Worry level reduce trick
               trick = item["start"]
               old_idx = 0
               for visit in item["visited"][idx]:
                    visited = monkeys[visit]
                    if visited["type_op"] == "+":
                         trick += int(visited["factor_op"]) % monkey["test"]
                    if visited["type_op"] == "*":
                         if visited["factor_op"] == "old":
                              trick *= item["old"][old_idx] % monkey["test"]
                              old_idx += 1
                         else:
                              trick *= int(visited["factor_op"]) % monkey["test"]                               
               # print()
               # print(item_id)
               # print(idx)
               # print(item["visited"][idx])
               
               # DEBUG
               if (worry % monkey["test"]) != (trick % monkey["test"]):
                    print()
                    print("DEBUGGGGGGGGGGGGGGGGGGGGGGGGGGG")
                    print(item_id)
                    print(idx)
                    print(item["visited"][idx])


               # Record item history
               for k, v in monkeys.items():
                    items[item_id]["remainders"][k] = (worry % v["test"])


               # Throw to another monkey
               # test = ((worry % monkey["test"]) == 0)
               test = ((trick % monkey["test"]) == 0)

               if test: 
                    # items[item_id]["visited"][idx] = [idx]
                    monkeys[monkey["true"]]["items"].append(item_id)
               else:
                    monkeys[monkey["false"]]["items"].append(item_id)


     if i in [1, 20, 100, 1000, 2000, 3000, 4000, 5000, 10000]:
          print(i)
          pprint(counters)

# Compute monkey business
counts = list(counters.values())
top_1 = max(counts)
counts = [c for c in counts if c != top_1]
top_2 = max(counts)

print(top_1 * top_2)

# pprint(items)