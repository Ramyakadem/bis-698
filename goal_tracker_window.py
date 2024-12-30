import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date
import random
from tkcalendar import DateEntry
import time
import threading
import login

# Connect to MySQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="BIS_698_Group2"
    )
except mysql.connector.Error as e:
    messagebox.showerror("Database Connection Error", f"Failed to connect to the database: {e}")
    exit()

# Define colors for the application
background_color = '#F9F9F9'  # Light gray similar to iOS Notes
text_color = '#333333'  # Dark gray for text
button_color = '#2962FF'  # Blue for buttons

# Function to get a random motivational message
def get_motivational_message():
    messages = [
        "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Your time is limited, don't waste it living someone else's life.",
        "The only limit to our realization of tomorrow will be our doubts of today.",
        "Do not wait to strike till the iron is hot, but make it hot by striking.",
        "Don't count the days, make the days count.",
        "It always seems impossible until it's done."
    ]
    return random.choice(messages)

# Create the main window
root = tk.Tk()
root.title("Goal Tracker Dashboard")
root.geometry("1200x600")  # Adjusted size for better visualization
root.configure(bg=background_color)

# Create a frame for the goals list
goals_list_frame = tk.Frame(root, bg=background_color)
goals_list_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ns")

# Create a label for the goals list
goal_list_label = tk.Label(goals_list_frame, text='Goal List:', fg=text_color, bg=background_color)
goal_list_label.pack(side='top', padx=10)

# Create a scrollbar for the goals list
goal_list_scrollbar = tk.Scrollbar(goals_list_frame, orient=tk.VERTICAL)
goal_list_scrollbar.pack(side='right', fill='y')

# Create a listbox to display the goals list
goal_list = tk.Listbox(goals_list_frame, yscrollcommand=goal_list_scrollbar.set)
goal_list.pack(side='left', fill='both', expand=1)
goal_list_scrollbar.config(command=goal_list.yview)

# Create a frame for goal information
goal_info_frame = tk.Frame(root, bg=background_color)
goal_info_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

# Create entry fields for goal name, deadline, and completion percentage
goal_label = tk.Label(goal_info_frame, text='Goal Name:', fg=text_color, bg=background_color)
goal_label.grid(row=0, column=0, padx=10, pady=(0, 5))

goal_entry = tk.Entry(goal_info_frame, width=30)
goal_entry.grid(row=1, column=0, padx=10)

deadline_label = tk.Label(goal_info_frame, text='Deadline:', fg=text_color, bg=background_color)
deadline_label.grid(row=2, column=0, padx=10)

deadline_calendar = DateEntry(goal_info_frame, date_pattern='yyyy-mm-dd', selectbackground=button_color)
deadline_calendar.grid(row=3, column=0, padx=10)

completion_percentage_label = tk.Label(goal_info_frame, text='Completion Percentage:', fg=text_color, bg=background_color)
completion_percentage_label.grid(row=4, column=0, padx=10)

completion_slider = tk.Scale(goal_info_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200, resolution=1)
completion_slider.grid(row=5, column=0, padx=10)

# Create buttons for adding, updating, deleting, and viewing progress of goals
add_button = tk.Button(goal_info_frame, text='Add Goal', fg=text_color, bg=button_color)
add_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")

update_button = tk.Button(goal_info_frame, text='Update Goal', fg=text_color, bg=button_color)
update_button.grid(row=7, column=0, padx=10, pady=10, sticky="ew")

delete_button = tk.Button(goal_info_frame, text='Delete Goal', fg=text_color, bg=button_color)
delete_button.grid(row=8, column=0, padx=10, pady=10, sticky="ew")

view_progress_button = tk.Button(goal_info_frame, text='View Progress Report', fg=text_color, bg=button_color)
view_progress_button.grid(row=9, column=0, padx=10, pady=10, sticky="ew")

# Create a frame for the motivational messages
motivational_frame = tk.Frame(root, bg=background_color)
motivational_frame.grid(row=0, column=2, padx=20, pady=20, sticky="ns")

# Create a label for the motivational messages
motivational_label = tk.Label(motivational_frame, text='Motivational Message:', fg=text_color, bg=background_color)
motivational_label.pack(side='top', padx=10)

# Create a text widget to display the motivational message
motivational_text = tk.Text(motivational_frame, height=10, width=30, wrap='word', fg=text_color, bg=background_color, font=('Helvetica', 10))
motivational_text.pack(side='bottom', padx=10)

# Function to update motivational message every 3 seconds
def update_motivational_periodically():
    while True:
        motivational_text.delete(1.0, tk.END)
        motivational_text.insert(tk.END, get_motivational_message())
        time.sleep(3)

# Create a thread for updating motivational message periodically
motivational_thread = threading.Thread(target=update_motivational_periodically)
motivational_thread.daemon = True  # Daemonize the thread to stop it when the main program exits
motivational_thread.start()

# Set row and column weights so that the sections can expand
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

root.mainloop()
