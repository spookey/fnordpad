# -.- coding: UTF-8 -.-

from flask import render_template, url_for, flash, redirect, send_from_directory, request, session, g
from app import app, logger
from service import list_images, list_all_images, find_image_path, uhr, datum, timestamp_now, json_status, get_batch_of_images, get_sort_image, move_image, filedups, zapp_image
from config import p_unsorted, p_public, p_reject, staticdir, i_default
from itertools import cycle

app.json = app.last_scrape = 0

@app.before_request
def before_request():
    if not 'served' in session:
        logger.info('set served images cookie')
        session['served'] = 0

scrolling = cycle(['It\'s Peanut Butter Jelly Time', 'Your ad here', 'This page intentionally left blank', 'Lorem ipsum dolor sit amet'])

@app.route('/index/')
@app.route('/')
def index():
    if timestamp_now()/60 - 20 >= app.last_scrape/60:
        app.json = json_status()
        app.last_scrape = timestamp_now()
    status = {
        'scroll': scrolling.next(),
        'served': session['served'],
        'avail': len(list_images(p_public)),
        'new': len(list_images(p_unsorted)),
        'uhr': uhr(),
        'datum': datum(),
        'json': app.json if isinstance(app.json, dict) else 0,
        }
    session['served'] += 23
    logger.info('/index requested')
    return render_template('main.html',
        title = 'fnordpad',
        images = get_batch_of_images(),
        status = status,
        )

@app.route('/duplicates/')
def duplicates():
    logger.info('/duplicates requested')
    return render_template('main.html',
        title = 'duplicates',
        duplicates = filedups(),
        )

@app.route('/zapp/<filename>')
def zapp(filename=None):
    if filename:
        zapp_image(filename)
    return redirect(url_for('duplicates'))

@app.route('/sort/', methods=['GET', 'POST'])
@app.route('/sort/<filename>', methods=['GET', 'POST'])
def sort(filename=None):
    logger.info('/sort requested')
    if request.method == 'POST':
        move_image(request.form)
    if not filename:
        filename = get_sort_image()
    if not filename in list_all_images():
        filename = i_default.split('/')[-1]
    flash('this: %s' %(filename))
    logger.info('this %s' %(filename))
    return render_template('main.html',
        title = 'sortpad',
        sort = filename,
        len_left = len(list_images(p_unsorted)),
        )

@app.route('/image/')
@app.route('/image/<filename>')
def image(filename=None):
    if not filename or not filename in list_all_images():
        logger.error('requested image not found: %s fallback to %s' %(filename, i_default.split('/')[-1]))
        filename = i_default.split('/')[-1]
    return send_from_directory(find_image_path(filename), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(staticdir, 'favicon.ico',
        mimetype='image/x-icon',
    )

@app.errorhandler(404)
def internal_error(error):
    logger.error('404: %s' %(error))
    logger.exception(error)
    flash('I checked twice!')
    return render_template('404.html',
        title = '404',
        error = True,
        ), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error('500: %s' %(error))
    logger.exception(error)
    return render_template('500.html',
        title = '500',
        error = True,
        ), 500
