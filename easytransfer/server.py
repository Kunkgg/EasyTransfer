import os

from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask import send_from_directory

from config import UPLOAD_FOLDER
from config import SERVER_HOST
from config import SERVER_PORT

UPLOAD_FOLDER = './uploads'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','zip'])
FORBIDEN_EXTENSIONS = set(['html', 'php', 'js'])
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5678

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() not in FORBIDEN_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p>
        <input type=file name=file>
        <input type=submit value=Upload>
      </p>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

# @app.route('/uploads/<dirname>')
# def uploaded_dir(dirname):
#     dirpath = os.path.join(UPLOAD_FOLDER,dirname)
#     return send_from_directory(dirpath)
#     send_from_directory()

if __name__ == "__main__":
    try:
        app.run(threaded=True,host=SERVER_HOST,port=SERVER_PORT)
    except OSError:
        pass
    # app.run(host='0.0.0.0', port=5678)
