from PyQt5.QtCore import QThread


class Thread_1(QThread):  # 线程1
    def __init__(self,func,args=()):
        super().__init__()
        self.func=func
        self.args=args
    def run(self):
        self.result=self.func(*args)