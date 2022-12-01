filename = "input.txt"

podium = {
     1: 0,
     2: 0,
     3: 0,
}
counter = 0 

def update_podium(npodium:dict, new_rank:int, new_score:int,) -> dict:
     for i in range(len(podium.keys()), new_rank, -1):
          podium[i] = podium[i-1]
     podium[new_rank] = new_score
     return podium

with open(filename) as f:
     for line in f:

          # New elf
          if line in ['\n', '\r\n'] :

               # Check counter against top 3
               for i, (k,v) in enumerate(podium.items()):
                    if counter > v:
                         podium = update_podium(podium, k, counter)
                         break
               counter = 0

          # Accumulate     
          else:
               counter += int(line)

print(podium)
print(f"Total = {sum(podium.values())}")