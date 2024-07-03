import tkinter as tk
from tkinter import messagebox
import random
import pyttsx3

engine = pyttsx3.init()
engine.say("NIGGA WELCOME TO SLOT MACHINE")
engine.runAndWait()
'''RATE'''
rate = engine.getProperty
print(rate)
engine.setProperty('rate', 99)

  
# Constants
MAX_LINES = 3
MAX_BET = 100
MIN_BET = 1
ROWS = 3
COLS = 3

symbol_count = {
    "A": 2,
    "B": 4,
    "C": 6,
    "D": 8
}

symbol_value = {
    "A": 5,
    "B": 4,
    "C": 3,
    "D": 2
}

class SlotMachineApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Slot Machine")
        self.geometry("600x400")
        self.balance = 0

        self.create_widgets()

    def create_widgets(self):
        # Deposit frame
        self.deposit_frame = tk.Frame(self)
        self.deposit_frame.pack(pady=10)

        tk.Label(self.deposit_frame, text="Deposit Amount: $").grid(row=0, column=0)
        self.deposit_entry = tk.Entry(self.deposit_frame)
        self.deposit_entry.grid(row=0, column=1)
        tk.Button(self.deposit_frame, text="Deposit", command=self.deposit).grid(row=0, column=2)

        # Betting frame
        self.betting_frame = tk.Frame(self)
        self.betting_frame.pack(pady=10)

        tk.Label(self.betting_frame, text="Number of Lines: ").grid(row=0, column=0)
        self.lines_entry = tk.Entry(self.betting_frame)
        self.lines_entry.grid(row=0, column=1)

        tk.Label(self.betting_frame, text="Bet per Line: $").grid(row=1, column=0)
        self.bet_entry = tk.Entry(self.betting_frame)
        self.bet_entry.grid(row=1, column=1)

        tk.Button(self.betting_frame, text="Place Bet", command=self.place_bet).grid(row=2, columnspan=2)

        # Slot machine display
        self.slot_frame = tk.Frame(self)
        self.slot_frame.pack(pady=10)

        self.slot_labels = [[tk.Label(self.slot_frame, text="", font=("Helvetica", 24)) for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].grid(row=r, column=c, padx=10, pady=5)

        # Results display
        self.results_frame = tk.Frame(self)
        self.results_frame.pack(pady=10)

        self.results_label = tk.Label(self.results_frame, text="", font=("Helvetica", 16))
        self.results_label.pack()

    def deposit(self):
        amount = self.deposit_entry.get()
        if amount.isdigit():
            amount = int(amount)
            if amount > 0:
                self.balance += amount
                messagebox.showinfo("Deposit Successful", f"Deposited ${amount}. Current balance: ${self.balance}")
            else:
                messagebox.showerror("Invalid Deposit", "Deposit amount must be greater than 0.")
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def place_bet(self):
        lines = self.lines_entry.get()
        bet = self.bet_entry.get()

        if not lines.isdigit() or not bet.isdigit():
            messagebox.showerror("Invalid Input", "Please enter valid numbers for lines and bet.")
            return

        lines = int(lines)
        bet = int(bet)

        if not (1 <= lines <= MAX_LINES):
            messagebox.showerror("Invalid Lines", f"Number of lines must be between 1 and {MAX_LINES}.")
            return

        if not (MIN_BET <= bet <= MAX_BET):
            messagebox.showerror("Invalid Bet", f"Bet per line must be between ${MIN_BET} and ${MAX_BET}.")
            return

        total_bet = lines * bet
        if total_bet > self.balance:
            messagebox.showerror("Insufficient Balance", f"Total bet of ${total_bet} exceeds current balance of ${self.balance}.")
            return

        self.balance -= total_bet
        self.spin(lines, bet)

    def spin(self, lines, bet):
        columns = get_slot_machine_spin(ROWS, COLS, symbol_count)

        for r in range(ROWS):
            for c in range(COLS):
                self.slot_labels[r][c].config(text=columns[c][r])

        winnings, winning_lines = check_winnings(columns, lines, bet, symbol_value)
        self.balance += winnings

        result_message = f"You won ${winnings}.\n"
        if winning_lines:
            result_message += f"Winning lines: {', '.join(map(str, winning_lines))}."
        else:
            result_message += "No winning lines."

        self.results_label.config(text=result_message)
        messagebox.showinfo("Spin Result", result_message + f"\nCurrent balance: ${self.balance}")

def check_winnings(columns, lines, bet, values):
    winnings = 0
    winning_lines = []
    for line in range(lines):
        symbol = columns[0][line]
        for column in columns:
            symbol_to_check = column[line]
            if symbol != symbol_to_check:
                break
        else:
            winnings += values[symbol] * bet
            winning_lines.append(line + 1)
    return winnings, winning_lines

def get_slot_machine_spin(rows, cols, symbols):
    all_symbols = []
    for symbol, symbol_count in symbols.items():
        all_symbols.extend([symbol] * symbol_count)

    columns = []
    for _ in range(cols):
        column = []
        current_symbols = all_symbols[:]
        for _ in range(rows):
            value = random.choice(current_symbols)
            current_symbols.remove(value)
            column.append(value)
        columns.append(column)
    return columns

if __name__ == "__main__":
    app = SlotMachineApp()
    app.mainloop()






