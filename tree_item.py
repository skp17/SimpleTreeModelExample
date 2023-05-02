
class TreeItem:
    """
    This is a basic class. It is used to hold column data and information about its position in the tree structure.
    """
    # display_string_column = 0

    def __init__(self, data, parent=None):
        """
        :param data: column data
        :type data: list
        :param parent: parent item
        :type parent: TreeItem
        """
        self._childItems = []
        self._itemData = data
        self._parentItem = parent

    def append_child(self, child):
        """
        :param child: child item
        :type child: TreeItem
        :return: None
        """
        self._childItems.append(child)

    def child(self, row):
        """
        :param row:
        :type row: int
        :return:
        :rtype: TreeItem
        """
        if (row < 0) or (row >= len(self._childItems)):
            return None
        return self._childItems[row]

    def child_count(self):
        """
        :return: number of children
        :rtype: int
        """
        return len(self._childItems)

    def column_count(self):
        """
        :return: number of columns
        :rtype: int
        """
        return len(self._itemData)

    def data(self, column):
        """
        :param column:
        :type column: int
        :return:
        :rtype: str
        """
        if (column < 0) or (column >= len(self._itemData)):
            return ''
        return self._itemData[column]

    def row(self):
        """
        :return: row
        :rtype: int
        """
        if self._parentItem:
            return self._parentItem._childItems.index(self)

        return 0

    def parent_item(self):
        """
        :return: parent item
        :rtype: TreeItem
        """
        return self._parentItem
