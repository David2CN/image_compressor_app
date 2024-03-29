import os
from flask import Flask, flash, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
from imgcomp.compressor import do_compression, clear_images, get_resolution
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed

abspath = os.getcwd()
img_path = "imgcomp/static/images/"
UPLOAD_FOLDER = os.path.join(abspath, img_path)
STORAGE_DURATION_LIMIT = 60   # minutes until created files start to get deleted
ALLOWED_FORMATS = ['png', 'jpg', 'jpeg']

class UploadForm(FlaskForm):
    picture = FileField("Drop Your File Here", validators=[FileAllowed(ALLOWED_FORMATS)])
    quality = SelectField(u'Quality Reduction (**only for JPG files!)', choices=[(70, "low"), (40, "medium"), (10, "high")])
    submit = SubmitField("Compress")


def get_image_details(picture, app, form):
    filename = secure_filename(picture.filename)
    img_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    form.picture.data.save(img_filepath)
    quality = int(form.quality.data)

    img_size, compressed_img_size, compressed_rate = do_compression(filename, quality=quality)
    img_resolution = get_resolution(img_filepath)

    return {"img_name": filename,
            "img_size": img_size,
            "compressed_img_size": compressed_img_size,
            "compressed_rate": compressed_rate,
            "img_resolution": img_resolution}


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    secret_key = "abd564"
    app.config['SECRET_KEY'] = secret_key

    @app.route('/', methods=['GET', 'POST'])
    def upload_file():

        form = UploadForm()

        if request.method == "POST":
            if not form.validate_on_submit():
                # flash a message for invalid files!
                flash('Invalid file!\nValid files include: JPG, PNG.')
                print("Invalid File")

        if form.validate_on_submit():

            # clear old files from storage
            clear_images(STORAGE_DURATION_LIMIT)

            # flash a message if no file is selected
            if not form.picture.data:
                flash('Select a file!')
                return redirect(request.url)

            if form.picture.data:
                uploads = get_image_details(form.picture.data, app, form)
                return render_template("compression.html", uploads=uploads)

        return render_template("index.html", form=form)

    @app.route('/imgcomp/static/images/<file_name>', methods=['GET', 'POST'])
    def download_file(file_name):
        return send_from_directory(app.config["UPLOAD_FOLDER"], file_name, as_attachment=True)

    @app.errorhandler(404)
    def error_404(error):
        return render_template("404.html"), 404

    @app.errorhandler(503)
    def error_503(error):
        return render_template("503.html"), 503

    return app
