import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database as db
from theme import create_styled_treeview, create_button, create_entry, create_label, create_labelframe, create_combobox


def auto_apply_rules(account_name):
    safe_name = db.sanitize_table_name(account_name)
    rules = db.get_category_rules()
    transactions = db.execute_query(f"SELECT description, category FROM {safe_name}", fetch=True) or []
    
    for trans_desc, trans_cat in transactions:
        for rule in rules:
            rule_applied_to = rule[2]
            rule_category = rule[3]
            
            if trans_cat == 'Delete':
                db.execute_query(
                    f"DELETE FROM {safe_name} WHERE description = ?",
                    (trans_desc,)
                )
            elif rule_applied_to == trans_desc and trans_cat == 'Please Select':
                db.execute_query(
                    f"UPDATE {safe_name} SET category = ? WHERE description = ?",
                    (rule_category, trans_desc)
                )


def auto_add_rule(rule_name, applied_to, category):
    if category == 'Please Select':
        messagebox.showwarning('Category Required', 'Please select a category for the rule')
    else:
        db.add_category_rule(rule_name, applied_to, category)


class CategoryRules(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        columns = ("ID", "Rule Name", "Matches Description", "Assigns Category")
        widths = (60, 150, 200, 150)
        tree_frame, self.tree = create_styled_treeview(main_container, columns, widths)
        tree_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        data_frame = create_labelframe(main_container, text="Rule Details")
        data_frame.pack(fill=X, pady=(0, 15))
        
        fields_container = ttk.Frame(data_frame)
        fields_container.pack(fill=X)
        
        create_label(fields_container, text="ID:").grid(row=0, column=0, padx=10, pady=8, sticky=E)
        self.id_entry = create_entry(fields_container, width=10, state='readonly')
        self.id_entry.grid(row=0, column=1, padx=10, pady=8, sticky=W)
        
        create_label(fields_container, text="Rule Name:").grid(row=0, column=2, padx=10, pady=8, sticky=E)
        self.name_entry = create_entry(fields_container, width=20)
        self.name_entry.grid(row=0, column=3, padx=10, pady=8, sticky=W)
        
        create_label(fields_container, text="Match Description:").grid(row=0, column=4, padx=10, pady=8, sticky=E)
        self.match_entry = create_entry(fields_container, width=25)
        self.match_entry.grid(row=0, column=5, padx=10, pady=8, sticky=W)
        
        create_label(fields_container, text="Category:").grid(row=0, column=6, padx=10, pady=8, sticky=E)
        self.category_combo = create_combobox(fields_container, width=18)
        self.category_combo.grid(row=0, column=7, padx=10, pady=8, sticky=W)
        self.category_combo.bind('<Button-1>', lambda e: self.update_category_options())
        
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=X)
        
        create_button(button_frame, text="Update Rule", command=self.update_record, bootstyle="info").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Delete Rule", command=self.remove_record, bootstyle="danger").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Clear Fields", command=self.clear_entries, bootstyle="secondary").pack(side=LEFT, padx=5)
        
        self.tree.bind("<ButtonRelease-1>", self.select_record)
        
        self.load_data()
    
    def update_category_options(self):
        self.category_combo['values'] = db.get_categories()
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = db.get_category_rules()
        
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(record[0], record[1], record[2], record[3]), tags=(tag,))
    
    def update_record(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a rule to update")
            
            db.update_category_rule(
                self.name_entry.get(),
                self.match_entry.get(),
                self.category_combo.get(),
                self.id_entry.get()
            )
            
            self.clear_entries()
            self.load_data()
            
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def remove_record(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a rule to delete")
            
            if messagebox.askyesno('Confirm Delete', 'Are you sure you want to delete this rule?'):
                db.delete_category_rule(self.id_entry.get())
                self.clear_entries()
                self.load_data()
                messagebox.showinfo('Deleted', 'Rule has been deleted')
                
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
        self.match_entry.insert(0, values[2])
        self.category_combo.set(values[3])
    
    def clear_entries(self):
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, END)
        self.id_entry.configure(state='readonly')
        self.name_entry.delete(0, END)
        self.match_entry.delete(0, END)
        self.category_combo.set('')
    
    def refresh(self):
        self.load_data()
    
    def refresh_cat_rules(self):
        self.refresh()
