import sys
from PyQt5 import QtWidgets, QtCore
from threading import Thread
import pynput
import cfg

# lockfile = QtCore.QLockFile(QtCore.QDir.tempPath() + '/my_app_name.lock')


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight,
                QtCore.Qt.AlignBottom,
                QtCore.QSize(1920, 30),
                QtWidgets.qApp.desktop().availableGeometry(),
            )
        )

    def mousePressEvent(self, event):
        self.hide()
        # qApp.quit()

# show message on screen
def setLabel(data={'name':"hello",'msg':"world"},idx=-1):
    if idx == -1:
        idx = ''
    else:
        idx = str(idx)
    if cfg.PAUSE:
        cfg.WINDOW.setStyleSheet("QMainWindow {background: '#0f0f0f';}")
    else:
        cfg.WINDOW.setStyleSheet("QMainWindow {background: 'white';}")
    cfg.MSG.setText(idx+'   '+data['name']+': '+data['msg'])
    if not cfg.VISIBLE:
        return
    cfg.WINDOW.show()

# socketio event handlers
@cfg.SIO.event
def message(data):
    print("message received with ", data)
    cfg.HISTORY.append(data)
    if not cfg.PAUSE:
        setLabel(data)

def emittor(msg = "hello", room = cfg.ROOM):
    data = data={'msg':msg,'room':room,'name':cfg.NAME}
    cfg.HISTORY.append(data)
    cfg.SIO.emit("message", data)
    return True


# keypress handler
def on_press(key):
    if key == pynput.keyboard.Key.f12:
        print("f12 - quitting app")
        QtWidgets.qApp.quit()
        return False
    if key == pynput.keyboard.Key.f1:
        cfg.VISIBLE = not cfg.VISIBLE
        print("f1 - VISIBILITY: ", cfg.VISIBLE)
        try:
            if cfg.VISIBLE:
                cfg.WINDOW.show()
            else:
                cfg.WINDOW.hide()
            return
        except:
            pass
    elif key == pynput.keyboard.Key.f2:
        cfg.MSG_RECORD = not cfg.MSG_RECORD
        print("f2 - RECORDING:", cfg.MSG_RECORD)
        return
    elif key == pynput.keyboard.Key.f3:
        cfg.PAUSE = not cfg.PAUSE
        print("f3 - PAUSE:", cfg.PAUSE)
        return
    elif key == pynput.keyboard.Key.f4:
        print("f4 - HISTORY:", cfg.HISTORY)
        return
    elif key == pynput.keyboard.Key.up:
        print("UP")
        if len(cfg.HISTORY) == 0:
            return
        cfg.HISTORYIDX = (cfg.HISTORYIDX - 1) % len(cfg.HISTORY)
        try:
            setLabel(cfg.HISTORY[cfg.HISTORYIDX],cfg.HISTORYIDX)
        except:
            pass
        return
    elif key == pynput.keyboard.Key.down:
        print("DOWN")
        if len(cfg.HISTORY) == 0:
            return
        cfg.HISTORYIDX = (cfg.HISTORYIDX + 1) % len(cfg.HISTORY)
        try:
            setLabel(cfg.HISTORY[cfg.HISTORYIDX],cfg.HISTORYIDX)
        except:
            pass
        return
    if not cfg.MSG_RECORD:
        return
    if key == pynput.keyboard.Key.enter:
        st = "".join(cfg.MESSAGE)
        try:
            emittor(st)
        except:
            pass
        cfg.MESSAGE.clear()
        return
    elif key == pynput.keyboard.Key.backspace:
        try:
            cfg.MESSAGE.pop()
            return
        except IndexError:
            pass
    elif key == pynput.keyboard.Key.space:
        cfg.MESSAGE.append(" ")
        return
    else:
        try:
            cfg.MESSAGE.append(key.char)
            return
        except AttributeError:
            print("special key {0} pressed".format(key))
            return




def main():
    app = QtWidgets.QApplication(sys.argv)
    cfg.WINDOW = MainWindow()
    cfg.MSG = QtWidgets.QLabel(cfg.WINDOW, alignment=QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
    cfg.MSG.setGeometry(0, 0, 1920, 30)
    cfg.MSG.setText("")
    cfg.WINDOW.show()
    # Start Messaging and Key Listener threads here
    listener = pynput.keyboard.Listener(on_press=on_press)
    listener.start()
    cfg.SIO.connect(cfg.BACKEND_URL)
    app.exec_()
    try:
        listener.stop()
    except:
        pass
    try:
        cfg.SIO.disconnect()
    except:
        pass
    sys.exit(0)



if __name__ == "__main__":
    main()
