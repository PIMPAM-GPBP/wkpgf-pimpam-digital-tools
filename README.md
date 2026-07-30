# World Bank WKPGF — PIM-PAM Digital Tools

A Python/Dash version of the Public Investment Management and Public Asset Management (PIM-PAM) site of World Bank - WKPGF.

## Files

- **`app.py`** — Main app: page routing, layouts, and all callbacks.
- **`utils.py`** — Reusable component builders (nav, footer, cards, drawers, etc.).
- **`constants.py`** — Design tokens, colors, and all site content/text.


## Setup (local)

1. **Create a virtual environment**:
```bash
   python -m venv venv
   source venv/bin/activate   # on Windows: venv\Scripts\activate
```
 
2. **Install dependencies:**
```bash
   pip install -r requirements.txt
```
 
3. **Run the app:**
```bash
   python app.py
```
 
4. **Open it in browser:**
```
   http://127.0.0.1:8050
```