from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time
import json
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)


def cur_time():
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    return dt


class ModelHelper(object):
    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


# 定义一个 Model，继承自 db.Model
class Blog(db.Model, ModelHelper):
    __tablename__ = 'blogs'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)
    # 定义关系
    user_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = cur_time()

    def comments(self):
        cs = Comment.query.filter_by(blog_id=self.id).all()
        return cs

    def username(self):
        un = User.query.filter_by(id=self.user_id).first().username
        return un

    def all_blogs(self):
        return Blog.query.all()

    def json(self):
        d = dict(
            id=self.id,
            content=self.content,
            user_id=self.user_id,
            created_time=self.created_time,
            username=self.username(),
        )
        return json.dumps(d, ensure_ascii=False)


class User(db.Model, ModelHelper):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.String())

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = cur_time()

    def blogs(self):
        bs = Blog.query.filter_by(user_id=self.id).all()
        return bs

    def valid(self):
        return len(self.username) > 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


class Comment(db.Model, ModelHelper):
    __tablename__ = 'comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.String())
    user_id = db.Column(db.Integer)
    blog_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = cur_time()

    def username(self):
        un = User.query.filter_by(id=self.user_id).first().username
        return un


def init_db():
    # 先 drop_all 删除所有数据库中的表
    # 再 create_all 创建所有的表
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    init_db()

