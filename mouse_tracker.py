from pynput.mouse import Listener
from datetime import datetime
from time import *
import csv
from tkinter import *


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
    def __init__(self):
        self.current_date = datetime.now().strftime('%Y-%m-%dT%H.%M.%S')
        self.start_time = time()
        self.button_pressed = False
        self.is_mouse_pressed = False
        self.saved_mouse_pos = None  # saves mouse position for later logging
        self.break_loop = False
        self.last_mouse_pos = None

        # file logging
        self.file_name = f'./Logs/{self.current_date}_mouse_log.csv'
        self.Logger = Logger(self.file_name)

        # ensures that the logger is not logging unnecessary data
        self.last_time_stamp = 0
        self.last_entry = list(range(5))
        self.running = False  # checks if user wants to run program before logging
        self.time_last_moved = 0  # checks when mouse was last moved

    @staticmethod
    def get_screen_size():
        window = Tk()
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()

        # write to file
        with open('./Logs/device_information.txt', 'w') as file:
            print('Logging screen size')
            screen_size = f'Screen size: {width}, {height}'
            file.write(screen_size)

        # close tk window
        window.destroy()

    def get_time_elapsed(self):
        current_time = time()
        return current_time - self.start_time

    # check if mouse was clicked or held down
    def on_click(self, x, y, button, pressed):
        # if program is not running, do not log
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
        # if the program is not running, do not log
        if not self.running:
            return

        # if the current entry is the same as the last entry, do not log
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
        # make header row if file path doesn't exist
        with open(self.file_name, 'a', newline='') as file:
            csv.writer(file).writerow(
                ['Time Since Start of Test', 'Mouse X Position', 'Mouse Y Position', 'Mouse Button Clicked', 'Pressed']
            )

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
        self.track = MouseTracker()

        title = Label(text='Welcome to Mouse Logger', font=('Arial', 25))
        title.pack(pady=20, padx=20)

        # window title
        master.title("Mouse Logger")

        # text to tell user if program is active or not
        self.status = StringVar()
        self.status.set("Status: OFF")
        Label(master, textvariable=self.status, font="Arial, 15").pack(pady=5)

        # Create buttons to start the infinite loop
        Button(master, text="Start Tracking", font="Arial, 20", command=self.start_program).pack(padx=20, pady=5)
        Button(master, text="Stop Tracking", font="Arial, 20", command=self.stop_program).pack(padx=20, pady=5)

    def start(self):
        # logs when program starts
        self.track.get_screen_size()
        self.track.create_file()

    def start_program(self):
        print('Starting program')
        self.status.set("Status: ON")
        self.track.main()
        self.track.running = True

    def stop_program(self):
        print('Stopping program')
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

    app.start()

    root.mainloop()
