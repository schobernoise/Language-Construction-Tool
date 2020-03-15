from PyQt5.QtWidgets import QApplication
from controllers.ctrls import lct_controller
from views.views import main_frame
from models.models import lct_voc

import sys

class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.vocab = lct_voc
        self.main_win = main_frame()
        self.main_controller = lct_controller(self.main_win, self.vocab, start_up=True)
        self.main_win.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())