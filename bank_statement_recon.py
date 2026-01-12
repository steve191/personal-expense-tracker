import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from dateutil import parser
import database as db
from theme import create_styled_treeview, create_button, create_entry, create_label, create_labelframe, create_combobox
from bank_import import add_bank_statement
from category_rules import auto_apply_rules


def date_changer(date, date_format=None):
    try:
        if date_format == 'display':
            return str(parser.parse(date).strftime('%Y-%m-%d'))
        else:
            return parser.parse(date).strftime('%Y%m%d')
    except (OverflowError, ValueError):
        return date


class BankStatementRecon(ttk.Frame):
    def __init__(self, parent, account_name, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.account_name = account_name
        
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        columns = ("ID", "Date", "Description", "Amount", "Category")
        widths = (50, 100, 250, 100, 150)
        tree_frame, self.tree = create_styled_treeview(main_container, columns, widths)
        tree_frame.pack(fill=BOTH, expand=True, pady=(0, 20))
        
        data_frame = create_labelframe(main_container, text="Transaction Details")
        data_frame.pack(fill=X, pady=(0, 15))
        
        row1 = ttk.Frame(data_frame)
        row1.pack(fill=X, pady=5)
        
        create_label(row1, text="ID:").pack(side=LEFT, padx=(0, 5))
        self.id_entry = create_entry(row1, width=8, state='readonly')
        self.id_entry.pack(side=LEFT, padx=(0, 20))
        
        create_label(row1, text="Date (YYYY-MM-DD):").pack(side=LEFT, padx=(0, 5))
        self.date_entry = create_entry(row1, width=15)
        self.date_entry.pack(side=LEFT, padx=(0, 20))
        
        create_label(row1, text="Description:").pack(side=LEFT, padx=(0, 5))
        self.desc_entry = create_entry(row1, width=30)
        self.desc_entry.pack(side=LEFT, padx=(0, 20))
        
        create_label(row1, text="Amount:").pack(side=LEFT, padx=(0, 5))
        self.amount_entry = create_entry(row1, width=12)
        self.amount_entry.pack(side=LEFT)
        
        row2 = ttk.Frame(data_frame)
        row2.pack(fill=X, pady=5)
        
        create_label(row2, text="Category:").pack(side=LEFT, padx=(0, 5))
        self.category_combo = create_combobox(row2, width=20)
        self.category_combo.pack(side=LEFT)
        self.category_combo.bind('<Button-1>', lambda e: self.update_category_options())
        
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=X)
        
        create_button(button_frame, text="Import Statement", command=self.import_statement, bootstyle="primary").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Add Transaction", command=self.add_record, bootstyle="success").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Update", command=self.update_record, bootstyle="info").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Delete Selected", command=self.remove_one, bootstyle="danger").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Create Rule", command=self.add_rule, bootstyle="warning").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Delete All & Account", command=self.remove_all, bootstyle="danger-outline").pack(side=LEFT, padx=5)
        create_button(button_frame, text="Clear", command=self.clear_entries, bootstyle="secondary").pack(side=LEFT, padx=5)
        
        self.tree.bind("<ButtonRelease-1>", self.select_record)
        
        self.load_data()
        auto_apply_rules(account_name)
    
    def update_category_options(self):
        self.category_combo['values'] = db.get_categories()
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        records = db.get_bank_statement_data(self.account_name)
        
        for i, record in enumerate(records):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                record[0],
                date_changer(record[1], 'display'),
                record[2],
                record[3],
                record[4]
            ), tags=(tag,))
    
    def import_statement(self):
        add_bank_statement(self.account_name)
        self.load_data()
    
    def add_record(self):
        try:
            date = self.date_entry.get().strip()
            desc = self.desc_entry.get().strip()
            amount = self.amount_entry.get().strip()
            category = self.category_combo.get() or 'Please Select'
            
            if not date or not desc or not amount:
                raise Exception("Please fill out all required fields")
            
            if len(date) < 8 or len(date) > 10:
                raise Exception("Use date format: YYYY-MM-DD or YYYYMMDD")
            
            if category not in db.get_categories():
                category = 'Please Select'
            
            db.add_transaction(
                self.account_name,
                date_changer(date),
                desc,
                amount,
                category
            )
            
            self.clear_entries()
            self.load_data()
            
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def update_record(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a transaction to update")
            
            category = self.category_combo.get()
            if category != 'Please Select' and category not in db.get_categories():
                raise Exception("Selected category is not valid")
            
            db.update_transaction(
                self.account_name,
                date_changer(self.date_entry.get()),
                self.desc_entry.get(),
                self.amount_entry.get(),
                category,
                self.id_entry.get()
            )
            
            self.clear_entries()
            self.load_data()
            
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def remove_one(self):
        try:
            if not self.id_entry.get():
                raise Exception("Please select a transaction to delete")
            
            if messagebox.askyesno('Confirm Delete', 'Delete this transaction?'):
                db.delete_transaction(self.account_name, self.id_entry.get())
                self.clear_entries()
                self.load_data()
                messagebox.showinfo('Deleted', 'Transaction deleted')
                
        except Exception as error:
            messagebox.showerror('Error', str(error))
    
    def remove_all(self):
        if messagebox.showwarning('Warning', 'This will DELETE ALL transactions and REMOVE the bank account!'):
            if messagebox.askyesno('Confirm', 'Are you absolutely sure?'):
                db.delete_bank_account(self.account_name)
                self.destroy()
    
    def add_rule(self):
        if not self.desc_entry.get() or not self.category_combo.get():
            messagebox.showwarning('Required', 'Select a transaction first, then choose a category')
            return
        
        popup = ttk.Toplevel(self.winfo_toplevel())
        popup.title("Create Auto-Sort Rule")
        popup.geometry("350x150")
        popup.transient(self.winfo_toplevel())
        popup.grab_set()
        
        frame = ttk.Frame(popup, padding=20)
        frame.pack(fill=BOTH, expand=True)
        
        create_label(frame, text="Rule Name:").pack(anchor=W)
        name_entry = create_entry(frame, width=40)
        name_entry.pack(fill=X, pady=(5, 15))
        
        def save_rule():
            from category_rules import auto_add_rule
            auto_add_rule(name_entry.get(), self.desc_entry.get(), self.category_combo.get())
            auto_apply_rules(self.account_name)
            self.load_data()
            popup.destroy()
        
        create_button(frame, text="Save Rule", command=save_rule, bootstyle="success").pack()
    
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
        self.date_entry.insert(0, values[1])
        self.desc_entry.insert(0, values[2])
        self.amount_entry.insert(0, values[3])
        self.category_combo.set(values[4])
    
    def clear_entries(self):
        self.id_entry.configure(state='normal')
        self.id_entry.delete(0, END)
        self.id_entry.configure(state='readonly')
        self.date_entry.delete(0, END)
        self.desc_entry.delete(0, END)
        self.amount_entry.delete(0, END)
        self.category_combo.set('')
    
    def refresh(self):
        auto_apply_rules(self.account_name)
        self.load_data()
