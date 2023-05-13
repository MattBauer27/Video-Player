import sys
from PyQt5.QtWidgets import QApplication, QFileDialog, QVBoxLayout, QSlider, QPushButton, QWidget, QMainWindow, QHBoxLayout, QStyle, QStyleOptionSlider
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget


class VideoPlayer(QMainWindow):
    def __init__(self, fileName, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowTitle("Video Player")
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #555;
                border-radius: 11px;
                background-color: #555;
                min-width: 80px;
                color: #ddd;
            }

            QPushButton:hover {
                background-color: #777;
            }
        """)

        self.playButton.clicked.connect(self.play)
        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)
        self.positionSlider.setStyleSheet("""
            QSlider::groove:horizontal {
                border: 1px solid #999;
                height: 8px;
                background: #555;
                margin: 2px 0;
                border-radius: 4px;
            }

            QSlider::handle:horizontal {
                background: #ddd;
                border: 1px solid #777;
                width: 13px;
                margin: -2px 0;
                border-radius: 7px;
            }

            QSlider::handle:horizontal:hover {
                background: #bbb;
            }

            QSlider::sub-page:horizontal {
                background: #777;
                border: 1px solid #777;
                height: 10px;
                border-radius: 2px;
            }
        """)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(fileName)))
        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.mediaPlayer.mediaStatusChanged.connect(self.mediaStatusChanged)
        self.playButton.setEnabled(True)

        widget = QWidget(self)
        widget.setStyleSheet("Background-color: #333")
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        controlLayout = QHBoxLayout()
        layout.addWidget(videoWidget)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        layout.addLayout(controlLayout)
        widget.setLayout(layout)

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            self.mediaPlayer.play()
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        print("Error: " + self.mediaPlayer.errorString())

    def mediaStatusChanged(self, status):
        if status == QMediaPlayer.LoadedMedia:
            self.mediaPlayer.pause()


class InitialWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Import Video')

        openButton = QPushButton("Import Video")
        openButton.setStyleSheet("""
            QPushButton {
                border: 2px solid #555;
                border-radius: 11px;
                background-color: #555;
                min-width: 80px;
                color: #ddd;
            }

            QPushButton:hover {
                background-color: #777;
            }
        """)

        openButton.clicked.connect(self.openFile)

        layout = QVBoxLayout()
        layout.addWidget(openButton)
        self.setLayout(layout)
        self.setStyleSheet("Background-color: #333")

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self, "Import Video", QDir.homePath())
        if fileName != '':
            self.player = VideoPlayer(fileName)
            self.player.resize(640, 480)
            self.player.show()
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    initial_window = InitialWindow()
    initial_window.show()
    sys.exit(app.exec_())
