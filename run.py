'''development launcher'''

from app import APP

if __name__ == '__main__':
    APP.config['USE_X_SENDFILE'] = False
    APP.run(debug=True, threaded=True)

