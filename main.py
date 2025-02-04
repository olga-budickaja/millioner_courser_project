import pygame
from PIL import Image, ImageSequence

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Хто хоче стати мільйонером?")

# loading img
icon = pygame.image.load("images/chto-chhochet-stat-mllionerom.png")
bg_img = pygame.image.load("images/chto-chhochet-stat-mllionerom-bg.png")
logo_img = pygame.image.load("images/chto-chhochet-stat-mllionerom.png")

# loading fonts
label_font = pygame.font.Font("fonts/Montserrat/Montserrat-SemiBold.ttf", 36)
text_welcome_lines = [
    "Вітаємо у грі:",
    "Хто хоче стати мільйонером?",
    'Для початку гри натисніть',
    'ENTER'
]

text_color = (255, 255, 255)
start_y = 200
line_spacing = 50
fade_speed = 5

# loading gif
def load_gif_frames(gif_path):
    gif = Image.open(gif_path)
    frames = []

    for frame in ImageSequence.Iterator(gif):
        frame = frame.convert("RGBA")
        frame = frame.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
        mode = frame.mode
        size = frame.size
        data = frame.tobytes()
        pygame_image = pygame.image.fromstring(data, size, mode)
        frames.append(pygame_image)

    return frames

gif_frames = load_gif_frames("images/bg.gif")
frame_index = 0
frame_delay = 20
frame_counter = 0

# loading musics
pygame.mixer.init()
welcome_music = pygame.mixer.Sound("musics/hello.mp3")
gameplay_music = pygame.mixer.Sound("musics/play.mp3")
# end_game_music = pygame.mixer.Sound("musics/end_game.mp3")

pygame.mixer.music.set_volume(0.1)
current_music = None

gameplay = False
run = True

while run:
    screen.fill((7, 8, 12))
    screen.blit(gif_frames[frame_index], (0, 0))
    frame_counter += 1

    if frame_counter >= frame_delay:
        frame_index = (frame_index + 1) % len(gif_frames)
        frame_counter = 0

    if not gameplay:
        for i, line in enumerate(text_welcome_lines):
            text_surface = label_font.render(line, True, text_color)
            text_width = text_surface.get_width()
            x = (SCREEN_WIDTH - text_width) // 2
            screen.blit(text_surface, (x, start_y + i * line_spacing))

        if current_music != welcome_music:
            if current_music:
                current_music.stop()
            welcome_music.play(-1)
            current_music = welcome_music
    else:
        screen.blit(bg_img, (0, 0))
        screen.blit(logo_img, (250, 50))

        if current_music != gameplay_music:
            if current_music:
                current_music.stop()
            gameplay_music.play(-1)
            current_music = gameplay_music


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                gameplay = True

    pygame.display.update()

pygame.quit()
