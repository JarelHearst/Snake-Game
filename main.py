from tkinter import *
import random
import pygame
pygame.mixer.init()


GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 50
SPACE_SIZE = 50
BODY_PARTS = 3

#We can pick any color we want, check hexadecimal sheet for maybe red?
#TODO: maybe think about changing relative colors in our game.
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])
            
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH//SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT//SPACE_SIZE)-1) * SPACE_SIZE
        
        self.coordinates = [x, y]
        
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")
    

# IMPORTANT: we pass the function name (next_turn) without parentheses
# because we want window.after() to call it later, not immediately.
# Adding parentheses (next_turn()) would run the function right now,
# which would break the timing.
def next_turn(snake, food):
    x, y = snake.coordinates[0]
    
    if direction == "up":
       y -= SPACE_SIZE
       
    elif direction == "down":
        y += SPACE_SIZE

    elif direction == "left":
        x -= SPACE_SIZE

    elif direction == "right":
        x += SPACE_SIZE
        
    snake.coordinates.insert(0, (x,y))
    
    sqaure = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake.squares.insert(0, sqaure)
    
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        pygame.mixer.music.load('food-ate.mp3')
        pygame.mixer.music.play()
        food = Food()
    
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
        
    else:   
        window.after(SPEED, next_turn, snake, food)
    
def change_direction(new_direction):
    global direction
    
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction        
    elif new_direction == "up":
            if direction != "down":
                direction = new_direction 
    elif new_direction == "down":
            if direction != "up":
                direction = new_direction      
                 
def check_collisions(snake): 
    x, y = snake.coordinates[0]
    
    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False


def restart_game():
    global snake, food, direction, score, replay_button
    
    replay_button.destroy()
    
    score = 0
    direction = 'down'
    label.config(text="Score:{}".format(score))
    
    canvas.delete(ALL)
    
    snake = Snake()
    food = Food()
    
    next_turn(snake, food)
def game_over():
    global replay_button
    
    pygame.mixer.music.load('gameover-sound.mp3')
    pygame.mixer.music.play()
    
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, 
                       canvas.winfo_height()/5,
                       font=('consolas', 70), 
                       text="GAME OVER", 
                       fill="red", 
                       tag="gameover"
                    )
    replay_button = Button(window, 
                           text="Play Again?", 
                           font=('consolas', 20),
                           command = restart_game
                    )
    canvas.create_window(canvas.winfo_width()/2, 
                         canvas.winfo_height()/2, 
                         window=replay_button
                    )

    

#NOTE: Tk is the main window object from the tkinter library, used to create GUI applications.
window = Tk()
window.title("Snek Game")
window.resizable(False,False)

score = 0
direction = 'down'

label = Label(window, text="Score:{}".format(score),font=('consolas', 40))

#NOTE: pack adds the widget to the window and automatically handles its layout.
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

#NOTE: x and y won't work if we don't typecast to int as a float cannot be passed through
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))


snake = Snake()
food = Food()

next_turn(snake, food)

#NOTE: mainloop keeps the window open and listens for user interactions.
window = mainloop()
