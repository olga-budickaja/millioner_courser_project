import pygame
from PIL import Image, ImageSequence
import random

from texts import text_rules_lines, text_welcome_lines, questions, text_win_lines, text_balls_lines

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
rule_4 = pygame.image.load("images/rule-4.png")
rule_1_end = pygame.image.load("images/rule-1_end.png")
rule_2_end = pygame.image.load("images/rule-2_end.png")
rule_3_end = pygame.image.load("images/rule-3_end.png")
rules_img = [rule_1, rule_2, rule_3, rule_4]


# loading fonts
label_font_36 = pygame.font.Font("fonts/Montserrat/Montserrat-SemiBold.ttf", 36)
label_font_18 = pygame.font.Font("fonts/Montserrat/Montserrat-SemiBold.ttf", 18)

text_color = (255, 255, 255)
highlight_color = (245, 233, 66)
correct_color = (3, 252, 57)
wrong_color = (252, 3, 36)
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

balls = []
total_ball = 0


# loading musics
pygame.mixer.init()
welcome_music = pygame.mixer.Sound("musics/hello.mp3")
gameplay_music = pygame.mixer.Sound("musics/play.mp3")
correct_music = pygame.mixer.Sound("musics/correct.mp3")
wrong_music = pygame.mixer.Sound("musics/wrong.mp3")
win_music = pygame.mixer.Sound("musics/win.mp3")
loose_music = pygame.mixer.Sound("musics/loose.mp3")
clock_music = pygame.mixer.Sound("musics/clock.mp3")
prompt_50_50_music = pygame.mixer.Sound("musics/50-50.mp3")
prompt_auditory_help_music = pygame.mixer.Sound("musics/aud_help.mp3")
# end_game_music = pygame.mixer.Sound("musics/end_game.mp3")

pygame.mixer.music.set_volume(0.1)
current_music = None

gameplay = False
rules = False
run = True

answer_result = False
current_answer = False
answer_selected = False
selected_answer_index = None
total_ball = 0

question_count = 0
max_questions = 10

# prompts
prompt_result_50_50 = False
prompt_auditory_help = False
prompt_friend_help = False
selected_wrong_idx = None

count_50_50 = 0
count_auditory_help = 0
count_friend_help = 0

def result_win(total: int):
    if total < 1000:
        return 0
    elif 1000 <= total < 8000:
        return 1000
    elif 8000 <= total < 125000:
        return 8000
    elif 125000 <= total < 1000000:
        return 125000

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
            color = highlight_color if part in ["a", "b", "c", "d", "n", "1", "2", "3", "ENTER", "q", "1 мілйон гривень", text_balls_lines[-1]] else text_color
            text_surface = label_font.render(part, True, color)
            screen.blit(text_surface, (x, y))
            x += text_surface.get_width()

def play_music(new_music):
    """Функція для відтворення музики, перевіряє чи вже відтворюється."""
    global current_music
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
question_label = label_font_18.render(question['question'], True, text_color)

def color_answer(idx: int, x: int, y: int, answer_result: bool, selected_answer_index: int):
    answer_obj = question['answers'][idx]
    answer_text = answer_obj['text']
    answer_result = answer_obj['result']

    if selected_answer_index is not None and selected_answer_index == idx:
        if answer_result:
            answer_label = label_font_18.render(answer_text, True, correct_color)
        else:
            answer_label = label_font_18.render(answer_text, True, wrong_color)
    else:
        answer_label = label_font_18.render(answer_text, True, text_color)

    screen.blit(answer_label, (x, y))

def enter_answers():
    for answer_obj in question['answers']:
        answer_text = answer_obj['text']
        answer_result = answer_obj['result']

        highlight_answer(answer_text, answer_result, selected_answer_index)

def highlight_answer(answer_text:str, answer_result:bool, selected_answer_index:int):
    var_answer = answer_text.split(".")[0]

    match var_answer:
        case "A":
            color_answer(0, 78, 471, answer_result, selected_answer_index)
        case "B":
            color_answer(1, 78, 519, answer_result, selected_answer_index)
        case "C":
            color_answer(2, 436, 471, answer_result, selected_answer_index)
        case "D":
            color_answer(3, 436, 519, answer_result, selected_answer_index)

def get_prompt(num_prompt: int, question):
    global selected_wrong_idx

    answers_wrong_idx = []

    for i, answer in enumerate(question['answers']):
        if answer['result']:
            if num_prompt == 1:
                highlight_answer(answer['text'], True, i)
        elif i not in answers_wrong_idx:
            answers_wrong_idx.append(i)

    if answers_wrong_idx and selected_wrong_idx is None:
        selected_wrong_idx = random.choice(answers_wrong_idx)

    if selected_wrong_idx is not None:
        random_wrong_text = question['answers'][selected_wrong_idx]['text']
        random_wrong_result = question['answers'][selected_wrong_idx]['result'] = True
        highlight_answer(random_wrong_text, random_wrong_result, selected_wrong_idx)


while run:
    screen.fill((7, 8, 12))

    events = pygame.event.get()

    if frame_counter >= frame_delay:
        frame_index = (frame_index + 1) % len(gif_frames)
        frame_counter = 0

    if gameplay:
        screen.blit(bg_img, (0, 0))
        screen.blit(logo_img, (250, 80))

        current_x = 50
        for img in rules_img:
            screen.blit(img, (current_x, 15))
            current_x += 105

        render_text_lines(text_balls_lines, 650, 20, label_font_18, 20)
        total_ball_label = label_font_18.render(str(total_ball), True, text_color)
        screen.blit(total_ball_label, (375, 30))

        screen.blit(question_label, (70, 405))

        enter_answers()

        play_music(gameplay_music)

        for event in events:
            if event.type == pygame.KEYDOWN and not answer_selected:
                if event.key == pygame.K_a:
                    current_answer = question['answers'][0]['result']
                    selected_answer_index = 0
                    answer_selected = True
                elif event.key == pygame.K_b:
                    current_answer = question['answers'][1]['result']
                    selected_answer_index = 1
                    answer_selected = True
                elif event.key == pygame.K_c:
                    current_answer = question['answers'][2]['result']
                    selected_answer_index = 2
                    answer_selected = True
                elif event.key == pygame.K_d:
                    current_answer = question['answers'][3]['result']
                    selected_answer_index = 3
                    answer_selected = True
                elif event.key == pygame.K_1:
                    if count_50_50 < 1:
                        prompt_result_50_50 = True
                        count_50_50 += 1
                elif event.key == pygame.K_2:
                    if count_auditory_help < 1:
                        prompt_auditory_help = True
                        count_auditory_help += 1
                elif event.key == pygame.K_3:
                    if count_friend_help < 1:
                        prompt_friend_help = True
                        count_friend_help += 1

        if answer_selected:
            prompt_result_50_50 = False
            prompt_auditory_help = False
            prompt_friend_help = False

            if current_answer:
                play_music(correct_music)
                balls.append(text_balls_lines[-1])

                total_ball = int(balls[-1])

                del text_balls_lines[-1]
            else:
                play_music(wrong_music)

            enter_answers()

            delay_time = pygame.time.get_ticks()
            while pygame.time.get_ticks() - delay_time < 4000:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

                pygame.display.update()

            question_count += 1
            if question_count >= max_questions:
                if len(text_balls_lines) > 0:
                    screen.blit(gif_frames[frame_index], (0, 0))
                    result = result_win(int(text_balls_lines[-1]))
                    print('balls: ', text_balls_lines[-1] if len(text_balls_lines)> 0 else 0)
                    text_loose_lines = [
                        ["Кінець гри!"],
                        ["Ви виграли"],
                        [f"{result} гривень"]
                    ]
                    result_text = text_loose_lines
                    play_music(loose_music)
                else:
                    screen.fill((7, 8, 12))
                    result_text = text_win_lines
                    play_music(win_music)

                render_text_lines(result_text, 50, 250, label_font_36, 50, center=True)
                pygame.display.update()
                pygame.time.delay(8000)
                run = False

            else:
                question = random_question(questions)
                question_label = label_font_18.render(question['question'], True, text_color)
                answer_selected = False
                selected_answer_index = None

        elif prompt_result_50_50:
            play_music(prompt_50_50_music)
            get_prompt(1, question)

            if rules_img:
                rules_img[0] = rule_1_end

            play_music(clock_music)

        elif prompt_auditory_help:
            play_music(prompt_auditory_help_music)

            pygame.time.delay(3000)
            get_prompt(2, question)

            if rules_img:
                rules_img[1] = rule_2_end

            play_music(clock_music)

        elif prompt_friend_help:
            play_music(clock_music)

            pygame.time.delay(3000)
            get_prompt(3, question)

            if rules_img:
                rules_img[2] = rule_3_end

    elif rules:
        render_text_lines(text_rules_lines, 50, 50, label_font_18)
    else:
        screen.blit(gif_frames[frame_index], (0, 0))
        frame_counter += 1

        render_text_lines(text_welcome_lines, 50, 200, label_font_36, 50, center=True)
        play_music(welcome_music)

    for event in events:
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                gameplay = True
            elif event.key == pygame.K_q:
                rules = True

    pygame.display.update()

pygame.quit()
