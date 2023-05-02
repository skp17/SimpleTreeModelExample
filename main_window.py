
import sys

from PyQt5 import QtCore, QtWidgets

from tree_model import TreeModel


def main():
    app = QtWidgets.QApplication(sys.argv)
    file = QtCore.QFile(r'.\default.txt')
    file.open(QtCore.QIODevice.ReadOnly | QtCore.QFile.Text)
    string = QtCore.QTextStream(file).readAll()
    model = TreeModel(string)
    file.close()

    view = QtWidgets.QTreeView()
    view.setModel(model)
    view.resize(600, 650)
    view.setWindowTitle('Simple Tree Model')
    view.resizeColumnToContents(0)
    view.resizeColumnToContents(1)
    view.expandAll()
    view.setAlternatingRowColors(True)
    view.show()

    app.exec_()


if __name__ == '__main__':
    main()
