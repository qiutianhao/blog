from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session

from models import User
from models import Blog
from models import Comment

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('blog', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/<username>')
def view(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        # b = Blog.query.all()
        # bs = Blog.query.filter_by(user_id=u.id).all()
        bs = u.blogs()
        return render_template('blog_view.html', blogs=bs)


@main.route('blog/add', methods=['POST'])
def add():
    u = current_user()
    if u is None:
        abort(401)
    else:
        form = request.form
        b = Blog(form)
        b.user_id = u.id
        b.save()
        return redirect(url_for('.view', username=u.username))


@main.route('/comment_add', methods=['POST'])
def comment_add():
    u = current_user()
    if u is not None:
        form = request.form
        c = Comment(form)
        c.user_id = u.id
        c.blog_id = form.get('blog_id')
        c.save()
        return redirect(url_for('.view', username=u.username))
    else:
        abort(401)
