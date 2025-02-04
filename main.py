import pygame
from PIL import Image, ImageSequence
import random

from texts import text_rules_lines, text_welcome_lines, text_balls_lines, questions

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Хто хоче стати мільйонером?")

# loading img
icon = pygame.image.load("images/chto-chhochet-stat-mllionerom.png")
bg_img = pygame.image.load("images/chto-chhochet-stat-mllionerom-bg.png")
logo_img = pygame.image.load("images/chto-chhochet-stat-mllionerom.png")

# loading rules img
rule_1 = pygame.image.load("images/rule-1.png")
rule_2 = pygame.image.load("images/rule-2.png")
rule_3 = pygame.image.load("images/rule-3.png")
rules_img = [rule_1, rule_2, rule_3]


# loading fonts
label_font_36 = pygame.font.Font("fonts/Montserrat/Montserrat-SemiBold.ttf", 36)
label_font_18 = pygame.font.Font("fonts/Montserrat/Montserrat-SemiBold.ttf", 18)

text_color = (255, 255, 255)
highlight_color = (245, 233, 66)
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
rules = False
run = True

def render_text_lines(texts, start_x: int, start_y: int, label_font, line_spacing:int=50, center: bool = False):
    """ Функція для рендерингу тексту з підсвіченими клавішами.
        Якщо center=True, текст центрується по ширині екрану. """
    for i, line_parts in enumerate(texts):
        y = start_y + i * line_spacing

        # Обчислюємо загальну ширину рядка для центрування
        total_width = sum(label_font.render(part, True, text_color).get_width() for part in line_parts)

        # Визначаємо початкову позицію x
        x = (SCREEN_WIDTH - total_width) // 2 if center else start_x

        for part in line_parts:
            # Визначаємо колір: якщо це клавіша — підсвічуємо
            color = highlight_color if part in ["a", "b", "c", "d", "n", "1", "2", "3", "ENTER", "q"] else text_color
            text_surface = label_font.render(part, True, color)
            screen.blit(text_surface, (x, y))
            x += text_surface.get_width()

def play_music(new_music):
    """Функція для відтворення музики, перевіряє чи вже відтворюється."""
    global current_music  # Використовуємо глобальну змінну
    if current_music != new_music:
        if current_music:
            current_music.stop()
        new_music.play(-1)
        current_music = new_music

# loading question
used_questions = []
def random_question(obj):
    if not obj:
        return None

    while True:
        random_idx = random.randint(0, len(obj) - 1)
        if random_idx not in used_questions:
            used_questions.append(random_idx)
            return obj[random_idx]

question = random_question(questions)
print(question)
question_label = label_font_18.render(question['question'], True, text_color)
answer_label = None
res_answer = False

while run:
    screen.fill((7, 8, 12))

    if frame_counter >= frame_delay:
        frame_index = (frame_index + 1) % len(gif_frames)
        frame_counter = 0

    if gameplay:
        screen.blit(bg_img, (0, 0))
        screen.blit(logo_img, (250, 60))
        current_x = 50

        for img in rules_img:
            screen.blit(img, (current_x, 15))
            current_x += 105

        render_text_lines(text_balls_lines, 650, 20, label_font_18, 20)

        screen.blit(question_label, (70, 405))

        for answer in question['answers']:  # Перебираємо кожну відповідь
            answer_text = answer['text']  # Отримуємо текст конкретної відповіді
            answer_label = label_font_18.render(answer_text, True, text_color)
            var_answer = answer_text.split(".")[0]  # Беремо першу частину (A, B, C, D)

            match var_answer:
                case "A":
                    screen.blit(answer_label, (78, 471))
                case "B":
                    screen.blit(answer_label, (78, 519))
                case "C":
                    screen.blit(answer_label, (436, 471))
                case "D":
                    screen.blit(answer_label, (436, 519))

        play_music(gameplay_music)
    elif rules:
        render_text_lines(text_rules_lines, 50, 50, label_font_18)
    else:
        screen.blit(gif_frames[frame_index], (0, 0))
        frame_counter += 1

        render_text_lines(text_welcome_lines, 50, 200, label_font_36, 50, center=True)

        play_music(welcome_music)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                gameplay = True
            elif event.key == pygame.K_q:
                rules = True



    pygame.display.update()

pygame.quit()
