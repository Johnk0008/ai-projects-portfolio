from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def dashboard():
    nodes = [
        {'name': 'linux-node', 'status': 'online', 'load': '30%'},
        {'name': 'windows-node', 'status': 'offline', 'load': '0%'}
    ]
    return render_template('dashboard.html', nodes=nodes)

if __name__ == '__main__':
    app.run(debug=True)