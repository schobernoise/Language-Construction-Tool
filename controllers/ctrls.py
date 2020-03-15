from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QMainWindow

from controllers.utils import utils

class lct_controller(QObject):
    def __init__(self, main_win, vocab, start_up):
        super().__init__()
        self.vocab = vocab
        self.main_win = main_win
        self.util = utils
        self.start_up = start_up

        # connect widgets to controller
        self.main_win._ui.spinBox_amount.valueChanged.connect(self.change_amount)
        self.main_win._ui.pushButton_reset.clicked.connect(lambda: self.change_amount(0))

        # listen for vocab event signals
        self.vocab.amount_changed.connect(self.on_amount_changed)
        self.vocab.even_odd_changed.connect(self.on_even_odd_changed)
        self.vocab.enable_reset_changed.connect(self.on_enable_reset_changed)
        
        # set a default value
        self.change_amount(42)

    @pyqtSlot(int)
    def on_amount_changed(self, value):
        self.main_win._ui.spinBox_amount.setValue(value)

    @pyqtSlot(str)
    def on_even_odd_changed(self, value):
        self.main_win._ui.label_even_odd.setText(value)

    @pyqtSlot(bool)
    def on_enable_reset_changed(self, value):
        self.main_win._ui.pushButton_reset.setEnabled(value)
    
    @pyqtSlot(int)
    def change_amount(self, value):
        self._model.amount = value

        # calculate even or odd
        self._model.even_odd = 'odd' if value % 2 else 'even'

        # calculate button enabled state
        self._model.enable_reset = True if value else False

