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
    """ transform stereo to mono """
    assert self.signal.ndim > 1
    self.signal = np.mean(self.signal, axis = 1)

  def slow_moving_average(self, n_speech_blocks = 26, scale = 1):
      """ apply simple moving average filter to signal 
          filter on center with adaptive window size on edges (hence the slow) """
      with tqdm(total = self.length) as pbar: 
        MAvg_signal = np.zeros(self.length)
        signal = np.abs(self.signal)
        for j in range(0,self.length):
          window = self.length // (n_speech_blocks*scale)
          left_window = window // 2
          right_window = window // 2

          if j-window < 0:
            left_window = j
          if j+window > self.length:
            right_window = self.length-j

          MAvg_signal[j] = np.mean(signal[j-left_window:j+right_window])
          pbar.update(1)

        # update this sloppyness - write reversion function 
        self.original_signal = self.signal
        self.signal = MAvg_signal

  def undo_moving_average(self):
    self.signal = self.original_signal
    del self.original_signal
        
  def segment_speech(self, thresh = 0.05, n_speech_blocks = None, scale = 4):
    """ segment signal by threshold """
    self.slow_moving_average(scale=scale)
    self.normalize()

    segment_signal = self.signal
    segment_signal -= thresh
    segment_signal[segment_signal <= 0] = 0

    sounds = np.where(segment_signal > 0)
    sounds = [item for sublist in sounds for item in sublist]
    start_audio = []
    stop_audio = []
    
    for i in sounds:
      if i == 0:
        start_audio.append(i)
      elif i == self.length-1:
        stop_audio.append(i)
      elif segment_signal[i-1] == 0:
        start_audio.append(i)
      elif segment_signal[i+1] == 0:
        stop_audio.append(i)

    if n_speech_blocks is not None:
      if n_speech_blocks != len(start_audio) or n_speech_blocks != len(stop_audio):
        """ segment again with higher threshold """
        self.undo_normalize()
        self.undo_moving_average()
        self.segment_speech(thresh = thresh+.01, 
          n_speech_blocks = n_speech_blocks)
      else:
        """ get dictionary of segments """
        self.undo_normalize()
        letters = list(string.ascii_lowercase)
        self.segmentation = {}
        for i, char in enumerate(letters):
          self.segmentation[char] = np.arange(start_audio[i], stop_audio[i], 1)
        self.undo_moving_average()
    else:
      """ return dict like above but un-even start/stops"""
      pass

  def standardize(self):
    self.signal = self.signal / np.std(self.signal)

  # future - make normalize a subclass 
  def normalize(self):
    self.max = np.max(self.signal)
    self.signal = self.signal / self.max

  def undo_normalize(self):
    self.signal = self.signal * self.max

  def clip(self, clip_len = 26*4):
    clip_len = self.length // clip_len
    self.signal = self.signal[clip_len:self.length]
    self.length = len(self.signal)

  def difference_series(self, lag, seq = False):
    if seq:
      with tqdm(total = lag) as pbar: 
        diff = self.signal
        for i in range(1,lag+1):
          diff = diff[1:] - diff[0:len(diff)-1]
          pbar.update(1)
    else:
      diff = self.signal[lag:] - self.signal[0:self.length-lag]
    self.signal = diff
    self.length = len(self.signal)


