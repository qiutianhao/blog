from flask import Flask

from routes import main as routes
from user import main as user_routes
from api import main as api_routes

app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = 'random string'
# 这一行是套路
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

app.register_blueprint(user_routes)
app.register_blueprint(routes, url_prefix='/blog')
app.register_blueprint(api_routes, url_prefix='/api')


@app.errorhandler(404)
def error404(e):
    return '404haha'


# 运行代码
# 默认端口是 5000
if __name__ == '__main__':
    app.run(debug=True)