# tr -d '\r' < input.txt | awk 'BEGIN {RS="";FS="\n"}; {print $1 ";" $2}' > input_awked.txt

from pprint import pprint
import itertools
from typing import Callable


def merge(left:list, right:list, compare:Callable) -> list:

	# If one array is empty, merge is done
	if len(left) == 0:
		return right
	if len(right) == 0:
		return left

	result = []
	index_left = index_right = 0

	while len(result) < len(left) + len(right):

		# Compare first elements
		if compare(left[index_left], right[index_right]):
			result.append(left[index_left])
			index_left += 1
		else:
			result.append(right[index_right])
			index_right += 1

		# Check if end of left or right
		if index_right == len(right):
			result += left[index_left:]
			break
		if index_left == len(left):
			result += right[index_right:]
			break

	return result


def merge_sort(array:list, compare:Callable) -> list:
	# Recursive split stop condition
	if len(array) <= 1:
		return array

	split = len(array) // 2 
	left = array[:split]
	right = array[split:]

	return merge(
		merge_sort(left, compare), 
		merge_sort(right, compare), 
		compare
		)


def is_order_correct(packet_1:list, packet_2:list) -> bool:

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
				return is_order_correct(packet_1[1:], packet_2[1:])
			else:
				# Test if lists comparaison outputs a decision
				test = is_order_correct([*packet_1[0]], [*packet_2[0]])
				if test == "draw":
					return is_order_correct(packet_1[1:],packet_2[1:])
				else:
					return test

		# Conditions on mixed types input
		elif isinstance(p_1, list) and isinstance(p_2, int):
			return is_order_correct(packet_1, [[p_2]] + packet_2[1:])
		elif isinstance(p_1, int) and isinstance(p_2, list):
			return is_order_correct([[p_1]] + packet_1[1:], packet_2)

		# Conditions on integer inputs
		elif p_1 == p_2:
			if len(packet_1) == 1 and len(packet_2) == 1:
				return "draw"
			else:
				return is_order_correct(packet_1[1:], packet_2[1:])
		elif p_1 < p_2:
			return True
		else:
			return False


filename = "input.txt"

# Parse pairs
pairs = []
with open(filename) as f:
	for line in f:
		line = line.strip()
		if line:
			pairs.append(eval(line))

# Append divider packets
pairs.append([[2]])
pairs.append([[6]])

# Order the pairs
ordered_pairs = merge_sort(pairs, is_order_correct)

# Compute distress signal decoder key
sig_1 = ordered_pairs.index([[2]]) + 1 
sig_2 = ordered_pairs.index([[6]]) + 1 
pprint(sig_1 * sig_2)
