import numpy as np


def execute(
     command:str, 
     state_H:np.array,
     state_T:np.array,
     visited_T:np.array,
     ):

     state_H, new_loc_H, state_T, visited_T = update_head(
          command, 
          state_H, 
          state_T, 
          visited_T
          )
     touching = check_touching(new_loc_H, state_T)
     if not touching:
          state_T, visited_T = update_tail(new_loc_H, state_T, visited_T)

     return state_H, state_T, visited_T


def add_row_up(state:np.array) -> np.array:
     n_cols = state.shape[1]
     state = np.vstack((
          np.array(["."]).repeat(n_cols).reshape(1, n_cols),
          state, 
          ))
     return state


def add_row_down(state:np.array) -> np.array:
     n_cols = state.shape[1]
     state = np.vstack((
          state, 
          np.array(["."]).repeat(n_cols).reshape(1, n_cols),
          ))
     return state


def add_col_right(state:np.array) -> np.array:
     n_rows = state.shape[0]
     state = np.hstack((
          state, 
          np.array(["."]).repeat(n_rows).reshape(n_rows,1),
          ))
     return state


def add_col_left(state:np.array) -> np.array:
     n_rows = state.shape[0]
     state = np.hstack((
          np.array(["."]).repeat(n_rows).reshape(n_rows,1),
          state, 
          ))
     return state


def update_head(
     command:str, 
     state_H:np.array,
     state_T:np.array,
     visited_T:np.array,
     ) -> (np.array, np.array):

     loc_H = np.where(state_H == "H")
     state_H[loc_H] = "."

     if (command == "R"):
          if (loc_H[1]+1) == state_H.shape[1]:
               state_H = add_col_right(state_H)
               state_T = add_col_right(state_T)
               visited_T = add_col_right(visited_T)
          state_H[loc_H[0], loc_H[1]+1] = "H"

     if (command == "L"):
          if (loc_H[1]-1) < 0:
               state_H = add_col_left(state_H)
               state_T = add_col_left(state_T)
               visited_T = add_col_left(visited_T)
               loc_H = (loc_H[0], 1)
          state_H[loc_H[0], loc_H[1]-1] = "H"

     if (command == "U"):
          if loc_H[0]-1 < 0:
               state_H = add_row_up(state_H)
               state_T = add_row_up(state_T)
               visited_T = add_row_up(visited_T)
               loc_H = (1, loc_H[1])
          state_H[loc_H[0]-1, loc_H[1]] = "H"

     if (command == "D"):
          if loc_H[0]+1 == state_H.shape[0]:
               state_H = add_row_down(state_H)
               state_T = add_row_down(state_T)
               visited_T = add_row_down(visited_T)
          state_H[loc_H[0]+1, loc_H[1]] = "H"

     new_loc_H = np.where(state_H == "H")

     return state_H, new_loc_H, state_T, visited_T


def check_touching(new_loc_H, state_T):
     loc_T = np.where(state_T == "T")
     if (
          (abs(new_loc_H[0] - loc_T[0]) <= 1) and
          (abs(new_loc_H[1] - loc_T[1]) <= 1) 
          ):

          
          return True
     return False


def update_tail(
     new_loc_H:np.array,
     state_T:np.array,
     visited_T:np.array,
     ) -> (np.array, np.array):

     loc_T = np.where(state_T == "T")
     state_T[loc_T] = "."
     visited_T[loc_T] = "#"

     # Horizontal gap
     if (new_loc_H[0] == loc_T[0]):
          diff = new_loc_H[1] - loc_T[1]
          if diff > 0:
               state_T[new_loc_H[0], new_loc_H[1]-1] = "T"
          else:
               state_T[new_loc_H[0], new_loc_H[1]+1] = "T"

     # Vertical gap
     elif (new_loc_H[1] == loc_T[1]):
          diff = new_loc_H[0] - loc_T[0]
          if diff > 0:
               state_T[new_loc_H[0]-1, new_loc_H[1]] = "T"
          else:
               state_T[new_loc_H[0]+1, new_loc_H[1]] = "T"

     # Diagonal gap
     else:
          if abs(new_loc_H[1] - loc_T[1]) >= 2:
               diff = new_loc_H[1] - loc_T[1]
               if diff > 0:
                    state_T[new_loc_H[0], new_loc_H[1]-1] = "T"
               else:
                    state_T[new_loc_H[0], new_loc_H[1]+1] = "T"

          elif abs(new_loc_H[0] - loc_T[0]) >= 2:
               diff = new_loc_H[0] - loc_T[0]
               if diff > 0:
                    state_T[new_loc_H[0]-1, new_loc_H[1]] = "T"
               else:
                    state_T[new_loc_H[0]+1, new_loc_H[1]] = "T"
          else:
               return "ERROR"

     return state_T, visited_T


filename = "input.txt"
state_H = np.array([
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     ["H", ".", ".", ".", ".", ".",],
     ])
state_T = np.array([
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     ["T", ".", ".", ".", ".", ".",],
     ])
visited_T = np.array([
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     [".", ".", ".", ".", ".", ".",],
     ])


# Parse input into array
with open(filename) as f:

     for line in f:
          command = line.strip().split()
          for it in range(int(command[1])): 

               state_H, state_T, visited_T = execute(
                    command[0], 
                    state_H, 
                    state_T, 
                    visited_T
                    )
               #print(state_H)          
               #print(state_T)
               #print(visited_T)

     # Do not forget last visit of T
     loc_T = np.where(state_T == "T")
     visited_T[loc_T] = "#"

     counter = np.where(visited_T == "#")[0].shape[0]
     print(f"Counter: {counter}")
     print(state_H)          
     print(state_T)
     print(visited_T)
