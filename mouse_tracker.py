from pynput.mouse import Listener
from datetime import datetime
from time import *
import csv
from tkinter import *
import os


class Logger:
    """
    Takes in a file location and stores data from class MouseTracker as a CSV
    """
    def __init__(self, file_path):
        self.file_path = file_path
        self.log_file = None
        self.csv_writer = None

    def __enter__(self):
        self.log_file = open(self.file_path, 'a', newline='')
        self.csv_writer = csv.writer(self.log_file)
        return self

    def write(self, data):
        self.csv_writer.writerow(data)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log_file.close()


class MouseTracker:
    """
    Logs mouse locations. Stores them later using class Logger
    """
    def __init__(self, is_cheater):
        self.current_date = datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
        self.start_time = time()
        self.button_pressed = False
        self.is_mouse_pressed = False
        self.saved_mouse_pos = None  # saves mouse position for later logging
        self.break_loop = False
        self.last_mouse_pos = None

        # ensures that the logger is not logging unnecessary data
        self.last_time_stamp = 0
        self.last_entry = list(range(5))
        self.running = False  # checks if user wants to run program before logging
        self.time_last_moved = 0  # checks when mouse was last moved

        self.is_cheater = is_cheater
        # if user is cheating, create file with certain file name attached to it
        if is_cheater:
            self.file_name = f'./Mouse Logs/{self.current_date}_mouse_log_cheater.csv'
        else:
            self.file_name = f'./Mouse Logs/{self.current_date}_mouse_log_innocent.csv'

        self.Logger = Logger(self.file_name)

    @staticmethod
    def get_screen_size():
        window = Tk()
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()

        # write to file
        with open('./Mouse Logs/device_information.txt', 'w') as file:
            print('Logged screen size')
            screen_size = f'Screen size: {width}, {height}'
            file.write(screen_size)

        # close tk window
        window.destroy()

    def get_time_elapsed(self):
        current_time = time()
        return current_time - self.start_time

    # check if mouse was clicked or held down
    def on_click(self, x, y, button, pressed):
        if not self.running:
            return

        # if the current entry is the same as the last entry, do not log
        current_time = self.get_time_elapsed()
        if self.last_entry == (round(current_time, 2), x, y, button, pressed):
            return

        self.saved_mouse_pos = (current_time, x, y, button, pressed)

        if pressed:
            # executes when mouse is pressed
            print(f'Pressed: {x}, {y} {button}')
            # for later tracking
            self.button_pressed = button
        else:
            # executes when mouse is released
            print(f'Released: {x}, {y} {button}')
            # for later tracking
            self.button_pressed = False

        # used for future checks
        self.last_entry = (round(current_time, 2), x, y, button, pressed)
        self.is_mouse_pressed = pressed

        # log to file
        self.write_to_csv(self.saved_mouse_pos)

    # logs where mouse was moved
    def on_move(self, x, y):
        if not self.running:
            return

        # if the current entry is the same as the last entry, do NOT log
        current_time = self.get_time_elapsed()
        if self.last_entry == (round(current_time, 2), x, y):
            return

        # get mouse position
        mouse_pos = (x, y)

        # if mouse positions are the same, do NOT log
        # if timestamps are less than 0.5 seconds apart, do NOT log
        if mouse_pos != self.last_mouse_pos and (current_time - self.time_last_moved) >= 0.5:
            self.last_mouse_pos = None
        else:
            return

        # save mouse position and timestamp. Useful if the mouse doesn't move on the next iteration
        self.last_mouse_pos = mouse_pos
        self.time_last_moved = current_time
        print(f'{current_time}\t{mouse_pos}')

        # log to file
        self.saved_mouse_pos = (current_time, mouse_pos[0], mouse_pos[1], self.button_pressed, self.is_mouse_pressed)
        self.write_to_csv(self.saved_mouse_pos)

    def main(self, start=True):
        # track mouse clicks
        listener = Listener(on_click=self.on_click, on_move=self.on_move)

        if start:
            listener.start()
        else:
            listener.stop()

    def create_file(self):
        folder = 'Mouse Logs'
        # if folder does not exist, make folder
        if folder in os.listdir():
            print(f'{folder} directory already exists!')
        else:
            os.mkdir(f'./{folder}/')
            print(f'Created {folder}')

        # make header row
        with open(self.file_name, 'a', newline='') as file:
            csv.writer(file).writerow(
                ['Time Since Start of Test', 'Mouse X Position', 'Mouse Y Position', 'Mouse Button Clicked', 'Pressed']
            )
        print(f'Created {self.file_name}')

    def write_to_csv(self, data):
        if data is not None:
            with self.Logger as log_file:
                log_file.write(data)
        else:
            return

        # clear mouse positions
        self.saved_mouse_pos = None


class Interface:
    """
    Interface that users see to log mouse movements
    """
    def __init__(self, master):
        self.master = master
        self.track = MouseTracker(is_cheater=True)  # instance of MouseTracker()

        title = Label(text='Welcome to Mouse Logger', font=('Arial', 25))
        title.pack(pady=20, padx=20)

        # window title
        master.title("Mouse Logger")

        # text to tell user if program is active or not
        self.status = StringVar()
        self.status.set("Status: OFF")
        Label(master, textvariable=self.status, font="Arial, 15").pack(pady=5)

        # Create buttons to start the infinite loop
        Button(master, text="Start Tracking", font="Arial, 20", command=lambda: self.start_program(True)).pack(padx=20,
                                                                                                               pady=5)
        Button(master, text="Stop Tracking", font="Arial, 20", command=lambda: self.start_program(False)).pack(padx=20,
                                                                                                               pady=5)

        # Tells user if they are cheating or not
        Label(master, text="Cheating Configurations", font="Arial, 20").pack()

        self.is_cheater = True
        self.cheating = StringVar()
        self.cheating.set('You are now CHEATING')
        Label(master, textvariable=self.cheating, font="Arial, 15").pack(pady=5)
        Button(master, text="Be a Cheater", font="Arial, 15", command=lambda: self.cheater(True, self.track.running)).pack(padx=20, pady=5)
        Button(master, text="Be Innocent", font="Arial, 15", command=lambda: self.cheater(False, self.track.running)).pack(padx=20, pady=5)

    def cheater(self, cheater, is_program_running):
        if is_program_running:
            # todo: alert user that they aren't allowed to switch cheating configs after they start
            print("ERROR: Cannot switch while program is running!")
            return

        if cheater:
            print('Switched to Cheater')
            self.cheating.set("You are now CHEATING")
            self.is_cheater = True
        else:
            print('Switched to Innocent')
            self.cheating.set("You are now INNOCENT")
            self.is_cheater = False

    @staticmethod
    def start_interface():
        # logs when program starts
        MouseTracker.get_screen_size()

    def start_program(self, start=True):
        if start:
            # if program is already running, ignore user input
            if self.track.running:
                print('Program is already running!')
                return

            # start new instance of MouseTracker() every time
            self.track = MouseTracker(self.is_cheater)
            print('Program started')
            self.status.set("Status: ON")
            self.track.create_file()
            self.track.main()
            self.track.running = True
        else:
            print('Program Stopped')
            self.status.set("Status: OFF")
            self.track.main(False)
            self.track.running = False

            # log remaining data
            self.track.write_to_csv(self.track.saved_mouse_pos)

    # creates main window
    @staticmethod
    def main():
        window = Tk()

        # window styling
        window.title('Mouse Logger')
        """
        # todo: add window icon (not high priority)
        ## icon in top-left
        photo = PhotoImage(file='./Images/Mouse_icon_vector.png')
        window.wm_iconphoto(False, photo)
        """


if __name__ == '__main__':
    # start interface
    root = Tk()
    root.resizable(height=None, width=None)  # prevents window from being resized
    app = Interface(root)

    app.start_interface()

    root.mainloop()
