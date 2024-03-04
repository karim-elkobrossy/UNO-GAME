import json
import pygame
import random
from numpy import polyfit
from sys import exit
#Assests path may need to be updated depending on where files are saved
assets_path = 'Assests'
cards_path = 'Assests/UNO_CARDS'

# Load the JSON data from the file
with open('cards.json', 'r') as file:
    cards_dict = json.load(file)

pygame.init()
WIN = pygame.display.set_mode((900, 700))
pygame.display.set_caption('UNO')
WHITE = (255, 255, 255)
TABLE_TOP = pygame.image.load(f"{assets_path}/Table_4.png").convert_alpha()
BACKGROUND = pygame.transform.scale(TABLE_TOP, (1100, 800))
UNO_LOGO = TABLE_TOP = pygame.image.load(
    f'{assets_path}/UNO_Logo.png').convert_alpha()
EMBLEM = pygame.transform.scale(UNO_LOGO, (175, 140))
NOTTS = pygame.image.load(f'{assets_path}/Notts.png').convert_alpha()
NOTTS_1 = pygame.transform.rotate(NOTTS, 20)
EMBLEM_1 = pygame.image.load(
    f'{assets_path}/Game-Over-Clipart-PNG.png').convert_alpha()
GAME_OVER = pygame.transform.scale(EMBLEM_1, (400, 200))
SCORE_BOX = f"{assets_path}/Score_Rect.png"
MENU_BACKGROUND = pygame.image.load(f'{assets_path}/Uno-1.jpg').convert_alpha()
MENU_BACKGROUND = pygame.transform.scale(MENU_BACKGROUND, (900, 700))
GAME_OVER_BACKGROUND = pygame.image.load(f'{assets_path}/Gameover_image.jpg').convert_alpha()
GAME_OVER_BACKGROUND = pygame.transform.scale(GAME_OVER_BACKGROUND, (900, 700))
screen_width, screen_height = pygame.display.get_surface().get_size()
deck_coor = screen_width//4, screen_height//2
dummy_coor = deck_coor


def get_font(size):
    return pygame.font.Font(f'{assets_path}/Cabin-Bold.ttf', size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)
               

PLAY_BUTTON = Button(image=pygame.image.load(f'{assets_path}/Play_Rect.png'), pos=(450, 390),
                     text_input="PLAY", font=get_font(50), base_color="Green", hovering_color="Blue")
QUIT_BUTTON = Button(image=pygame.image.load(f'{assets_path}/Quit_Rect.png'), pos=(450, 550),
                     text_input="QUIT", font=get_font(50), base_color="Red", hovering_color="Yellow")


def draw_window(main_colour):
    WIN.fill(WHITE)
    WIN.blit(BACKGROUND, (-100, -50))
    WIN.blit(EMBLEM, (340, 290))
    colour_x_coor = 425
    colour_y_coor = 450
    font_size = 25
    Red = Button(image=None, pos=(colour_x_coor, colour_y_coor),
                 text_input="RED", font=get_font(font_size), base_color="Red", hovering_color="Red")
    Green = Button(image=None, pos=(colour_x_coor, colour_y_coor),
                   text_input="GREEN", font=get_font(font_size), base_color="Green", hovering_color="Green")
    Blue = Button(image=None, pos=(colour_x_coor, colour_y_coor),
                  text_input="BLUE", font=get_font(font_size), base_color="Blue", hovering_color="Blue")
    Yellow = Button(image=None, pos=(colour_x_coor, colour_y_coor),
                    text_input="YELLOW", font=get_font(font_size), base_color="Yellow", hovering_color="Yellow")
    if main_colour == 'red':
        Red.update(WIN)
    elif main_colour == 'green':
        Green.update(WIN)
    elif main_colour == 'blue':
        Blue.update(WIN)
    elif main_colour == 'yellow':
        Yellow.update(WIN)


def colour_choice_screen():
    Choosing = True

    while Choosing:
        RED = pygame.image.load(f'{assets_path}/RED_Rect.png')
        RED = pygame.transform.scale(RED, (175, 200))
        GREEN = pygame.image.load(f'{assets_path}/GREEN_Rect.png')
        GREEN = pygame.transform.scale(GREEN, (175, 200))
        BLUE = pygame.image.load(f'{assets_path}/BLUE_Rect.png')
        BLUE = pygame.transform.scale(BLUE, (175, 200))
        YELLOW = pygame.image.load(f'{assets_path}/YELLOW_Rect.png')
        YELLOW = pygame.transform.scale(YELLOW, (175, 200))
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        TEXT = Score(image=pygame.image.load(f'{assets_path}/Options_Rect.png'), pos=(450, 175),
                     text_input="Choose a colour", font=get_font(70), base_color="Black")
        RED_OPTION = Button(image=RED, pos=(150, 420),
                            text_input=" ", font=get_font(50), base_color="Red", hovering_color="white")
        GREEN_OPTION = Button(image=GREEN, pos=(350, 420),
                              text_input=" ", font=get_font(50), base_color="Green", hovering_color="white")
        BLUE_OPTION = Button(image=BLUE, pos=(550, 420),
                             text_input=" ", font=get_font(50), base_color="Blue", hovering_color="white")
        YELLOW_OPTION = Button(image=YELLOW, pos=(750, 420),
                               text_input=" ", font=get_font(50), base_color="Yellow", hovering_color="white")
        for button in [RED_OPTION, GREEN_OPTION, BLUE_OPTION, YELLOW_OPTION]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        for button in [TEXT]:
            button.update(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if RED_OPTION.checkForInput(MENU_MOUSE_POS):
                    return "red"
                if GREEN_OPTION.checkForInput(MENU_MOUSE_POS):
                    return "green"
                if BLUE_OPTION.checkForInput(MENU_MOUSE_POS):
                    return "blue"
                if YELLOW_OPTION.checkForInput(MENU_MOUSE_POS):
                    return "yellow"
        pygame.display.update()

# Function to blip up for 2 seocnds after a player chooses a colour


def message_display(text):
    active = True

    while active:
        Colour_choice = Score(image=pygame.image.load(SCORE_BOX), pos=(450, 450),
                              text_input="f'{player.ID}' has chosen: f'{card.colour}' ", font=get_font(25), base_color="Black")
        for button in [Colour_choice]:
            button.update(WIN)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
    pygame.time.wait(2000)
    pygame.display.update()
    active = False


class Card():
    def __init__(self, number, colour, priority, effect=""):
        self.number = number
        self.colour = colour
        self.effect = effect
        # This is a history of whether a card has been hovered upwards or not
        self.hovering_hist = False
        # This variable determines whether the card is being played or not (useful for doing the animation)
        self.is_played = False
        self.on_deck = False
        self.priority = priority

    def __repr__(self):
        return f"{self.number}->{self.colour}->{self.effect}"

    def update_variables(self, img_file_name, hovering_height, hovering_dir, rotate, pos, dim, player_ID):
        self.img_file_name = img_file_name
        # Only load the image when you want to use instead of initializing it with the class due to memory efficiency
        self.image = pygame.image.load(
            f'{cards_path}/{img_file_name}').convert_alpha()
        self.hovering_height = hovering_height
        self.hovering_dir = hovering_dir
        self.player_ID = player_ID
        self.rotate = rotate
        # These dimensions are for scaling the card (New dimension after scaling)
        self.width, self.height = dim
        # These dimensions are the coordinates of the card initially and will be altered later on using draw method
        if not self.is_played and not self.on_deck:
            self.x, self.y = pos
        self.image = pygame.transform.scale(
            self.image, (self.width, self.height))
        if self.rotate:
            self.image = pygame.transform.rotate(self.image, -90)
        self.image_rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, mouse_pos, compatible_effect):
        if not compatible_effect:
            self.image_rect = self.image.get_rect(topleft=(self.x, self.y))
        else:
            if self.player_ID == 0 and mouse_pos is not None:
                if self.checkForInput(mouse_pos):
                    hovering_dist = self.hovering_height
                    self.hovering_hist = True
                # If no hovering -> check if it was hovered before in order to retain it to its initial place
                else:
                    if self.hovering_hist:
                        hovering_dist = -self.hovering_height
                        self.hovering_hist = False
                    else:
                        hovering_dist = 0
                if self.hovering_dir == 'y':
                    self.image_rect = self.image.get_rect(
                        topleft=(self.x, self.y+hovering_dist))
                else:
                    self.image_rect = self.image.get_rect(
                        topleft=(self.x+hovering_dist, self.y))
        WIN.blit(self.image, self.image_rect)

    def checkForInput(self, position):
        _, screen_height = pygame.display.get_surface().get_size()
        if position[0] in range(self.image_rect.left, self.image_rect.right) and position[1] in range(self.image_rect.top, screen_height):
            return True
        return False

    def move_to_discard(self, all_cards, old_top_card, main_colour):
        screen_width, screen_height = pygame.display.get_surface().get_size()
        xc = round(screen_width*0.60)
        yc = screen_height//2
        close_by = False
        old_top_card.x, old_top_card.y = xc, yc
        all_cards_temp = all_cards + [old_top_card] + [self]
        self.img_file_name = cards_dict[self.__repr__()]
        self.image = pygame.image.load(
            f'{cards_path}/{self.img_file_name}').convert_alpha()
        self.image = pygame.transform.scale(self.image, (72, 105))
        # If within boundary of the center, then make it exactly at the center
        self.is_played = False
        self.on_deck = True
        x = [xc, self.x]
        y = [yc, self.y]
        slope, intercept = polyfit(x, y, 1)
        is_x_dist_bigger = True if abs(xc-self.x) > abs(yc-self.y) else False
        if is_x_dist_bigger:
            movement_x = (xc-self.x)/100
        else:
            movement_y = (yc-self.y)/100
        is_right = xc > self.x

        while True:
            PLAY_MOUSE_POS = pygame.mouse.get_pos()
            if is_x_dist_bigger:
                self.x += movement_x
                old_y = self.y
                self.y = slope*self.x + intercept
                movement_y = self.y-old_y
            else:
                self.y += movement_y
                old_x = self.x
                self.x = (self.y-intercept)/slope
                movement_x = self.x-old_x
            if is_right and self.x >= xc:
                self.image_rect = self.image.get_rect(topleft=(xc, yc))
                return
            if not is_right and xc >= self.x:
                self.image_rect = self.image.get_rect(topleft=(xc, yc))
                return
            self.image_rect.move_ip(movement_x, movement_y)
            draw_window(main_colour)
            for card in all_cards_temp:
                card.draw(None, compatible_effect=False)
            pygame.display.update()
            pygame.time.wait(10)

class Deck():
    # available_deck is the full deck at the beginning of the game
    available_deck = []
    # Keeping track of the discarded pile for implementing the AI later
    discard_pile = []

    def __init__(self):
        self.build()
        print(f"deck: {len(self.available_deck)}")
        # Initial deck shuffle
        self.shuffle()

    def build(self):
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        colours = ['red', 'green', 'blue', 'yellow']
        effects = ['plus2', 'block', 'reverse']
        wilds = ['anycolour', 'plus4']
        third_priority = 3
        second_priority = 2
        first_priority = 1
        """ The method build_deck is designed to return a list containing all 108
        cards used in UNO. The full deck consists of 4 colours with 2 copies of
        1-9 cards, 1 copy of 0 cards, 2 copies of reverse cards, 2 copies of
        plus 2 cards, 2 copies of block cards for each colour. It also contains
        4 draw 4 cards and 4 colour switch cards, independent of colour.

        The nested for loops below are designed to add an object of type card
        to a list bsed on the list of possible parameters above - Ciaran"""
        # 4 (coloured) cars per number - Karim
        self.available_deck.extend([Card(number, colour, third_priority)
                                   for number in numbers for colour in colours])
        # Another 4 (coloured) cars per number excluding 0 - Karim
        self.available_deck.extend([Card(number, colour, third_priority)
                                   for number in numbers[1:] for colour in colours])
        # 10 is used here as a placeholder as the effect cards don't have numbers, only colours - Ciaran
        self.available_deck.extend(
            [Card(10, colour, second_priority, effect) for _ in range(2) for colour in colours for effect in effects])
        # extend list with four of each wild card, these have any colour and no number - Ciaran
        self.available_deck.extend([Card(10, 'any', first_priority, wild)
                                   for _ in range(4) for wild in wilds])

    def shuffle(self):
        random.shuffle(self.available_deck)


class Player():
    def __init__(self, ID, p_type):
        self.cardsInPossession = []
        self.ID = ID
        self.p_type = p_type
        # Default status until declared win
        self.status = "lose"

    def __repr__(self):
        return f"{self.p_type}->player_ID: {self.ID}"


class Score():
	def __init__(self, image, pos, text_input, font, base_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color = base_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False



