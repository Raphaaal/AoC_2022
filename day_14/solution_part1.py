from pprint import pprint
from typing import Callable
import pdb
import copy


FILENAME = "input.txt"


def map_many(funcs:[Callable], iterable:list):
	for f in funcs:
		iterable = map(f, iterable)
	return iterable


# Parse occupied positions
positions = []

with open(FILENAME) as f:
	for i, line in enumerate(f):

		# Parse coordinates
		coords = map_many(
			[
				lambda l : l.strip(),
				lambda l : l.split(","),
				lambda l : [int(coord) for coord in l],
			],
			line.strip().split("->")
			)

		# Encode walls
		prev = False
		for c in coords :
			positions.append({"i": c[0], "j": c[1], "type": "wall"})

			if prev:
				if prev[0] != c[0]:
					# Build row
					order = 1
					if prev[0] > c[0]:
						order = -1
					for step in range(prev[0], c[0], order):
						positions.append({"i": step, "j": c[1], "type": "wall"})
				else:
					# Build column
					order = 1
					if prev[1] > c[1]:
						order = -1
					for step in range(prev[1], c[1], order):
						positions.append({"i": c[0], "j": step, "type": "wall"})
			prev = c

# Remove duplicates
positions = [dict(t) for t in {tuple(d.items()) for d in positions}]

# Establish borders
borders = {
	"i_min": min([p["i"] for p in positions]),
	"i_max": max([p["i"] for p in positions]),
	"j_max": max([p["j"] for p in positions]),
	"j_min": 0,
}

def out_of_border(sand:dict, borders:dict):
	if (
			(sand["i"] < borders["i_min"]) or 
			(sand["i"] > borders["i_max"]) or 
			(sand["j"] > borders["j_max"])
		):
		return True

	return False


def pour(sand: dict, positions:list, borders:dict):

	def blocked_down(sand:dict, positions:list):
		for p in positions:
			if p["i"] == sand["i"] and p["j"] == sand["j"] + 1:
				return True
		return False

	def blocked_down_left(sand:dict, positions:list):
		for p in positions:
			if p["i"] == sand["i"] - 1 and p["j"] == sand["j"] + 1:
				return True
		return False

	def blocked_down_right(sand:dict, positions:list):
		for p in positions:
			if p["i"] == sand["i"] + 1 and p["j"] == sand["j"] + 1:
				return True
		return False

	while True:

		# Check if fall into void
		if out_of_border(sand, borders):
			return False, positions

		# Try falling down straight
		if blocked_down(sand, positions): 	

			# Try falling down left
			if blocked_down_left(sand, positions):

				# Try falling down right
				if blocked_down_right(sand, positions):
					break
				else:
					sand["i"] += 1
					sand["j"] += 1
			else:
				sand["i"] -= 1
				sand["j"] += 1
		
		else:
			sand["j"] += 1

	# Add new position once sand is stable
	positions.insert(0, sand)

	return True, positions

# Make sand pour
sand_units = 0
while True:
	sand = {"i": 500, "j": 0, "type": "sand"}
	keep_pouring, positions = pour(sand, positions, borders)
	if keep_pouring:
		sand_units += 1
	else: 
		break

print(sand_units)






