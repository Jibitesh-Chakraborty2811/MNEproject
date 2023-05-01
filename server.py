from flask import Flask,render_template,request,redirect
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mne




app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/submit",methods=['GET','POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
        
    file = request.files['file']
    file.save(file.filename)
    raw = mne.io.read_raw_edf(file.filename,preload=True)
    raw.plot(start = 0, duration=60)
    plt.savefig('./static/eeg_signals1.png')
    channel_names = raw.ch_names
    sfreq = raw.info['sfreq']
    duration = raw.times[-1]
    raw.notch_filter(sfreq/3)
    raw.filter(0.5, sfreq/3)
    raw.plot(start=0,duration=60)
    plt.savefig('./static/eeg_signals2.png')
    return render_template('upload.html',n_channels=len(channel_names), 
                            channel_names=', '.join(channel_names), sfreq=sfreq, duration=duration)



if __name__ == '__main__':
    app.run()

