import os
import random
import tkinter as tk

# Constants
WIDTH = 500
HEIGHT = 500
GRID_SIZE = 20
SNAKE_COLOR = "#4CAF50"  # Green Snake
FOOD_COLOR = "#FF5733"   # Bright Orange-Red Square Food
BG_COLOR = "#F0F0F0"     # Light Gray Background

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")

        # Score Variable
        self.score = 0

        # Create Canvas
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=BG_COLOR)
        self.canvas.pack()

        # Create Score Label
        self.score_label = tk.Label(root, text=f"Score: {self.score}", font=("Arial", 14), bg=BG_COLOR)
        self.score_label.pack()

        # Restart Button (Initially Hidden)
        self.restart_button = tk.Button(root, text="Restart", font=("Arial", 14), command=self.restart_game)
        self.restart_button.pack()
        self.restart_button.place_forget()  # Hide initially

        # Initialize game variables
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.food = self.place_food()
        self.direction = "Right"
        self.running = True

        # Draw initial snake and food
        self.draw_snake()
        self.draw_food()

        # Bind keys for movement
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

        # Start the game loop
        self.run_game()

    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")  # Clear previous snake
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=SNAKE_COLOR, tag="snake")

    def draw_food(self):
        """Draw the food as a square on the canvas."""
        self.canvas.delete("food")  # Remove previous food
        x, y = self.food
        self.canvas.create_rectangle(x, y, x + GRID_SIZE, y + GRID_SIZE, fill=FOOD_COLOR, tag="food")

    def place_food(self):
        """Place food at a random location ensuring it does not overlap with the snake."""
        while True:
            x = random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE
            y = random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, new_direction):
        """Change the snake's direction based on key input."""
        opposite_directions = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposite_directions.get(self.direction, ""):
            self.direction = new_direction

    def move_snake(self):
        """Move the snake in the current direction."""
        if not self.running:
            return

        head_x, head_y = self.snake[0]

        # Move in the selected direction
        if self.direction == "Up":
            head_y -= GRID_SIZE
        elif self.direction == "Down":
            head_y += GRID_SIZE
        elif self.direction == "Left":
            head_x -= GRID_SIZE
        elif self.direction == "Right":
            head_x += GRID_SIZE

        new_head = (head_x, head_y)

        # Check for collisions
        if (new_head in self.snake) or (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT):
            self.game_over()
            return

        # Move the snake
        self.snake.insert(0, new_head)

        # Check if food is eaten
        if new_head == self.food:
            self.score += 10  # Increase score
            self.score_label.config(text=f"Score: {self.score}")  # Update Scoreboard
            self.food = self.place_food()  # Generate new food
            self.draw_food()
        else:
            self.snake.pop()  # Remove last segment if food not eaten

        self.draw_snake()

    def run_game(self):
        """Game loop that updates movement."""
        if self.running:
            self.move_snake()
            self.root.after(100, self.run_game)  # Adjust speed

    def game_over(self):
        """Handle game over scenario."""
        self.running = False
        self.canvas.create_text(WIDTH // 2, HEIGHT // 2, text="Game Over!", fill="black", font=("Arial", 24))
        self.restart_button.place(x=WIDTH // 2 - 40, y=HEIGHT // 2 + 40)  # Show restart button

    def restart_game(self):
        """Restart the game when the restart button is clicked."""
        self.canvas.delete("all")  # Clear canvas
        self.score = 0  # Reset score
        self.score_label.config(text=f"Score: {self.score}")  # Reset Scoreboard
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Reset snake
        self.food = self.place_food()  # Reset food
        self.direction = "Right"
        self.running = True
        self.restart_button.place_forget()  # Hide restart button

        # Redraw everything
        self.draw_snake()
        self.draw_food()
        self.run_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
