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

    Methods:
    - write(text: str, top: bool = True) -> None:
        Writes the specified text to the top or bottom row of the display.

        Parameters:
        - text (str): The text to be displayed.
        - top (bool): If True, write to the top row; otherwise, write to the bottom row.
    """
    def __init__(self, numbering_mode, cols, rows, pin_rw, pin_rs, pin_e, pins_data):
        self.rows = rows
        self.columns = cols
        self.grid = [[' ' for _ in range(self.columns)] for _ in range(self.rows)]
        self.lcd = CharLCD(numbering_mode=numbering_mode, 
                           cols=cols, rows=rows, 
                           pin_rw=pin_rw, pin_rs=pin_rs, pin_e=pin_e, pins_data=pins_data)
        
    def write(self, text, top=True):
        """
        Writes the specified text to the top or bottom row of the display.
        Truncates the text to a maximum of 16 characters.

        Parameters:
        - text (str): The text to be displayed.
        - top (bool): If True, write to the top row; otherwise, write to the bottom row.
        """
        self.lcd.clear()  # Clear the entire display

        # Truncate the text to a maximum of 16 characters
        truncated_text = text[:self.columns]

        row = 0 if top else 1
        if top:
            for i, char in enumerate(truncated_text):
                self.grid[row][i] = char
        else:
            top_text = ''.join(self.grid[0])
            bottom_text = truncated_text
            # Display both top and bottom row text
            self.lcd.write_string(top_text + '\n\r' + bottom_text)
            
        # Update the character grid
        for i, char in enumerate(truncated_text):
            self.grid[row][i] = char
