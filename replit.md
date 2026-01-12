# Personal Expense Tracker

## Overview
A Python desktop application for managing personal income and expenses. Built with Python 3 and ttkbootstrap (modern Tkinter), it provides a modern dark-themed GUI to handle transactions, import bank statements, and manage budgets.

## Current State
- Repository imported from: https://github.com/Devon-GS/personal-expense-tracker
- Version: 4.0.0 (Modernized)
- Status: Active development

## Project Structure
- `main.py` - Main application entry point with modern tabbed interface
- `database.py` - Centralized database helper with connection pooling and parameterized queries
- `theme.py` - Modern UI theme configuration using ttkbootstrap
- `categories.py` - Category management with budget tracking
- `category_rules.py` - Auto-sorting rules for transactions
- `bank_import.py` - Bank statement import functionality (CSV/OFX)
- `bank_statement_recon.py` - Bank statement reconciliation and transaction management
- `accounts.py` - Budget summary and spending overview
- `init_database.py` - Database initialization wrapper

## Tech Stack
- **Language**: Python 3.11
- **GUI**: ttkbootstrap (modern Tkinter with dark "superhero" theme)
- **Database**: SQLite (local file: database.db)
- **Dependencies**: python-dateutil, pandas, ofxtools, ttkbootstrap, pillow

## Key Features
1. Import bank statements (CSV or OFX format)
2. Custom account categories for income/expenses
3. Auto-sorting rules for recurring transactions
4. Custom transaction entry
5. Budget management with visual status indicators
6. Multiple bank account support
7. Modern dark-themed UI

## Architecture Improvements (v4.0.0)
- Centralized database module with context managers
- Parameterized SQL queries (SQL injection prevention)
- Removed global variables in favor of instance attributes
- Consistent modern styling via theme module
- Improved code organization and separation of concerns

## Running the Application
Run via VNC desktop view: `python main.py`

## Building as Executable
See `BUILD.md` for instructions on compiling the app to a standalone Windows .exe file using PyInstaller.

## Recent Changes
- January 12, 2026: Major UI modernization with ttkbootstrap dark theme
- January 12, 2026: Code refactoring - centralized database operations, removed globals
- January 12, 2026: Initial import from GitHub repository
