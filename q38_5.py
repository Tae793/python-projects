array = []
for i in range(6): 
    numbers = int(input("enter 6 number: "))
    array.append(numbers)

choice = input("do you want to see the average or the total of these numbers: ")

if choice == "average":
    sum = sum(array)/len(array)
    print(sum)
elif choice == "total":
    sum = sum(array)
    print(sum)
else:
    print("Invalid choice. Please enter 'average' or 'total'.")