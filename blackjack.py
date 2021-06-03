"""
Blackjack (Code in Place Final Project)
------------------------------------------------------------
andrejenkino@gmail.com
------------------------------------------------------------
This program implements a basic text version of blackjack
for one player versus the computer. Instructions and rules 
can be found in the introduction() function definition.
"""

# Module used for generating RNG.
import random

# Constant for starting chips in the game.
PLAYER_CHIPS = 50

# Constant representing the size of the deck of cards.
DECK_SIZE = 52

# Deck of cards in the form of a dictionary.
deck = {
    1: ["A♧", 1],
    2: ["A♢", 1],
    3: ["A♡", 1],
    4: ["A♤", 1],
    5: ["2♧", 2],
    6: ["2♢", 2],
    7: ["2♡", 2],
    8: ["2♤", 2],
    9: ["3♧", 3],
    10: ["3♢", 3],
    11: ["3♡", 3],
    12: ["3♤", 3],
    13: ["4♧", 4],
    14: ["4♢", 4],
    15: ["4♡", 4],
    16: ["4♤", 4],
    17: ["5♧", 5],
    18: ["5♢", 5],
    19: ["5♡", 5],
    20: ["5♤", 5],
    21: ["6♧", 6],
    22: ["6♢", 6],
    23: ["6♡", 6],
    24: ["6♤", 6],
    25: ["7♧", 7],
    26: ["7♢", 7],
    27: ["7♡", 7],
    28: ["7♤", 7],
    29: ["8♧", 8],
    30: ["8♢", 8],
    31: ["8♡", 8],
    32: ["8♤", 8],
    33: ["9♧", 9],
    34: ["9♢", 9],
    35: ["9♡", 9],
    36: ["9♤", 9],
    37: ["10♧", 10],
    38: ["10♢", 10],
    39: ["10♡", 10],
    40: ["10♤", 10],
    41: ["J♧", 10],
    42: ["J♢", 10],
    43: ["J♡", 10],
    44: ["J♤", 10],
    45: ["Q♧", 10],
    46: ["Q♢", 10],
    47: ["Q♡", 10],
    48: ["Q♤", 10],
    49: ["K♧", 10],
    50: ["K♢", 10],
    51: ["K♡", 10],
    52: ["K♤", 10]
}

def main():
    # Welcomes and explains the game to the player.
    introduction()
    # Sets the amount of chips.
    current_chips = PLAYER_CHIPS
    # Sets the loop conditions for the game.
    while current_chips > 0:
        # Asks for player to make bet.
        current_bet = bet(current_chips)
        # Deals initial hands.
        house_hand, player_hand, cards_drawn = deal_cards()
        # Shows initial cards drawn.
        show_hand(house_hand, player_hand)
        # Checks if there is a blackjack.
        winner = check_winner(house_hand, player_hand)
        if winner == "blackjack":
            move = ""
        # If no blackjack, game goes on.
        else:
            move = player_action()
            # Player decides to hit.
            while move == "h":
                player_hand, cards_drawn = hit(player_hand, cards_drawn)
                # Checks if player busts while getting new cards.
                bust_check = hand_value(player_hand)
                if bust_check[1] > 21:
                    winner = check_winner(player_hand, house_hand)
                    break
                show_cards(player_hand)
                move = player_action()
            # Player is feeling lucky! Or counting cards, maybe?
            if move == "d":
                player_hand, cards_drawn = hit(player_hand, cards_drawn)               
            # Finally, this is the stay pick.
            else:
                pass
            # Player is done with interacting. House moves.
            house_hand, cards_drawn = house_action(house_hand, cards_drawn)
            winner = check_winner(house_hand, player_hand)
        # Match is over. Time to update the score and check results.
        current_chips = update_score(current_bet, current_chips, winner, move)
        show_score(house_hand, player_hand, winner, current_bet, move)
    # Player has no chips left.
    play_again()

def introduction():
    print("----------------------------------------")
    print("Let's play a game of Blackjack!")
    print("----------------------------------------")
    print("Do you want to see instructions on how to play?")
    instructions = input("Choose (Y)es or (N)o: ").lower()
    options = ["y","n"]
    # Makes sure player can only give a valid input.
    while instructions not in options:
        instructions = input("Choose (Y)es or (N)o: ").lower()
    print("")
    if instructions == options[0]:
        print("""Card    Value
---------------
Ace     1 or 11
2-10    2-10
J,Q,K   10

Rules
------------------------------------------------------------
The goal of blackjack is to get to 21 or as close to 21 as
possible without going over. Player gets two cards facing up
and the house gets two cards, with only one facing up. Then 
the player decides to either Hit to get other cards, Double
to get only one more card an double the bet or Stay to keep 
the cards at hand. After the player calls Stay, then the
house reveals the other card and Hits till it gets to 17.
Ace value always favors the player.

Victory Conditions
------------------------------------------------------------
1. If the player gets dealt an initial blackjack (21 points)
the player wins double the bet.
2. If the player exceeds 21 points, the house wins, even if
the house busts.
3. If the house exceeds 21 points and the player doesn't,
the player wins.
4. If player and house don't bust, the winner is the one
with the higher sum of cards.
5. If both the player and the house have the same points, 
it's a tie and no one wins.""")
        print("")
    elif instructions == options[1]:
        print("Alright! Good luck!")
        print("")

def bet(current_chips):
    # Shows amount of chips held.
    print("You have", current_chips, "chips.")
    # Makes sure player can only give a valid input.
    while True:
        try:
            chips = int(input("How many chips would you like to bet? "))
            while chips <= 0 or chips > current_chips:
                chips = int(input("How many chips would you like to bet? "))
            return chips
        except ValueError:
            continue
 
def deal_cards():
    # This function makes sure four unique cards are drawn.
    cards_drawn = []
    # Generates the list with the initial cards.
    for i in range(4):
        cards_drawn.append(random.randint(1, DECK_SIZE))
    # Ensures there are no duplicate values.
    set_size = list(set(cards_drawn))
    while len(set_size) != len(cards_drawn):
        difference = len(cards_drawn) - len(set_size)
        cards_drawn = set_size
        for i in range(difference):
            cards_drawn.append(random.randint(1, DECK_SIZE))
        set_size = list(set(cards_drawn))
    # Cards get their initial assignment.
    house_hand, player_hand = [],[]
    for i in range(2):
        house_hand.append(cards_drawn[i])
        player_hand.append(cards_drawn[i+2])
    return house_hand, player_hand, cards_drawn

def check_winner(house_hand, player_hand):
    # Hands get checked.
    house = hand_value(house_hand)
    player = hand_value(player_hand)
    # Checks winning conditions with current hands.
    winner = ""
    if player[0] == 2 and house[0] == 2 and player[1] == 21:
        winner = "blackjack"
    elif player[1] > 21:
        winner = "house"
    elif player[1] <= 21 and house[1] > 21:
        winner = "player"
    elif player[1] <= 21 and house[1] <= 21:
        if player[1] > house[1]:
            winner = "player"
        elif player[1] == house[1]:
            winner = "tie"
        elif player[1] < house[1]:
            winner = "house"
    return winner

def hand_value(input):
    # Initializes output data.
    sum = 0
    ace_count = 0
    hand_output = []
    length = len(input)
    # Creates the aces list for ace check.
    aces = []
    for i in range(4):
        aces.append(i+1)
    # Calculates hand sum and ace count.
    for i in input:
        sum += deck[i][1]
        if i in aces:
            ace_count += 1
    # Corrects hand sum based on ace value.
    if ace_count != 0:
        if sum <= 11:
            sum += 10
    # Assembles output values.
    hand_output.append(length)
    hand_output.append(sum)
    return hand_output

def player_action():
    print("What is your move, player?")
    move = ""
    options = ["h","d","s"]
    # Gets player decision. Makes sure player can only give a valid input.
    while move not in options:
        move = input("Choose (H)it to get another card, (D)ouble to double your bet or (S)tay to keep your current cards: ").lower()
    return move

def hit(hand, cards_drawn):
    # Adds a new card to the player hand and lists it with the cards drawn
    new_card = random.randint(1, DECK_SIZE)
    # Makes sure the card is really new.
    while new_card in cards_drawn:
        new_card = random.randint(1, DECK_SIZE)
    hand.append(new_card)
    cards_drawn.append(new_card)
    return hand, cards_drawn

def house_action(house_hand, cards_drawn):
    # Makes the house draw cards till 17.
    hand = hand_value(house_hand)
    while hand[1] < 17:
        house_hand, cards_drawn = hit(house_hand, cards_drawn)
        hand = hand_value(house_hand)
    return house_hand, cards_drawn

def update_score(current_bet, current_chips, winner, move):
    # Gets winner results and bet values and updates the score.
    winning_conditions = ["blackjack","house","tie", "player"]
    if winner == winning_conditions[0]:
        current_bet *= 2
    elif winner == winning_conditions[1]:
        current_bet = -current_bet
    elif winner == winning_conditions[2]:
        current_bet = 0
    elif winner == winning_conditions[3] and move == "d":
        current_bet *= 2
    else:
        pass
    current_chips += current_bet
    return current_chips

def show_hand(house_hand, player_hand):
    # A fluff. Nothing else.
    house_cards(house_hand)
    print("⇧⇧ House hand ⇧⇧")
    print("       ×")
    print("⇩⇩ Player hand ⇩⇩")
    show_cards(player_hand)

def show_cards(hand):
    # The structure the ASCII art uses to show the cards.
    hand_size = len(hand)
    print(hand_size*'┌─────┐')
    for i in hand:
        if len(str(deck[i][0])) == 3:
            print("│" + str(deck[i][0]) + "  │", end= "")
        else:
            print("│" + str(deck[i][0]) + "   │", end= "")
    print("")
    print(hand_size*"│     │")
    for i in hand:
        if len(str(deck[i][0])) == 3:
            print("│  " + str(deck[i][0]) + "│", end= "")
        else:
            print("│   " + str(deck[i][0]) + "│", end= "")
    print("")
    print(hand_size*"└─────┘")

def house_cards(hand):
    # Same structure as before, but hiding the first card.
    hand_size = len(hand)
    print(hand_size*'┌─────┐')
    for index, item in enumerate(hand):
        if not index:
            print("│??   │", end= "")
        elif len(str(deck[item][0])) == 3:
            print("│" + str(deck[item][0]) + "  │", end= "")
        else:
            print("│" + str(deck[item][0]) + "   │", end= "")
    print("")
    print(hand_size*"│     │")
    for index, item in enumerate(hand):
        if not index:
            print("│   ??│", end= "")
        elif len(str(deck[item][0])) == 3:
            print("│  " + str(deck[item][0]) + "│", end= "")
        else:
            print("│   " + str(deck[item][0]) + "│", end= "")
    print("")
    print(hand_size*"└─────┘")

def show_score(house_hand, player_hand, winner, current_bet, move):
    # Shows results of the match. With a fluff, ofc.
    print ("------------------------------------------------------------")
    show_cards(house_hand)
    print("⇧⇧ House hand ⇧⇧")
    print("       ×")
    print("⇩⇩ Player hand ⇩⇩")
    show_cards(player_hand)
    winning_conditions = ["blackjack","house","tie", "player"]
    if winner == winning_conditions[0]:
        print("\o/ YOU GOT A BLACKJACK! \o/")
        print("The house got", hand_value(house_hand)[1], "points.")
        print("You got", hand_value(player_hand)[1], "points.")
        print("You win", current_bet, "chips!")
    elif winner == winning_conditions[1]:
        print("Not this time, player...")
        print("The house got", hand_value(house_hand)[1], "points.")
        print("You got", hand_value(player_hand)[1], "points.")
        print("You lose", current_bet, "chips.")
    elif winner == winning_conditions[2]:
        print("What are the odds?!? It's a tie.")
        print("The house got", hand_value(house_hand)[1], "points.")
        print("You got", hand_value(player_hand)[1], "points.")
        print("You get your chips back.")
    elif winner == winning_conditions[3] and move == "d":
        print("Hooray! The risk was worth it!")
        print("The house got", hand_value(house_hand)[1], "points.")
        print("You got", hand_value(player_hand)[1], "points.")
        print("You win", current_bet, "chips!")
    else:
        print("Congratulations! You win this one!")
        print("The house got", hand_value(house_hand)[1], "points.")
        print("You got", hand_value(player_hand)[1], "points.")
        print("You win", current_bet, "chips.")
    print ("------------------------------------------------------------")
    print("")

def play_again():
    print("Do you want to play again?")
    instructions = input("Choose (Y)es or (N)o: ").lower()
    options = ["y","n"]
    # Asks if player wants to play again. Makes sure player can only give a valid input.
    while instructions not in options:
        instructions = input("Choose (Y)es or (N)o: ").lower()
    print("")
    if instructions == options[0]:
        main()
    else:
        pass

if __name__ == "__main__":
    main()