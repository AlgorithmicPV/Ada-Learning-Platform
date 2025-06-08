from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def landing():
    return render_template('landing_page.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

if __name__ == '__main__':
    app.run(debug=True)
