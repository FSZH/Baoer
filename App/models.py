from App.exts import db


# 文章分类表
class Classification(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    alias = db.Column(db.String(100))   # 别名
    keyword = db.Column(db.String(100))   # 关键字
    parentnode = db.Column(db.String(50))  # 父节点
    describe = db.Column(db.Text)  # 描述
    # 关系，关联文章
    contents = db.relationship('Content', backref='my_classification', lazy='dynamic')


# 博客文章表
class Content(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    text = db.Column(db.Text)  # 文本内容
    comment = db.Column(db.Integer, default=0)
    keyword = db.Column(db.String(50))
    describe = db.Column(db.Text)  # 描述
    label = db.Column(db.String(50), default='无')   # 标签
    img = db.Column(db.String(200))
    data = db.Column(db.DateTime)
    # 关联栏目外键
    classification = db.Column(db.Integer, db.ForeignKey(Classification.id))


# 用户表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), unique=True)
    passwd = db.Column(db.String(20))
    username = db.Column(db.String(20), unique=True)
    phone = db.Column(db.String(30))



