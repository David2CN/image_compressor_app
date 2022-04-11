import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from compressor import do_compression, clear_images

abspath = os.getcwd()
img_path = "static/images/"
UPLOAD_FOLDER = os.path.join(abspath, img_path)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
STORAGE_DURATION_LIMIT = 5   # minutes until created files are start to get deleted

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
secret_key = "abd564"
app.config['SECRET_KEY'] = secret_key


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':

        # clear old files from storage
        clear_images(STORAGE_DURATION_LIMIT)

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            comp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], "compressed_"+filename)
            file.save(filepath)
            img_size, compressed_img_size, compressed_rate = do_compression(filename)
            print(filepath, comp_filepath)
            filepath = "static"+filepath.split("static")[1]
            comp_filepath = "static"+comp_filepath.split("static")[1]

            return render_template("compression.html",
                                   img_filepath=filepath, compressed_img_filepath=comp_filepath,
                                   img_size=img_size, compressed_img_size=compressed_img_size,
                                   compressed_rate=compressed_rate,
                                   file_name="compressed_"+filename)

    return render_template("base.html")


@app.route('/static/images/<file_name>', methods=['GET', 'POST'])
def download_file(file_name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], file_name, as_attachment=True)


if __name__ == "__main__":
    app.run()
