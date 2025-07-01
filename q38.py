array=[]
for i in range (1,5):
    movies=input("give me a film: ")
    array.append(movies)
print(array[:2])
array.remove(array[-1])
print(array)
print(array[0])