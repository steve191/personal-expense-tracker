import ttkbootstrap as ttk
from ttkbootstrap.constants import *

THEME_NAME = "superhero"

COLORS = {
    'primary': '#4582ec',
    'secondary': '#adb5bd',
    'success': '#02b875',
    'info': '#17a2b8',
    'warning': '#f0ad4e',
    'danger': '#d9534f',
    'light': '#f8f9fa',
    'dark': '#343a40',
    'bg': '#0f1214',
    'fg': '#ffffff',
}

def configure_treeview_style(style):
    style.configure(
        "Treeview",
        rowheight=30,
        font=('Segoe UI', 10),
    )
    style.configure(
        "Treeview.Heading",
        font=('Segoe UI', 10, 'bold'),
    )
    
def create_styled_treeview(parent, columns, column_widths, show_scrollbar=True):
    frame = ttk.Frame(parent)
    
    tree = ttk.Treeview(
        frame, 
        columns=columns,
        show='headings',
        selectmode="browse",
        bootstyle="dark"
    )
    
    for col, width in zip(columns, column_widths):
        tree.heading(col, text=col, anchor=W)
        tree.column(col, width=width, anchor=W)
    
    if show_scrollbar:
        scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview, bootstyle="dark-round")
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
    
    tree.pack(side=LEFT, fill=BOTH, expand=True)
    
    tree.tag_configure('oddrow', background='#1a1d21')
    tree.tag_configure('evenrow', background='#252830')
    
    return frame, tree

def create_button(parent, text, command, bootstyle="primary", **kwargs):
    return ttk.Button(
        parent,
        text=text,
        command=command,
        bootstyle=bootstyle,
        padding=(15, 8),
        **kwargs
    )

def create_entry(parent, **kwargs):
    return ttk.Entry(parent, bootstyle="dark", **kwargs)

def create_label(parent, text, **kwargs):
    return ttk.Label(parent, text=text, **kwargs)

def create_labelframe(parent, text, **kwargs):
    return ttk.Labelframe(parent, text=text, bootstyle="primary", padding=15, **kwargs)

def create_combobox(parent, values=None, **kwargs):
    combo = ttk.Combobox(parent, bootstyle="dark", **kwargs)
    if values:
        combo['values'] = values
    return combo
