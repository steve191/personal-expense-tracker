import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import database as db
from theme import create_styled_treeview, create_labelframe


class Accounts(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        main_container = ttk.Frame(self, padding=20)
        main_container.pack(fill=BOTH, expand=True)
        
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=X, pady=(0, 20))
        
        title_label = ttk.Label(
            header_frame,
            text="Budget Summary",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(side=LEFT)
        
        columns = ("Category", "Total Spent", "Budget Limit", "Status")
        widths = (200, 120, 120, 100)
        tree_frame, self.tree = create_styled_treeview(main_container, columns, widths)
        tree_frame.pack(fill=BOTH, expand=True)
        
        self.tree.tag_configure('over', foreground='#d9534f')
        self.tree.tag_configure('within', foreground='#02b875')
        self.tree.tag_configure('no_budget', foreground='#adb5bd')
        
        self.load_data()
    
    def calculate_totals(self):
        all_transactions = db.get_all_transactions()
        all_categories = db.get_all_categories_with_budget()
        
        if not all_transactions:
            return None
        
        cat_totals = {}
        
        cat_totals["Please Select"] = [0.0, 'None']
        
        for cat, budget in all_categories:
            if cat not in cat_totals:
                cat_totals[cat] = [0.0, budget]
        
        for amount, category in all_transactions:
            if category not in cat_totals:
                cat_totals[category] = [0.0, 'None']
            
            try:
                if category == "Please Select":
                    cat_totals[category][0] += abs(float(amount))
                else:
                    cat_totals[category][0] += float(amount)
            except (ValueError, TypeError):
                pass
        
        if "Please Select" in cat_totals:
            cat_totals['Uncategorized'] = cat_totals.pop('Please Select')
        
        return dict(sorted(cat_totals.items()))
    
    def load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        data = self.calculate_totals()
        
        if not data:
            return
        
        for i, (category, values) in enumerate(data.items()):
            amount = values[0]
            budget = values[1]
            
            display_amount = abs(amount) if amount < 0 else amount
            display_amount = f"${display_amount:,.2f}"
            
            if budget == 'None':
                display_budget = '-'
                status = '-'
                row_tag = 'no_budget'
            else:
                display_budget = f"${float(budget):,.2f}"
                if abs(amount) < float(budget):
                    status = 'Within Budget'
                    row_tag = 'within'
                else:
                    status = 'OVER BUDGET'
                    row_tag = 'over'
            
            base_tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(category, display_amount, display_budget, status), tags=(base_tag,))
    
    def refresh(self):
        self.load_data()
