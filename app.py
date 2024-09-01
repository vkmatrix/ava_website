from flask import Flask, request, render_template, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("Home.html")

@app.route('/reportgen')
def reportgen():
    return render_template("Report Generation.html")

@app.route('/govtschemes')
def govtschemes():
    return render_template("schemes.html")

@app.route('/govtschemecheck')
def govtschemecheck():
    patient_id = request.args.get('patientID')
    
    if not patient_id:
        return jsonify({"error": "Patient ID is required"}), 400
    
    try:
        # Fetch patient data
        patient_response = requests.get(f'http://54.89.108.128:8000/patients/{patient_id}')
        patient_data = patient_response.json()
        
        # Check if patient data was found
        if 'error' in patient_data:
            return jsonify({"error": "Patient not found"}), 404
        
        # Extract patient attributes
        age = patient_data.get('Age')
        income = patient_data.get('Income')
        gender = patient_data.get('Gender')

        # Fetch government schemes
        schemes_response = requests.get('http://54.89.108.128:8000/govtschemes')
        schemes_data = schemes_response.json()
        
        eligible_schemes = []

        # Validate patient data against schemes
        for scheme in schemes_data:
            scheme_gender = scheme.get('Gender')
            scheme_lower_age = scheme.get('LowerAge')
            scheme_upper_age = scheme.get('UpperAge')
            scheme_lower_income = scheme.get('LowerIncome')
            scheme_upper_income = scheme.get('UpperIncome')

            if (age >= scheme_lower_age and age <= scheme_upper_age and
                (scheme_gender == 'All' or scheme_gender == gender) and
                (age < 18 or (income is not None and income >= scheme_lower_income and income <= scheme_upper_income))):
                eligible_schemes.append(scheme.get('SchemeName'))

        return jsonify(eligible_schemes)
    
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
