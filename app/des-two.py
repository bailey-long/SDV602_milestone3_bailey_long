import PySimpleGUI as sg
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sys

# Get username from the login screen
if "--username" in sys.argv:
    # Find the index of "--username" in the command-line arguments
    index = sys.argv.index("--username")

    # Get the username value from the next argument
    username = sys.argv[index + 1]


# Define the PySimpleGUI layout
layout = [
    [sg.Text(f"Welcome, {username}!")],
    [sg.Text("Select a CSV file:")],
    [sg.InputText(key="csv_file"), sg.FileBrowse()],
    [sg.Button("Load"), sg.Button("Back")],
    [sg.Canvas(key="-CANVAS-")],
]

# Create the window
window = sg.Window("CSV Data Chart", layout, finalize=True)

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

            # Convert 'birth_year' to string to avoid the 'value' error
            df['birth_year'] = df['birth_year'].astype(str)

            # Create a bar chart based on 'birth_year' and 'death_year'
            plt.figure(figsize=(10, 6))
            plt.bar(df['birth_year'], df['death_year'])
            plt.xlabel('Birth Year')
            plt.ylabel('Death Year')
            plt.title('Bar Chart of birth and death years')

            # Embed the Matplotlib chart in the PySimpleGUI window
            canvas_elem = window["-CANVAS-"]
            canvas = FigureCanvasTkAgg(plt.gcf(), master=canvas_elem.Widget)
            canvas.draw()
            canvas.get_tk_widget().pack(side="top", fill="both", expand=1)

        except Exception as e:
            sg.popup_error(f"Error: {str(e)}")

# Close the window
window.close()
