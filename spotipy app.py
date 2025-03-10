import sys
import torch
import soundfile as sf
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from espnet_model_zoo.downloader import ModelDownloader
from espnet2.bin.tts_inference import Text2Speech

class TTSApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tts_model = self.load_vits_model()
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

    def initUI(self):
        self.setWindowTitle("VITS Text-to-Speech App")
        self.setStyleSheet("background-color: #121212; color: white;")

        layout = QVBoxLayout()
        
        self.label = QLabel("Enter text:")
        layout.addWidget(self.label)
        
        self.text_input = QTextEdit()
        self.text_input.setStyleSheet("background-color: #1E1E1E; color: white;")
        layout.addWidget(self.text_input)
        
        self.speak_button = QPushButton("Convert to Speech")
        self.speak_button.setStyleSheet("background-color: #BB86FC; color: black;")
        self.speak_button.clicked.connect(self.generate_speech)
        layout.addWidget(self.speak_button)
        
        self.setLayout(layout)
    
    def load_vits_model(self):
        downloader = ModelDownloader()
        model_path = downloader.download_and_unpack("espnet/kan-bayashi_ljspeech_vits")
        return Text2Speech.from_pretrained(model_tag="espnet/kan-bayashi_ljspeech_vits")

    def generate_speech(self):
        text = self.text_input.toPlainText()
        if text.strip():
            print("Generating speech...")
            speech = self.tts_model(text)["wav"]
            sf.write("output.wav", speech.numpy(), 22050)
            self.play_audio("output.wav")
        else:
            print("Please enter some text.")

    def play_audio(self, file_path):
        self.player.setSource(QUrl.fromLocalFile(file_path))
        self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TTSApp()
    window.show()
    sys.exit(app.exec())
