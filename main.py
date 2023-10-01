import tkinter as tk
import json

# Function to move the squares with the mouse while the left button is held
def move_squares():
    if left_button_pressed:
        x, y = canvas.winfo_pointerxy()
        x -= window.winfo_rootx() + canvas.winfo_x()
        y -= window.winfo_rooty() + canvas.winfo_y()
        
        # Calculate the x-coordinates with a 10-pixel gap between the squares
        x1 = x - SQUARE_SIZE - GAP // 2
        x2 = x + GAP // 2
        
        # Keep the y-coordinates constant
        y1 = canvas.coords(square1)[1]
        y2 = canvas.coords(square2)[1]
        
        canvas.coords(square1, x1, y1, x1 + SQUARE_SIZE, y1 + SQUARE_SIZE)
        canvas.coords(square2, x2, y2, x2 + SQUARE_SIZE, y2 + SQUARE_SIZE)
        
        # Update the position of the "R" and "Y" text elements
        canvas.coords(text1, x1 + SQUARE_SIZE / 2, y1 - 10)  # Move "R" up by 10 pixels
        canvas.coords(text2, x2 + SQUARE_SIZE / 2, y2 - 10)  # Move "Y" up by 10 pixels

        # Update the position of the "0" text elements
        canvas.coords(text0_1, x1 + SQUARE_SIZE / 2, y1 + SQUARE_SIZE / 2)  # Centered within the left square
        canvas.coords(text0_2, x2 + SQUARE_SIZE / 2, y2 + SQUARE_SIZE / 2)  # Centered within the right square
    
    # Update the window title with the current width and height
    window.title(f"Osu! Key Counter ({window.winfo_width()}x{window.winfo_height()})")
    
    # Schedule the move_squares function to run again after 1/144 seconds (144 FPS)
    window.after(int(1000 / 144), move_squares)

# Function to handle mouse button press events
def on_left_button_press(event):
    global left_button_pressed
    left_button_pressed = True

# Function to handle mouse button release events
def on_left_button_release(event):
    global left_button_pressed
    left_button_pressed = False

# Function to count up to infinity when keycode "82" ("R") is pressed on the left square
def count_up_r(event):
    global counter_r
    counter_r += 1
    canvas.itemconfig(text0_1, text=str(counter_r))  # Update the number inside the left square
    print(f"Key 'R' had been pressed {counter_r} times")
    save_data()

# Function to count up to infinity when keycode "89" ("Y") is pressed on the right square
def count_up_y(event):
    global counter_y
    counter_y += 1
    canvas.itemconfig(text0_2, text=str(counter_y))  # Update the number inside the right square
    print(f"Key 'Y' had been pressed {counter_y} times")
    save_data()

# Function to save the press counts to a JSON file
def save_data():
    data = {
        "R": counter_r,
        "Y": counter_y,
    }
    with open("presses.json", "w") as json_file:
        json.dump(data, json_file)

# Function to load press counts from a JSON file
def load_data():
    try:
        with open("presses.json", "r") as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError:
        return {}

# Create the main window
window = tk.Tk()

# Set the window size to 200x100
window.geometry("200x100")

# Create a Canvas widget
canvas = tk.Canvas(window, width=200, height=100, bg="black")
canvas.pack()

# Constants for square size and gap (doubled square size)
SQUARE_SIZE = 48  # Doubled size
GAP = 10  # Gap between squares

# Calculate the initial position to spawn on the left side of the window for square1
initial_x1 = GAP
initial_y = (canvas.winfo_reqheight() - SQUARE_SIZE) / 2

# Calculate the initial position to spawn on the right side of the window for square2
initial_x2 = canvas.winfo_reqwidth() - SQUARE_SIZE - GAP
initial_y = (canvas.winfo_reqheight() - SQUARE_SIZE) / 2

# Create the left square with a black fill and white outline on the left side
square1 = canvas.create_rectangle(
    initial_x1, initial_y, initial_x1 + SQUARE_SIZE, initial_y + SQUARE_SIZE, fill="black", outline="white"
)

# Create the right square with the same characteristics on the right side
square2 = canvas.create_rectangle(
    initial_x2, initial_y, initial_x2 + SQUARE_SIZE, initial_y + SQUARE_SIZE, fill="black", outline="white"
)

# Add white text "R" to the center of the left square (font size 15)
text1 = canvas.create_text(
    initial_x1 + SQUARE_SIZE / 2, initial_y - 10, text="R", fill="white", font=("Arial", 15)
)

# Add white text "Y" to the center of the right square (font size 15)
text2 = canvas.create_text(
    initial_x2 + SQUARE_SIZE / 2, initial_y - 10, text="Y", fill="white", font=("Arial", 15)
)

# Add "0" to the center of the left square (font size 15)
text0_1 = canvas.create_text(
    initial_x1 + SQUARE_SIZE / 2, initial_y + SQUARE_SIZE / 2, text="0", fill="white", font=("Arial", 15)
)

# Add "0" to the center of the right square (font size 15)
text0_2 = canvas.create_text(
    initial_x2 + SQUARE_SIZE / 2, initial_y + SQUARE_SIZE / 2, text="0", fill="white", font=("Arial", 15)
)

# Initialize left button pressed flag
left_button_pressed = False

# Bind mouse events to move both squares
canvas.bind("<ButtonPress-1>", on_left_button_press)
canvas.bind("<ButtonRelease-1>", on_left_button_release)

# Bind key events to count up and print messages
window.bind("r", count_up_r)  # Count up and print message when "R" key is pressed
window.bind("y", count_up_y)  # Count up and print message when "Y" key is pressed

# Initialize counters
data = load_data()
counter_r = data.get("R", 0)
counter_y = data.get("Y", 0)

# Update the numbers in the squares based on loaded data
canvas.itemconfig(text0_1, text=str(counter_r))
canvas.itemconfig(text0_2, text=str(counter_y))

# Start the move_squares function to control the movement and update the window title every frame
move_squares()

# Start the main event loop
window.mainloop()
