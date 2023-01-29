import pygame, sys
from Score import Score
from functions import *
from itertools import chain
from utils import *

def game_over(winner, all_cards):
    deck = Deck()
    players = set_players(deck)
    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill(WHITE)
        WIN.blit(GAME_OVER_BACKGROUND, (0,0))
        WIN.blit(GAME_OVER, (300, 20))
        if winner != 0:
            SCORE_CARD = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 260),
                            text_input=f"Winner: Player {winner}" , font=get_font(35), base_color="Yellow")
            SCORE_CARD_1 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 320),
                            text_input=f"Your score: {len(all_cards[0])}" , font=get_font(30), base_color="Green")
            SCORE_CARD_2 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 370),
                            text_input=f"Player 1: {len(all_cards[1])}" , font=get_font(30), base_color="Blue")  
            SCORE_CARD_3 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 420),
                            text_input=f"Player 2: {len(all_cards[2])}" , font=get_font(30), base_color="Red")  
            SCORE_CARD_4 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 470),
                            text_input=f"Player 3: {len(all_cards[3])}" , font=get_font(30), base_color="Yellow")    
        else:
            SCORE_CARD = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 260),
                            text_input=f"You Won!" , font=get_font(35), base_color="Yellow") 
            SCORE_CARD_1 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 320),
                            text_input=f"Your score: {len(all_cards[0])}" , font=get_font(30), base_color="Green")
            SCORE_CARD_2 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 370),
                            text_input=f"Player 1: {len(all_cards[1])}" , font=get_font(30), base_color="Blue")  
            SCORE_CARD_3 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 420),
                            text_input=f"Player 2: {len(all_cards[2])}" , font=get_font(30), base_color="Red")  
            SCORE_CARD_4 = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 470),
                            text_input=f"Player 3: {len(all_cards[3])}" , font=get_font(30), base_color="Yellow")  
        MAIN_MENU = Button(image=pygame.image.load(f"{assets_path}/Play_Rect.png"), pos=(250, 550), 
                            text_input="MAIN MENU", font=get_font(50), base_color="Green", hovering_color="Blue")
        QUIT_BUTTON = Button(image=pygame.image.load(f"{assets_path}/Quit_Rect.png"), pos=(650, 550), 
                            text_input="QUIT", font=get_font(50), base_color="Red", hovering_color="Yellow")
                
        for button in [SCORE_CARD, SCORE_CARD_1, SCORE_CARD_2, SCORE_CARD_3, SCORE_CARD_4]:
            button.update(WIN)
        for button in [MAIN_MENU, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MAIN_MENU.checkForInput(MENU_MOUSE_POS):
                    main_menu()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

def play():
    # Initializing the game variables
    deck = Deck()
    players = set_players(deck)
    # Choose the top card randomly, then update it using the players' cards
    top_card = deck.available_deck.pop()
    #Dummy card representing draw pile
    dummy_card = deck.available_deck.pop()
    update_cards([dummy_card], 2)
    dummy_card.image = pygame.image.load(f'{cards_path}/final_Robin.jpg').convert_alpha()
    dummy_card.image = pygame.transform.scale(dummy_card.image, (dummy_card.width, dummy_card.height))
    dummy_card.x, dummy_card.y = dummy_coor
    direction = 1
    playerTurn = -1
    cardstoadd = 0
    ghost_colour = False
    old_top_card = False
    cardstoadd += plus2or4(top_card)
    all_cards = {}
    for player in players:
        all_cards[player.ID] = update_cards(player.cardsInPossession, player.ID)
    '''These lines are setting the values of the INITIAL top card'''
    update_cards([top_card], 2)
    screen_width, screen_height = pygame.display.get_surface().get_size()
    xc = round(screen_width*0.60)
    yc = screen_height//2
    top_card.x, top_card.y = xc, yc
    top_card.image_rect = top_card.image.get_rect(topleft=(xc, yc))
    main_colour = top_card.colour

    while True:
        print(f"NUMBER OF CARDS: {len(deck.available_deck)}")
        if direction == 1: playerTurn += 1
        else: playerTurn -= 1
        if playerTurn == 4: playerTurn = 0
        if playerTurn == -1: playerTurn = 3
        print(f"player_ID: {players[playerTurn].ID}")
        old_top_card = top_card
        # Move to the SCORE SCREEN
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        if players[playerTurn].p_type == 'pc':
            old_top_card = top_card
            top_card, winner, cardstoadd, ghost_colour = AIturn(playerTurn, deck, players, cardstoadd, top_card, old_top_card, ghost_colour, direction, main_colour, all_cards, dummy_card)
            if top_card is not old_top_card:
                if winner is not None: all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession + [top_card], players[playerTurn].ID)
                flatten_list_cards = list(chain.from_iterable(all_cards.values())) + [dummy_card]
                top_card.move_to_discard(flatten_list_cards, old_top_card, main_colour)
                #Remove top card from player's cards
                if winner is not None: all_cards[players[playerTurn].ID][:-1]
            all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
            if winner is not None: game_over(winner, all_cards)

        if players[playerTurn].p_type == 'human': 
            old_top_card = top_card
            top_card, winner, cardstoadd, ghost_colour = Playerturn(playerTurn, deck, players, cardstoadd, top_card, old_top_card, ghost_colour, direction, main_colour, all_cards, dummy_card)
            if top_card is not old_top_card:
                if winner is not None: all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession + [top_card], players[playerTurn].ID)
                flatten_list_cards = list(chain.from_iterable(all_cards.values())) + [dummy_card]
                top_card.move_to_discard(flatten_list_cards, old_top_card, main_colour)
                #Remove top card from player's cards
                if winner is not None: all_cards[players[playerTurn].ID][:-1]
            all_cards[players[playerTurn].ID] = update_cards(players[playerTurn].cardsInPossession, players[playerTurn].ID)
            if winner is not None: game_over(winner, all_cards)

        print(f"top_card: {top_card}")
        if top_card.effect == "plus2" and old_top_card is not top_card\
        or top_card.effect == "plus4" and old_top_card is not top_card:
            cardstoadd += plus2or4(top_card)
        else: cardstoadd = 0
        direction = reverse_checker(top_card, direction, old_top_card)
        playerTurn += block_checker(top_card, direction, old_top_card)
        playerTurn = player_turn_within_limit(playerTurn)
        if top_card is not old_top_card:
            if top_card.colour == "any":
                ghost_colour = colourpicker(playerTurn, players)
            else:
                ghost_colour = False
        if ghost_colour: main_colour = ghost_colour
        else:
            main_colour = top_card.colour       
        flatten_list_cards = list(chain.from_iterable(all_cards.values())) + [dummy_card]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()                
                
        print(f"MAIN COLOUR IS {main_colour}")
        draw_window(main_colour)
        for card in flatten_list_cards:
            card.draw(PLAY_MOUSE_POS, compatible_effect=False)
        # This means that the player played the card that is now the top_card
        #if top_card is not old_top_card: all_cards[player.ID].remove(top_card)
        pygame.display.update()
    #print(f"Winner is player: {winner}")

def main_menu():

    while True:
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        WIN.fill(WHITE)
        WIN.blit(MENU_BACKGROUND, (0, 0))
        LOGO = pygame.image.load(f'{assets_path}/UNO_Logo.svg.png')
        MENU_LOGO = pygame.transform.scale(LOGO, (300, 200))
        MENU_RECT = MENU_LOGO.get_rect(center=(440, 150))
        PLAY_BUTTON = Button(image=pygame.image.load(f'{assets_path}/Play_Rect.png'), pos=(450, 390),
                            text_input="PLAY", font=get_font(50), base_color="Green", hovering_color="Blue")
        QUIT_BUTTON = Button(image=pygame.image.load(f'{assets_path}/Quit_Rect.png'), pos=(450, 550),
                            text_input="QUIT", font=get_font(50), base_color="Red", hovering_color="Yellow")
        WIN.blit(MENU_LOGO, MENU_RECT)        
        WIN.blit(NOTTS_1, (300, 150))
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)      
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        
main_menu()
