import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database as db
from theme import create_styled_treeview, create_button, create_entry, create_label, create_labelframe


class Categories(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        columns = ("ID", "Category", "Budget")
        widths = (60, 200, 120)
        tree_frame, self.tree = create_styled_treeview(main_container, columns, widths)
        tree_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        data_frame = create_labelframe(main_container, text="Category Details")
        data_frame.pack(fill=X, pady=(0, 15))
        
        fields_container = ttk.Frame(data_frame)
        fields_container.pack(fill=X)
        
        create_label(fields_container, text="ID:").grid(row=0, column=0, padx=10, pady=8, sticky=E)
        self.id_entry = create_entry(fields_container, width=10, state='readonly')
        self.id_entry.grid(row=0, column=1, padx=10, pady=8, sticky=W)
        
        create_label(fields_container, text="Category Name:").grid(row=0, column=2, padx=10, pady=8, sticky=E)
        self.name_entry = create_entry(fields_container, width=25)
        self.name_entry.grid(row=0, column=3, padx=10, pady=8, sticky=W)
        
        create_label(fields_container, text="Budget:").grid(row=0, column=4, padx=10, pady=8, sticky=E)
        self.budget_entry = create_entry(fields_container, width=15)
        self.budget_entry.grid(row=0, column=5, padx=10, pady=8, sticky=W)
        
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=X)
        
        create_button(button_frame, text="Add Category", command=self.add_record, bootstyle="success").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Update Selected", command=self.update_record, bootstyle="info").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Delete Selected", command=self.remove_record, bootstyle="danger").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Clear Fields", command=self.clear_entries, bootstyle="secondary").pack(side=LEFT, padx=5)
        
        self.tree.bind("<ButtonRelease-1>", self.select_record)
        
        self.load_data()
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = db.execute_query("SELECT rowid, * FROM category", fetch=True) or []
        
        for i, record in enumerate(records):
            budget = record[2] if record[2] != 'None' else '-'
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(record[0], record[1], budget), tags=(tag,))
    
    def add_record(self):
        try:
            name = self.name_entry.get().strip()
            budget = self.budget_entry.get().strip()
            
            if not name:
                raise Exception("Please enter a category name")
            
            if budget:
                int(budget)
                budget_val = budget
            else:
                budget_val = 'None'
            
            db.add_category(name, budget_val)
            self.clear_entries()
            self.load_data()
            
        except ValueError:
            messagebox.showerror('Error', 'Budget must be a number')
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def update_record(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a record to update")
            
            name = self.name_entry.get().strip()
            if name == 'Delete':
                raise Exception("The 'Delete' category cannot be modified")
            
            budget = self.budget_entry.get().strip()
            if budget and budget != '-' and budget != 'None':
                int(budget)
                budget_val = budget
            else:
                budget_val = 'None'
            
            db.update_category(name, budget_val, self.id_entry.get())
            self.clear_entries()
            self.load_data()
            
        except ValueError:
            messagebox.showerror('Error', 'Budget must be a number')
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def remove_record(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a record to delete")
            
            if self.name_entry.get() == 'Delete':
                raise Exception("The 'Delete' category cannot be removed")
            
            if messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this category?'):
                db.delete_category(self.id_entry.get())
                self.clear_entries()
                self.load_data()
                messagebox.showinfo('Deleted', 'Category has been deleted')
                
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def select_record(self, event):
        selected = self.tree.focus()
        if not selected:
            return
        
        values = self.tree.item(selected, 'values')
        if not values:
            return
        
        self.clear_entries()
        
        self.id_entry.configure(state='normal')
        self.id_entry.insert(0, values[0])
        self.id_entry.configure(state='readonly')
        self.name_entry.insert(0, values[1])
        self.budget_entry.insert(0, values[2])
    
    def clear_entries(self):
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, END)
        self.id_entry.configure(state='readonly')
        self.name_entry.delete(0, END)
        self.budget_entry.delete(0, END)


def get_cat_data():
    return db.get_categories()
