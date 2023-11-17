import PySimpleGUI as sg
import pandas as pd
import sys

# Get username from the login screen
if "--username" in sys.argv:
    # Find the index of "--username" in the command-line arguments
    index = sys.argv.index("--username")

    # Get the username value from the next argument
    username = sys.argv[index + 1]

# Define the GUI layout
layout = [
    [sg.Text(f"Welcome, {username}!")],
    [sg.Text("Select a CSV file:")],
    [sg.InputText(key="-FILE-"), sg.FileBrowse()],
    [sg.Button("Load"), sg.Button("Back")],
    [sg.Multiline("", size=(150, 30), key="-TABLE-")],
]

# Create the window
window = sg.Window("CSV Viewer", layout, resizable=True)

# Function to format table
def format_table(df):
    formatted_table = ""
    
    # Calculate maximum width for each column based on data
    col_widths = [max(len(str(max(df[col], key=lambda x: len(str(x))))), len(col)) for col in df.columns]
    
    # Format and append headers
    formatted_table += " | ".join(f"{col:<{width}}" for col, width in zip(df.columns, col_widths)) + "\n"
    
    # Format and append data
    for index, row in df.iterrows():
        formatted_table += " | ".join(f"{str(row[col]):<{width}}" for col, width in zip(df.columns, col_widths)) + "\n"
    
    return formatted_table

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Back":
        break
    if event == "Load":
        # Get the selected CSV file path
        file_path = values["-FILE-"]
        if file_path.endswith(".csv"):
            try:
                df = pd.read_csv(file_path)
                headings = ", ".join(df.columns)
                table_str = format_table(df)
                window["-TABLE-"].update(table_str)
            except Exception as e:
                print(f"Error: {str(e)}")
                sg.popup_error(f"An error occurred: {str(e)}")
        else:
            sg.popup_error("Please select a valid CSV file.")
# Close the window
window.close()
