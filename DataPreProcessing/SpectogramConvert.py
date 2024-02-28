import torchaudio
import pandas as pd
from Constants.DataPaths import LABELS_DATASET_PATH

dataframe = pd.read_csv(LABELS_DATASET_PATH,usecols=['audio_path'])

def process_audio(path):
    audio, sr = torchaudio.load(path)
    
    if audio.shape[1] == 2:
        audio = audio.mean(dim=1) #makes it mono
    
    #if audio.shape[1] == 1:
    #audio = audio.mean(dim=2) #makes it dual

    spectogram = torchaudio.transforms.Spectrogram()(audio)
    
    #hay que ver si el espectograma es de Mel
    #melspec = torchaudio.transforms.MelSpectrogram()(audio)
    #plt.imshow(melspec.log2())
    #plt.show()
    #stft es para espectograma de mel
    
    spectogram_np= spectogram.numpy()
    
    return spectogram_np

spectograms = []

for audio in dataframe['audio_path']:
    spectogram_np = process_audio(audio)
    spectograms.append(spectogram_np)

dataframe['spectogram_of_audio'] = spectograms
new_path = LABELS_DATASET_PATH.replace("labeled_dataset.csv", "audios_with_spectograms.csv")
dataframe.to_csv(new_path)

