from flask import Flask, render_template, request, redirect
from entities.monster import Monster

app = Flask(__name__)


@app.route('/')
def index():
    monsters = Monster.get_all()
    return render_template('index.html', monsters=monsters)


@app.route('/monster', methods=['POST'])
def save_monster():
    monster = Monster(name=request.form['name'],
                      power=request.form['power'])
    monster.save()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
