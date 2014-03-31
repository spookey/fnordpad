# -.- coding: UTF-8 -.-

'''run fnordpad at localhost:5000'''

from app import app

app.config['USE_X_SENDFILE'] = False

app.run(debug=True, threaded=True)
