from pprint import pprint
import copy


filename = "input.txt"


def dijkstra(graph, start, end):

     # Initialize
     visited = {}
     costs = {}
     for node in graph.keys():
          if node == start:
               costs[node] = 0
          else:
               costs[node] = 10e6

     def get_next_visit(costs):
          minimum = 10e6
          for node, cost in costs.items():
               if cost <= minimum:
                    minimum = cost
                    next_visit = node
          return next_visit

     # Explore paths from start node
     while len(costs) > 0:

          # Get next exploration
          next_visit = get_next_visit(costs)
          visited[next_visit] = costs[next_visit]
          path_length = costs[next_visit]
          del costs[next_visit]

          # Break condition
          if next_visit == end:
               break

          # Update neighbors if not visited
          neighbors = graph[next_visit]["neighbors"]
          for n in neighbors:
               if (
                    (n in costs) and
                    ((path_length + 1) < costs[n])
                    ):
                    costs[n] = path_length + 1
     
     return visited


def a_star(graph, start, end, thresh=None):

     # Initialize
     visited = {}
     costs = {}
     for node in graph.keys():
          if node == start:
               costs[node] = 0
          else:
               costs[node] = 10e6
     scores = copy.deepcopy(costs)

     def heuristic(graph, node, end):
          h = (
               abs(graph[node]["row"] - graph[end]["row"]) + 
               abs(graph[node]["col"] - graph[end]["col"])
               )
          return h

     def get_next_visit(graph, costs, end):
          minimum = 10e6
          for node, cost in costs.items():
               estim = heuristic(graph, node, end) + cost
               if estim <= minimum:
                    minimum = estim
                    next_visit = node
          return next_visit

     # Explore paths from start node
     while len(costs) > 0:

          # Get next exploration
          next_visit = get_next_visit(graph, costs, end)
          visited[next_visit] = costs[next_visit]
          path_length = costs[next_visit]
          del costs[next_visit]

          # Threshold condition
          if thresh:
               if path_length > thresh:
                    return {end: 10e6}

          # Break condition
          if next_visit == end:
               break

          # Update neighbors if better score
          neighbors = graph[next_visit]["neighbors"]
          for n in neighbors:
               score = path_length + 1
               if score < scores[n]:
                    costs[n] = score
                    scores[n] = score
     return visited


# Parse heightmap into lists
heightmap = []
start_a = []
counter = 0
with open(filename) as f:
     for line in f:
          row = list(line.strip())
          for col_id, val in enumerate(row):
               if val == "S":
                    start_E = counter
                    start_a.append(counter)
                    row[col_id] = "a"
               if val == "E":
                    end = counter
                    row[col_id] = "z"
               if val == "a":
                    start_a.append(counter)

               counter += 1
          heightmap.append(row)


# Create graph from height map
graph = {}
counter = 0
with open(filename) as f:

     for row_id, row in enumerate(heightmap):

          for col_id, val in enumerate(row):

               # Create node
               graph[counter] = {"row": row_id, "col": col_id, "val": val}

               # Neighbors 
               neighbors = []
               if row_id > 0:
                    # Upwards
                    up = heightmap[row_id - 1][col_id]
                    if ord(up) <= ord(val) + 1:
                         neighbors.append(counter - len(row))
               if row_id < len(heightmap) - 1:
                    # Downwards
                    down = heightmap[row_id + 1][col_id]
                    if ord(down) <= ord(val) + 1:
                         neighbors.append(counter + len(row))
               if col_id > 0:
                    # Left
                    left = row[col_id - 1]
                    if ord(left) <= ord(val) + 1:
                         neighbors.append(counter - 1)

               if col_id < len(row) - 1:
                    # Right
                    right = row[col_id + 1]
                    if ord(right) <= ord(val) + 1:
                         neighbors.append(counter + 1)

               graph[counter]["neighbors"] = neighbors

               # Increment
               counter += 1

# Create inverse graph from height map
graph_inverse = {}
counter = 0
with open(filename) as f:

     for row_id, row in enumerate(heightmap):

          for col_id, val in enumerate(row):

               # Create node
               graph_inverse[counter] = {"row": row_id, "col": col_id, "val": val}

               # Neighbors 
               neighbors = []
               if row_id > 0:
                    # Upwards
                    up = heightmap[row_id - 1][col_id]
                    if ord(up) + 1 >= ord(val):
                         neighbors.append(counter - len(row))
               if row_id < len(heightmap) - 1:
                    # Downwards
                    down = heightmap[row_id + 1][col_id]
                    if ord(down) + 1 >= ord(val):
                         neighbors.append(counter + len(row))
               if col_id > 0:
                    # Left
                    left = row[col_id - 1]
                    if ord(left) +1 >= ord(val):
                         neighbors.append(counter - 1)

               if col_id < len(row) - 1:
                    # Right
                    right = row[col_id + 1]
                    if ord(right) + 1 >= ord(val):
                         neighbors.append(counter + 1)

               graph_inverse[counter]["neighbors"] = neighbors

               # Increment
               counter += 1

# PART 1

# The trick is to compute all shortest paths
# from 'E' to 'S', in order to prepare for part 2

costs = dijkstra(graph_inverse, end, start_E) # Using Dijkstra
# costs_S = a_star(graph, start_E, end) # Using A*

shortest = costs[start_E]
print(shortest)


# PART 2

# Get the shortest shortest path among
# paths from 'E' that end with 'a'

a_nodes = [
     n 
     for n 
     in graph 
     if graph[n]["val"] == "a"
     ]
shortest_a = min([
     costs[a] 
     for a 
     in a_nodes 
     if a in costs
     ])
print(shortest_a)


