from flask import Blueprint, render_template, request, redirect, url_for, session
from App.models import *

blue = Blueprint('blog', __name__)


# 博客首页
@blue.route('/')
def user_index():
    contents = Content.query.all()
    classifications = Classification.query.all()
    return render_template('home/index.html', contents=contents, classifications=classifications)

# 首页搜索
@blue.route('/index/search/', methods=['GET', 'POST'])
def user_search():
    if request.method == 'POST':
        keywords = request.form.get('keyboard')
        # print(keywords)
        if Content.query.filter(Content.keyword==keywords).count():
            contents = Content.query.filter(Content.keyword==keywords)
            classifications = Classification.query.all()
            return render_template('home/index.html', contents=contents, classifications=classifications)
        elif Classification.query.filter(Classification.keyword == keywords).count():
            classifications = Classification.query.filter(Classification.keyword == keywords)
            # print(classifications)
            contents = []
            for classification in classifications:
                content = Classification.query.get(classification.id).contents
                contents.extend(content)
            classifications = Classification.query.all()
            return render_template('home/index.html', contents=contents, classifications=classifications)
        else:
            classifications = Classification.query.all()
            contents = Content.query.all()
            return render_template('home/index.html', contents=contents, classifications=classifications)
    else:
        classifications = Classification.query.all()
        contents = Content.query.all()
        return render_template('home/index.html', contents=contents, classifications=classifications)


# 首页分类搜索栏
@blue.route('/index/fenlei/<int:classificationid>')
def user_fenlei1(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/index.html', contents=contents, classifications=classifications)

# 关于我
@blue.route('/about/')
def user_about():
    classifications = Classification.query.all()
    return render_template('home/about.html', classifications=classifications)

# 留言
@blue.route('/gbook/')
def user_gbook():
    classifications = Classification.query.all()
    return render_template('home/gbook.html', classifications=classifications)

# 内容页
@blue.route('/info/')
def user_info():
    classifications = Classification.query.all()
    return render_template('home/info.html', classifications=classifications)

# 内容页2
@blue.route('/infopic/')
def user_infopic():
    classifications = Classification.query.all()
    return render_template('home/infopic.html', classifications=classifications)

# 我的日记
@blue.route('/list/')
def user_list():
    contents = Content.query.all()
    classifications = Classification.query.all()
    return render_template('home/list.html', contents=contents, classifications=classifications)

# 日记分类搜索
@blue.route('/list/fenlei/<int:classificationid>')
def user_fenlei2(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/list.html', contents=contents, classifications=classifications)

# 留言分类搜索
@blue.route('/index/fenlei/<int:classificationid>')
def user_fenlei3(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/index.html', contents=contents, classifications=classifications)

# 关于我分类搜索
@blue.route('/index/fenlei/<int:classificationid>')
def user_fenlei4(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/index.html', contents=contents, classifications=classifications)

# 内容页1分类搜索
@blue.route('/index/fenlei/<int:classificationid>')
def user_fenlei5(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/index.html', contents=contents, classifications=classifications)

# 内容页2分类搜索
@blue.route('/index/fenlei/<int:classificationid>')
def user_fenlei6(classificationid):
    classifications = Classification.query.all()
    contents = Classification.query.get(classificationid).contents
    return render_template('home/index.html', contents=contents, classifications=classifications)


# 我的相册
@blue.route('/share/')
def user_share():
    # contents = Content.query.all()
    # classifications = Classification.query.all()
    res = redirect(url_for('blog.user_share_page', page=1))
    # return render_template('admin/article.html', contents=contents, username=username)
    return res

# 我的相册分页
@blue.route('/share/<int:page>', methods=['GET', 'POST'])
def user_share_page(page):
    if not page:
        page = 1
    # page = int(request.args.get('page', 1))  # 页码，1 是设置默认打开是第一页
    # per_page = int(request.args.get('per_page', 3))  # 每页显示的个数
    # contents = Content.query.offset((page - 1) * per_page).limit(per_page)
    c = Content.query.paginate(page=page, per_page=8, error_out=False)
    # contents = c.items
    # contents = Content.query.all()
    # classifications = Classification.query.all()
    return render_template('home/share.html', contents=c)

# 后台登录
@blue.route('/admin/login/', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # 接收客户端提交的参数
        username = request.form.get('username')
        userword = request.form.get('userpwd')
        # 验证登录是否能成功
        if username == '刘先生' and userword == '123456':
            res = redirect(url_for('blog.admin_index'))  # 重定向到index.html
            # 设置session
            session["username"] = username
            return res
        return 'login failed'
    return render_template('admin/login.html')

# 后台退出登录
@blue.route('/admin/deletelogin/')
def delete_login():
    res = redirect(url_for('blog.admin_login'))
    # 删除session
    session.pop('username')
    return res

# 后台首页
@blue.route('/admin/index/')
def admin_index():
    # session获取
    count = len(Content.query.all())
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/index.html', username=username, count=count)

# 后台文章
@blue.route('/admin/article/', methods=['GET', 'POST'])
def admin_article():
    # contents = Content.query.all()
    username = session.get('username', '')
    if username == '':
        res1 = redirect(url_for('blog.admin_login'))
        return res1
    # classifications = Classification.query.all()
    res = redirect(url_for('blog.admin_article_page', page=1))
    # return render_template('admin/article.html', contents=contents, username=username)
    return res

# 后台文章分页
@blue.route('/admin/article/<int:page>', methods=['GET', 'POST'])
def admin_article_page(page):
    if not page:
        page = 1
    # page = int(request.args.get('page', 1))  # 页码，1 是设置默认打开是第一页
    # per_page = int(request.args.get('per_page', 3))  # 每页显示的个数
    # contents = Content.query.offset((page - 1) * per_page).limit(per_page)
    c = Content.query.paginate(page=page, per_page=6, error_out=False)
    # contents = c.items
    # contents = Content.query.all()
    username = session.get('username', '')
    # classifications = Classification.query.all()
    return render_template('admin/article.html', contents=c, username=username)

# 添加文章
@blue.route('/admin/add_article/', methods=['GET', 'POST'])
def admin_add_article():
    # contents = Content.query.all()
    classifications = Classification.query.all()
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    if request.method == 'POST' and request.form.get('title') and request.form.get('content'):
        # 接收客户端提交的参数
        c = Content()
        c.title = request.form.get('title')
        c.text = request.form.get('content')
        c.keyword = request.form.get('keywords')
        c.describe = request.form.get('describe')
        c.classification = request.form.get('category')
        c.label = request.form.get('tags')
        c.img = request.form.get('titlepic')
        c.data = request.form.get('time')
        db.session.add(c)
        db.session.commit()
        res = redirect(url_for('blog.admin_add_article'))
        return res
    return render_template('admin/add-article.html', classifications=classifications, username=username)


# 后台栏目
@blue.route('/admin/category/', methods=['GET', 'POST'])
def admin_category():
    # contents = Content.query.all()
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    classifications = Classification.query.all()
    if request.method == 'POST':
        # 接收客户端提交的参数
        c = Classification()
        c.name = request.form.get('name')
        c.alias = request.form.get('alias')
        c.keyword = request.form.get('keywords')
        c.describe = request.form.get('describe')
        c.parentnode = request.form.get('fid')  # 父节点
        db.session.add(c)
        db.session.commit()
        res = redirect(url_for('blog.admin_category'))
        return res
    return render_template('admin/category.html', classifications=classifications, username=username)

# 更新文章
@blue.route('/admin/update-article/<int:contentid>', methods=['GET', 'POST'])
def update_article(contentid):
    classifications = Classification.query.all()
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    c = Content.query.get(contentid)
    if request.method == 'POST':
        # 接收客户端提交的参数
        c.title = request.form.get('title')
        c.text = request.form.get('content')
        c.keyword = request.form.get('keywords')
        c.describe = request.form.get('describe')
        c.classification = request.form.get('category')
        c.label = request.form.get('tags')
        c.img = request.form.get('titlepic')
        c.data = request.form.get('time')
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        res = redirect(url_for('blog.admin_article'))
        return res
    return render_template('admin/update-article.html', classifications=classifications, contents=c, username=username)

# 删除文章
@blue.route('/admin/delete-article/<int:contentid>')
def delete_article(contentid):
    content = Content.query.get(contentid)
    try:
        db.session.delete(content)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    res = redirect(url_for('blog.admin_article'))
    return res

# 更新栏目
@blue.route('/admin/update-category/<int:classificationid>', methods=['GET', 'POST'])
def update_category(classificationid):
    c = Classification.query.get(classificationid)
    classifications = Classification.query.all()
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    if request.method == 'POST':
        # 接收客户端提交的参数
        c.name = request.form.get('name')
        c.alias = request.form.get('alias')
        c.keyword = request.form.get('keywords')
        c.describe = request.form.get('describe')
        c.parentnode = request.form.get('fid')  # 父节点
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        res = redirect(url_for('blog.admin_category'))
        return res
    return render_template('admin/update-category.html', classification=c, classifications=classifications, username=username)

# 删除栏目
@blue.route('/admin/delete-category/<int:classificationid>')
def delete_category(classificationid):
    classification = Classification.query.get(classificationid)
    try:
        db.session.delete(classification)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    res = redirect(url_for('blog.admin_category'))
    return res

# 后台公告
@blue.route('/admin/notice/')
def notice():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/notice.html', username=username)

# 后台增加公告
@blue.route('/admin/addnotice/')
def add_notice():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/add-notice.html', username=username)

# 后台评论
@blue.route('/admin/comment/')
def comment():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/comment.html', username=username)

# 后台其他
@blue.route('/admin/flink/')
def flink():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/flink.html', username=username)

# 后台其他友情链接
@blue.route('/admin/addflink/')
def add_flink():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/add-flink.html', username=username)

# 后台其他访问记录
@blue.route('/admin/loginlog/')
def loginlog():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/loginlog.html', username=username)

# 后台用户管理
@blue.route('/admin/manageuser/')
def manage_user():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/manage-user.html', username=username)

# 后台基本设置
@blue.route('/admin/setting/')
def setting():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/setting.html', username=username)

# 后台用户设置
@blue.route('/admin/readset/')
def readset():
    username = session.get('username', '')
    if username == '':
        res = redirect(url_for('blog.admin_login'))
        return res
    return render_template('admin/readset.html', username=username)

