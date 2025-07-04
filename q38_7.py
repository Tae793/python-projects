computer_games = []
loop = True

def print_games_list():
    print("current computer games in the list are: " + str(computer_games))

while loop:
    response = input("do you want to add, edit, delete a game, print all games from the list or exit?: ")
    if response.lower() == "add":
        game = input("what is the name of the game you want to add?: ")
        computer_games.append(game)
    elif response.lower() == "edit":
        print_games_list()
        game = input("what game would you like to edit?")
        new_game = input("what would you like to change the game to be: ")
        index = computer_games.index(game)
        computer_games[index] = new_game
    elif response.lower() == "delete":
        print_games_list()
        game = input("which game would you like to delete from the list?: ")
        computer_games.remove(game)
    elif response.lower() == "print":
        print(computer_games)
    elif response.lower() == "exit":
        print("exiting program")
        loop = False
    else:
        print("error that is not one of the options")