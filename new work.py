# Enhanced Employee and Task Management App with Sorting, Export, Dark Mode, and More
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from datetime import date
import csv

# Database Setup
conn = sqlite3.connect("employee_tasks.db")
cursor = conn.cursor()

# Create Tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emp_id TEXT,
    name TEXT NOT NULL,
    date_of_joining TEXT,
    account_no TEXT,
    ifsc_code TEXT,
    id_type TEXT,
    id_no TEXT,
    contact_no TEXT,
    emp_mail TEXT,
    personal_mail TEXT,
    address TEXT,
    designation TEXT,
    skills TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_name TEXT NOT NULL,
    employee_id INTEGER,
    deadline TEXT,
    status TEXT NOT NULL CHECK(status IN ('Pending', 'Completed', 'In Progress')),
    project_id TEXT,
    description_id TEXT,
    quantity INTEGER,
    company_name TEXT,
    division_name TEXT,
    contact_person TEXT,
    task_date TEXT,
    completion_date TEXT,
    po_id TEXT,
    project_scope TEXT,
    team_members TEXT,
    extra_expenditure REAL,
    FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
)
""")

conn.commit()

cursor.execute("SELECT * FROM users WHERE username=?", ("admin",))
if not cursor.fetchone():
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("admin", "admin"))
    conn.commit()

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x300")

        ttk.Label(root, text="Username:").pack(pady=5)
        self.username_entry = ttk.Entry(root)
        self.username_entry.pack(pady=5)
        self.username_entry.focus()

        ttk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = ttk.Entry(root, show='*')
        self.password_entry.pack(pady=5)

        ttk.Button(root, text="Login", command=self.authenticate).pack(pady=10)

    def authenticate(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        if cursor.fetchone():
            self.root.destroy()
            main_app()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

class EmployeeTaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee and Task Management")
        self.root.geometry("1366x768")

        self.dark_mode = False              
        ttk.Button(self.root, text="Toggle Dark Mode", command=self.toggle_theme).pack(side="top", anchor="ne", padx=10, pady=5)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 9), padding=4)
        style.configure("TLabel", font=("Segoe UI", 9))
        style.configure("TEntry", font=("Segoe UI", 9))
        style.configure("TCombobox", font=("Segoe UI", 9))
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))
        style.configure("Treeview", rowheight=24, font=("Segoe UI", 9))

        self.tab_control = ttk.Notebook(root)
        self.employee_tab = ttk.Frame(self.tab_control)
        self.task_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(self.employee_tab, text="Employees")
        self.tab_control.add(self.task_tab, text="Tasks")
        self.tab_control.pack(expand=1, fill="both")

        self.selected_employee_id = None
        self.selected_task_id = None

        self.create_employee_tab()
        self.create_task_tab()

        self.load_employees()
        self.load_tasks()
        self.load_employee_dropdown()

    def add_placeholder(self, entry, text):
        entry.insert(0, text)
        entry.config(fg="grey")
        def on_focus_in(event):
            if entry.get() == text:
                entry.delete(0, tk.END)
                entry.config(fg="black")
        def on_focus_out(event):
            if not entry.get():
                entry.insert(0, text)
                entry.config(fg="grey")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def treeview_sort_column(self, tree, col, reverse):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        try:
            data.sort(key=lambda t: float(t[0]) if t[0].replace('.', '', 1).isdigit() else t[0], reverse=reverse)
        except Exception:
            data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        tree.heading(col, command=lambda: self.treeview_sort_column(tree, col, not reverse))

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        style = ttk.Style()
        if self.dark_mode:
            style.theme_use("clam")
            style.configure(".", background="#2e2e2e", foreground="white", fieldbackground="#2e2e2e")
            style.map("Treeview", background=[("selected", "#4a4a4a")])
        else:
            style.theme_use("clam")
            style.configure(".", background="SystemButtonFace", foreground="black", fieldbackground="white")

    def create_employee_tab(self):
        labels = [
            "Employee ID", "Employee Name", "Date Of Joining", "Account No", "IFSC Code",
            "ID Type", "ID No", "Contact No", "Employee Mail", "Personal Mail ID",
            "Address", "Designation", "Skills"
        ]
        self.emp_entries = {}
        for i, label in enumerate(labels):
            row = i // 2
            col = (i % 2) * 2
            ttk.Label(self.employee_tab, text=f"{label}:").grid(row=row+1, column=col, padx=5, pady=2, sticky='w')
            entry = tk.Entry(self.employee_tab, width=30)
            entry.grid(row=row+1, column=col+1, padx=5, pady=2)
            self.emp_entries[label] = entry

        ttk.Label(self.employee_tab, text="Search Employee:").grid(row=0, column=0, padx=5)
        self.emp_search_var = tk.StringVar()
        self.emp_search_var.trace_add("write", lambda *args: self.filter_employees())
        ttk.Entry(self.employee_tab, textvariable=self.emp_search_var).grid(row=0, column=1, padx=5)

        ttk.Button(self.employee_tab, text="Add/Update Employee", command=self.save_employee).grid(row=7, column=0, columnspan=2, pady=10)

        self.emp_list = ttk.Treeview(self.employee_tab, columns=["ID", *labels], show="headings", height=8)
        for col in ["ID", *labels]:
            self.emp_list.heading(col, text=col)
            self.emp_list.column(col, width=120, anchor="w")
        self.emp_list.grid(row=8, column=0, columnspan=4, padx=10, pady=5)
        self.emp_list.bind("<Double-1>", self.select_employee)

        ttk.Button(self.employee_tab, text="Delete Employee", command=self.delete_employee).grid(row=9, column=0, columnspan=4, pady=5)

    def create_task_tab(self):
        ttk.Label(self.task_tab, text="Task Name:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.task_name = tk.Entry(self.task_tab, width=30)
        self.task_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.task_tab, text="Assign To:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.task_emp = ttk.Combobox(self.task_tab, width=28)
        self.task_emp.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.task_tab, text="Deadline:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.task_deadline = DateEntry(self.task_tab, date_pattern='yyyy-mm-dd', width=28)
        self.task_deadline.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.task_tab, text="Status:").grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.task_status = ttk.Combobox(self.task_tab, values=["Pending", "In Progress", "Completed"], state='readonly', width=28)
        self.task_status.grid(row=4, column=1, padx=5, pady=5)
        self.task_status.set("Pending")

        ttk.Label(self.task_tab, text="Search Task:").grid(row=0, column=0, padx=5, sticky='w')
        self.task_search_var = tk.StringVar()
        self.task_search_var.trace_add("write", lambda *args: self.filter_tasks())
        ttk.Entry(self.task_tab, textvariable=self.task_search_var, width=30).grid(row=0, column=1, padx=5)

        ttk.Button(self.task_tab, text="Add/Update Task", command=self.save_task).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Button(self.task_tab, text="Export Tasks to CSV", command=self.export_tasks_csv).grid(row=6, column=0, columnspan=2, pady=5)

        self.task_list = ttk.Treeview(self.task_tab, columns=("ID", "Task", "Employee", "Deadline", "Status"), show="headings", height=10)
        for col in ("ID", "Task", "Employee", "Deadline", "Status"):
            self.task_list.heading(col, text=col)
            self.task_list.column(col, width=120, anchor="w")
        self.task_list.grid(row=7, column=0, columnspan=2, padx=10, pady=5)
        self.task_list.bind("<Double-1>", self.select_task)

        ttk.Button(self.task_tab, text="Delete Task", command=self.delete_task).grid(row=8, column=0, columnspan=2, pady=5)

    def filter_employees(self):
        keyword = self.emp_search_var.get().lower()
        self.emp_list.delete(*self.emp_list.get_children())
        for emp in cursor.execute("SELECT * FROM employees").fetchall():
            if any(keyword in str(field).lower() for field in emp):
                self.emp_list.insert("", "end", values=emp)

    def filter_tasks(self):
        keyword = self.task_search_var.get().lower()
        self.task_list.delete(*self.task_list.get_children())
        for task in cursor.execute("SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id").fetchall():
            if any(keyword in str(field).lower() for field in task):
                self.task_list.insert("", "end", values=task)

    def load_employees(self):
        self.emp_list.delete(*self.emp_list.get_children())
        for emp in cursor.execute("SELECT * FROM employees").fetchall():
            self.emp_list.insert("", "end", values=emp)

    def load_tasks(self):
        self.task_list.delete(*self.task_list.get_children())
        for task in cursor.execute("SELECT tasks.id, tasks.task_name, employees.name, tasks.deadline, tasks.status FROM tasks LEFT JOIN employees ON tasks.employee_id = employees.id").fetchall():
            self.task_list.insert("", "end", values=task)

    def load_employee_dropdown(self):
        employees = cursor.execute("SELECT id, name FROM employees").fetchall()
        self.task_emp['values'] = [f"{emp[0]} - {emp[1]}" for emp in employees]

    
    def save_employee(self):
        values = [e.get() for e in self.emp_entries.values()]
        if all(values):
            if self.selected_employee_id:
                cursor.execute("""
                    UPDATE employees SET emp_id=?, name=?, date_of_joining=?, account_no=?, ifsc_code=?, id_type=?, id_no=?,
                    contact_no=?, emp_mail=?, personal_mail=?, address=?, designation=?, skills=? WHERE id=?
                """, (*values, self.selected_employee_id))
            else:
                cursor.execute("INSERT INTO employees (emp_id, name, date_of_joining, account_no, ifsc_code, id_type, id_no, contact_no, emp_mail, personal_mail, address, designation, skills) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
            conn.commit()
            for e in self.emp_entries.values():
                e.delete(0, tk.END)
            self.selected_employee_id = None
            self.load_employees()
            self.load_employee_dropdown()
        else:
            messagebox.showwarning("Input Error", "All fields are required")

    
    def select_employee(self, event):
        selected = self.emp_list.selection()
        if selected:
            values = self.emp_list.item(selected)['values']
            self.selected_employee_id = values[0]
            for i, key in enumerate(self.emp_entries):
                self.emp_entries[key].delete(0, tk.END)
                self.emp_entries[key].insert(0, values[i+1])
    
    def delete_employee(self):
        selected = self.emp_list.selection()
        if selected:
            emp_id = self.emp_list.item(selected)['values'][0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?"):
                cursor.execute("DELETE FROM employees WHERE id = ?", (emp_id,))
                conn.commit()
                self.load_employees()
                self.load_employee_dropdown()
    
    def create_task_tab(self):
        task_tab = ttk.Frame(self.tab_control)
        self.tab_control.add(task_tab, text='Tasks')

        # ======= Task Form =======
        task_form_frame = ttk.LabelFrame(task_tab, text="Task Information", padding=10)
        task_form_frame.pack(padx=10, pady=10, fill="x")

        # --- Basic Info ---
        ttk.Label(task_form_frame, text="Task Name:").grid(row=0, column=0, sticky="w")
        self.task_name = ttk.Entry(task_form_frame)
        self.task_name.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Assigned Employee:").grid(row=0, column=2, sticky="w")
        self.task_emp = ttk.Combobox(task_form_frame, state="readonly")
        self.task_emp.grid(row=0, column=3, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Deadline:").grid(row=1, column=0, sticky="w")
        self.task_deadline = DateEntry(task_form_frame, width=12)
        self.task_deadline.grid(row=1, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(task_form_frame, text="Status:").grid(row=1, column=2, sticky="w")
        self.task_status = ttk.Combobox(task_form_frame, values=['Pending', 'Completed', 'In Progress'], state="readonly")
        self.task_status.set("Pending")
        self.task_status.grid(row=1, column=3, padx=5, pady=2, sticky="ew")

        # --- Project Details ---
        ttk.Label(task_form_frame, text="Project ID:").grid(row=2, column=0, sticky="w")
        self.task_project_id = ttk.Entry(task_form_frame)
        self.task_project_id.grid(row=2, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Description ID:").grid(row=2, column=2, sticky="w")
        self.task_description_id = ttk.Entry(task_form_frame)
        self.task_description_id.grid(row=2, column=3, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Quantity:").grid(row=3, column=2, sticky="w")
        self.task_quantity = ttk.Entry(task_form_frame)
        self.task_quantity.grid(row=3, column=3, padx=5, pady=2, sticky="ew")

        # --- Company Info ---
        ttk.Label(task_form_frame, text="Company Name:").grid(row=4, column=0, sticky="w")
        self.task_company_name = ttk.Entry(task_form_frame)
        self.task_company_name.grid(row=4, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Division Name:").grid(row=4, column=2, sticky="w")
        self.task_division_name = ttk.Entry(task_form_frame)
        self.task_division_name.grid(row=4, column=3, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Contact Person:").grid(row=5, column=0, sticky="w")
        self.task_contact_person = ttk.Entry(task_form_frame)
        self.task_contact_person.grid(row=5, column=1, padx=5, pady=2, sticky="ew")

        # --- Dates & PO ---
        ttk.Label(task_form_frame, text="Task Date:").grid(row=5, column=2, sticky="w")
        self.task_date = DateEntry(task_form_frame, width=12)
        self.task_date.grid(row=5, column=3, padx=5, pady=2, sticky="w")

        ttk.Label(task_form_frame, text="Completion Date:").grid(row=6, column=0, sticky="w")
        self.task_completion_date = DateEntry(task_form_frame, width=12)
        self.task_completion_date.grid(row=6, column=1, padx=5, pady=2, sticky="w")

        ttk.Label(task_form_frame, text="PO ID:").grid(row=6, column=2, sticky="w")
        self.task_po_id = ttk.Entry(task_form_frame)
        self.task_po_id.grid(row=6, column=3, padx=5, pady=2, sticky="ew")

        # --- Additional Info ---
        ttk.Label(task_form_frame, text="Project Scope:").grid(row=7, column=0, sticky="w")
        self.task_project_scope = ttk.Entry(task_form_frame)
        self.task_project_scope.grid(row=7, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Team Members:").grid(row=7, column=2, sticky="w")
        self.task_team_members = ttk.Entry(task_form_frame)
        self.task_team_members.grid(row=7, column=3, padx=5, pady=2, sticky="ew")

        ttk.Label(task_form_frame, text="Extra Expenditure:").grid(row=8, column=0, sticky="w")
        self.task_extra_expenditure = ttk.Entry(task_form_frame)
        self.task_extra_expenditure.grid(row=8, column=1, padx=5, pady=2, sticky="ew")

        # Stretch columns to fill space
        for col in range(4):
            task_form_frame.columnconfigure(col, weight=1)

        # === Buttons ===
        button_frame = ttk.Frame(task_tab)
        button_frame.pack(padx=10, pady=5, fill="x")

        ttk.Button(button_frame, text="Add Task", command=self.add_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Task", command=self.update_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Reset Form", command=self.reset_task_form).pack(side="left", padx=5)

        # === Treeview ===
        self.task_tree = ttk.Treeview(task_tab, columns=("Task Name", "Employee", "Deadline", "Status"), show="headings")
        for col in ("Task Name", "Employee", "Deadline", "Status"):
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, width=100)

        self.task_tree.pack(padx=10, pady=10, fill="both", expand=True)
        self.task_tree.bind("<<TreeviewSelect>>", self.select_task)

        self.refresh_task_tree()

    
    def save_task(self):
        task_name = self.task_name.get()
        selected_emp = self.task_emp.get()
        deadline = self.task_deadline.get()
        status = self.task_status.get()

        # New fields
        project_id = self.task_project_id.get()
        description_id = self.task_description_id.get()
        quantity = self.task_quantity.get()
        company_name = self.task_company_name.get()
        division_name = self.task_division_name.get()
        contact_person = self.task_contact_person.get()
        task_date = self.task_date.get()
        completion_date = self.task_completion_date.get()
        po_id = self.task_po_id.get()
        project_scope = self.task_project_scope.get()
        team_members = self.task_team_members.get()
        extra_expenditure = self.task_extra_expenditure.get()

        if not selected_emp or " - " not in selected_emp:
            messagebox.showwarning("Input Error", "Please select a valid employee.")
            return

        emp_id = selected_emp.split(" - ")[0]

        if task_name and emp_id and deadline and status:
            if self.selected_task_id:
                cursor.execute("""
                    UPDATE tasks SET task_name=?, employee_id=?, deadline=?, status=?,
                        project_id=?, description_id=?, quantity=?,
                        company_name=?, division_name=?, contact_person=?, task_date=?,
                        completion_date=?, po_id=?, project_scope=?, team_members=?, extra_expenditure=?
                    WHERE id=?""",
                    (task_name, emp_id, deadline, status,
                    project_id, description_id, quantity,
                    company_name, division_name, contact_person, task_date,
                    completion_date, po_id, project_scope, team_members, extra_expenditure,
                    self.selected_task_id)
                )
            else:
                cursor.execute("""
                    INSERT INTO tasks (
                        task_name, employee_id, deadline, status,
                        project_id, description_id, quantity,
                        company_name, division_name, contact_person, task_date,
                        completion_date, po_id, project_scope, team_members, extra_expenditure
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (task_name, emp_id, deadline, status,
                    project_id, description_id, quantity,
                    company_name, division_name, contact_person, task_date,
                    completion_date, po_id, project_scope, team_members, extra_expenditure)
                )

            conn.commit()
            self.reset_task_form()
            self.load_tasks()


    def select_task(self, event):
        selected = self.task_list.selection()
        if selected:
            values = self.task_list.item(selected)['values']
            if not values:
                return

            self.selected_task_id = values[0]

            self.task_name.delete(0, tk.END)
            self.task_name.insert(0, values[1])

            # Reconstruct "Employee ID - Name" format
            self.task_emp.set(f"{values[0]} - {values[2]}")  # You might want to map this better

            self.task_deadline.set_date(values[3])
            self.task_status.set(values[4])

            # New Fields
            self.task_project_id.delete(0, tk.END)
            self.task_project_id.insert(0, values[5])

            self.task_description_id.delete(0, tk.END)
            self.task_description_id.insert(0, values[6])

            self.task_quantity.delete(0, tk.END)
            self.task_quantity.insert(0, values[8])

            self.task_company_name.delete(0, tk.END)
            self.task_company_name.insert(0, values[9])

            self.task_division_name.delete(0, tk.END)
            self.task_division_name.insert(0, values[10])

            self.task_contact_person.delete(0, tk.END)
            self.task_contact_person.insert(0, values[11])

            self.task_date.set_date(values[12])
            self.task_completion_date.set_date(values[13])

            self.task_po_id.delete(0, tk.END)
            self.task_po_id.insert(0, values[14])

            self.task_project_scope.delete(0, tk.END)
            self.task_project_scope.insert(0, values[15])

            self.task_team_members.delete(0, tk.END)
            self.task_team_members.insert(0, values[16])

            self.task_extra_expenditure.delete(0, tk.END)
            self.task_extra_expenditure.insert(0, values[17])

    def add_task(self):
        task_data = (
            self.task_name.get(),
            self.task_emp.get(),
            self.task_deadline.get(),
            self.task_status.get(),
            self.task_project_id.get(),
            self.task_description_id.get(),
            self.task_quantity.get(),
            self.task_company_name.get(),
            self.task_division_name.get(),
            self.task_contact_person.get(),
            self.task_date.get(),
            self.task_completion_date.get(),
            self.task_po_id.get(),
            self.task_project_scope.get(),
            self.task_team_members.get(),
            self.task_extra_expenditure.get()
        )

        if not task_data[0]:  # Task Name is empty
            messagebox.showwarning("Input Error", "Please enter a Task Name.")
            return

        self.cursor.execute('''
            INSERT INTO tasks (
                task_name, assigned_employee, deadline, status,
                project_id, description_id, quantity,
                company_name, division_name, contact_person,
                task_date, completion_date, po_id,
                project_scope, team_members, extra_expenditure
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', task_data)

        self.conn.commit()
        self.refresh_task_tree()
        self.reset_task_form()



    def reset_task_form(self):
            self.task_name.delete(0, tk.END)
            self.task_emp.set('')
            self.task_deadline.set_date(date.today())
            self.task_status.set("Pending")

            for field in [
                self.task_project_id, self.task_description_id,
                self.task_quantity, self.task_company_name, self.task_division_name,
                self.task_contact_person, self.task_po_id,
                self.task_project_scope, self.task_team_members, self.task_extra_expenditure
            ]:
                field.delete(0, tk.END)

            self.task_date.set_date(date.today())
            self.task_completion_date.set_date(date.today())
            self.selected_task_id = None



    
    
    def update_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a task to update.")
            return

        task_id = self.task_tree.item(selected[0], 'values')[0]  # Assuming first column is task ID

        updated_data = (
            self.task_name.get(),
            self.task_emp.get(),
            self.task_deadline.get(),
            self.task_status.get(),
            self.task_project_id.get(),
            self.task_description_id.get(),
            self.task_quantity.get(),
            self.task_company_name.get(),
            self.task_division_name.get(),
            self.task_contact_person.get(),
            self.task_date.get(),
            self.task_completion_date.get(),
            self.task_po_id.get(),
            self.task_project_scope.get(),
            self.task_team_members.get(),
            self.task_extra_expenditure.get(),
            task_id
        )

        self.cursor.execute('''
            UPDATE tasks SET
                task_name = ?, assigned_employee = ?, deadline = ?, status = ?,
                project_id = ?, description_id = ?, quantity = ?,
                company_name = ?, division_name = ?, contact_person = ?,
                task_date = ?, completion_date = ?, po_id = ?,
                project_scope = ?, team_members = ?, extra_expenditure = ?
            WHERE id = ?
        ''', updated_data)

        self.conn.commit()
        self.refresh_task_tree()
        self.reset_task_form()

    
    def delete_task(self):
        selected_item = self.task_list.selection()
        if selected_item:
            task_id = self.task_list.item(selected_item)['values'][0]
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?"):
                cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
                self.load_tasks()



    def export_tasks_csv(self):
        file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file:
            with open(file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "ID", "Task", "Employee", "Deadline", "Status", "Project ID",
                    "Description ID", "Quantity", "Company Name",
                    "Division Name", "Contact Person", "Date", "Completion Date",
                    "PO ID", "Project Scope", "Team Members", "Extra Expenditure"
                ])
                for row in self.task_list.get_children():
                    writer.writerow(self.task_list.item(row)['values'])
            messagebox.showinfo("Export Successful", f"Tasks exported to {file}")



def main_app():
    root = tk.Tk()
    app = EmployeeTaskApp(root)
    root.mainloop()

if  __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()