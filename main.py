import os
from flask import Flask, request, url_for, flash, redirect, render_template
from werkzeug.utils import secure_filename
from commandrecognition import CommandRecognition
import librosa
import librosa.display
from matplotlib import pyplot as plt
plt.style.use('seaborn')


def plot_signal(SIGNAL_PATH=None):
    signal, sr = librosa.load(SIGNAL_PATH)
    #signal = librosa.amplitude_to_db((signal))

    fig, axs = plt.subplots(1, 3, figsize=(25, 8))

    librosa.display.waveshow(signal[:8000], ax=axs[0])

    MELSPEC = librosa.feature.melspectrogram(signal[:8000])
    MELSPEC = librosa.amplitude_to_db(MELSPEC)
    img = librosa.display.specshow(MELSPEC, sr=8000, ax=axs[1], y_axis='linear', x_axis='time')
    plt.colorbar(img, ax=axs[1])

    mfcc = librosa.feature.mfcc(signal[:8000], n_mfcc=13)
    img = librosa.display.specshow(
        mfcc, ax=axs[2], y_axis='linear', x_axis='time')
    plt.colorbar(img, ax=axs[2])

    axs[0].set_title('Time-Amplitude fig')
    axs[1].set_title('melspectrogram fig')
    axs[2].set_title('mfcc fig')
    plt.savefig('static/images/signal.png')


UPLOAD_FOLDER = 'audio'
ALLOWED_EXTENSIONS = {'wav', 'webm'}

app = Flask(__name__)
# CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
# @app.route('/index')
def index():
    return render_template("index.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('index'))

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            signal_path = str(UPLOAD_FOLDER) + '/' + str(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # predict

            CmdRec = CommandRecognition()
            predicted_command = CmdRec.predict(AUDIO_PATH=signal_path)

            D = str(predicted_command)[3:-3]
            plot_signal(SIGNAL_PATH=str(signal_path))
            return render_template('result.html', transcript=D)

    return


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8000)
