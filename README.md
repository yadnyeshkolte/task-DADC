# task-DADC
Perform data analysis and create dashboards for better understanding.

## Run Dashboard

### Python Version
- Python 3.11+

### Install
```bash
pip install -r requirements.txt
```

### Start app
```bash
streamlit run app.py
```

### Data loading
The app expects `Kittchen PNL Data.xlsx - Sheet 1 - stores.csv` in the project root and reads it with `skiprows=1`.
You can also upload a CSV from the sidebar.
