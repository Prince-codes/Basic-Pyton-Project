import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import csv

# Database Setup
conn = sqlite3.connect("employee_tasks.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Default admin user
cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    position TEXT NOT NULL,
    department TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    employee_id INTEGER,
    deadline TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('Pending', 'Completed', 'In Progress')),
    priority TEXT DEFAULT 'Medium',
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
)
""")
conn.commit()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        ttk.Label(root, text="Username:").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="Password:").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = ttk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        login_btn = ttk.Button(root, text="Login", command=self.check_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=10)

        root.bind("<Return>", lambda event: self.check_login())

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if cursor.fetchone():
            self.root.destroy()
            main_root = tk.Tk()
            app = EmployeeTaskApp(main_root)
            main_root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)

        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mouse wheel scrolling
        self.scrollable_frame.bind("<Enter>", lambda e: self._bind_to_mousewheel(canvas))
        self.scrollable_frame.bind("<Leave>", lambda e: self._unbind_from_mousewheel(canvas))

    def _bind_to_mousewheel(self, widget):
        widget.bind_all("<MouseWheel>", lambda e: widget.yview_scroll(-1 * int(e.delta / 120), "units"))

    def _unbind_from_mousewheel(self, widget):
        widget.unbind_all("<MouseWheel>")

class EmployeeTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee and Task Management")
        self.root.geometry("900x750")

        self.scrollable = ScrollableFrame(self.root)
        self.scrollable.pack(fill="both", expand=True)
        self.frame = self.scrollable.scrollable_frame

        self.create_ui()

    def create_ui(self):
        # EMPLOYEE SECTION
        ttk.Label(self.frame, text="Employees", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10, sticky="w")

        ttk.Label(self.frame, text="Name:").grid(row=1, column=0, sticky="e")
        self.emp_name = ttk.Entry(self.frame)
        self.emp_name.grid(row=1, column=1, sticky="w")

        ttk.Label(self.frame, text="Position:").grid(row=2, column=0, sticky="e")
        self.emp_position = ttk.Entry(self.frame)
        self.emp_position.grid(row=2, column=1, sticky="w")

        ttk.Label(self.frame, text="Department:").grid(row=3, column=0, sticky="e")
        self.emp_department = ttk.Entry(self.frame)
        self.emp_department.grid(row=3, column=1, sticky="w")

        ttk.Button(self.frame, text="Add Employee", command=self.add_employee).grid(row=4, column=0, columnspan=2, pady=10)

        self.emp_list = ttk.Treeview(self.frame, columns=("ID", "Name", "Position", "Department"), show="headings", height=8)
        for col in ("ID", "Name", "Position", "Department"):
            self.emp_list.heading(col, text=col)
        self.emp_list.grid(row=5, column=0, columnspan=2, padx=10)

        ttk.Button(self.frame, text="Delete Employee", command=self.delete_employee).grid(row=6, column=0, columnspan=2, pady=5)

        # TASK SECTION
        ttk.Label(self.frame, text="Tasks", font=("Arial", 14, "bold")).grid(row=7, column=0, columnspan=2, pady=15, sticky="w")

        ttk.Label(self.frame, text="Task Name:").grid(row=8, column=0, sticky="e")
        self.task_name = ttk.Entry(self.frame)
        self.task_name.grid(row=8, column=1, sticky="w")

        ttk.Label(self.frame, text="Assign To:").grid(row=9, column=0, sticky="e")
        self.task_emp = ttk.Combobox(self.frame)
        self.task_emp.grid(row=9, column=1, sticky="w")

        ttk.Label(self.frame, text="Deadline:").grid(row=10, column=0, sticky="e")
        self.task_deadline = DateEntry(self.frame, date_pattern="yyyy-mm-dd")
        self.task_deadline.grid(row=10, column=1, sticky="w")

        ttk.Label(self.frame, text="Status:").grid(row=11, column=0, sticky="e")
        self.task_status = ttk.Combobox(self.frame, values=["Pending", "In Progress", "Completed"], state="readonly")
        self.task_status.grid(row=11, column=1, sticky="w")
        self.task_status.set("Pending")

        ttk.Label(self.frame, text="Priority:").grid(row=12, column=0, sticky="e")
        self.task_priority = ttk.Combobox(self.frame, values=["Low", "Medium", "High"], state="readonly")
        self.task_priority.grid(row=12, column=1, sticky="w")
        self.task_priority.set("Medium")

        ttk.Button(self.frame, text="Add Task", command=self.add_task).grid(row=13, column=0, columnspan=2, pady=10)

        self.task_list = ttk.Treeview(self.frame, columns=("ID", "Task", "Employee", "Deadline", "Status", "Priority"), show="headings", height=8)
        for col in ("ID", "Task", "Employee", "Deadline", "Status", "Priority"):
            self.task_list.heading(col, text=col)
        self.task_list.grid(row=14, column=0, columnspan=2, padx=10)

        ttk.Button(self.frame, text="Delete Task", command=self.delete_task).grid(row=15, column=0, pady=5)
        ttk.Button(self.frame, text="Export Tasks to CSV", command=self.export_to_csv).grid(row=15, column=1, pady=5)

        self.load_employees()
        self.load_tasks()
        self.load_employee_dropdown()

    def load_employees(self):
        self.emp_list.delete(*self.emp_list.get_children())
        for emp in cursor.execute("SELECT * FROM employees").fetchall():
            self.emp_list.insert("", "end", values=emp)

    def load_tasks(self):
        self.task_list.delete(*self.task_list.get_children())
        for task in cursor.execute("""
            SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status, tasks.priority 
            FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id
        """).fetchall():
            self.task_list.insert("", "end", values=task)

    def load_employee_dropdown(self):
        employees = cursor.execute("SELECT id, name FROM employees").fetchall()
        self.task_emp['values'] = [f"{emp[0]} - {emp[1]}" for emp in employees]

    def add_employee(self):
        name, position, department = self.emp_name.get(), self.emp_position.get(), self.emp_department.get()
        if name and position and department:
            cursor.execute("INSERT INTO employees (name, position, department) VALUES (?, ?, ?)", (name, position, department))
            conn.commit()
            self.load_employees()
            self.load_employee_dropdown()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    def delete_employee(self):
        selected_item = self.emp_list.selection()
        if selected_item:
            emp_id = self.emp_list.item(selected_item)['values'][0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
                cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
                conn.commit()
                self.load_employees()
                self.load_employee_dropdown()

    def add_task(self):
        task_name = self.task_name.get()
        selected_emp = self.task_emp.get()
        deadline = self.task_deadline.get()
        status = self.task_status.get()
        priority = self.task_priority.get()

        if task_name and selected_emp and deadline and status and priority:
            emp_id = selected_emp.split(" - ")[0]
            cursor.execute("INSERT INTO tasks (task_name, employee_id, deadline, status, priority) VALUES (?, ?, ?, ?, ?)", 
                           (task_name, emp_id, deadline, status, priority))
            conn.commit()
            self.load_tasks()
            self.task_name.delete(0, tk.END)
            self.task_emp.set('')
            self.task_deadline.set_date('')
            self.task_status.set("Pending")
            self.task_priority.set("Medium")
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    def delete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item)['values'][0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                self.load_tasks()

    def export_to_csv(self):
        tasks = cursor.execute("""
            SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status, tasks.priority 
            FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id
        """).fetchall()
        with open("tasks_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Task", "Employee", "Deadline", "Status", "Priority"])
            writer.writerows(tasks)
        messagebox.showinfo("Export Successful", "Tasks exported to 'tasks_export.csv'")

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
