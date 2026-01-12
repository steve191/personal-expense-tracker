import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import database as db
from theme import THEME_NAME, create_styled_treeview, create_button, create_entry, create_label, create_labelframe, configure_treeview_style
from categories import Categories
from category_rules import CategoryRules
from bank_statement_recon import BankStatementRecon
from accounts import Accounts


class Options(ttk.Frame):
    def __init__(self, parent, add_banks_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.add_banks_callback = add_banks_callback
        
        db.init_database()
        
        COLUMNS = {chr(65+i): i for i in range(26)}
        COLUMNS_LOOKUP = {v: k for k, v in COLUMNS.items()}
        
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=LEFT, fill=BOTH, padx=(0, 20))
        
        ofx_frame = create_labelframe(left_frame, text="Import Format")
        ofx_frame.pack(fill=X, pady=(0, 20))
        
        self.import_var = ttk.IntVar()
        
        format_container = ttk.Frame(ofx_frame)
        format_container.pack(pady=10)
        
        csv_radio = ttk.Radiobutton(
            format_container, 
            text="CSV Format", 
            variable=self.import_var, 
            value=1,
            command=lambda: db.update_ofx_csv_setting(1),
            bootstyle="primary-toolbutton"
        )
        csv_radio.pack(side=LEFT, padx=10)
        
        ofx_radio = ttk.Radiobutton(
            format_container, 
            text="OFX Format", 
            variable=self.import_var, 
            value=2,
            command=lambda: db.update_ofx_csv_setting(2),
            bootstyle="primary-toolbutton"
        )
        ofx_radio.pack(side=LEFT, padx=10)
        
        current_setting = db.get_ofx_csv_setting()
        self.import_var.set(current_setting if current_setting else 1)
        
        csv_frame = create_labelframe(left_frame, text="CSV Column Mapping")
        csv_frame.pack(fill=X)
        
        info_label = create_label(
            csv_frame, 
            text="Specify column letters (A, B, C, etc.) for each field:"
        )
        info_label.pack(pady=(0, 15))
        
        fields_frame = ttk.Frame(csv_frame)
        fields_frame.pack(fill=X)
        
        create_label(fields_frame, text="Date Column:").grid(row=0, column=0, padx=10, pady=8, sticky=E)
        self.date_entry = create_entry(fields_frame, width=10)
        self.date_entry.grid(row=0, column=1, padx=10, pady=8, sticky=W)
        
        create_label(fields_frame, text="Amount Column:").grid(row=1, column=0, padx=10, pady=8, sticky=E)
        self.amount_entry = create_entry(fields_frame, width=10)
        self.amount_entry.grid(row=1, column=1, padx=10, pady=8, sticky=W)
        
        create_label(fields_frame, text="Description Column:").grid(row=2, column=0, padx=10, pady=8, sticky=E)
        self.desc_entry = create_entry(fields_frame, width=10)
        self.desc_entry.grid(row=2, column=1, padx=10, pady=8, sticky=W)
        
        def save_csv_options():
            try:
                d = self.date_entry.get().upper()
                amt = self.amount_entry.get().upper()
                desc = self.desc_entry.get().upper()
                
                if d not in COLUMNS or amt not in COLUMNS or desc not in COLUMNS:
                    raise ValueError("Invalid column letter")
                
                db.update_options(COLUMNS[d], COLUMNS[amt], COLUMNS[desc])
                messagebox.showinfo('Saved', 'Column settings saved successfully!')
                
            except (KeyError, ValueError):
                messagebox.showerror('Error', 'Please use single letters (A-Z) only.')
        
        save_btn = create_button(csv_frame, text="Save Settings", command=save_csv_options)
        save_btn.pack(pady=15)
        
        options = db.get_options()
        if options:
            opt = options[0]
            self.date_entry.insert(0, COLUMNS_LOOKUP.get(opt[1], ''))
            self.amount_entry.insert(0, COLUMNS_LOOKUP.get(opt[2], ''))
            self.desc_entry.insert(0, COLUMNS_LOOKUP.get(opt[3], ''))
        
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=LEFT, fill=BOTH, expand=True)
        
        bank_frame = create_labelframe(right_frame, text="Bank Accounts")
        bank_frame.pack(fill=BOTH, expand=True)
        
        columns = ("ID", "Account Name")
        widths = (60, 200)
        tree_frame, self.bank_tree = create_styled_treeview(bank_frame, columns, widths)
        tree_frame.pack(fill=BOTH, expand=True, pady=(0, 15))
        
        add_frame = ttk.Frame(bank_frame)
        add_frame.pack(fill=X)
        
        create_label(add_frame, text="New Account:").pack(side=LEFT, padx=(0, 10))
        self.account_entry = create_entry(add_frame, width=25)
        self.account_entry.pack(side=LEFT, padx=(0, 10))
        
        def add_bank_account():
            try:
                name = self.account_entry.get().strip()
                
                if not name:
                    raise Exception("Account name cannot be empty")
                if len(name) > 25:
                    raise Exception("Account name too long (max 25 characters)")
                
                account_name = ''.join(word.capitalize() if i > 0 else word.lower() 
                                       for i, word in enumerate(name.split()))
                
                db.add_bank_account(account_name)
                
                self.account_entry.delete(0, END)
                self.refresh()
                self.add_banks_callback()
                
            except Exception as error:
                messagebox.showerror('Error', str(error))
        
        add_btn = create_button(add_frame, text="Add Account", command=add_bank_account, bootstyle="success")
        add_btn.pack(side=LEFT)
        
        self.load_bank_accounts()
    
    def load_bank_accounts(self):
        for item in self.bank_tree.get_children():
            self.bank_tree.delete(item)
        
        accounts = db.get_bank_accounts()
        for i, acc in enumerate(accounts):
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.bank_tree.insert('', 'end', values=(i + 1, acc[0]), tags=(tag,))
    
    def refresh(self):
        self.load_bank_accounts()


class ExpenseTrackerApp:
    def __init__(self):
        self.root = ttk.Window(themename=THEME_NAME)
        self.root.title("Personal Expense Tracker")
        self.root.geometry("1100x650")
        self.root.minsize(900, 500)
        
        configure_treeview_style(ttk.Style())
        
        self.notebook = ttk.Notebook(self.root, bootstyle="dark")
        self.notebook.pack(expand=True, fill=BOTH, padx=10, pady=10)
        
        self.options_tab = Options(self.notebook, self.add_bank_tabs)
        self.categories_tab = Categories(self.notebook)
        self.rules_tab = CategoryRules(self.notebook)
        self.accounts_tab = Accounts(self.notebook)
        
        self.notebook.add(self.options_tab, text="  Settings  ")
        self.notebook.add(self.categories_tab, text="  Categories  ")
        self.notebook.add(self.rules_tab, text="  Auto-Sort Rules  ")
        self.notebook.add(self.accounts_tab, text="  Budget Summary  ")
        
        self.bank_tabs = {}
        self.bank_acc_created = []
        self.add_bank_tabs()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def add_bank_tabs(self):
        accounts = db.get_bank_accounts()
        
        for acc in accounts:
            name = acc[0]
            if name not in self.bank_acc_created:
                self.bank_acc_created.append(name)
                tab = BankStatementRecon(self.notebook, name)
                self.notebook.add(tab, text=f"  {name}  ")
                self.bank_tabs[name] = tab
    
    def on_tab_change(self, event):
        selected_idx = self.notebook.index('current')
        tab_name = self.notebook.tab(selected_idx, 'text').strip()
        
        if selected_idx == 0:
            self.options_tab.refresh()
        elif selected_idx == 2:
            self.rules_tab.refresh()
        elif selected_idx == 3:
            self.accounts_tab.refresh()
        elif selected_idx > 3 and tab_name in self.bank_tabs:
            self.bank_tabs[tab_name].refresh()
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.run()
