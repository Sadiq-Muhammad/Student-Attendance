from screeninfo import get_monitors
from customtkinter import CTkFont

screen = get_monitors()[0]

SCREEN_WIDTH = screen.width
SCREEN_HEIGHT = screen.height

WIN_WIDTH = int(SCREEN_WIDTH * 0.5)
WIN_HEIGHT = int(SCREEN_HEIGHT * 0.5)

def Arial(size: int):
    return CTkFont(family="Arial", size=size, weight="normal")