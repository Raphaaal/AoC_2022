import numpy as np


def is_visible(
     idx:tuple,
     forest:np.array, 
     ):

     i, j = idx
     tree_height = forest[i, j]

     # Border of forest
     if (
          (i == 0) or 
          (j == 0) or 
          (i == forest.shape[0] - 1) or
          (j == forest.shape[1] - 1)
          ):
          return True

     # Within forest
     else:
          max_top = np.max(forest[:i, j])
          max_bottom = np.max(forest[i+1:, j])
          max_left = np.max(forest[i, :j])
          max_right = np.max(forest[i, j+1:])

          if (
               (tree_height <= max_top) and
               (tree_height <= max_bottom) and
               (tree_height <= max_left) and
               (tree_height <= max_right) 
               ):
               return False

     return True


def scenic_score(
     idx:tuple,
     forest:np.array, 
     ):

     i, j = idx
     tree_height = forest[i, j]

     blocked_top = -1
     blocked_bottom = -1
     blocked_left = -1
     blocked_right = -1

     # Border of forest
     if (i == 0):
          blocked_top = 0
     if (j == 0):
           blocked_left = 0
     if (i == forest.shape[0] - 1):
          blocked_bottom = 0
     if (j == forest.shape[1] - 1):
          blocked_right = 0

     # Within forest
     if blocked_top == -1:
          view = np.flipud(forest[:i, j])
          # Not blocked
          if np.max(view) < tree_height:
               blocked_top = view.shape[0]
          else:
               blocked_top = np.argmax(view >= tree_height) + 1

     if blocked_bottom == -1:
          view = forest[i+1:, j]
          # Not blocked
          if np.max(view) < tree_height:
               blocked_bottom = view.shape[0]
          else:
               blocked_bottom = np.argmax(view >= tree_height) + 1

     if blocked_left == -1:
          view = np.flipud(forest[i, :j])
          # Not blocked
          if np.max(view) < tree_height:
              blocked_left = view.shape[0]
          else:
               blocked_left = np.argmax(view) + 1

     if blocked_right == -1:
          view = forest[i, j+1:]
          # Not blocked
          if np.max(view) < tree_height:
              blocked_right = view.shape[0]
          else:
               blocked_right = np.argmax(view >= tree_height) + 1

     return blocked_top * blocked_bottom * blocked_left * blocked_right
     

filename = "input.txt"
forest = []

# Parse input into array
with open(filename) as f:

     for line in f:
          line = line.strip()
          line = np.array([
               int(i) 
               for i 
               in line
               ])
          forest.append(line)

forest = np.vstack(forest)
forest_scores = np.zeros((forest.shape[0], forest.shape[1]))
counter = 0

# Compute visbility of each tree in the forest
for i in range(forest.shape[0]):
     for j in range(forest.shape[1]):

          # Accumulate
          if is_visible((i, j), forest):
               counter += 1
          # Comput scenic score
          score = scenic_score((i, j), forest)
          forest_scores[i, j] = score

print(counter)
print(int(forest_scores.max()))




