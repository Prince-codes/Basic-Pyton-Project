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

class EmployeeTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee and Task Management")
        self.root.geometry("800x650")

        self.tab_control = ttk.Notebook(root)
        self.employee_tab = ttk.Frame(self.tab_control)
        self.task_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.employee_tab, text="Employees")
        self.tab_control.add(self.task_tab, text="Tasks")
        self.tab_control.pack(expand=1, fill="both")

        self.employees = []
        self.tasks = []

        self.create_task_tab()
        self.create_employee_tab()

        self.load_employees()
        self.load_tasks()
        self.load_employee_dropdown()

    def create_employee_tab(self):
        ttk.Label(self.employee_tab, text="Employee Name:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        self.emp_name = tk.Entry(self.employee_tab)
        self.emp_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.employee_tab, text="Position:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        self.emp_position = tk.Entry(self.employee_tab)
        self.emp_position.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.employee_tab, text="Department:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        self.emp_department = tk.Entry(self.employee_tab)
        self.emp_department.grid(row=2, column=1, padx=10, pady=5)

        self.add_emp_btn = ttk.Button(self.employee_tab, text="Add Employee", command=self.add_employee)
        self.add_emp_btn.grid(row=3, column=0, columnspan=2, pady=10)

        self.emp_list = ttk.Treeview(self.employee_tab, columns=("ID", "Name", "Position", "Department"), show="headings")
        for col in ("ID", "Name", "Position", "Department"):
            self.emp_list.heading(col, text=col)
        self.emp_list.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        self.del_emp_btn = ttk.Button(self.employee_tab, text="Delete Employee", command=self.delete_employee)
        self.del_emp_btn.grid(row=5, column=0, columnspan=2, pady=5)

    def load_employees(self):
        self.emp_list.delete(*self.emp_list.get_children())
        for emp in cursor.execute("SELECT * FROM employees").fetchall():
            self.emp_list.insert("", "end", values=emp)

    def load_tasks(self):
        self.task_list.delete(*self.task_list.get_children())
        for task in cursor.execute("SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status, tasks.priority FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id").fetchall():
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

    def create_task_tab(self):
        ttk.Label(self.task_tab, text="Task Name:").grid(row=0, column=0, padx=10, pady=5)
        self.task_name = tk.Entry(self.task_tab)
        self.task_name.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.task_tab, text="Assign To:").grid(row=1, column=0, padx=10, pady=5)
        self.task_emp = ttk.Combobox(self.task_tab)
        self.task_emp.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.task_tab, text="Deadline:").grid(row=2, column=0, padx=10, pady=5)
        self.task_deadline = DateEntry(self.task_tab, date_pattern='yyyy-mm-dd')
        self.task_deadline.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.task_tab, text="Status:").grid(row=3, column=0, padx=10, pady=5)
        self.task_status = ttk.Combobox(self.task_tab, values=["Pending", "In Progress", "Completed"], state='readonly')
        self.task_status.grid(row=3, column=1, padx=10, pady=5)
        self.task_status.set("Pending")

        ttk.Label(self.task_tab, text="Priority:").grid(row=4, column=0, padx=10, pady=5)
        self.task_priority = ttk.Combobox(self.task_tab, values=["Low", "Medium", "High"], state="readonly")
        self.task_priority.grid(row=4, column=1, padx=10, pady=5)
        self.task_priority.set("Medium")

        self.add_task_btn = ttk.Button(self.task_tab, text="Add Task", command=self.add_task)
        self.add_task_btn.grid(row=5, column=0, columnspan=2, pady=10)

        self.task_list = ttk.Treeview(self.task_tab, columns=("ID", "Task", "Employee", "Deadline", "Status", "Priority"), show="headings")
        for col in ("ID", "Task", "Employee", "Deadline", "Status", "Priority"):
            self.task_list.heading(col, text=col)
        self.task_list.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

        self.del_task_btn = ttk.Button(self.task_tab, text="Delete Task", command=self.delete_task)
        self.del_task_btn.grid(row=7, column=0, columnspan=2, pady=5)

        self.export_csv_btn = ttk.Button(self.task_tab, text="Export Tasks to CSV", command=self.export_to_csv)
        self.export_csv_btn.grid(row=8, column=0, columnspan=2, pady=5)

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
        tasks = cursor.execute("SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status, tasks.priority FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id").fetchall()
        with open("tasks_export.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Task", "Employee", "Deadline", "Status", "Priority"])
            writer.writerows(tasks)
        messagebox.showinfo("Export Successful", "Tasks exported to 'tasks_export.csv'")

if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()