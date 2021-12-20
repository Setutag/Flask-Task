import psycopg2 as p
from flask import Flask
from flask import redirect, render_template, abort


def get_data():
    con = p.connect(dbname='user_statistics', user='postgres',
                    password='w86799107', host='localhost')

    cr = con.cursor()

    cr.execute("SELECT * FROM tablet;")
    data = cr.fetchall()

    con.commit()
    con.close()

    all_data = []
    for record in data:
        all_data.append({'username': record[0], 'id': record[1], 'lvl': record[2], 'frac': record[3]})
    return all_data



info = get_data()

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/users/')


@app.route('/users/')
def users():
    clickers = []
    for record in get_data():
        clickers.append(['/users/{0}'.format(record['username']), record['username']])
    return render_template("list.html", data=clickers)

@app.route('/users/<username>')
def profile(username):
    usernames = []
    for record in get_data():
        usernames.append(record['username'])
    if username in usernames:
        i = usernames.index(username)
        return render_template("profile.html", data=get_data()[i])
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)
