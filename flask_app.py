import os
from flask import Flask

app = Flask(__name__, static_url_path="/static")

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'form-secret-key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # limit upload size upto 8mb


import routes

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
    
#if __name__== '__main__':
#    app.run(debug=True)
