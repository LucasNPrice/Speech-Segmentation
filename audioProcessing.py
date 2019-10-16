import os
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import string


class AudioProcessing():

  def __init__(self, file):
    self.file = file
    self.sampling_frequency, self.signal = wavfile.read(self.file)
    self.length = len(self.signal)

  def toMono(self):
    """ transform stero to mono """
    assert self.signal.ndim > 1
    self.signal = np.mean(self.signal, axis = 1)

  def moving_average(self, n_speech_blocks = 26):
      """ apply simple moving average filter to signal """
      with tqdm(total = self.length) as pbar: 
        MAvg_signal = np.zeros(self.length)
        signal = np.abs(self.signal)
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
        self.signal = MAvg_signal

  def segment_speech(self, thresh = 100):
    """ segment signal by threshold """
    start_audio = []
    stop_audio = []
    i = 1
    while i < self.length:
      i = self.__start(i, 100)
      start_audio.append(i)
      i = self.__stop(i, 100)
      stop_audio.append(i)
      if len(start_audio) == 26 and len(stop_audio) == 26:
        break

    letters = list(string.ascii_lowercase)
    assert len(start_audio) == len(stop_audio)
    assert len(start_audio) == len(letters)

    self.segmentation = {}
    segments = len(start_audio)
    for i, char in enumerate(letters):
      self.segmentation[char] = np.arange(start_audio[i], stop_audio[i], 1)

  def __start(self, j, thresh):
    for i in range(j, self.length):
      if self.signal[i] >= thresh and self.signal[i-1] < thresh:
        return i
  
  def __stop(self, j, thresh):
    for i in range(j, self.length):
      if self.signal[i] >= thresh and self.signal[i+1] < thresh:
        return i



