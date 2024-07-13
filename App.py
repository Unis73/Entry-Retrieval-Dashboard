from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

file_path = "D:/Interlining Data.xlsx"
os.chmod(file_path, 0o666)  # Set permissions to read/write for all users

# Function to load data from the Excel file
def load_data():
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()  # Trim spaces from column names
    except FileNotFoundError:
        df = pd.DataFrame(columns=[
            "Indent Number", "Stage", "Customer", "Style", "Wash",
            "Content", "GSM", "Structure", "Count_Cons", "Type of construction",
            "Collar Skin", "Collar Patch", "Inner Collar", "Inner NB", "NB Patch",
            "Outer NB", "CF T P", "CF D P", "Top Cuff", "In cuff", "Top SP",
            "Inner SP", "Label Patch", "Moon Patch", "Welt", "Flap"
        ])
        df.to_excel(file_path, index=False)
    return df

# Function to save new data entry to the Excel file
def save_data(new_data):
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip()  # Trim spaces from column names
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
        df.to_excel(file_path, index=False)
    except PermissionError:
        flash("Permission denied: Ensure the file is not open", "danger")
    except Exception as e:
        flash(f"Error saving data: {e}", "danger")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
def save():
    new_data = {
        "Indent Number": request.form.get('indent_number'),
        "Stage": request.form.get('stage'),
        "Customer": request.form.get('customer'),
        "Style": request.form.get('style'),
        "Wash": request.form.get('wash'),
        "Content": request.form.get('content'),
        "GSM": request.form.get('gsm'),
        "Structure": request.form.get('structure'),
        "Count_Cons": request.form.get('count_cons'),
        "Type of construction": request.form.get('type_of_construction'),
        "Collar Skin": request.form.get('collar_skin'),
        "Collar Patch": request.form.get('collar_patch'),
        "Inner Collar": request.form.get('inner_collar'),
        "Inner NB": request.form.get('inner_nb'),
        "NB Patch": request.form.get('nb_patch'),
        "Outer NB": request.form.get('outer_nb'),
        "CF T P": request.form.get('cf_t_p'),
        "CF D P": request.form.get('cf_d_p'),
        "Top Cuff": request.form.get('top_cuff'),
        "In cuff": request.form.get('in_cuff'),
        "Top SP": request.form.get('top_sp'),
        "Inner SP": request.form.get('inner_sp'),
        "Label Patch": request.form.get('label_patch'),
        "Moon Patch": request.form.get('moon_patch'),
        "Welt": request.form.get('welt'),
        "Flap": request.form.get('flap')
    }
    save_data(new_data)
    flash("Data saved successfully!", "success")
    return redirect(url_for('index'))

@app.route('/retrieve', methods=['GET', 'POST'])
def retrieve():
    if request.method == 'POST':
        filters = {
            "Indent Number": request.form.get('indent_number_retrieve'),
            "Customer": request.form.get('customer_retrieve'),
            "Style": request.form.get('style_retrieve'),
            "Wash": request.form.get('wash_retrieve'),
            "Content": request.form.get('content_retrieve'),
            "GSM": request.form.get('gsm_retrieve'),
            "Structure": request.form.get('structure_retrieve'),
            "Type of construction": request.form.get('type_of_construction_retrieve')
        }
        filters = {k: v for k, v in filters.items() if v}
        
        df = load_data()
        filtered_df = df
        for key, value in filters.items():
            if key in ["Indent Number", "GSM"]:
                filtered_df = filtered_df.loc[filtered_df[key].astype(str) == value]
            else:
                filtered_df = filtered_df.loc[filtered_df[key] == value]

        if filtered_df.empty:
            flash("No matching records found.", "warning")
        else:
            return render_template('index.html', tables=[filtered_df.to_html(classes='data')], titles=filtered_df.columns.values)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
