# Code originally generated by beta.openai.com and polished

# Initialize the input
stack1 = ["N", "B", "D", "T", "V", "G", "Z", "J"]
stack2 = ["S", "R", "M", "D", "W", "P", "F"]
stack3 = ["V", "C", "R", "S", "Z"]
stack4 = ["R", "T", "J", "Z", "P", "H", "G"]
stack5 = ["T", "C", "J", "N", "D", "Z", "Q", "F"]
stack6 = ["N", "V", "P", "W", "G", "S", "F", "M"]
stack7 = ["G", "C", "V", "B", "P", "Q"]
stack8 = ["Z", "B", "P", "N"]
stack9 = ["W", "P", "J"]

print("1:", stack1)
print("2:", stack2)
print("3:", stack3)
print("4:", stack4)
print("5:", stack5)
print("6:", stack6)
print("7:", stack7)
print("8:", stack8)
print("9:", stack9)
print()

# Parse the instructions line by line
with open("input.txt", "r") as f:
    for instruction in f.readlines():
        commands = instruction.split(" ")
        quantity = int(commands[1])
        from_stack = int(commands[3])
        to_stack = int(commands[5])

# Apply the instructions
        if from_stack == 1:
            from_stack_items = stack1[-quantity:]
            stack1 = stack1[:-quantity]
        elif from_stack == 2:
            from_stack_items = stack2[-quantity:]
            stack2 = stack2[:-quantity]
        elif from_stack == 3:
            from_stack_items = stack3[-quantity:]
            stack3 = stack3[:-quantity]
        elif from_stack == 4:
            from_stack_items = stack4[-quantity:]
            stack4 = stack4[:-quantity]
        elif from_stack == 5:
            from_stack_items = stack5[-quantity:]
            stack5 = stack5[:-quantity]
        elif from_stack == 6:
            from_stack_items = stack6[-quantity:]
            stack6 = stack6[:-quantity]
        elif from_stack == 7:
            from_stack_items = stack7[-quantity:]
            stack7 = stack7[:-quantity]
        elif from_stack == 8:
            from_stack_items = stack8[-quantity:]
            stack8 = stack8[:-quantity]
        elif from_stack == 9:
            from_stack_items = stack9[-quantity:]
            stack9 = stack9[:-quantity]
        
        from_stack_items.reverse()
        if to_stack == 1:
            stack1.extend(from_stack_items)
        elif to_stack == 2:
            stack2.extend(from_stack_items)
        elif to_stack == 3:
            stack3.extend(from_stack_items)
        elif to_stack == 4:
            stack4.extend(from_stack_items)
        elif to_stack == 5:
            stack5.extend(from_stack_items)
        elif to_stack == 6:
            stack6.extend(from_stack_items)
        elif to_stack == 7:
            stack7.extend(from_stack_items)
        elif to_stack == 8:
            stack8.extend(from_stack_items)
        elif to_stack == 9:
            stack9.extend(from_stack_items)

# Stacks results after applying the instructions
print("1:", stack1)
print("2:", stack2)
print("3:", stack3)
print("4:", stack4)
print("5:", stack5)
print("6:", stack6)
print("7:", stack7)
print("8:", stack8)
print("9:", stack9)