import tensorflow.keras as keras

import librosa
import pandas as pd
import numpy as np

import warnings
warnings.simplefilter('ignore')


MODEL_PATH = 'models/melspec_model.h5'
MAPPING_FILE_PATH = 'pkl_files/mapping_file.npy'

model = keras.models.load_model(MODEL_PATH)
mapping_dictionary = pd.read_csv(MAPPING_FILE_PATH, names=['mapping']).values


#================================================================
class CommandRecognition():
    ONE_SEC_SAMPLES = 22050
    _instance = None
    _prediction = None
    model = None
    
    def predict(self, SIGNAL=None, AUDIO_PATH=None):

        if AUDIO_PATH is not None:
            signal, sr = librosa.load(AUDIO_PATH)

        else :
            signal = SIGNAL
        
        mfcc = self.Signal_melspectrogram_preprcoessin(signal)
        prediction_index = model.predict(mfcc).argmax(axis=1)
        prediction = mapping_dictionary[prediction_index]

        return prediction
    
    
    def Signal_melspectrogram_preprcoessin(self, signal):
        
        if len(signal) <= self.ONE_SEC_SAMPLES:

            signal = np.append(signal, np.zeros(22050 - len(signal)))
            melspec = librosa.feature.melspectrogram(signal)
            melspec = melspec.reshape(1, 128, 44, 1)
        
        else:
            
            signal = signal[:22050]
            melspec = librosa.feature.melspectrogram(signal)
            melspec = melspec.reshape(1, 128, 44, 1)
            
        return melspec
#============================================================

if CommandRecognition._instance is None:
    
    CommandRecognition._instance = CommandRecognition()
    CommandRecognition.model = model
    
CmdRec = CommandRecognition._instance
