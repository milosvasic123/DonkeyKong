from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
import time


class LightsMovement(QObject):
    lightsMovementSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.is_done = False
        # move the Worker object to the Thread object
        # "push" self from the current thread to this thread
        self.moveToThread(self.thread)
        # Connect Thread started signal to Worker operational slot method
        self.thread.started.connect(self.__work__)

    def start(self):
        """
        Start notifications.
        """
        self.thread.start()

    def die(self):
        """
        End notifications.
        """
        self.is_done = True
        self.thread.quit()

    @pyqtSlot()
    def __work__(self):
        """
        A slot with no params.
        """
        while not self.is_done:
            self.lightsMovementSignal.emit()
            time.sleep(5)
