# Speech-Segmentation

### Segment patches of audio data ###

#### Input/Output ####
- Current usage segments .wav audio files.
- Each input file contains the spoken alphabet.
- Speech-Segmentation pipeline segments each .wav file into 26 separate .wav files, each containing a distinct spoken letter.  

**audioProcessing.py**
  - audio processing methods (currently only stero-to-mono)
  
**detectSpeech.py**
  - performs segmentation of speech files 

**Note:**
- Input data was aquired from https://robertmassaioli.bitbucket.io/alphabet-upload.html?
