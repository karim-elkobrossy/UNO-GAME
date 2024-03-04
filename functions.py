from itertools import chain
import random
import pygame
#cards path may need to be updated depending on where files are saved
from sys import exit
from utils import *


def distribute_cards(players, deck):
    """ This assigns 7 random cards from a full deck to each player
    in a list of players that are playing. It works with a nested for
    loop that runs for each player of class player in a list. It
    takes a random choice from the full deck and appends the players
    'cardInPossession' parameter, as well as deleting the card from the
    list of full cards - Ciaran """
    for player in players:
        for i in range(1, 8):
            x = deck.available_deck.pop()
            player.cardsInPossession.append(x)


def set_players(deck):
    """ This function allows player input to set the number of players,
    it can be inserted into the distribute deck function - Ciaran"""
    players = []
    num_players = 4
    players.append(Player(0, "human"))
    for i in range(num_players-1):
        players.append(Player(i+1, "pc"))
    distribute_cards(players, deck)
    return players


def is_card_compatible(player_card, top_card, old_top_card, ghost_colour):
    if ghost_colour:
        if (player_card.colour == ghost_colour)\
                or (player_card.effect == top_card.effect):
            return True
    else:
        if old_top_card == top_card:
            if (player_card.number == top_card.number and player_card.number != 10)\
                    or (player_card.colour == top_card.colour and top_card.effect == "")\
                    or (player_card.effect != "" and player_card.effect == top_card.effect)\
                    or (top_card.effect != "" and player_card.colour == top_card.colour)\
                    or (top_card.effect == "" and player_card.colour == "any"):
                return True
            else:
                return False
        else:
            if (player_card.number == top_card.number and player_card.number != 10)\
                    or (player_card.colour == top_card.colour and top_card.effect == "")\
                    or (player_card.effect != "" and player_card.effect == top_card.effect)\
                    or (player_card.effect == top_card.effect and player_card.colour == "any")\
                    or (top_card.effect == "" and player_card.colour == "any"):
                return True
            else:
                return False


def counter_plus_card(player_card, top_card):
    if (top_card.effect == "plus2" or top_card.effect == "plus4")\
            and (player_card.effect == top_card.effect):
        return True
    else:
        return False

def reverse_checker(top_card, direction, old_top_card):

    if top_card.effect == 'reverse' and direction == -1:
        if top_card is old_top_card:
            direction = -1
        else:
            direction = 1
    elif top_card.effect == 'reverse' and direction == 1:
        if top_card is old_top_card:
            direction = 1
        else:
            direction = -1
    return direction

def block_checker(top_card, direction, old_top_card):
    if top_card == old_top_card:
        return 0
    if top_card.effect == 'block' and direction == 1:
        return 1
    elif top_card.effect == 'block' and direction == -1:
        return -1
    else:
        return 0

def plus2or4(top_card):
    if top_card.effect == "plus2":
        cardstoadd = 2
    elif top_card.effect == "plus4":
        cardstoadd = 4
    else:
        cardstoadd = 0
    return cardstoadd

def colourpicker(playerTurn, players):
    if players[playerTurn].p_type == 'pc':
        frequencyDict = {'red': 0, 'blue': 0, 'green': 0, 'yellow': 0}
        print(players[playerTurn].cardsInPossession)
        for card in players[playerTurn].cardsInPossession:
            try: frequencyDict[card.colour]+=1
            except: pass
        colour_choice = (max(frequencyDict, key=frequencyDict.get))
    else:
        colour_choice = colour_choice_screen()
    return colour_choice


def cardswap(playerTurn, deck, players, main_colour, top_card, flatten_list_cards, all_cards, dummy_card, y_player, x_player):
    if players[playerTurn].p_type != 'pc':        
        cardToSwap = player_input_card(players, players[playerTurn].cardsInPossession, top_card, main_colour, playerTurn, all_cards, dummy_card, is_swap=True)
        cardToSwap.move_to_discard(flatten_list_cards, top_card, main_colour)
        players[playerTurn].cardsInPossession.remove(cardToSwap)
        deck.discard_pile.append(cardToSwap)
        print(f"\n{cardToSwap} has been returned to the deck\n")
        card = pickup(deck, top_card, flatten_list_cards, playerTurn, players, main_colour, y_player, x_player)
        players[playerTurn].cardsInPossession.append(card)
        print(f"\nIt has been swapped for a {card}\n")
        print(f"Final cards for human: {players[playerTurn].cardsInPossession}")

def pickup(deck, top_card, flatten_list_cards, playerTurn, players, main_colour, y_player, x_player):
    try:
        card = deck.available_deck.pop()
    # When available_deck is empty, assign it to the discard_deck and shuffle it
    except:
        deck.available_deck = deck.discard_pile
        deck.discard_pile = []
        print("SHUFFLING DISCARD PILE")
        deck.shuffle()
        card = deck.available_deck.pop()
        for card in deck.available_deck:
            card.on_deck=False
    update_cards([card], 2)
    #initial coordinates of deck
    card.x, card.y = deck_coor
    all_cards_temp = flatten_list_cards + [top_card] + [card]
    dict_movement = {0: {"movement_x": 0, "movement_y": 1},
                     1: {"movement_x": -1, "movement_y": 0},
                     2: {"movement_x": 0, "movement_y": -1}, 
                     3: {"movement_x": 1, "movement_y": 0}}    

    while True:       
        if playerTurn == 0:
            if card.y >= y_player:
                return card
        elif playerTurn == 1:
            if card.x <= x_player:
                return card
        elif playerTurn == 2:
            if card.y <= y_player:
                return card
        elif playerTurn == 3:
            if card.x >= x_player:
                return card
        card.x += dict_movement[playerTurn]["movement_x"]
        card.y += dict_movement[playerTurn]["movement_y"]
        card.image_rect.move_ip(dict_movement[playerTurn]["movement_x"], dict_movement[playerTurn]["movement_y"])
        draw_window(main_colour)
        for card in all_cards_temp:
            card.draw(None, compatible_effect=False)
        pygame.display.update()
        #pygame.time.wait(10)


def player_turn_within_limit(playerTurn):
    if playerTurn == 4:
        playerTurn = 0
    elif playerTurn == -1:
        playerTurn = 3
    return playerTurn

'''This function takes player_cards, player_ID as input and alters the attributes of the card dynamically every
round to show them correctly on the screen. This funtion is capable of adjusting the dimensions of the cards based
on the number of cards available taking into consideration the constant screen size'''

def update_cards(player_cards, player_ID):
    for i, card in enumerate(player_cards):
        if player_ID != 0:
            img_file_name = '/final_Robin.jpg'
        else:
            img_file_name = cards_dict[card.__repr__()]
        num_cards = len(player_cards)
        screen_width, screen_height = pygame.display.get_surface().get_size()
        spacing = 5
        card_height = 105
        default_card_width = 72
        # Subtraction of 2*card height -> leaving beginning and ending distances
        # Calculation itself is dynamically altering the width of the card to suit the screen (In case there is a large number of cards, their width will be small)
        card_width = min(
            ((screen_width if player_ID % 2 == 0 else screen_height)-(2*card_height+spacing*num_cards))/num_cards, default_card_width)
        if player_ID % 2 == 0:
            hovering_height = -30 if player_ID == 0 else 30
            hovering_dir = 'y'
            rotate = False
        else:
            hovering_height = 30 if player_ID == 1 else -30
            hovering_dir = 'x'
            rotate = True
        var1 = i*(card_width+spacing) + card_height + hovering_height
        var2 = spacing
        if player_ID == 0:
			# 2*hovering_height in order to make it the same as the top cards
            x, y = var1-2*hovering_height, screen_height-var2-card_height
        elif player_ID == 1:
            y, x = var1, var2
        elif player_ID == 2:
            x, y = var1, var2
        elif player_ID == 3:
            y, x = var1-2*hovering_height, screen_width-var2-card_height
        card.update_variables(img_file_name, hovering_height, hovering_dir, rotate, pos=(x, y),
                                dim=(card_width, card_height), player_ID = player_ID)
    return player_cards


def Playerturn(playerTurn, deck, players, cardstoadd, top_card, old_top_card, ghost_colour, direction, main_colour, all_cards, dummy_card):
    """Code here is for the human player and their interaction with the game. The
        program checks the list of cards that the player has and pulls up any compatible.
        The player can then select which card they want to play. For the part where 
        the player doesn't have compatible cards, I have adapted Karim's AI code, but altered it
        to give more user friendly messages- Ciaran"""

    print(players[playerTurn].cardsInPossession)
    flatten_list_cards = list(chain.from_iterable(all_cards.values())) + [dummy_card]
    y_player = players[playerTurn].cardsInPossession[0].y
    x_player = players[playerTurn].cardsInPossession[0].x
    # Swaps a card and adds a new random one to the player's cards
    cardswap(playerTurn, deck, players, main_colour,top_card, flatten_list_cards, all_cards, dummy_card, y_player, x_player)
    all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
    counter_cards = []
    compatible_cards = []
    print(f"Top card initial: {top_card}")
    for card in (players[playerTurn].cardsInPossession):
        if counter_plus_card(card, top_card):
            counter_cards.append(card)
    if not counter_cards:
        if cardstoadd:
            """If player can't counter, needs to add cards from plus 2 or plus 4"""
            for _ in range(cardstoadd):
                card = pickup(deck, top_card, flatten_list_cards,playerTurn, players, main_colour, y_player, x_player)
                players[playerTurn].cardsInPossession.append(card)
                print(
                    f"\nThe plus {top_card} has caused you to pick up {card}!\n")
                cardstoadd = 0            
            """Loop for picking cards up ends here"""
        for card in (players[playerTurn].cardsInPossession):
            if is_card_compatible(card, top_card, old_top_card, ghost_colour):
                compatible_cards.append(card)
        if not compatible_cards:
            print("No cards available to play! You'll have to pick up")
            card = pickup(deck, top_card, flatten_list_cards,
                          playerTurn, players, main_colour, y_player, x_player)
            players[playerTurn].cardsInPossession.append(card)
            print(f"\nYou picked up a {card}\n")
            # If compatible card, add it directly to discard pile
            if is_card_compatible(card, top_card, old_top_card, ghost_colour):
                cardToPlay = player_input_card(players, [card], old_top_card, main_colour, playerTurn, all_cards, dummy_card, is_swap=False)
                print("\nThe card will be added to the pile\n")
                if cardToPlay is not None:
                    deck.discard_pile.append(top_card)
                    players[playerTurn].cardsInPossession.remove(cardToPlay)
                    all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
                    top_card = cardToPlay
                return top_card, None, cardstoadd, ghost_colour
            else:
                print(
                    "\nThe card you picked up was not compatible and has been added to your deck\n")
                print(
                    f"Final cards in possession already: {players[playerTurn].cardsInPossession}")
                print(f"Top card then: {top_card}")
            return top_card, None, cardstoadd, ghost_colour
        else:
            compatible_cards = set(compatible_cards)
            compatible_cards = list(compatible_cards)
            """List of compatible cards is converted to a set and then back to a list to remove duplicate
            cards that satisfy more than one condition of is_card_compatible - Ciaran"""
            print("\nYou have compatible cards!\n")
            for q, playable_card in enumerate(compatible_cards):
                print(f"{q+1}:  {playable_card}")
            cardToPlay = player_input_card(players, compatible_cards, top_card, main_colour, playerTurn, all_cards, dummy_card, is_swap=False)
            deck.discard_pile.append(top_card)
            players[playerTurn].cardsInPossession.remove(cardToPlay)
            all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
            FinalCard = cardToPlay
            if len(players[playerTurn].cardsInPossession) == 0:
                return FinalCard, players[playerTurn].ID, cardstoadd, ghost_colour            
            return FinalCard, None, cardstoadd, ghost_colour

    else:
        counter_cards = set(counter_cards)
        counter_cards = list(counter_cards)
        """List of counter cards is converted to a set and then back to a list to remove duplicate
        cards that might occur - Ciaran"""

        print("\nYou have to counter the last card to avoid picking up!\n")
        for q, playable_card in enumerate(counter_cards):
            print(f"{q+1}:  {playable_card}")        
        cardToPlay = player_input_card(players, counter_cards, top_card, main_colour, playerTurn, all_cards, dummy_card, is_swap=False)
        deck.discard_pile.append(top_card)
        players[playerTurn].cardsInPossession.remove(cardToPlay)
        all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
        FinalCard = cardToPlay
        print(f"Final player cards before declaring winner: {players[playerTurn].cardsInPossession}")
        if len(players[playerTurn].cardsInPossession) == 0:
            return FinalCard, players[playerTurn].ID, cardstoadd, ghost_colour
        else:
            return FinalCard, None, cardstoadd, ghost_colour


def AIturn(playerTurn, deck, players, cardstoadd, top_card, old_top_card, ghost_colour, direction, main_colour, all_cards, dummy_card):
    flatten_list_cards = list(chain.from_iterable(all_cards.values())) + [dummy_card]
    #cardswap(playerTurn,deck,players, top_card)
    compatible_cards = []
    counter_cards = []
    y_player = players[playerTurn].cardsInPossession[0].y
    x_player = players[playerTurn].cardsInPossession[0].x
    print(f"Top card initial: {top_card}")
    for card in (players[playerTurn].cardsInPossession):
        if counter_plus_card(card, top_card):
            counter_cards.append(card)
    if not counter_cards:
        if cardstoadd:
            """If player can't counter, needs to add cards from plus 2 or plus 4"""
            for _ in range(cardstoadd):
                card = pickup(deck, top_card, flatten_list_cards, playerTurn, players, main_colour, y_player, x_player)
                players[playerTurn].cardsInPossession.append(card)
                print(
                    f"\nThe plus {top_card} has caused the AI to pick up {card}!\n")
                cardstoadd = 0
            """Loop for picking cards up ends here"""            
        for card in (players[playerTurn].cardsInPossession):
            if is_card_compatible(card, top_card, old_top_card, ghost_colour):
                compatible_cards.append(card)
        if not compatible_cards:
            print("AI has no cards, picking up...")
            card = pickup(deck, top_card, flatten_list_cards, playerTurn, players, main_colour, y_player, x_player)
            print(f"\nAI picked up a {card}\n")
            # If compatible card, add it directly to discard pile
            if is_card_compatible(card, top_card, old_top_card, ghost_colour):
                deck.discard_pile.append(top_card)
                old_top_card = top_card
                top_card = card
            else:
                players[playerTurn].cardsInPossession.append(card)
                old_top_card = top_card
                print(
                    "\nThe card the AI picked up was not compatible and has been added to their deck\n")
            return top_card, None, cardstoadd, ghost_colour
        else:
            FinalCard, is_game_over = AIcardpicker(compatible_cards, players, playerTurn, direction, deck, top_card)
            if is_game_over:
                return FinalCard, players[playerTurn].ID, cardstoadd, ghost_colour
            return FinalCard, None, cardstoadd, ghost_colour
    else:
        counter_cards = set(counter_cards)
        counter_cards = list(counter_cards)
        """List of counter cards is converted to a set and then back to a list to remove duplicate
        cards that might occur - Ciaran"""

        print("\nYou have to counter the last card to avoid picking up!\n")
        for q, playable_card in enumerate(counter_cards):
            print(f"{q+1}:  {playable_card}")
        cardToPlay = random.choice(range(len(counter_cards)))
        deck.discard_pile.append(top_card)
        if counter_cards[int(cardToPlay)-1] in players[playerTurn].cardsInPossession:
            players[playerTurn].cardsInPossession.remove(counter_cards[int(cardToPlay)-1])
        FinalCard = counter_cards[int(cardToPlay)-1]
        if len(players[playerTurn].cardsInPossession) == 0:
            return FinalCard, players[playerTurn].ID, cardstoadd, ghost_colour
        else:
            return FinalCard, None, cardstoadd, ghost_colour

def player_input_card(players, compatible_cards, top_card, main_colour, playerTurn, all_cards, dummy_card, is_swap):
    all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
    if len(compatible_cards) == 0: return None
    if is_swap:
        PLAY_BACK = Button(image=None, pos=(425, 200),
                           text_input="SWAPPING", font=get_font(40), base_color="Red", hovering_color="Green")
    all_cards_temp = []
    for player in players:
        all_cards_temp.extend(player.cardsInPossession)
    all_cards_temp.extend([top_card, dummy_card])
    while True:
        # Move to the SCORE SCREEN
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(PLAY_MOUSE_POS):
                    play()
                # Check for pressed card and change self.is_played to true
                for card in all_cards_temp:
                    if card.player_ID == 0 and card.checkForInput(PLAY_MOUSE_POS):
                        if card in compatible_cards: return card        
        draw_window(main_colour)
        if is_swap:
            PLAY_BACK.update(WIN)
        for card in all_cards_temp:
            if card in compatible_cards:
                card.draw(PLAY_MOUSE_POS, compatible_effect=True)
            else:
                card.draw(PLAY_MOUSE_POS, compatible_effect=False)
        # This means that the player played the card that is now the top_card
        pygame.display.update()
        #pygame.time.wait(100)

def AIcardpicker(compatible_cards, players, playerTurn, direction, deck, top_card):
    compatible_cards = set(compatible_cards)
    compatible_cards = list(compatible_cards)
    third_priority = []
    second_priority = []
    first_priority = []

    """List of compatible cards is converted to a set and then back to a list to remove duplicate
    cards that satisfy more than one condition of is_card_compatible - Ciaran"""

    print("\nAI has compatible cards\n")
    for q, playable_card in enumerate(compatible_cards):
        print(f"{q+1}:  {playable_card}")
        if playable_card.priority == 3:
            third_priority.append(playable_card)
        elif playable_card.priority == 2:
            second_priority.append(playable_card)
        else:
            first_priority.append(playable_card)

    if len(players[player_turn_within_limit(playerTurn+direction)].cardsInPossession) <= 3:
        if second_priority:
            cardToPlay = random.choice(second_priority)
            deck.discard_pile.append(top_card)
        elif first_priority:
            cardToPlay = random.choice(first_priority)
            deck.discard_pile.append(top_card)
        else:
            cardToPlay = random.choice(third_priority)
            deck.discard_pile.append(top_card)

    else:
        if third_priority:
            cardToPlay = random.choice(third_priority)
            deck.discard_pile.append(top_card)
        elif second_priority:
            cardToPlay = random.choice(second_priority)
            deck.discard_pile.append(top_card)
        else:
            cardToPlay = random.choice(first_priority)
            deck.discard_pile.append(top_card)

    for q, card in enumerate(compatible_cards):
        if card == cardToPlay:
            cardToPlay = q

    if compatible_cards[cardToPlay] in players[playerTurn].cardsInPossession:
        players[playerTurn].cardsInPossession.remove(
            compatible_cards[cardToPlay])
    FinalCard = compatible_cards[cardToPlay]
    if len(players[playerTurn].cardsInPossession) == 0:
        is_game_over = True
        return FinalCard, is_game_over
    else:
        is_game_over = False
        return FinalCard, is_game_over


