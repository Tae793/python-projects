table = [
    ["alfie little", 24, 32, 5], 
    ["billy bob junior II", 22, 22, 53], 
    ["mark jones", 43, 54, 23], 
    ["king plonker", 23, 12, 32]
    ]
table[2][2] = 76

table[0].append(37)
table[1].append(99)
table[2].append(32)
table[3].append(42)

print(table)

print(table[0][1]+table[0][2]+table[0][3]+table[0][4]/4)