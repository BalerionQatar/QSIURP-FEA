import subprocess
import os
import time
import pyautogui
import stat

# Path to the directory you want to change permissions for
directory_path = "C:/Users/Mohammad Annan/Desktop"

# Get the current permissions
permissions = stat.S_IMODE(os.lstat(directory_path).st_mode)

# Add write permissions
os.chmod(directory_path, permissions | stat.S_IWUSR)
# Directory where your .k file is located
directory = r"C:\Users\Mohammad Annan\Desktop"

# Filename of your .k file
filename = "test3.k"

# Get full file path
file_path = os.path.join(directory, filename)
# Define commands to run
commands = [
    [os.path.join(os.getcwd(), 'C:\Program Files\ANSYS 2020R2 LS-DYNA Student 12.0.0\LS-PrePost\LS-Run 1.0\lsrun.exe'), file_path],
]

for cmd in commands:
    # Run the command
    process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Check if the command was successful
    if process.returncode != 0:
        print(f"Command {cmd} failed. Exiting.")
        print(f"Output: {process.stdout.decode()}")
        print(f"Error: {process.stderr.decode()}")
        exit(1)
# Wait for the application to start
time.sleep(5)

# Locate the button image on the screen
button_location = pyautogui.locateOnScreen("ls-run-play-button.png")
if button_location is None:
    print('Could not find the button image. Exiting.')
    exit(1)
# Click on the center of the button image
button_x, button_y, button_width, button_height = button_location
pyautogui.click(button_x + button_width / 2, button_y + button_height / 2)

# Wait for the simulation to complete
time.sleep(5)
print("Simulation completed successfully")
