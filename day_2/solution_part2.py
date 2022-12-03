filename = "input.txt"

POINTS_HAND = {
     "A": 1,
     "B": 2,
     "C": 3,
}
counter_hand = 0 

LOSE_HAND = {
     "A": "C",
     "B": "A",
     "C": "B",
}
WIN_HAND = {
     "A": "B",
     "B": "C",
     "C": "A",
}
counter_win = 0 

with open(filename) as f:
     for line in f:

          # Parse
          hands = line.split()
          opponent_hand = hands[0]
          outcome_needed = hands[1]

          # Points for outcome
          if outcome_needed == "X":
               my_hand = LOSE_HAND[opponent_hand]
          elif outcome_needed == "Y":
               my_hand = opponent_hand
               counter_win += 3
          else:
               my_hand = WIN_HAND[opponent_hand]
               counter_win += 6

          # Points for my hand
          counter_hand += POINTS_HAND[my_hand]

print(f"Total = {counter_hand + counter_win}")