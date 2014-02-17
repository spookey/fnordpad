# -.- coding: UTF-8 -.-

from flask import render_template, url_for, flash, redirect, send_from_directory, request, session, g
from app import app, logger
from .service import list_images, list_all_images, find_image_path, mk_content_cache, read_cache, uhr, datum, timestamp_now, json_status, get_batch_of_images, get_sort_image, move_image, get_image_stats
from .suppenkasper import kasper
from config import p_unsorted, p_public, p_reject, staticdir, i_default, taglines
from itertools import cycle

app.json = app.last_scrape = 0
tagline = cycle(taglines)

@app.route('/index/')
@app.route('/')
def index():
    if timestamp_now()/60 - 20 >= app.last_scrape/60:
        mk_content_cache()
        app.json = json_status()
        app.last_scrape = timestamp_now()
    status = {
        'tagline': next(tagline),
        'uhr': uhr(),
        'datum': datum(),
        'json': app.json,
        'imagestats': get_image_stats()
        }
    logger.info('/index requested')
    return render_template('main.html',
        title = 'fnordpad',
        images = get_batch_of_images(),
        status = status,
    )

@app.route('/sort/', methods=['GET', 'POST'])
@app.route('/sort/<filename>', methods=['GET', 'POST'])
def sort(filename=None):
    logger.info('/sort requested')
    if request.method == 'POST':
        move_image(request.form)
    if not filename:
        filename = get_sort_image()
    if not filename in list_all_images():
        filename = i_default
    flash('# %s' %(filename))
    logger.info('this %s' %(filename))
    return render_template('main.html',
        title = 'sortpad',
        sort = filename,
        len_left = len(read_cache()['unsorted']),
    )

@app.route('/image/')
@app.route('/image/<filename>')
def image(filename=None):
    if not filename or not filename in list_all_images():
        logger.error('requested image not found: %s fallback to %s' %(filename, i_default))
        filename = i_default
    return send_from_directory(find_image_path(filename), filename)

@app.route('/crawl/<action>')
def crawl(action=False):
    if action is not False:
        toload = kasper(view=action)
        return render_template('main.html',
            title = 'crawlpad',
            text = toload,
        )
    return redirect(url_for('index'))

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
    flash('This is weird!')
    return render_template('500.html',
        title = '500',
        error = True,
    ), 500
