from flask import Flask

app = Flask(__name__)

@app.route('/api/medical_records/welcome')
def welcome_message():
    return 'Welcome to the Medical Records API!'

if __name__ == '__main__':
    app.run(debug=True)
