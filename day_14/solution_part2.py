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

# Identify walls
WALLS = [p for p in positions if p["type"] == "wall"]

# Establish borders
borders = {
	"i_min": min([p["i"] for p in positions]),
	"i_max": max([p["i"] for p in positions]),
	"j_max": max([p["j"] for p in positions]),
}

# Add floor row
for i in range(borders["i_min"] - borders["j_max"] - 100, borders["i_max"] + borders["j_max"] + 100):
	positions.append({"i": i, "j": borders["j_max"] + 2, "type": "wall"})


# Update borders taking into account the newly created floor row
borders = {
	"i_min": min([p["i"] for p in positions]),
	"i_max": max([p["i"] for p in positions]),
	"j_min": 0,
	"j_max": max([p["j"] for p in positions]),
}


def display(positions:list, borders:list) -> None:
	rows = []
	for row in range(borders["j_min"], borders["j_max"] + 1):
		line = [" " for col in range(borders["i_min"], borders["i_max"] + 1)]
		rows.append(line)

	rows[0][500-borders["i_min"]] = "X"
	for p in positions:
		if p["type"] == "wall":
			rows[p["j"] - borders["j_min"]][p["i"] - borders["i_min"]] = "#"
		else:
			rows[p["j"] - borders["j_min"]][p["i"] - borders["i_min"]] = "o"

	for row in rows:
		print(row)



def clean_pos(pos: dict, positions: list) -> list:

	def is_separated(pos, p, axis):
		if axis == "i":
			other = "j"
		else:
			other = "i"
		for w in WALLS:
			if w[other] == pos[other] == p[other]:
				if (
					(w[axis] < pos[axis]) and (w[axis] > p[axis]) or
					(w[axis] < p[axis]) and (w[axis] > pos[axis])
					):
					return True
		return False
	
	touching_down = False
	touching_up = False
	touching_right = False
	touching_left = False

	for p in positions:
		if not ((p["i"] == pos["i"]) and (p["j"] == pos["j"])) and (p["type"] == "sand"):

			if ((pos["i"] + 2 <= p["i"]) and (pos["j"] == p["j"]) and (not is_separated(pos, p, "i"))):
				touching_down = True
			if ((pos["i"] - 2 >= p["i"]) and (pos["j"] == p["j"]) and (not is_separated(pos, p, "i"))):
				touching_up = True
			if ((pos["j"] + 2 <= p["j"]) and (pos["i"] == p["i"]) and (not is_separated(pos, p, "j"))):
				touching_right = True
			if ((pos["j"] - 2 >= p["j"]) and (pos["i"] == p["i"]) and (not is_separated(pos, p, "j"))):
				touching_left = True
		
		if touching_down and touching_up and touching_right and touching_left:
			return [p for p in positions if not ((p["i"] == pos["i"]) and (p["j"] == pos["j"]))]

	return positions

def clean(positions: list) -> list:
	positions_cp = copy.deepcopy(positions)
	for p in positions_cp:
		if p["type"] == "sand":
			positions = clean_pos(p, positions)

	return positions



def source_blocked(sand:dict, source:dict) -> bool:
	if (
			(sand["i"] == source["i"]) and 
			(sand["j"] == source["j"])
		):
		return True

	return False


def pour(sand: dict, positions:list, source:dict) ->tuple:

	def blocked_down(sand:dict, positions:list) -> bool:
		for p in positions:
			if p["i"] == sand["i"] and p["j"] == sand["j"] + 1:
				return True
		return False

	def blocked_down_left(sand:dict, positions:list) -> bool:
		for p in positions:
			if p["i"] == sand["i"] - 1 and p["j"] == sand["j"] + 1:
				return True
		return False

	def blocked_down_right(sand:dict, positions:list) -> bool:
		for p in positions:
			if p["i"] == sand["i"] + 1 and p["j"] == sand["j"] + 1:
				return True
		return False

	while True:

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

	# Check if sands rests at origin
	if source_blocked(sand, source):
		return False, positions

	# print(sand)
	return True, positions


# Make sand pour
sand_units = 0
source = {"i": 500, "j": 0}
while True:

	keep_pouring, positions = pour({"i": 500, "j": 0, "type": "sand"}, positions, source)
	if keep_pouring:
		sand_units += 1
	else: 
		sand_units += 1
		break

	if (sand_units % 1000 == 0) or (sand_units == 1):
		# Clean positions
		positions = clean(positions)

print(sand_units)
