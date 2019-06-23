from . import web
from flask import render_template
from app.lib.verify_code import verify_code
from flask import jsonify
from flask import abort

@web.route('/test')
def test():
    return render_template('pending.html')


@web.route('/verify_code')
def verify_code_test():
    verify = verify_code()
    image = verify["image"]
    code = verify["code"]
    return render_template('me/verify_code_test.html', image=image, code=code)


@web.route('/t')
def template_test():
    return render_template('auth/register.html')

@web.route('/test02')
def test02():
    return jsonify(success=1)