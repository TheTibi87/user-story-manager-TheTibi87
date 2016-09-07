from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template

username = "tiborkiss"
password = "TheTibi87"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + username + ':' + password + '@localhost/Flask'
# app.run(debug=True)
db = SQLAlchemy(app)


class Form_Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    story_title = db.Column(db.String(50), unique=True)
    user_story = db.Column(db.String(500), unique=True)
    acceptance_criteria = db.Column(db.String(500))
    business_value = db.Column(db.Integer)
    estimation = db.Column(db.Float)
    status = db.Column(db.String(10))

    def __init__(self, story_title, user_story, acceptance_criteria, business_value, estimation, status):
        self.story_title = story_title
        self.user_story = user_story
        self.acceptance_criteria = acceptance_criteria
        self.business_value = business_value
        self.estimation = estimation
        self.status = status

    def __repr__(self):
        return '<Form_Page%r>' % self.story_title


@app.route('/')
def starting_page():
    return render_template('form.html')


@app.route('/story', methods=['POST'])
def save_data():
    form_page = Form_Page(request.form['story_title'], request.form['user_story'], request.form['acceptance_criteria'],
    request.form['business_value'], request.form['estimation'], request.form['status'])
    db.session.add(form_page)
    db.session.commit()
    return redirect(url_for('list_stories'))


@app.route('/story/<story_id>', methods=['GET'])
def edit_page(story_id):
    queried_story = Form_Page.query.filter_by(id=story_id).first()
    return render_template('edit_page.html', queried_story=queried_story)



# @app.route('/ and /list', methods=['GET'])
# def update(story_id):
#     update_story = Form_Page.query.filter_by(id=story_id).first()
#     return render_template('list.html', all_story=all_story)


@app.route('/ and /list', methods=['GET'])
def list_stories():
    all_story = Form_Page.query.all()
    return render_template('list.html', all_story=all_story)


@app.route('/delete/<story_id>', methods=['GET'])
def delete_stories(story_id):
    delete_story = Form_Page.query.filter_by(id=story_id).first()
    db.session.delete(delete_story)
    db.session.commit()
    return redirect(url_for('list_stories'))


if __name__ == "__main__":
    app.run(debug=True)
