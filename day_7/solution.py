### PART 1


filename = "input.txt"


def change_dir(command:str, path:list) -> list:
     target = command[3:]
     if target == "..":
          path = path[:-1]
     else:
          path.append(target)
     return path


def get_size(dir_path:str, all_dirs:dict) -> int:
     directory = all_dirs[dir_path]
     size = directory["size"]
     children = directory["children"]
     if len(children) > 0:
          for child in children:
               #print("/" + child)
               size += get_size(child, all_dirs)
     return size


all_dirs = {}
path = []
to_update = False


with open(filename) as f:

     for line in f:
          line = line.strip()

          # Command
          if line.startswith("$ cd"):

               if to_update:
                    all_dirs["/".join(path)] = current_dir
                    to_update = False

               path = change_dir(line[2:], path)

          elif line.startswith("$ ls"):

               current_dir = {
                    "children": [],
                    "size": 0,
               }
               to_update = True

          # Directory contents
          else:
               if line.startswith("dir"):
                    current_dir["children"].append(
                         "/".join(path) + "/" + line[4:]
                         )
               else:
                    current_dir["size"] += int(line.split(" ")[0])

     # Do not forget the last directory
     if to_update:
          all_dirs["/".join(path)] = current_dir
          to_update = False               

#print([d for i, d in enumerate(all_dirs.items()) if i > len(all_dirs)-2])

# Compute the complete size of each directory
for path, directory in all_dirs.items():
     directory["complete_size"] = get_size(path, all_dirs)

# Sum directory sizes less than 100_000
counter = 0
for directory in all_dirs.values():
     if directory["complete_size"] <= 100_000:
          counter += directory["complete_size"]

print(f"Solution part 1 = {counter}")


### PART 2


# Compute available space
root = list(all_dirs.values())[0]
available = 70_000_000 - root["complete_size"]

# Find the smallest directory to delete 
# to end up with at least 30_000_000 empty space
minimum = 70_000_000
path = "/"
for dir_path, directory in all_dirs.items():
     if (
          (available + directory["complete_size"] >= 30_000_000) and 
          (directory["complete_size"] < minimum)
          ):
          to_delete = dir_path
          minimum = directory["complete_size"]

print(f"Solution part 2 = {all_dirs[to_delete]['complete_size']}")


