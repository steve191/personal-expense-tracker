import sqlite3
import os
import re
from contextlib import contextmanager

DATABASE_FILE = 'database.db'

def sanitize_table_name(name):
    """Validate and sanitize table names to prevent SQL injection.
    Only allows alphanumeric characters and underscores."""
    if not name or not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', name):
        raise ValueError(f"Invalid table name: {name}")
    if len(name) > 64:
        raise ValueError("Table name too long")
    reserved = {'select', 'insert', 'update', 'delete', 'drop', 'create', 
                'alter', 'table', 'from', 'where', 'and', 'or', 'not'}
    if name.lower() in reserved:
        raise ValueError(f"Reserved word cannot be used as table name: {name}")
    return name

@contextmanager
def get_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    try:
        yield conn
    finally:
        conn.close()

def execute_query(query, params=None, fetch=False, fetchone=False):
    with get_connection() as conn:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            result = cursor.fetchall()
        elif fetchone:
            result = cursor.fetchone()
        else:
            result = None
        
        conn.commit()
        return result

def execute_many(query, params_list):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.executemany(query, params_list)
        conn.commit()

def init_database(reinit=None):
    file = DATABASE_FILE
    
    if not os.path.exists(file) or reinit == 'reinit':
        with get_connection() as conn:
            c = conn.cursor()
            
            c.execute('''CREATE TABLE IF NOT EXISTS bankStatement (
                date TEXT,
                description TEXT,
                amount TEXT,
                category TEXT
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS options (
                id INTEGER, 
                date INTEGER, 
                amount INTEGER, 
                description INTEGER
            )''')
            
            if reinit != 'reinit':
                c.execute("INSERT INTO options VALUES (?, ?, ?, ?)", (0, 0, 0, 0))
            
            c.execute('''CREATE TABLE IF NOT EXISTS category (
                category TEXT, 
                budget TEXT
            )''')
            
            c.execute("SELECT * FROM category")
            records = c.fetchall()
            
            if len(records) == 0:
                category_list = ['Income', 'Entertainment Expense', 'Rates and Taxes', 'Fuel', 'Delete']
                for cat in category_list:
                    c.execute("INSERT INTO category VALUES (?, ?)", (cat, 'None'))
            
            c.execute('''CREATE TABLE IF NOT EXISTS categoryRules (
                ruleName TEXT, 
                appliedTo TEXT, 
                category TEXT
            )''')
            
            c.execute('''CREATE TABLE IF NOT EXISTS ofxCsv (
                id INTEGER, 
                selected INTEGER
            )''')
            
            if reinit != 'reinit':
                c.execute("INSERT INTO ofxCsv VALUES (?, ?)", (0, 0))
            
            c.execute("CREATE TABLE IF NOT EXISTS bankAccountNames (account TEXT)")
            
            conn.commit()

def get_categories():
    result = execute_query("SELECT category FROM category", fetch=True)
    return tuple(cat[0] for cat in result) if result else ()

def get_category_rules():
    return execute_query("SELECT rowid, * FROM categoryRules", fetch=True) or []

def get_bank_accounts():
    return execute_query("SELECT * FROM bankAccountNames", fetch=True) or []

def get_options():
    return execute_query("SELECT * FROM options", fetch=True) or []

def get_ofx_csv_setting():
    result = execute_query("SELECT selected FROM ofxCsv", fetchone=True)
    return result[0] if result else 0

def update_ofx_csv_setting(value):
    execute_query("UPDATE ofxCsv SET selected = ? WHERE id = ?", (value, 0))

def get_bank_statement_data(account_name):
    safe_name = sanitize_table_name(account_name)
    return execute_query(f"SELECT rowid, * FROM {safe_name}", fetch=True) or []

def add_category(category, budget='None'):
    execute_query("INSERT INTO category VALUES (?, ?)", (category.title(), budget))

def update_category(category, budget, oid):
    execute_query(
        "UPDATE category SET category = ?, budget = ? WHERE oid = ?",
        (category.title(), budget, oid)
    )

def delete_category(oid):
    execute_query("DELETE FROM category WHERE oid = ?", (oid,))

def add_category_rule(rule_name, applied_to, category):
    execute_query(
        "INSERT INTO categoryRules VALUES (?, ?, ?)",
        (rule_name, applied_to, category)
    )

def update_category_rule(rule_name, applied_to, category, oid):
    execute_query(
        "UPDATE categoryRules SET ruleName = ?, appliedTo = ?, category = ? WHERE oid = ?",
        (rule_name, applied_to, category, oid)
    )

def delete_category_rule(oid):
    execute_query("DELETE FROM categoryRules WHERE oid = ?", (oid,))

def add_bank_account(account_name):
    safe_name = sanitize_table_name(account_name)
    execute_query("INSERT INTO bankAccountNames VALUES (?)", (safe_name,))
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {safe_name} (
            date TEXT,
            description TEXT,
            amount TEXT,
            category TEXT
        )''')
        conn.commit()

def delete_bank_account(account_name):
    safe_name = sanitize_table_name(account_name)
    with get_connection() as conn:
        c = conn.cursor()
        c.execute(f"DROP TABLE IF EXISTS {safe_name}")
        c.execute("DELETE FROM bankAccountNames WHERE account = ?", (safe_name,))
        conn.commit()

def add_transaction(account_name, date, description, amount, category='Please Select'):
    safe_name = sanitize_table_name(account_name)
    execute_query(
        f"INSERT INTO {safe_name} VALUES (?, ?, ?, ?)",
        (date, description, amount, category)
    )

def update_transaction(account_name, date, description, amount, category, oid):
    safe_name = sanitize_table_name(account_name)
    execute_query(
        f"UPDATE {safe_name} SET date = ?, description = ?, amount = ?, category = ? WHERE oid = ?",
        (date, description, amount, category, oid)
    )

def delete_transaction(account_name, oid):
    safe_name = sanitize_table_name(account_name)
    execute_query(f"DELETE FROM {safe_name} WHERE oid = ?", (oid,))

def update_options(date_col, amount_col, desc_col):
    execute_query(
        "UPDATE options SET date = ?, amount = ?, description = ? WHERE id = ?",
        (date_col, amount_col, desc_col, 0)
    )

def get_all_transactions():
    bank_accounts = get_bank_accounts()
    all_records = []
    
    for acc in bank_accounts:
        acc_name = acc[0]
        safe_name = sanitize_table_name(acc_name)
        records = execute_query(f"SELECT amount, category FROM {safe_name}", fetch=True)
        if records:
            all_records.extend(records)
    
    return all_records

def get_all_categories_with_budget():
    return execute_query("SELECT * FROM category", fetch=True) or []
