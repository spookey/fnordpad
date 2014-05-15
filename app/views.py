'''main screen turn on, we get signal'''

from flask import flash, render_template, redirect, url_for, send_from_directory, Response, stream_with_context, request
from app.log import LOGGER
from app import APP, TAGLINES, RDB, DUPLICATES, SUPPENKASPER

def conf_globals():
    result = dict()
    result['js'] = {'delay': RDB.get_ropt('image_timeout')*1000}
    result['ji'] = {'sort_slices': RDB.get_ropt('sort_slices')}
    return result
APP.jinja_env.globals.update(conf_globals=conf_globals())

@APP.route('/index/')
@APP.route('/')
def index():
    '''homepage'''
    sidebar = {
        'status': RDB.get_status(),
        'imagestats': RDB.get_imagestats(),
        'tagline': next(TAGLINES),
        }
    LOGGER.info('index requested')
    return render_template('main.html',
        title='fnordpad',
        image=RDB.random_image(folder='public'),
        sidebar=sidebar,
        )

@APP.route('/stream/<string:channel>/')
def stream_channel(channel=None):
    if channel:
        if channel in [APP.config['REDIS_OPT'][psc] for psc in APP.config['REDIS_OPT'] if psc.endswith('_pubsub')]:
            LOGGER.info('stream for %s requested' %(channel))
            return Response(
                stream_with_context(RDB.browser_shout(APP.config['REDIS_OPT']['%s_pubsub' %(channel)])),
                direct_passthrough=True,
                mimetype='text/event-stream'
                )

@APP.route('/shout/<string:text>/')
@APP.route('/shout/', methods=['GET','POST'])
def shout(text=None):
    if request.method == 'POST':
        result = str()
        for part in request.form.keys():
            RDB.redis_shout(APP.config['REDIS_OPT']['shout_pubsub'], part)
            result += part
        return result
    if text is not None:
        return RDB.redis_shout(APP.config['REDIS_OPT']['shout_pubsub'], text)
    return redirect(url_for('index'))

@APP.route('/sort/<string:ressource>/<int:page>/')
@APP.route('/sort/<string:ressource>/')
@APP.route('/sort/<int:page>/')
@APP.route('/sort/')
def sort(ressource='unsorted', page=0):
    imagestats = RDB.get_imagestats();
    sortimages = dict()
    folderimages = list()
    if ressource in APP.config['CONTENTSUB'].keys():
        # folder/rdb match
        sortimages = RDB.get_sort_images(folder=ressource, page=page)
        if len(sortimages) == 0 and page != 0:
            return redirect(url_for('sort', ressource=ressource, page=page-1))
        folderimages = RDB.get_dict_images(folder=ressource)
    elif ressource in RDB.get_all_images():
        # file match
        sortimages[ressource] = RDB.locate_image(ressource)
    else:
        return redirect(url_for('sort'))
    flash('%s left: %i, page: %i' %(ressource, len(folderimages), page))
    return render_template('sort.html',
        title='sort',
        folderimages=folderimages,
        sortimages=sortimages,
        imagestats=imagestats,
        )

@APP.route('/sort/action/', methods=['POST'])
def action():
    if request.method == 'POST':
        if request.json:
            target = None
            if request.json['action'] == 'plus':
                target = 'public'
            if request.json['action'] == 'minus':
                target = 'reject'
            if target:
                RDB.move_image(request.json['image'], target)
                return '%s -> %s' %(request.json['image'], target)

@APP.route('/flush')
def flush():
    RDB.flush_all()
    flash('redis flushed')
    RDB.get_images()
    return redirect(url_for('index'))


def stream_template(templatename, **context):
        APP.update_template_context(context)
        template = APP.jinja_env.get_template(templatename)
        rv = template.stream(context)
        rv.enable_buffering(5)      # you might want to buffer up a few items in the template
        return rv

@APP.route('/duplicates/<string:delete>/')
@APP.route('/duplicates/')
def duplicates(delete=None):
    duplicates = DUPLICATES.check if not delete else DUPLICATES.delete
    return Response(
        stream_with_context(
            stream_template(
                'sort.html',
                title='duplicates',
                duplicates=duplicates(),
                ),
            ),
        )

@APP.route('/crawl')
def crawl():
    kasper = SUPPENKASPER.kasper
    return Response(
        stream_with_context(
            stream_template(
                'sort.html',
                title='suppenkasper',
                suppenkasper=kasper(),
                ),
            ),
        )


@APP.route('/favicon.ico')
def favicon():
    '''favicon'''
    return send_from_directory(APP.static_folder, 'favicon.ico',
        mimetype='image/x-icon',
        )

@APP.errorhandler(404)
def not_found(error):
    '''404'''
    LOGGER.error(error)
    flash(error)
    return render_template('main.html',
        title='404',
        error='I checked twice!',
        ), 404

@APP.errorhandler(500)
def internal_error(error):
    '''500'''
    LOGGER.error(error)
    flash(error)
    return render_template('main.html',
        title='500',
        error='This is weird!',
        ), 500

def redis_error(error=None):
    '''brain not found'''
    return render_template('main.html',
        title='DB error',
        error=error,
        )

