from pprint import pprint

# filename = "input_sample.txt"
filename = "input.txt"


def dijkstra(graph, start):

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

          # Update neighbors if not visited
          neighbors = graph[next_visit]["neighbors"]
          for n in neighbors:
               if (
                    (n in costs) and
                    ((path_length + 1) < costs[n])
                    ):
                    costs[n] = path_length + 1

     return visited

# Parse heightmap into lists
heightmap = []
counter = 0
with open(filename) as f:
     for line in f:
          row = list(line.strip())
          for col_id, val in enumerate(row):
               if val == "S":
                    start = counter
                    row[col_id] = "a"
               if val == "E":
                    end = counter
                    row[col_id] = "z"

               counter += 1
          heightmap.append(row)


# Create graph from heigth map
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

costs = dijkstra(graph, start)
print(costs[end])