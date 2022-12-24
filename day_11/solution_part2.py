# tr -d '\r' < input.txt | awk 'BEGIN {RS="";FS="\n"} ; {split($2, items, ":")} ; {split($3, op, "=")} ; {split($4, test, "by")} ; {split($5, true, "monkey")} ; {split($6, false, "monkey")} ; {print substr($1, 8, 1) ";" items[2] ";" op[2] ";" test[2] ";" true[2] ";" false[2]}' > input_awked.txt

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


# Initialize the items
for m, monkey in monkeys.items():

     for i in monkey["items"]:

          for k in monkeys.keys():          
               # items[i]["visited"][k] = [m]
               items[i]["visited"][k] = []
               items[i]["counts"] = 0

# Initialize counters for monkey business
counters = {
     k:0 
     for k 
     in monkeys.keys()
     }


def get_trick(item, m_id):
     trick = item["start"]
     old_idx = 0

     for visit in item["visited"][m_id]:
          visited = monkeys[visit]
          if visited["type_op"] == "+":
               trick += int(visited["factor_op"]) % monkeys[m_id]["test"]
          if visited["type_op"] == "*":
               if visited["factor_op"] == "old":
                    trick *= item["old"][old_idx][m_id] % monkeys[m_id]["test"]
                    old_idx += 1
               else:
                    trick *= int(visited["factor_op"]) % monkeys[m_id]["test"] 
     # print(trick)
     return trick



for i in range(1, 10001):

     for idx, monkey in monkeys.items():

          while len(monkey["items"]) > 0:

               item_id = monkey["items"].pop(0)
               item = items[item_id]
               item["counts"] += 1

               # Count items inspected
               counters[idx] += 1

               # Standard way: evaluate worry level
               # worry = eval(monkey["op"])(item["current"])
               # item["current"] = worry

               # Trick way: evaluate worry level in a faster way
               trick = item["start"]
               old_idx = 0
               # Previously visited
               for visit in item["visited"][idx]:
                    visited = monkeys[visit]
                    if visited["type_op"] == "+":
                         trick += int(visited["factor_op"]) % monkey["test"]
                    if visited["type_op"] == "*":
                         if visited["factor_op"] == "old":
                              trick *= item["old"][old_idx][idx] % monkey["test"]
                              old_idx += 1
                         else:
                              trick *= int(visited["factor_op"]) % monkey["test"] 
               # Current monkey
               if monkey["type_op"] == "+":
                    trick += int(monkey["factor_op"]) % monkey["test"]
               if monkey["type_op"] == "*":
                    if monkey["factor_op"] == "old":
                         item_copy = copy.deepcopy(item)
                         item["old"].append({
                              k: get_trick(item_copy, k)
                              for k
                              in monkeys.keys()
                              })
                         trick *= item["old"][old_idx][idx] % monkey["test"]
                         old_idx += 1
                    else:
                         trick *= int(monkey["factor_op"]) % monkey["test"] 


               if item["counts"] > 0:
                    # Update item visit history
                    for k in monkeys.keys():
                         if k in item["visited"]:
                              item["visited"][k].append(idx)
                         else:
                              item["visited"][k] = [idx]
               
               # # DEBUG
               # if (worry % monkey["test"]) != (trick % monkey["test"]):
               #      print()
               #      print("DEBUG")
               #      print(idx)
               #      print()

               # Throw to another monkey
               test = ((trick % monkey["test"]) == 0)

               if test: 
                    monkeys[monkey["true"]]["items"].append(item_id)
               else:
                    monkeys[monkey["false"]]["items"].append(item_id)


     if i in [1, 20, 1000, 2000, 3000, 4000, 5000, 10000]:
          print(i)
          pprint(counters)

# Compute monkey business
counts = list(counters.values())
top_1 = max(counts)
counts = [c for c in counts if c != top_1]
top_2 = max(counts)

print(top_1 * top_2)

# pprint(items)