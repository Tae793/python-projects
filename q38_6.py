genders = []
quit_typed = False
while quit_typed == False:
    gender = input("what is your gender: MALE, FEMALE, QUIT: ")
    genders.append(gender.upper())
    if gender.upper() == "QUIT":
        quit_typed = True
        count_males = genders.count("MALE")
        count_females = genders.count("FEMALE")
        print ("males = " + str(count_males))
        print ("females = " + str(count_females))
