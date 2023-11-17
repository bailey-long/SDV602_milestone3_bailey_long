import pandas as pd
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# Get username from the login screen
if "--username" in sys.argv:
    # Find the index of "--username" in the command-line arguments
    index = sys.argv.index("--username")

    # Get the username value from the next argument
    username = sys.argv[index + 1]

# Define the layout of the PySimpleGUI window
layout = [
    [sg.Text(f"Welcome, {username}!")],
    [sg.Text("Select a CSV file:")],
    [sg.InputText(key="csv_file"), sg.FileBrowse()],
    [sg.Button("Load"), sg.Button("Back")],
    [sg.Canvas(key="-CANVAS-")],
]

# Create the PySimpleGUI window
window = sg.Window("Scatter Plot App", layout, finalize=True)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Back":
        break

    if event == "Load":
        # Get the selected CSV file path
        csv_file = values["csv_file"]

        try:
            # Read the CSV file into a Pandas DataFrame
            df = pd.read_csv(csv_file)

            # Create a scatter plot based on the data
            plt.figure(figsize=(10, 6))
            print(df.columns)
            plt.scatter(df['x'], df['y'])
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Scatter Plot')

            # Embed the Matplotlib chart in the PySimpleGUI window
            canvas_elem = window["-CANVAS-"]
            canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_elem.Widget)
            canvas.draw()
            canvas_elem.drawn_canvas = canvas

        except Exception as e:
            print(f"Error: {e}")
            sg.popup_error(f"Error: {e}")

# Close the PySimpleGUI window
window.close()