import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from datetime import datetime

tasks = []

def load_tasks():
    try:
        with open('tasks.txt', 'r') as tasks_file:
            for line in tasks_file:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    tasks.append({'task': parts[0], 'due': parts[1]})
    except FileNotFoundError:
        pass

def save_tasks():
    with open('tasks.txt', 'w') as tasks_file:
        for task in tasks:
            tasks_file.write(f"{task['task']}|{task['due']}\n")
        messagebox.showinfo('Tasks Saved!', 'Tasks saved!')

def refresh_listbox():
    for row in tree.get_children():
        tree.delete(row)
    try:
        sorted_tasks = sorted(tasks, key=lambda task: task['due'])
    except ValueError:
        sorted_tasks = tasks
    for task in sorted_tasks:
        tree.insert('', tk.END, values=(task['task'], task['due']), tags=('row',))


def add_task():
    task = simpledialog.askstring("New Task", "Enter task:")
    due = simpledialog.askstring("Due", "Enter due date(MM-DD-YYYY):")
    if task and due:
        tasks.append({'task': task, 'due': due})
        refresh_listbox()

def delete_task():
    selected = tree.selection()
    if selected:
        index = tree.index(selected[0])
        del tasks[index]
        refresh_listbox()

def on_closing():
    save_tasks()
    root.destroy()

# GUI
root = tk.Tk()
root.configure(bg='#f6f0fa')
root.title("🐾 My To-Do List")

style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", font=('Comic Sans MS', 11), padding=6.5)

style.layout("Treeview", [
    ('Treeview.treearea', {'sticky': 'nswe'})
])

style.configure("Treeview",
    background="#f6f0fa",

    foreground="black",
    fieldbackground="#f6f0fa",
    rowheight=30,
    font=('Comic Sans MS', 11),
    bordercolor='gray', relief='flat')


style.configure("Treeview.Heading",
    font=('Comic Sans MS', 12, 'bold'),
    background="#d1eaff",
    foreground="black")

style.map('Treeview', background=[('selected', '#cce7ff')])

title = ttk.Label(root, text="🐾 My To-Do List 🐾", anchor='center', background='#f6f0fa')
title.pack(pady=(15,5))

try:
    root.tk.call('tk', 'scaling', 1.0)
except:
    pass

canvas = tk.Canvas(root, width=360, height=250, bg='#f6f0fa', highlightthickness=0)
canvas.pack(pady=5)

canvas.create_rectangle(10, 10, 350, 240, outline='', fill='#f6f0fa', width=0)
frame = tk.Frame(canvas, bg='#f6f0fa')
canvas.create_window((180, 125), window=frame, anchor='center')

columns = ('Task', 'Due Date')
tree = ttk.Treeview(frame, columns=columns, show='headings', height=5)
tree.heading('Task', text='Task')
tree.heading('Due Date', text='Due Date')
tree.column('Task', anchor='w', width=220)
tree.column('Due Date', anchor='center', width=100)
tree.tag_configure('row', background='white', foreground='black')
tree.grid(row=0, column=0, columnspan=3, pady=5)

# buttons
ttk.Button(frame, text="Add Task", command=add_task).grid(row=1, column=0, padx=4, pady=5)
ttk.Button(frame, text="Delete Task", command=delete_task).grid(row=1, column=1, padx=4, pady=5)
ttk.Button(frame, text="Save Tasks", command=save_tasks).grid(row=1, column=2, padx=4, pady=5)

frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_columnconfigure(2, weight=1)

try:
    img = Image.open("catsleeping.png").resize((40, 40), Image.LANCZOS)
    catsleeping_img = ImageTk.PhotoImage(img)
    cat_label = tk.Label(root, image=catsleeping_img, bg='#f6f0fa')
    cat_label.image = catsleeping_img
    cat_label.pack(pady=(0, 5))
except Exception as e:
    print("Cat image failed to load:", e)

load_tasks()
refresh_listbox()

root.geometry("390x360")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
