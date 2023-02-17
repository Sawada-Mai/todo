from flask import Flask, render_template, request, redirect 
#render_templateはHTMLを読み込む、 request、redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db' # todo.dbという名前のデータベースを作成
db = SQLAlchemy(app) #データベースを生成

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True) #整数値・主キー
    title = db.Column(db.String(30), nullable=False) #30字以内の文字列・空にするのはNG
    detail = db.Column(db.String(100)) # 100字以内の文字列・空でもOK
    due = db.Column(db.DateTime, nullable=False) # 日付型・期限空はNG

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        posts = Post.query.all() #データベースから全ての投稿を取り出す
        return render_template('index.html', posts = posts) #トップページに情報を渡す
    
    else:
        title = request.form.get('title') #入力したタイトルを変数に代入
        detail = request.form.get('detail') #入力した内容を変数に代入
        due = request.form.get('due') #入力した日付を変数に代入

        due = datetime.strptime(due, '%Y-%m-%d') #python上で文字列から日付型に変更
        new_post = Post(title=title, detail=detail, due=due) #データベース作成時に付けたクラス(Post)に受け取った内容を渡す

        db.session.add(new_post) #代入したnew_postをデータベースに追加
        db.session.commit()
        return redirect('/')

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/detail/<int:id>')
def read(id):
    post = Post.query.get(id) #該当するidの投稿内容を取得
    return render_template('detail.html', post=post) #detail.htmlに先程代入したpostを渡している

@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id) #該当するidの投稿内容を取得

    db.session.delete(post)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    post = Post.query.get(id)
    if request.method == 'GET':
        return render_template('update.html', post=post)
    else:
        post.title = request.form.get('title')
        post.detail = request.form.get('detail')
        post.due = datetime.strptime(request.form.get('due'), '%Y-%m-%d')

        db.session.commit()
        return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)