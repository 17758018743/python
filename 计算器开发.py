import tkinter as tk
from tkinter import messagebox


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Python 强哥计算器")
        master.resizable(False, False)  # 禁止调整窗口大 小

        # 尝试设置应用程序图标（如果存在）
        try:
            master.iconbitmap("calculator.ico")
            print(f'good')
        except:
            print(f'no')
            pass  # 如果图标文件不存在，忽略错误

        # 创建显示区域
        self.display = tk.Entry(master, width=20, font=('Arial', 16), justify='right', bd=5)
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, ipady=5)
        self.display.insert(0, "0")

        # 初始化变量
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.reset_display = None

        # 创建按钮
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0)
        ]

        # 布置按钮
        for (text, row, col) in buttons:
            if text == 'C':
                cmd = self.clear
                bg = 'orange'
                col_span = 1
            elif text == '=':
                cmd = self.calculate
                bg = 'lightblue'
                col_span = 1
            elif text in '+-*/':
                cmd = lambda x=text: self.set_operation(x)
                bg = 'lightgray'
                col_span = 1
            else:
                cmd = lambda x=text: self.add_to_display(x)
                bg = 'white'
                col_span = 1

            btn = tk.Button(master, text=text, width=5, height=2,
                            command=cmd, bg=bg, font=('Arial', 12))
            btn.grid(row=row, column=col, columnspan=col_span, padx=2, pady=2, sticky="nsew")

        # 添加清除按钮（单独一行）
        clear_btn = tk.Button(master, text='Clear', height=2,
                              command=self.clear, bg='orange', font=('Arial', 12))
        clear_btn.grid(row=5, column=1, columnspan=3, padx=2, pady=2, sticky="nsew")

        # 绑定键盘事件
        master.bind('<Key>', self.key_press)
        self.display.focus_set()  # 设置焦点到输入框

    def key_press(self, event):
        key = event.char
        if key in '0123456789':
            self.add_to_display(key)
        elif key in '+-*/':
            self.set_operation(key)
        elif key == '.':
            self.add_to_display('.')
        elif key == '\r':  # Enter键
            self.calculate()
        elif key == '\x08' or key == '\x7f':  # Backspace或Delete键
            self.clear()

    def add_to_display(self, value):
        if self.reset_display:
            self.display.delete(0, tk.END)
            self.reset_display = False

        current = self.display.get()
        if current == "0" and value != '.':
            self.display.delete(0, tk.END)

        # 防止多个小数点
        if value == '.' and '.' in self.display.get():
            return

        self.display.insert(tk.END, value)

    def clear(self):
        self.display.delete(0, tk.END)
        self.display.insert(0, "0")
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.reset_display = False

    def set_operation(self, op):
        self.previous_input = self.display.get()
        self.operation = op
        self.reset_display = True

    def calculate(self):
        if self.operation is None:
            return

        self.current_input = self.display.get()

        try:
            if self.operation == '+':
                result = float(self.previous_input) + float(self.current_input)
            elif self.operation == '-':
                result = float(self.previous_input) - float(self.current_input)
            elif self.operation == '*':
                result = float(self.previous_input) * float(self.current_input)
            elif self.operation == '/':
                if float(self.current_input) == 0:
                    messagebox.showerror("错误", "不能除以0!")
                    self.clear()
                    return
                else:
                    result = float(self.previous_input) / float(self.current_input)

            # 格式化结果（如果是整数，显示为整数；否则显示小数）
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display.delete(0, tk.END)
            self.display.insert(0, str(result))
            self.reset_display = True
            self.operation = None

        except ValueError:
            messagebox.showerror("错误", "无效的计算!")
            self.clear()


# 创建主窗口并运行应用
if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)

    root.mainloop()
