# -.- coding: UTF-8 -.-

from flask import render_template, url_for, flash, redirect, send_from_directory, request, Response, stream_with_context
from app import app, logger
from .service import timestamp_now, shout_to_browser, shout_to_redis, list_all_images, find_image_path, mk_image_cache, get_image, move_image, get_image_stats, scrape_status, json_status
from .suppenkasper import kasper
from config import i_default, taglines, image_channel, shout_channel, statusjsonurl
from itertools import cycle

app.last_scrape = 0
tagline = cycle(taglines)

@app.route('/index/')
@app.route('/index/<refresh>')
@app.route('/')
def index(refresh=None):
    if refresh is not None:
        if refresh == 'stream':
            return Response(
                stream_with_context(shout_to_browser(image_channel)),
                direct_passthrough=True,
                mimetype='text/event-stream'
            )
        else:
            image = get_image()
            shout_to_redis(image_channel, image)
            return image

    if timestamp_now()/60 - 20 >= app.last_scrape/60:
        mk_image_cache()
        scrape_status(statusjsonurl)
        app.last_scrape = timestamp_now()
    status = {
        'tagline': next(tagline),
        'json': json_status(),
        'imagestats': get_image_stats(),
        }
    logger.info('/index requested')

    return render_template('main.html',
        title = 'fnordpad',
        image = get_image(),
        status = status,
    )

@app.route('/sort/', methods=['GET', 'POST'])
@app.route('/sort/<filename>', methods=['GET', 'POST'])
def sort(filename=None):
    imgleft = get_image_stats()['unsorted']
    if request.method == 'POST':
        move_image(request.form)
    if not filename:
        filename = get_image('unsorted')
    flash('# %s' %(filename))
    logger.info('currently sorting: %s' %(filename))
    return render_template('main.html',
        title = 'sortpad',
        sort = filename,
        len_left = imgleft,
    )

@app.route('/crawl/<action>')
def crawl(action=False):
    if action is not False:
        toload = kasper(view=action)
        return render_template('main.html',
            title = 'crawlpad',
            text = toload,
        )
    return redirect(url_for('index'))


@app.route('/shout/', methods=['GET', 'POST'])
@app.route('/shout/<text>')
def shout(text=None):
    if request.method == 'POST':
        for s in request.form.keys():
            shout_to_redis(shout_channel, s)
        return s
    if text is not None:
        if text == 'stream':
            return Response(
               stream_with_context(shout_to_browser(shout_channel)),
                direct_passthrough=True,
                mimetype='text/event-stream'
            )
        shout_to_redis(shout_channel, text)
        return text
    return redirect(url_for('index'))

@app.route('/image/')
@app.route('/image/<filename>')
def image(filename=None):
    if not filename or not filename in list_all_images():
        logger.error('requested image not found: %s fallback to %s' %(filename, i_default))
        filename = i_default
    return send_from_directory(find_image_path(filename), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico',
        mimetype='image/x-icon',
    )

@app.errorhandler(404)
def not_found(error):
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
