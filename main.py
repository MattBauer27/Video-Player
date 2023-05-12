import sys
from PyQt5.QtCore import Qt, QUrl, QTimer
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QSlider, QAction, QFileDialog, QLabel, QSizePolicy


class VideoPlayer(QMainWindow):

    def __init__(self):
        super().__init__()

        # Create a QMediaPlayer object
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        # Create a QVideoWidget object
        self.videoWidget = QVideoWidget()

        # Rotation value
        self.rotation = 0

        # Create Open button
        openBtn = QPushButton('Open Video')
        openBtn.clicked.connect(self.openFile)

        # Create Rotate button
        rotateBtn = QPushButton('Rotate Video')
        rotateBtn.clicked.connect(self.rotateVideo)

        # Create Play button
        self.playBtn = QPushButton()
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(
            self.style().standardIcon(self.style().SP_MediaPlay))
        self.playBtn.clicked.connect(self.play)

        # Create a QSlider
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.setPosition)

        # Create a QLabel
        self.label = QLabel()
        self.label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)

        # Create a QVBoxLayout
        layout = QVBoxLayout()
        layout.addWidget(openBtn)
        layout.addWidget(rotateBtn)
        layout.addWidget(self.playBtn)
        layout.addWidget(self.videoWidget)
        layout.addWidget(self.slider)
        layout.addWidget(self.label)

        # Create a QWidget
        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)

        # Media player signals
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie")
        if fileName != '':
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playBtn.setEnabled(True)

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.mediaPlayer.pause()

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def rotateVideo(self):
        self.rotation = (self.rotation + 90) % 360
        self.mediaPlayer.setVideoOutput(None)
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.videoWidget.setAspectRatioMode(Qt.IgnoreAspectRatio)
        self.videoWidget.rotate(self.rotation)

    def positionChanged(self, position):
        self.slider.setValue(position)

    def durationChanged(self, duration):
        self.slider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
