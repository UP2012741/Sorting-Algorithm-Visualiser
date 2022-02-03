import math
from pickle import TRUE
from re import T
import pygame
import random

pygame.init()


class Drawing:
    # RGB COLOUR
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 107, 219, 90
    BLUE = 46, 37, 143

    BACKGROUND_COLOUR = WHITE
    # Shades of Orange
    SHADES = [
        (255, 98, 0),
        (253, 147, 70),
        (253, 183, 119
         )
    ]

    FONT = pygame.font.SysFont('Helvetica Neue', 30)
    BOLD_FONT = pygame.font.SysFont('Helvetica Neue', 30, bold=True)

    SIDE_PADDING = 100  # 50px to the left 50 px to right
    TOP_PADDING = 150

    def __init__(self, width, height, list):
        self.width = width
        self.height = height

        # creating a window
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("SORTING ALGORITHM")

        self.set_list(list)

    def set_list(self, list):
        self.list = list
        self.min_value = min(list)
        self.max_value = max(list)

        self.block_width = round((self.width - self.SIDE_PADDING) / len(list))
        self.block_height = math.floor(
            (self.height - self.TOP_PADDING) / (self.max_value - self.min_value))
        self.start_x = self.SIDE_PADDING // 2


def draw(drawing, algorithm_name, ascending):
    drawing.window.fill(Drawing.BACKGROUND_COLOUR)

    header = drawing.FONT.render(
        f"{algorithm_name} - {'Ascending' if  ascending else 'Descending'}", 1, drawing.BLACK)
    drawing.window.blit(header, (drawing.width/2 - header.get_width()/2, 5))

    controls = drawing.FONT.render(
        "R: Reset | Space: Sort | A:Ascending | D: Descending", 1, drawing.BLACK)
    drawing.window.blit(
        controls, (drawing.width/2 - controls.get_width()/2, 35))  # 35 height because Font size is 30

    algorithms = drawing.FONT.render(
        "I: Insertion | B: Bubble Sort | S: Selection Sort", 1, drawing.BLACK)
    drawing.window.blit(
        algorithms, (drawing.width/2 - algorithms.get_width()/2, 65))  # 65 height because Font size is 30

    draw_list(drawing)
    pygame.display.update()


def draw_list(drawing, colour_position={}, clear_bg=False):
    list = drawing.list

    # Clears the blocks
    if clear_bg:
        clear_rect = (drawing.SIDE_PADDING//2, drawing.TOP_PADDING, drawing.width -
                      drawing.SIDE_PADDING, drawing.height - drawing.TOP_PADDING)

        pygame.draw.rect(drawing.window, drawing.BACKGROUND_COLOUR, clear_rect)

    for i, value in enumerate(list):
        x = drawing.start_x + i * drawing.block_width
        y = drawing.height - (value - drawing.min_value) * drawing.block_height

        # Assign each block with different shade depending on the module of the I
        colour = Drawing.SHADES[i % 3]

        if(i in colour_position):
            colour = colour_position[i]

        pygame.draw.rect(drawing.window, colour,
                         (x, y, drawing.block_width, drawing.height))

    if clear_bg:
        pygame.display.update()


# Randomly creating list
def starting_list(n, min_value, max_value):
    list = []

    for _ in range(n):
        value = random.randint(min_value, max_value)
        list.append(value)

    return list

# SORTING ALGORITHM FUNCTIONS


def bubble_sort(drawing, ascending=True):
    list = drawing.list
    # Bubble Sort algorithm
    for i in range(len(list) - 1):
        for j in range(len(list)-1 - i):
            num1 = list[j]
            num2 = list[j+1]

            # If statement covers both ascending order and descending order
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                list[j], list[j+1] = list[j + 1], list[j]
                # Changes the colours of the two blocks that will be swapped
                draw_list(drawing, {j: drawing.GREEN, j+1: drawing.BLUE}, True)
                yield True  # function return a generator
    return list


def insertion_sort(drawing, ascending=True):
    list = drawing.list
    # Insertion Sort Algorithm
    for i in range(1, len(list)):
        currentValue = list[i]

        for i in range(1, len(list)):
            currentValue = list[i]

            while True:
                ascending_sort = i > 0 and list[i -
                                                1] > currentValue and ascending
                descending_sort = i > 0 and list[i -
                                                 1] < currentValue and not ascending

                if not ascending_sort and not descending_sort:
                    break

                list[i] = list[i-1]
                i = i-1
                list[i] = currentValue
                draw_list(drawing, {i: drawing.GREEN, i-1: drawing.BLUE}, True)
                yield True

        return list


def selection_sort(drawing, ascending=True):
    list = drawing.list
    for i in range(0, len(list) - 1):
        min_index = i

        for j in range(i + 1, len(list)):
            if(list[j] < list[min_index] and ascending) or (list[j] > list[min_index] and not ascending):
                min_index = j

        if min_index != i:
            temp = list[i]
            list[i], list[min_index] = list[min_index], list[i]
            list[min_index] = temp
            draw_list(drawing, {i: drawing.GREEN, j: drawing.BLUE}, True)
            yield True

    return list


def main():
    run = True
    clock = pygame.time.Clock()
    n = 50
    min_value = 0
    max_value = 100

    list = starting_list(n, min_value, max_value)
    drawing = Drawing(800, 600, list)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Bubble Sort"
    sorting_algorithm_generator = None

    # loop running in background and handling events
    while run:
        clock.tick(300)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
            draw(drawing, sorting_algorithm_name, ascending)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:  # if press R key
                list = starting_list(n, min_value, max_value)
                drawing.set_list(list)
                sorting = False
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algorithm_generator = sorting_algorithm(
                    drawing, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algorithm_name = "Insertion Sort"
            elif event.key == pygame.K_y and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algorithm_name = "Bubble Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algorithm_name = "Selection Sort"

    pygame.quit()


if __name__ == "__main__":
    main()
