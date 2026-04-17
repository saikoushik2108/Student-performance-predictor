from flask import Flask, render_template, request, jsonify
from model import create_model

app = Flask(__name__)
inference = create_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    result = inference.query(
        variables=['Performance'],
        evidence={
            'StudyHours': int(data['study']),
            'Attendance': int(data['attendance']),
            'Sleep': int(data['sleep']),
            'Motivation': int(data['motivation']),
            'PreviousGrades': int(data['grades'])
        }
    )

    return jsonify({
        'pass': round(float(result.values[0]), 3),
        'fail': round(float(result.values[1]), 3)
    })

if __name__ == '__main__':
    app.run(debug=True)