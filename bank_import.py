from ofxtools.Parser import OFXTree
import pandas as pd
from tkinter.filedialog import askopenfile, askopenfilename
from tkinter import messagebox
import database as db
from category_rules import auto_apply_rules


def add_bank_statement(account_name):
    current_records = db.get_bank_statement_data(account_name)
    
    curr_trans = [[r[1], r[2], r[3]] for r in current_records]
    
    select = db.get_ofx_csv_setting()
    
    try:
        if select == 1:
            options = db.get_options()
            if options:
                opt = options[0]
                date_col = opt[1]
                amount_col = opt[2]
                desc_col = opt[3]
            else:
                raise Exception("Please configure CSV column settings first")
            
            file = askopenfile(
                title='Select CSV Bank Statement', 
                initialdir='/', 
                filetypes=(('CSV files', '*.csv'),)
            )
            
            if not file:
                messagebox.showinfo('Cancelled', 'No file selected')
                return
            
            df = pd.read_csv(file)
            df_filter = df.iloc[:, [date_col, desc_col, amount_col]].values.tolist()
            
            new_trans = []
            for row in df_filter:
                new_trans.append([
                    str(row[0]), 
                    " ".join(str(row[1]).split()), 
                    str("{:.2f}".format(row[2]))
                ])
            
            added_count = 0
            for trans in new_trans:
                if trans not in curr_trans:
                    if trans[1] not in ('OPEN BALANCE', 'CLOSE BALANCE'):
                        db.add_transaction(account_name, trans[0], trans[1], trans[2])
                        added_count += 1
            
            auto_apply_rules(account_name)
            messagebox.showinfo('Success', f'Added {added_count} new transactions')
            
        else:
            file = askopenfilename(
                title='Select OFX Bank Statement', 
                initialdir='/', 
                filetypes=(('OFX files', '*.ofx'),)
            )
            
            if not file:
                messagebox.showinfo('Cancelled', 'No file selected')
                return
            
            ofx = OFXTree()
            ofx.parse(file)
            ofx_obj = ofx.convert()
            
            statement = ofx_obj.statements
            transactions = statement[0].transactions
            
            new_trans = []
            for trans in transactions:
                date = trans.dtposted.strftime("%Y-%m-%d").replace('-', '')
                description = trans.memo[:30] if trans.memo else ''
                amount = trans.trnamt
                
                new_trans.append([
                    str(date), 
                    " ".join(str(description).split()), 
                    str("{:.2f}".format(amount))
                ])
            
            added_count = 0
            for trans in new_trans:
                if trans not in curr_trans:
                    db.add_transaction(account_name, trans[0], trans[1], trans[2])
                    added_count += 1
            
            auto_apply_rules(account_name)
            messagebox.showinfo('Success', f'Added {added_count} new transactions')
    
    except IndexError:
        messagebox.showerror('Error', 'Please check that the correct columns are selected in Settings')
    
    except FileNotFoundError:
        messagebox.showinfo('No File', 'No bank statement imported')
    
    except Exception as e:
        messagebox.showerror('Error', str(e))
