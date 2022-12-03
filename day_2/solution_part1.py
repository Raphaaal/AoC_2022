filename = "input.txt"

POINTS_HAND = {
     "X": 1,
     "Y": 2,
     "Z": 3,
}
counter_hand = 0 

WIN_HAND = {
     "X": "C",
     "Y": "A",
     "Z": "B",
}
DRAW_HAND = {
     "X": "A",
     "Y": "B",
     "Z": "C",
}
counter_win = 0 

with open(filename) as f:
     for line in f:

          # Parse
          hands = line.split()
          opponent_hand = hands[0]
          my_hand = hands[1]

          # Points for my hand
          counter_hand += POINTS_HAND[my_hand]

          # Points for the outcome
          if WIN_HAND[my_hand] == opponent_hand:
               counter_win += 6
               continue
          if DRAW_HAND[my_hand] == opponent_hand:
               counter_win += 3

print(f"Total = {counter_hand + counter_win}")