from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    db.session.commit()


@app.route('/')
def index():
    return render_template("base.html")


@app.route('/post')
def post():
    articles = Article.query.order_by(Article.data.desc()).all()
    return render_template("post.html", articles=articles)

@app.route('/post/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)

@app.route('/post/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/post')
    except:
        return "Error 404"

@app.route('/post/<int:id>/edit', methods=['GET', 'POST'])
def post_edit(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.username = request.form['username']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/post')
        except:
            return "When you send an error has occurred"
    else:
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        username = request.form['username']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, username=username, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/create')
        except:
            return "When you send an error has occurred"
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)
