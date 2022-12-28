# tr -d '\r' < input.txt | awk 'BEGIN {RS="";FS="\n"}; {print $1 ";" $2}' > input_awked.txt

from pprint import pprint
import itertools


def is_order_correct(packet_1:list, packet_2:list, idx) -> bool:

	for p_1, p_2 in list(itertools.zip_longest(packet_1, packet_2)):

		# Conditions on one side running out of inputs
		if p_1 is None and p_2 is not None:
			return True
		elif p_1 is not None and p_2 is None:
			return False

		# Conditions on lists inputs
		elif isinstance(p_1, list) and isinstance(p_2, list):
			if len(p_1) == 0 and len(p_2) > 0:
				return True
			elif len(p_1) > 0 and len(p_2) == 0:
				return False
			elif len(p_1) == 0 and len(p_2) == 0:
				return is_order_correct(
					packet_1[1:], 
					packet_2[1:],
					idx
					)
			else:
				# Test if lists comparaison outputs a decision
				test = is_order_correct(
					[*packet_1[0]], 
					[*packet_2[0]], 
					idx
					)
				if test == "draw":
					return is_order_correct(
						packet_1[1:], 
						packet_2[1:], 
						idx
						)
				else:
					return test

		# Conditions on mixed types input
		elif isinstance(p_1, list) and isinstance(p_2, int):
			return is_order_correct(
				packet_1, 
				[[p_2]] + packet_2[1:],
				idx
				)
		elif isinstance(p_1, int) and isinstance(p_2, list):
			return is_order_correct(
				[[p_1]] + packet_1[1:],
				packet_2,
				idx
				)

		# Conditions on integer inputs
		elif p_1 == p_2:
			if len(packet_1) == 1 and len(packet_2) == 1:
				return "draw"
			else:
				return is_order_correct(packet_1[1:], packet_2[1:], idx)
		elif p_1 < p_2:
			return True
		else:
			return False


# filename = "input_sample_awked.txt"
filename = "input_awked.txt"

# Parse pairs
pairs = []
with open(filename) as f:
	for line in f:
		line = line.strip().split(";")
		packet_1 = eval(line[0])
		packet_2 = eval(line[1])
		pairs.append([packet_1, packet_2])

# Compute correct pairs
correct = []
for idx, p in enumerate(pairs):
	is_p_correct = is_order_correct(p[0], p[1], idx+1)
	correct.append(is_p_correct)

# Sum indices of correct pairs
sum_correct_idx = 0
for idx, p in enumerate(correct):
	if p:
		sum_correct_idx += idx + 1
print(sum_correct_idx)
