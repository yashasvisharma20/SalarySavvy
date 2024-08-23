from flask import Flask, request, render_template, jsonify
import joblib

app = Flask(__name__)

# Load the model
model = joblib.load('models/rfr.lb')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == "POST":
        try:
            # Input values
            age = int(request.form.get('age', ''))
            gender = request.form.get('gender', '')
            gender_male = 1 if gender == 'Male' else 0
            gender_female = 1 if gender == 'Female' else 0
            gender_other = 1 if gender == 'Other' else 0

            education_level = request.form.get('education_level', '')
            if education_level == 'High School':
                education_level_encoded = 1
            elif education_level == 'Bachelors':
                education_level_encoded = 2
            elif education_level == 'Masters':
                education_level_encoded = 3
            else:
                education_level_encoded = 0  # Default or unknown value

            year = int(request.form.get('year_of_experience', ''))
            job_role = request.form.get('job_role', '')
            job_roles = ['Content Marketing Manager', 'Data Analyst', 'Data Scientist','Digital Marketing Manager', 'Director of Data Science',
                         'Director of HR', 'Director of Marketing', 'Financial Analyst','Financial Manager', 'Front End Developer',
                         'Full Stack Engineer', 'Human Resources Coordinator','Human Resources Manager', 'Junior HR Coordinator','Junior HR Generalist', 
                         'Junior Marketing Manager','Junior Sales Associate', 'Junior Sales Representative','Junior Software Developer', 'Junior Software Engineer',
                         'Junior Web Developer', 'Marketing Analyst', 'Marketing Coordinator','Marketing Director', 'Marketing Manager', 'Operations Manager',
                         'Product Designer', 'Product Manager', 'Receptionist','Research Director', 'Research Scientist', 'Sales Associate','Sales Director', 
                         'Sales Executive', 'Sales Manager','Sales Representative', 'Senior Data Scientist', 'Senior HR Generalist','Senior Human Resources Manager', 
                         'Senior Product Marketing Manager','Senior Project Engineer', 'Senior Research Scientist', 'Senior Software Engineer', 'Software Developer',
                           'Software Engineer','Software Engineer Manager', 'Web Developer'
                         ]
            job_role_flags = [1 if job_role == jr else 0 for jr in job_roles]

            features = [age, gender_male, gender_female, gender_other, education_level_encoded, year] + job_role_flags

            # Make prediction
            prediction = round(model.predict([features])[0])


            # Render the result page with the prediction and input information
            return render_template('result.html', prediction=prediction, age=age, gender=gender, year_of_experience=year, job_role=job_role)
        
        except Exception as e:
            return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
