
from Button_1 import Button
import pygame
from Score import Score
from sys import exit
#Assests path may need to be updated depending on where files are saved
assets_path = 'Assests'

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
    if main_colour == 'red': Red.update(WIN)
    elif main_colour == 'green': Green.update(WIN)
    elif main_colour == 'blue': Blue.update(WIN)
    elif main_colour == 'yellow': Yellow.update(WIN)

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

#Function to blip up for 2 seocnds after a player chooses a colour
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

