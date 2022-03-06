from vosk import Model, KaldiRecognizer
import json
from scipy.io import wavfile
import noisereduce as nr
import scipy.signal as sps
import wave
import numpy as np

model_floppa = Model(r"vosk-model-small-ru-0.22")
# model_floppa = Model(r"vosk-model-ru-0.10")

new_rate = 16000
sampling_rate, data = wavfile.read("test1.wav")
number_of_samples = round(len(data) * float(new_rate) / sampling_rate)
data = sps.resample(data, number_of_samples)
reduced_noise = nr.reduce_noise(y=data, sr=new_rate)
wavfile.write('test.wav', new_rate, reduced_noise.astype(np.int16))

wf = wave.open(r'test.wav', "rb")

rec = KaldiRecognizer(model_floppa, new_rate)

result = ''
last_n = False
time_word = {}
time = 0
while True:

    data = wf.readframes(new_rate)
    if len(data) == 0:
        break
    rec.AcceptWaveform(data)
    if str(len(json.loads(rec.PartialResult())["partial"].split(' '))) not in time_word.keys():
        time_word[len(json.loads(rec.PartialResult())["partial"].split(' '))] = time
    time -= -1

js=json.loads(rec.FinalResult())['text'].split(' ')
for i in range (len(js)):
    temp_str="  (time: "

    if i in time_word.keys():
        temp_str+= str(time_word[i])+"c)"
    else:
        temp_str=''
    print(js[i]+ temp_str)