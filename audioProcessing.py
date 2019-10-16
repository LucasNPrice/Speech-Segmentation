import os
import numpy as np
from scipy.io import wavfile
from tqdm import tqdm
# import pandas as pd
import matplotlib.pyplot as plt

class AudioProcessing():

  def __init__(self, dirPath):

    self.signal_names = []
    self.signals = []
    self.sampling_frequency = []

    for file in os.listdir(dirPath):
      self.signal_names.append(file)
      fs, signal = wavfile.read(dirPath + '/' + file)
      self.sampling_frequency.append(fs)
      self.signals.append(signal)

  def toMono(self):

    for i, signal in enumerate(self.signals):
      if signal.ndim != 1:
        self.signals[i] = np.mean(signal, axis = 1)




