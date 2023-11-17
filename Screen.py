from RPLCD.gpio import CharLCD
from typing import List

class Screen:
    """
    Represents a two-row display using the CharLCD library.

    Parameters:
    - numbering_mode (str): GPIO numbering mode for the CharLCD ('BOARD' or 'BCM').
    - cols (int): Number of columns in the display.
    - rows (int): Number of rows in the display.
    - pin_rw (int): GPIO pin for the Read/Write control.
    - pin_rs (int): GPIO pin for the Register Select control.
    - pin_e (int): GPIO pin for the Enable control.
    - pins_data (List[int]): List of GPIO pins for data communication.

    Attributes:
    - rows (int): Number of rows in the display.
    - columns (int): Number of columns in the display.
    - grid (List[List[str]]): Two-dimensional list representing the character grid.
    - lcd (CharLCD): CharLCD object for display control.
    - top_text (str): Default text for the top row.
    - bottom_text (str): Default text for the bottom row.

    Methods:
    - write(top_text: str = None, bottom_text: str = None) -> None:
        Writes the specified text to the top or bottom row of the display.
        If no text is provided, it uses the default values specified during initialization.
    - clear() -> None:
        Clears the display.
    """
    def __init__(self, numbering_mode, cols, rows, pin_rw, pin_rs, pin_e, pins_data):
        self.rows = rows
        self.columns = cols
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.lcd = CharLCD(numbering_mode=numbering_mode, 
                           cols=cols, rows=rows, 
                           pin_rw=pin_rw, pin_rs=pin_rs, pin_e=pin_e, pins_data=pins_data)
        
        self.top_text = "GENERATIVE"
        self.bottom_text = "AMBIENT MACHINE"

        self.lcd.clear()

    def write(self, top_text=None, bottom_text=None):
        # if strings are provided, truncate them; otherwise, use class attributes
        truncated_top_text = top_text[:16] if top_text is not None else self.top_text[:16]
        truncated_bottom_text = bottom_text[:16] if bottom_text is not None else self.bottom_text[:16]

        # save new messages 
        self.top_text = truncated_top_text
        self.bottom_text = truncated_bottom_text

        # build output message
        new_message = self.top_text + '\n\r' + self.bottom_text
        
        # print to LCD
        self.lcd.clear()
        self.lcd.write_string(new_message)

    def clear(self):
        self.lcd.clear()

    def show_cursor(self):
        self.lcd.cursor_mode = 'blink'

    def hide_cursor(self):
        self.lcd.cursor_mode = 'hide'

    def set_cursor(self, row):
        self.lcd.cursor_pos = (row, 15)


