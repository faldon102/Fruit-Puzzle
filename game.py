import pygame
from pygame.locals import * 
from all_classes import Button, change_music
import random
from pygame import mixer

pygame.init()

display_surface = pygame.display.set_mode((1200, 800))
pygame.display.set_caption("Fruit Puzzle")
icon = pygame.image.load("question_mark.png")
pygame.display.set_icon(icon)

# Background
background = pygame.image.load("fruit_background.png")
background = pygame.transform.scale(background, (1200,800))

# Music
mixer.music.load("Underwater.mp3")
mixer.music.play(-1)
music = set(())

white = (255, 255, 255)
yellow = (255,255,0,0)
pink = (255, 0, 255)
black = (0, 0, 0)

# Coordinates inputted in here simply as a placeholder, they will be changed by the while loop
grapes_one = Button(205, 260, "grape.png")
grapes_two = Button(375, 260, "grape.png")
apple_one = Button(545, 260, "apple.png")
apple_two = Button(715, 260, "apple.png")
orange_one = Button(885, 260, "orange.png")
orange_two = Button(205, 420, "orange.png")
banana_one = Button(375, 420, "banana.png")
banana_two = Button(545, 420, "banana.png")
strawberry_one = Button(715, 420, "strawberry.png")
strawberry_two = Button(885, 420, "strawberry.png")

fruits_arr = [grapes_one, grapes_two, apple_one, apple_two, orange_one, orange_two, banana_one, banana_two, strawberry_one, strawberry_two]
used_dict = {}
coors = [(205, 260), (375, 260), (545, 260), (715, 260), (885, 260), (205, 420), (375, 420), (545, 420), (715, 420), (885, 420)]
coors_dict = {"205260": None, "375260": None, "545260": None, "715260": None, "885260": None, "205420": None, "375420": None, "545420": None, "715420": None, "885420": None}

showed = False
iter_count = 0
click_count = 0
disappeared_images = {}
currently_in_decision_images = {}

# Track Level and make level text
level = 1
level_font = pygame.font.Font("freesansbold.ttf", 32)
level_text = level_font.render("Level: ", True, yellow, pink)
level_rect = level_text.get_rect()
level_rect.center = (600, 200)

clock = pygame.time.Clock()
delay_level = 5000
current_time = 0.0
last_time = 0.0

# Makes the while loop break after closing tab (not deleting from terminal, just closing tab on MAC)
need_to_break = False

# Main Loop
while True:

    # Decrease delay amount after certain levels
    if level <= 2:
        delay_level = 5000
    elif level <= 4:
        delay_level = 3000
    elif level <= 6:
        delay_level = 2500
    elif level <= 8:
        delay_level = 2000
        if len(music) == 0:
            change_music(level)

        music.add(level)
    else:
        delay_level = 1000
        if 9 not in music:
            change_music(level)
        
        music.add(level)

    display_surface.blit(background, (0,0))

    # Timer image being displayed
    pygame.draw.rect(display_surface, black, (250, 560, 700, 50), 8)
    pygame.draw.rect(display_surface, white, (255, 565, 691, 41))
    
    # Level text displayed
    level_text = level_font.render("Level: " + str(level), True, yellow, pink)
    display_surface.blit(level_text, level_rect)

    if showed == False and iter_count > 0:
        showed = True

        for fruit in fruits_arr:

            # Pick random integer that has not been used till now, and index into coors arr and find coordinates
            random_int = random.randint(0, 9)
            while random_int in used_dict:
                random_int = random.randint(0, 9)

            fruit.set_x(coors[random_int][0])
            fruit.set_y(coors[random_int][1])
            used_dict[random_int] = "Used"

            # Black Rectangle behind Fruits
            pygame.draw.rect(display_surface, black, (fruit.get_x(), fruit.get_y(), 110, 110), 0, 9)

            # Image of fruit displayed
            image = pygame.image.load(fruit.image)
            image = pygame.transform.scale(image, (110, 110))
            display_surface.blit(image, (fruit.get_x(), fruit.get_y()))

            coors_dict[str(fruit.get_x()) + str(fruit.get_y())] = fruit
        
        used_dict = {}

    elif showed == True and iter_count > 0:

        if iter_count == 2:
            pygame.time.delay(delay_level)

        question_image = pygame.image.load("question_mark.png")
        question_image = pygame.transform.scale(question_image, (110, 110))

        for fruit in fruits_arr:

            # Black Rectangle behind Fruits
            pygame.draw.rect(display_surface, black, (fruit.get_x(), fruit.get_y(), 110, 110), 0, 9)

            # Image of fruit displayed
            image = pygame.image.load(fruit.image)
            image = pygame.transform.scale(image, (110, 110))
            display_surface.blit(image, (fruit.get_x(), fruit.get_y()))

            if str(fruit.get_x()) + str(fruit.get_y()) in currently_in_decision_images or str(fruit.get_x()) + str(fruit.get_y()) in disappeared_images:
                continue

            # Question mark image on top of fruit images
            display_surface.blit(question_image, (fruit.get_x(), fruit.get_y()))

    iter_count += 1
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            need_to_break = True
            break

        # Event added to increase brightness of question mark image when hovered upon
        # if event.type == MOUSEMOTION:
        #     pos = pygame.mouse.get_pos()

        #     for coor in coors:
        #         if pos[0] >= coor[0] and pos[0] <= coor[0] + 120 and pos[1] >= coor[1] and pos[1] <= coor[1] + 120:
        #             img = Image.open("question_mark.png")
        #             enhancer = ImageEnhance.Brightness(img)
        #             output = enhancer.enhance(1)
        #             output.save("question_mark.png")

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            for coor in coors:
                if pos[0] >= coor[0] and pos[0] <= coor[0] + 120 and pos[1] >= coor[1] and pos[1] <= coor[1] + 120:
                    # User has clicked inside a box

                    if str(coor[0]) + str(coor[1]) not in currently_in_decision_images and str(coor[0]) + str(coor[1]) not in disappeared_images:
                        # This means the button has not already been clicked

                        click_count += 1

                        if click_count <= 2:
                            currently_in_decision_images[str(coor[0]) + str(coor[1])] = coors_dict[str(coor[0]) + str(coor[1])]

                            if click_count == 2:
                                coor_one = ""
                                coor_two = ""
                                for key in currently_in_decision_images.keys():
                                    if coor_one == "":
                                        coor_one = key
                                    else:
                                        coor_two = key

                                if currently_in_decision_images[coor_one].image == currently_in_decision_images[coor_two].image:
                                    disappeared_images[coor_one] = currently_in_decision_images[coor_one]
                                    disappeared_images[coor_two] = currently_in_decision_images[coor_two]

                                currently_in_decision_images = {}
                                click_count = 0

    if len(disappeared_images) == 10:
        level += 1

        showed = False
        iter_count = 0
        click_count = 0
        disappeared_images = {}
        currently_in_decision_images = {}
        # music = []

        current_time = 0
        last_time = 0

    if need_to_break == True:
        break

    pygame.display.update()
    clock.tick(50)
    current_time += 0.05
    if str(current_time)[0] != str(last_time)[0]:
        print(current_time)
        last_time += 1

    decimal_current_time = str(current_time).find(".")
    decimal_last_time = str(last_time).find(".")
    if str(current_time)[:decimal_current_time] != str(last_time)[:decimal_last_time]:
        print(current_time)
        last_time += 1.0


# # First row of RECTs
# pygame.draw.rect(display_surface, pink, (205, 260, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (375, 260, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (545, 260, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (715, 260, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (885, 260, 110, 110), 0, 9)

# # Second row of RECTs
# pygame.draw.rect(display_surface, pink, (205, 420, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (375, 420, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (545, 420, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (715, 420, 110, 110), 0, 9)
# pygame.draw.rect(display_surface, pink, (885, 420, 110, 110), 0, 9)