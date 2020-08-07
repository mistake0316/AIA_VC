import librosa
import librosa.display
import sounddevice as sd
import numpy as np

import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                QWidget, QAction, QTabWidget,
                QVBoxLayout, QMessageBox, QHBoxLayout, QGroupBox, QLabel, QFileDialog, QComboBox)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt, QCoreApplication

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import inspect
import collections
import json
#=========================================

from . import convert_helper


class App(QMainWindow):

  def __init__(self, *args, **kwargs):
    super().__init__()
    self.title = 'Display Sample'
    self.left = 0
    self.top = 0
    self.width = 800
    self.height = 800
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)
    
    self.main_widget = ModelDisplayWidget(self, *args, label="Just A Label", **kwargs)
    self.setCentralWidget(self.main_widget)

    self.show()

class ModelDisplayWidget(QWidget):
  def __init__ (self, parent, default_config, addition_config=None, label=""):
    super(QWidget, self).__init__(parent)
    self.model_config = default_config
    if addition_config != None:
      self.update_config(self.model_config, addition_config)
      print(f"with addtion_config:{self.model_config}")

    self.layout = QVBoxLayout(self)
   
    self.trg_combo_box = QComboBox()
    self.trg_combo_box.addItems(self.model_config["speakers"])
    self.trg_combo_box.currentIndexChanged.connect(lambda : self.change_target())

    self.convert_button = QPushButton("convert")
    self.convert_button.clicked.connect(self.go_convert)

    self.signal, self.sr = np.random.rand(44100), 44100

    self.layout.addWidget(self.trg_combo_box)
    self.layout.addWidget(self.convert_button)

    self.setLayout(self.layout)
  
  def update_config(self, base_config, addition_config):
    for k,v in addition_config.items():
      if isinstance(v, collections.abc.Mapping):
        base_config[k] = self.update_config(base_config.get(k, {}), v)
      else:
        base_config[k] = v
    return base_config
        
  def change_target(self, trg=None):
    if trg != None:
      self.model_config["convert_config"]["trg_spk"] = trg
      return
    self.model_config["convert_config"]["trg_spk"] = self.trg_combo_box.currentText()

  def go_convert(self):
    signal, sr = convert_helper.process_one_sound(self.signal, self.sr, self.model_config)
    return signal, sr

  def set_signal(self, signal, sr):
    self.signal = signal
    self.sr = sr


if __name__ == "__main__":
  app = QApplication(sys.argv)
  
  ex = App(default_config=json.load(open('./config.json','r')), addition_config={"congert_config":{"trg_spk": "fuck"}})
  path = "/mnt/26EAD496EAD46419/VC/DATA/temp_data/temp_input/temp_speaker/temp_speaker_source.wav"
  signal, sr = librosa.core.load(path)
  ex.main_widget.set_signal(signal, sr)
  sys.exit(app.exec_())
