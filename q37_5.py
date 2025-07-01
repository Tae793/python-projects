array=[]
for i in range (1,4):
    games=input("give me a game: ")
    array.append(games)
array.sort()
print(array)
index_number=int(input("which index number would you like to see: "))
print(array[index_number-1])