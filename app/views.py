# -.- coding: UTF-8 -.-

from flask import render_template, url_for, flash, redirect, send_from_directory, session
from app import app
from service import list_images, list_all_images, find_image_path, get_batch_of_images, get_sort_image, filedups, zapp_image
from config import p_unsorted, p_public, p_reject

@app.before_request
def before_request():
    if not 'served' in session:
        session['served'] = 0;

@app.route('/index/')
@app.route('/')
def index():
    session['served'] += 1
    return render_template('main.html',
        title = 'fnordpad',
        images = get_batch_of_images(),
        )

@app.route('/duplicates/')
def duplicates():
    return render_template('main.html',
        title = 'duplicates',
        duplicates = filedups(),
        )

@app.route('/zapp/')
def zapp():
    zapp_image('filename')
    return redirect(url_for('duplicates'))

@app.route('/sort/')
@app.route('/sort/<filename>')
def sort(filename=None):
    if not filename:
        filename = get_sort_image()
    if not filename in list_all_images():
        filename = 'fnord.jpeg'
    return render_template('main.html',
        title = 'sortpad',
        sort = filename,
        text = filename,
        )

@app.route('/image/')
@app.route('/image/<filename>')
def image(filename=None):
    if not filename or not filename in list_all_images():
        filename = 'fnord.jpeg'
    return send_from_directory(find_image_path(filename), filename)

@app.errorhandler(404)
def internal_error(error):
    flash('I checked twice!')
    return render_template('404.html',
        title = '404',
        refreshing = True,
        ), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html',
        title = '500',
        refreshing = True,
        ), 500
