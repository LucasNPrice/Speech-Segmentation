import numpy as np
from tqdm import tqdm
import string

class DetectSpeech():

  def __init__(self, audio):
    self.audio = audio
    self.length = len(self.audio)

  def moving_average(self, n_speech_blocks = 26):
    """ apply simple moving average filter to signal """
    with tqdm(total = self.length) as pbar: 
      MAvg_signal = np.zeros(self.length)
      signal = np.abs(self.audio)
      for j in range(0,self.length):
        window = self.length // (n_speech_blocks*8)
        left_window = window
        right_window = window
        if j-window < 0:
          left_window = j
        if j+window > self.length:
          right_window = self.length-j
        MAvg_signal[j] = np.mean(signal[j-left_window:j+right_window])
        pbar.update(1)
      self.audio = MAvg_signal

  def segment_speech(self, thresh = 100):
    """ segment signal by threshold """
    start_audio = []
    stop_audio = []
    for i in range(0, self.length):
      if i != 0 and i != self.length:
        if self.audio[i] >= thresh and self.audio[i-1] < thresh:
          start_audio.append(i-1)
        elif self.audio[i] >= thresh and self.audio[i+1] < thresh:
          stop_audio.append(i+1)

    letters = list(string.ascii_lowercase)
    assert len(start_audio) == len(stop_audio)
    assert len(start_audio) == len(letters)

    self.segmentation = {}
    segments = len(start_audio)
    for i, char in enumerate(letters):
      self.segmentation[char] = np.arange(start_audio[i], stop_audio[i], 1)

