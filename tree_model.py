
from PyQt5 import QtCore, QtGui, QtWidgets
# import typing

from tree_item import TreeItem


class TreeModel(QtCore.QAbstractItemModel):
    def __init__(self, data: str, parent: QtCore.QObject = None):
        super(TreeModel, self).__init__(parent)
        self._root_item = TreeItem(["Title", "Summary"])
        self._setup_model_data(data.split('\n'), self._root_item)

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> str:
        if not index.isValid():
            return ''

        if role == QtCore.Qt.DisplayRole:
            item: TreeItem = index.internalPointer()
            return item.data(index.column())

    def flags(self, index: QtCore.QModelIndex) -> QtCore.Qt.ItemFlags:
        if not index.isValid():
            return QtCore.Qt.ItemFlags(QtCore.Qt.NoItemFlags)

        return QtCore.QAbstractItemModel.flags(self, index)

    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = ...) -> str:
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._root_item.data(section)

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = ...) -> QtCore.QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QtCore.QModelIndex()

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item: TreeItem = parent.internalPointer()

        child_item = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QtCore.QModelIndex()

    def parent(self, index: QtCore.QModelIndex) -> QtCore.QModelIndex:
        if not index.isValid():
            return QtCore.QModelIndex()

        child_item: TreeItem = index.internalPointer()
        parent_item = child_item.parent_item()

        if parent_item == self._root_item:
            return QtCore.QModelIndex()

        return self.createIndex(parent_item.row(), 0, parent_item)

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parent_item = self._root_item
        else:
            parent_item: TreeItem = parent.internalPointer()

        return parent_item.child_count()

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        if parent.isValid():
            return parent.internalPointer().column_count()
        return self._root_item.column_count()

    def _setup_model_data(self, lines: [], parent: TreeItem):
        parents = []
        indentations = []
        parents.append(parent)
        indentations.append(0)

        number = 0

        while number < len(lines):
            position = 0
            while position < len(lines[number]):
                if lines[number][position] != ' ':
                    break
                position += 1

            line_data = lines[number][position:].strip()

            if line_data:
                # Read the column data from the rest of the line.
                column_data = [string for string in line_data.split('\t') if string != '']

                if position > indentations[-1]:
                    # The last child of the current parent is now the new parent
                    # unless the current parent has no children.
                    parents[-1]: TreeItem
                    if parents[-1].child_count() > 0:
                        parents.append(
                            parents[-1].child(parents[-1].child_count() - 1)
                        )
                        indentations.append(position)
                else:
                    while (position < indentations[-1]) and (len(parents) > 0):
                        parents.pop()
                        indentations.pop()

                # Append a new item to the current parent's list of children.
                parents[-1].append_child(TreeItem(column_data, parents[-1]))

            number += 1
