import tkinter as tk
from tkinter import ttk
from forex_python.converter import CurrencyRates
from datetime import datetime
import tkcalendar
import tkinter.font as font
import tkinter.simpledialog as simpledialog

cr = CurrencyRates()



root = tk.Tk()
root.title("Currency Converter")

currencies = list(cr.get_rates("USD").keys())

class CalendarDialog(simpledialog.Dialog):
    def __init__(self, parent, title, date):
        self.result = None
        simpledialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        self.calendar = tkcalendar.Calendar(master)
        self.calendar.pack(expand=1, fill="both")
        return self.calendar

    def apply(self):
        self.result = self.calendar.get_date()

def show_calendar_dialog(parent, title, date):
    dlg = CalendarDialog(parent, title, date)
    if dlg.result:
        return dlg.result
    else:
        return None


def convert():
    amount = float(amount_entry.get())
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    
    date_input = date_entry.get()
    print(date_input)
    date = datetime.strptime(date_input, "%m/%d/%Y")
    date = date.strftime('%Y-%m-%d')
    print(date)
    date_obj = datetime.strptime(date, "%Y-%m-%d")


    result = cr.convert(from_currency, to_currency, amount, date_obj)
    result_label.config(text=f"{result:.2f} {to_currency}")

amount_label = ttk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10)

amount_entry = ttk.Entry(root)
amount_entry.grid(row=0, column=1, padx=10, pady=10)

from_currency_label = ttk.Label(root, text="From Currency:")
from_currency_label.grid(row=1, column=0, padx=10, pady=10)

from_currency_var = tk.StringVar()
from_currency_var.set("INR")
from_currency_menu = ttk.Combobox(root, textvariable=from_currency_var, values=currencies)
from_currency_menu.grid(row=1, column=1, padx=10, pady=10)

to_currency_label = ttk.Label(root, text="To Currency:")
to_currency_label.grid(row=2, column=0, padx=10, pady=10)

to_currency_var = tk.StringVar()
to_currency_var.set("USD")
to_currency_menu = ttk.Combobox(root, textvariable=to_currency_var, values=currencies)
to_currency_menu.grid(row=2, column=1, padx=10, pady=10)

date_label = ttk.Label(root, text="Date (YYYY-MM-DD):")
date_label.grid(row=3, column=0, padx=10, pady=10)

date_var = tk.StringVar()
date_var.set("Enter date")
date_entry = tk.Entry(root, textvariable=date_var, state="readonly")
date_entry.grid(row=3, column=1, padx=10, pady=10)

convert_button = ttk.Button(root, text="Convert", command=convert)
convert_button.grid(row=4, column=0, columnspan=2, pady=10)

result_label = ttk.Label(root)
result_label.grid(row=5, column=0, columnspan=2, pady=10)

def on_date_entry_click(event):
    date = show_calendar_dialog(root, "Select date", None)
    if date:
        date_obj = datetime.strptime(date, "%m/%d/%y")
        date_entry_str = "{}/{}/{}".format(date_obj.month, date_obj.day, date_obj.year)
        date_var.set(date_entry_str)
        #print("Selected date:", date_entry_str)
date_entry.bind("<FocusIn>", on_date_entry_click)

root.mainloop()
