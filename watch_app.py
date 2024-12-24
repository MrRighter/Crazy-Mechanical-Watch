from datetime import datetime
from sys import exit
from base64 import b64decode
from io import BytesIO
import math

import pygame
import pytz

from class_PicButton import PicButton
from string_data_values import *


# инициализация pygame; создание окна с именем
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("CRAZY MECHANICAL WATCH")
WIDTH, HEIGHT = pygame.display.get_surface().get_size()  # берём ширину и высоту окна как константы

current_theme = True  # по умолчанию светлая тема
bg_color_theme = "#F2F2F2"  # по умолчанию светлый - становится тёмным
font_text_color = "#323232"  # по умолчанию тёмный - становится светлым
font_city_color = "#F2B800"  # по умолчанию жёлтый - становится фиолетовым

# берём закодированный шрифт и создаём необходимые переменные
decoded_font = b64decode(RussoOne_font)
caption_font = pygame.font.Font(BytesIO(decoded_font), HEIGHT // 25)
main_text_font = pygame.font.Font(BytesIO(decoded_font), HEIGHT // 12)
city_name_font = pygame.font.Font(BytesIO(decoded_font), HEIGHT // 12)
clock_hands_font = pygame.font.Font(BytesIO(decoded_font), HEIGHT // 50)

# создание служебных кнопок
close_button = PicButton(WIDTH - (WIDTH // 30) - 10, 10, WIDTH // 30, HEIGHT // 17, red_button_close)
change_theme_button = PicButton(20, 20, WIDTH // 16, HEIGHT // 18.4, light_theme)

# параметры для кнопок со странами
button_height = HEIGHT // 11.14  # Высота кнопки
spacing = HEIGHT // 44  # Расстояние между кнопками
total_height = 7 * button_height + (7 - 1) * spacing - spacing * 7
start_y = (HEIGHT - total_height) // 2  # начальная позиция для первой кнопки

# массив с данными о каждой кнопке
countries = [
    ("Лондоне", "Europe/London", "United Kingdom", United_Kingdom_light, WIDTH // 3.88),
    ("Нью-Йорке", "America/New_York", "United States", United_States_light, WIDTH // 4.58),
    ("Москве", "Europe/Moscow", "Russia", Russia_light, WIDTH // 5.4),
    ("Дубае", "Asia/Dubai", "Arab Emirates", Arab_Emirates_light, WIDTH // 6.16),
    ("Токио", "Asia/Tokyo", "Japan",  Japan_light, WIDTH // 5.6),
    ("Париже", "Europe/Paris", "France", France_light, WIDTH // 5.1),
    ("Сиднее", "Australia/Sydney", "Australia", Australia_light, WIDTH // 4.5)
]

# автоматическое создание кнопок
buttons = []
for i, (_, _, country, color, width) in enumerate(countries):
    button = PicButton(20, start_y + i * (button_height + spacing), width, button_height, color)
    buttons.append(button)


def update_buttons(theme):
    """метод для обновления кнопок при смене темы"""

    for i, (_, _, country, _, width) in enumerate(countries):
        if theme == "dark":
            color = globals()[f"{country.replace(' ', '_')}_dark"]
        else:
            color = globals()[f"{country.replace(' ', '_')}_light"]
        buttons[i] = PicButton(20, start_y + i * (button_height + spacing), width, button_height, color)


def update_text_colors():
    """функция для обновления цвета текста"""

    global CMW, text, city
    CMW = caption_font.render("CRAZY MECHANICAL WATCH", True, font_text_color)
    text = city_name_font.render("ТЕКУЩЕЕ ВРЕМЯ В ", True, font_text_color)
    city = city_name_font.render(current_city_text, True, font_city_color)

    screen.blit(CMW, (WIDTH - CMW.get_width() - 5, HEIGHT - CMW.get_height()))
    screen.blit(text, ((WIDTH - text.get_width() - city.get_width()) // 2, 20))
    screen.blit(city, ((WIDTH - text.get_width() - city.get_width()) // 2 + text.get_width(), 20))


def get_time(city):
    """функция для взятия текущего времени определённого города"""

    timezone = pytz.timezone(city)
    return datetime.now(timezone).strftime("%H:%M:%S")


def draw_hand(value, length, color):
    """функция для отрисовки стрелок из чисел"""

    step = HEIGHT // 30  # расстояние между числами
    angle = int(value) * (360 - 6) + 180  # угол отклонения стрелки (6 градусов)
    start_pos = (clock_frame.centerx, clock_frame.centery)  # начальная позиция для отрисовки

    for i in range(int(length // step)):
        current_length = step * (i + 1)  # текущая длина от центра до конца стрелки
        # конечная позиция для отрисовки
        end_pos = (
            start_pos[0] + current_length * math.sin(math.radians(angle)),
            start_pos[1] + current_length * math.cos(math.radians(angle))
        )

        hand_text = clock_hands_font.render(value, True, color)
        hand_rect = hand_text.get_rect(center=end_pos)
        screen.blit(hand_text, hand_rect)  # отрисовка стрелки на экране


# город и время по умолчанию
current_city_text = "Москве"
current_time_in_city = get_time("Europe/Moscow")

# основной цикл
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if close_button.collidepoint(event.pos):  #  проверка для закрытия окна
                exit()
            elif change_theme_button.collidepoint(event.pos):  # проверка для изменения темы оформления
                if current_theme:
                    current_theme = False
                    bg_color_theme = "#323232"
                    font_text_color = "#F2F2F2"
                    font_city_color = "#7030A0"
                    update_buttons("dark")
                    change_theme_button = PicButton(20, 20, WIDTH // 16, HEIGHT // 18.4, dark_theme)
                else:
                    current_theme = True
                    bg_color_theme = "#F2F2F2"
                    font_text_color = "#323232"
                    font_city_color = "#F2B800"
                    update_buttons("light")
                    change_theme_button = PicButton(20, 20, WIDTH // 16, HEIGHT // 18.4, light_theme)
            else:
                # для каждой из оставшихся кнопок проверяем город
                # затем меняем название города в соответствии с кнопкой
                for i, button in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        current_city_text = countries[i][0]  # получаем название города

    # обновляем текущее время
    current_time_in_city = get_time(countries[[country[0] for country in countries].index(current_city_text)][1])

    screen.fill(bg_color_theme)  # фоновое заполнение окна

    update_text_colors()  # обновляем цвет текстов и отрисовываем их на экран

    # отрисовываем кнопки на экран
    for button in buttons:
        button.draw(screen)

    # отрисовываем служебные кнопки
    close_button.draw(screen)
    change_theme_button.draw(screen)

    # отрисовываем рамку часов на экран и центральную точку для красоты
    radius = HEIGHT // 2 - HEIGHT // 12
    clock_frame = pygame.draw.circle(screen, font_text_color, (WIDTH // 2, HEIGHT // 2 + HEIGHT // 20), radius, width=8)
    pygame.draw.circle(screen, font_text_color, (clock_frame.centerx, clock_frame.centery), clock_frame.width // 120)

    draw_hand(current_time_in_city[:-6], radius * 0.5, font_text_color)  # часовая стрелка
    draw_hand(current_time_in_city[3:-3], radius * 0.8, font_text_color)  # минутная стрелка
    draw_hand(current_time_in_city[6:], radius * 0.93, "#ff483b")  # секундная стрелка

    pygame.display.flip()  # обновляем экран
