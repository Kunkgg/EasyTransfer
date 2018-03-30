import datetime
import os
import shutil

from flask import Flask
from flask import request
from flask import render_template
from flask import url_for
from flask import redirect
from flask import flash
from flask import send_from_directory
from werkzeug.utils import secure_filename

from config import UPLOAD_FOLDER
from config import SERVER_HOST
from config import SERVER_PORT
from config import MAX_MSG
from config import msg_cache
from config import FORBIDEN_EXTENSIONS


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/', methods=['GET', 'POST'])
def index():
    msgs = read_msg_cache()
    _, subdirlist, filelist = next(os.walk(UPLOAD_FOLDER))
    if request.method == 'POST':
        msg = request.form.get('message')
        flash('typemsg:{}'.format(type(msg)))
        if msg:
            message(msgs,msg)
        else:
            upload_file()
    return render_template('localpage.html', 
                            msgs=msgs, 
                            subdirlist=subdirlist, 
                            filelist=filelist)

def read_msg_cache():
    """read msg from the cache file."""
    msgs = []
    try:
        with open(msg_cache,'r') as f:
            for line in f:
                msgs.append(line.strip())
        msgs.reverse()
    except FileNotFoundError:
        pass
    return msgs

def write_msg_cache(msgs,max_msg=MAX_MSG):
    """message cache in a text file"""
    msgs = msgs[:max_msg]
    msgs.reverse()
    with open(msg_cache,'w') as f:
        f.writelines('\n'.join(msgs))

def message(msgs,msg):
    msgs.insert(0,msg)
    write_msg_cache(msgs)

@app.route('/clrmsg')
def clearmsg():
    try:
        os.remove(msg_cache)
    except FileNotFoundError:
        pass
    return redirect(url_for('index'))

def upload_file():
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
        flash('Filename:{}'.format(filename))
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(request.url)

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename,
                               as_attachment=True)

@app.route('/uploadsdir/<path:dirname>/')
def uploaded_dir(dirname):
    dirpath = os.path.join(UPLOAD_FOLDER, dirname)
    _, subdirlist, filelist = next(os.walk(dirpath))
    return render_template('subdir.html', dirname=dirname, subdirlist=subdirlist, filelist=filelist)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() not in FORBIDEN_EXTENSIONS
    
@app.route('/clruploaded')
def clearuploaded():
    try:
        shutil.rmtree(UPLOAD_FOLDER)
        os.mkdir(UPLOAD_FOLDER)
    except (FileNotFoundError, FileExistsError):
        pass
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    # app.debug = True
    app.run(host=SERVER_HOST, port=SERVER_PORT, threaded=True)

