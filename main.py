#!/usr/bin/env python
import librosa
import librosa.display
import sounddevice as sd
import numpy as np
import time


import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton,
                QWidget, QAction, QTabWidget,
                QVBoxLayout, QMessageBox, QHBoxLayout, QGroupBox, QLabel
                ,QWidget)
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtCore import pyqtSlot, Qt

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon

import inspect

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import json
from collections import defaultdict
# =================== My Modules =============
import display.display as display
import record
import record.record_tools
import record.ui
from model_util import helper as model_helper

class App(QMainWindow):
  def __init__(self, model_config=json.load(open('./config.json',"r"))):
    super().__init__()
    self.title = "Voice Conversion App"
    self.left = 0
    self.top = 0
    self.width = 800
    self.height = 800
    self.setWindowTitle(self.title)
    self.setGeometry(self.left, self.top, self.width, self.height)
    #========================= some default setting =========================
    self.image_mapping = defaultdict(lambda:model_config["default_image"],model_config["speakers_image"])
    self.model_config = model_config

    self.central_widget = QWidget()
    self.layout = QHBoxLayout(self.central_widget)

    self.speaker_widget = display.SignalDisplayWidget(self, "Speaker")
    self.convert_widget = display.SignalDisplayWidget(self, "Convert")

    self.control_panel  = QGroupBox("Control Panel")
    self.build_control_widget() # will create self.control_widget
    #========================= start connect something ======================

    self.left_group = QGroupBox("Speaker")
    self.left_group_layout = QHBoxLayout(self.left_group)

    self.left_group_layout.addWidget(self.speaker_widget)
    self.left_group_layout.addWidget(self.control_widget)
    self.layout.addWidget(self.left_group)
    self.layout.addWidget(self.convert_widget)
    self.layout.addWidget(self.Movie_Label)
    
    self.control_items["Load"].clicked.connect(lambda: self.load_audio())
    self.control_items["Record"].clicked.connect(lambda: self.record_callback())

    self.setCentralWidget(self.central_widget)
    self.show()
    
  def build_control_widget(self):
    self.control_widget = QWidget()
    self.control_layout = QVBoxLayout()
    self.control_items = dict()
    CI = self.control_items
    
    # Label
    CI["Label_Sound"] = QLabel("==Sound==")
    # Push Buttons
    sound_button_names = ["Load", "Record"]
    for _name in sound_button_names:
      CI[_name] = QPushButton(_name, self)
    
    
    CI["Label_Model"] = QLabel("==Model==")
    CI["model_widget"] = self.construct_model_widget()
    
    
    for _, item in CI.items():
       self.control_layout.addWidget(item)
    self.control_layout.addStretch(1)
    self.control_widget.setLayout(self.control_layout)
  
  def record_callback(self):
    signal, sr = record.ui.record_dialog()
    self.set_audio(signal, sr)

  def load_audio(self):
    signal,sr = self.speaker_widget.load_audio()
    self.set_audio(signal, sr)

  def set_audio(self, signal, sr):
    self.speaker_widget.set_audio(signal, sr)
    self.model_widget.set_signal(signal, sr)
      

  def construct_model_widget(self):
    self.model_widget = model_helper.ModelDisplayWidget(self, self.model_config)
    
    but = self.model_widget.convert_button
    but.clicked.disconnect()
    but.clicked.connect(self.go_convert)

    combo_box = self.model_widget.trg_combo_box
    combo_box.currentIndexChanged.connect(self.change_target)
    self.movie = QMovie(self)
    self.Movie_Label = QLabel(self)
    self.Movie_Label.setMovie(self.movie)
    
    self.change_target() # change target image

    return self.model_widget
  
  def go_convert(self):
    start_time = time.time()
    signal, sr = self.model_widget.go_convert() 
    print(signal, sr)
    self.convert_widget.set_audio(signal, sr)
    print(f"cost {time.time()-start_time:.2f} sec")
    

  def change_target(self):
    self.movie.setPaused(True)
    trg_name = self.model_widget.trg_combo_box.currentText()
    image_path = self.image_mapping[trg_name]
    self.movie.setFileName(image_path)
    self.movie.start()
    


if __name__ == "__main__":
  app = QApplication(sys.argv)
  ex = App()
  sys.exit(app.exec_())
