# Personal Expense Tracker

## Overview
A Python desktop application for managing personal income and expenses. Built with Python 3 and Tkinter, it provides a GUI to handle transactions, import bank statements, and manage budgets.

## Current State
- Repository imported from: https://github.com/Devon-GS/personal-expense-tracker
- Version: 3.2.0-alpha
- Status: Ready for development

## Project Structure
- `main.py` - Main application entry point with Tkinter GUI
- `init_database.py` - Database initialization
- `categories.py` - Category management
- `category_rules.py` - Auto-sorting rules for transactions
- `bank_import.py` - Bank statement import functionality
- `bank_statement_recon.py` - Bank statement reconciliation
- `accounts.py` - Account management
- `options.py` - Application settings

## Tech Stack
- **Language**: Python 3.11
- **GUI**: Tkinter
- **Database**: SQLite (local file: database.db)
- **Dependencies**: python-dateutil, pandas, ofxtools

## Key Features
1. Import bank statements (CSV or OFX format)
2. Custom account categories for income/expenses
3. Auto-sorting rules for recurring transactions
4. Custom transaction entry
5. Budget management with alerts
6. Multiple bank account support

## Running the Application
Run via VNC desktop view: `python main.py`

## Recent Changes
- January 12, 2026: Initial import from GitHub repository
