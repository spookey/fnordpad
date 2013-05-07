# -.- coding: UTF-8 -.-

from flask import render_template, url_for, flash, send_from_directory, request, redirect, session, g
from app import app
from config import staticdir, p_unsorted, p_public, p_reject
from side import getrandomimage, imagelist, pathimagelist, getnamedimage, getbg, datum, uhr, json_leases, listnamedups, snapnamedups
import os
from itertools import cycle

@app.before_request
def before_request():
    if not 'served' in session:
        session['served'] = 0
    app.jinja_env.globals.update(datum=datum())
    app.jinja_env.globals.update(uhr=uhr())
    app.jinja_env.globals.update(leases=json_leases())
    app.jinja_env.globals.update(served=session['served'])
    app.jinja_env.globals.update(yeah='it\'s peanut butter jelly time')

@app.route('/index/')
@app.route('/')
def index():
    image = getrandomimage(p_public)
    app.jinja_env.globals.update(getbg=getbg(os.path.join(staticdir, image)))
    app.jinja_env.globals.update(length=len(imagelist(p_public)))
    session['served'] += 1
    return render_template('main.html',
        title = 'fnordpad',
        image = image,
        refreshing = True,
        )


@app.route('/sort/', methods=['GET', 'POST'])
@app.route('/sort/<folder>/<image>', methods=['GET', 'POST'])
def sort(folder=None, image=None):

    if folder == 'public':
        folder = p_public
    elif folder == 'reject':
        folder = p_reject
    elif not folder or folder == 'unsorted':
        folder = p_unsorted

    if not image:
        image = getrandomimage(folder)
    else:
        image = getnamedimage(folder, image)
        print '\n\nsort called: sort/%s/%s' %(folder, image)

    app.jinja_env.globals.update(getbg=getbg(os.path.join(staticdir, image)))
    app.jinja_env.globals.update(length=len(imagelist(folder)))
    flash('this: %s' %(image.split('/')[-1]))
    if request.method == 'POST':
        sourceimage = os.path.join(staticdir, request.form['image'])
        cimage = sourceimage.split('/')[-1]

        if os.path.exists(sourceimage):
            if not cimage.endswith('fnordpad.jpg'):
                if 'plus' in request.form:
                    os.rename(sourceimage, os.path.join(p_public, cimage))
                    flash('plus %s' %(cimage))
                elif 'minus' in request.form:
                    os.rename(sourceimage, os.path.join(p_reject, cimage))
                    flash('minus %s' %(cimage))
                else:
                    flash('kaputt')
            else:
                flash('all done!')
    return render_template('main.html',
        title = 'sortpad',
        image = image,
        buttons = True,
        duplicates = listnamedups(),
        )


@app.route('/view/')
@app.route('/view/<folder>')
def view(folder=None):

    if folder == 'public':
        folder = p_public
    elif folder == 'reject':
        folder = p_reject
    elif not folder or folder == 'unsorted':
        folder = p_unsorted
    else:
        flash('<span class="red">%s</span> not found' %(folder))
        return redirect(url_for('view'))

    app.jinja_env.globals.update(length=len(imagelist(folder)))
    flash('welcome in traffic hell!')
    return render_template('main.html',
        title = 'view',
        thumbs = pathimagelist(folder),
        )

@app.route('/snap/name/')
def snap():
    snapnamedups('jpg')
    return redirect('index')

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
