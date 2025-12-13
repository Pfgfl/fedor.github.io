import tkinter
import tkinter.ttk
import tkinter.messagebox
from tkinter import Entry


class Application(tkinter.ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master.title('calculator')
        self.master.geometry('300x200')
        self.master.resizable(False, False)
    def create_widgets(self):
        self.a = tkinter.StringVar()
        self.b = tkinter.StringVar()

        self.entry_a = tkinter.ttk.Entry(self, textvariable=self.a)
        self.entry_a.pack()

        self.entry_b = tkinter.ttk.Entry(self, textvariable=self.b)
        self.entry_b.pack()

        self.place_result = Entry(self, width=24, state='readonly')
        self.place_result.pack()

        self.Btnplus = tkinter.ttk.Button(self, text = '+')
        self.Btnplus.bind('<ButtonRelease>', self.plus)
        self.Btnplus.pack()
        self.Btnminus = tkinter.ttk.Button(self, text = '-')
        self.Btnminus.bind('<ButtonRelease>', self.minus)
        self.Btnminus.pack()
    def plus(self, evt):
        try:
            result = int(self.a.get()) + int(self.b.get())
            self.place_result.config(state='normal')  # Разрешаем редактирование
            self.place_result.delete(0, 'end')  # Очищаем поле
            self.place_result.insert(0, str(result))  # Вставляем результат
            self.place_result.config(state='readonly')  # Возвращаем в состояние 'readonly'
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter valid integers.")
    def minus(self, evt):
        try:
            result = int(self.a.get()) - int(self.b.get())
            self.place_result.config(state='normal')  # Разрешаем редактирование
            self.place_result.delete(0, 'end')  # Очищаем поле
            self.place_result.insert(0, str(result))  # Вставляем результат
            self.place_result.config(state='readonly')  # Возвращаем в состояние 'readonly'
        except ValueError:
            tkinter.messagebox.showerror("Input Error", "Please enter valid integers.")

root = tkinter.Tk()
app = Application(master = root)
root.mainloop()

