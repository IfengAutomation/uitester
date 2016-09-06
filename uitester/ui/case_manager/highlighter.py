from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MyHighlighter(QSyntaxHighlighter):

    def __init__(self, parent, load_lib_kw_list=None):
        QSyntaxHighlighter.__init__(self, parent)
        self.parent = parent
        keyword = QTextCharFormat()
        reserved_classes = QTextCharFormat()
        assignment_operator = QTextCharFormat()
        delimiter = QTextCharFormat()
        special_constant = QTextCharFormat()
        boolean = QTextCharFormat()
        number = QTextCharFormat()
        comment = QTextCharFormat()
        string = QTextCharFormat()
        single_quoted_string = QTextCharFormat()

        self.highlightingRules = []

        if load_lib_kw_list is not None:
            # load lib keyword
            brush = QBrush(Qt.darkYellow, Qt.SolidPattern)
            keyword.setForeground(brush)
            keyword.setFontWeight(QFont.Bold)
            for word in load_lib_kw_list:
                pattern = QRegExp("\\b" + word + "\\b")
                rule = HighlightingRule(pattern, keyword)
                self.highlightingRules.append(rule)

        # keyword
        brush = QBrush(Qt.darkGreen, Qt.SolidPattern)
        keyword.setForeground(brush)
        keyword.setFontWeight(QFont.Bold)
        keywords = ["break", "else", "for", "if", "in", "next", "repeat", "return", "switch", "try", "while"]

        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, keyword)
            self.highlightingRules.append(rule)

        # reservedClasses
        reserved_classes.setForeground(brush)
        reserved_classes.setFontWeight(QFont.Bold)
        keywords = ["array", "character", "complex",
                                "data.frame", "double", "factor",
                                "function", "integer", "list",
                                "logical", "matrix", "numeric",
                                "vector"]
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, reserved_classes)
            self.highlightingRules.append(rule)

        # assignmentOperator
        brush = QBrush(QColor(17, 127, 101), Qt.SolidPattern)
        pattern = QRegExp("(<){1,2}-")
        assignment_operator.setForeground(brush)
        assignment_operator.setFontWeight(QFont.Bold)
        rule = HighlightingRule(pattern, assignment_operator)
        self.highlightingRules.append(rule)

        # delimiter
        pattern = QRegExp("[\)\(]+|[\{\}]+|[][]+")
        delimiter.setForeground(brush)
        delimiter.setFontWeight(QFont.Bold)
        rule = HighlightingRule(pattern, delimiter)
        self.highlightingRules.append(rule)

        # specialConstant
        brush = QBrush(QColor(148, 85, 141), Qt.SolidPattern)
        special_constant.setForeground(brush)
        keywords = ["Inf", "NA", "NaN", "NULL"]
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, special_constant)
            self.highlightingRules.append(rule)

        # boolean
        boolean.setForeground(brush)
        keywords = ["TRUE", "FALSE"]
        for word in keywords:
            pattern = QRegExp("\\b" + word + "\\b")
            rule = HighlightingRule(pattern, boolean)
            self.highlightingRules.append(rule)

        # number
        brush = QBrush(QColor(68, 118, 186), Qt.SolidPattern)
        pattern = QRegExp("[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?")
        pattern.setMinimal(True)
        number.setForeground(brush)
        rule = HighlightingRule(pattern, number)
        self.highlightingRules.append(rule)

        # comment
        brush = QBrush(Qt.blue, Qt.SolidPattern)
        pattern = QRegExp("#[^\n]*")
        comment.setForeground(brush)
        rule = HighlightingRule(pattern, comment)
        self.highlightingRules.append(rule)

        # string
        # brush = QBrush(Qt.darkCyan, Qt.SolidPattern)
        brush = QBrush(QColor(203, 119, 44), Qt.SolidPattern)
        pattern = QRegExp("\".*\"")
        pattern.setMinimal(True)
        string.setForeground(brush)
        rule = HighlightingRule(pattern, string)
        self.highlightingRules.append(rule)

        # singleQuotedString
        pattern = QRegExp("\'.*\'")
        pattern.setMinimal(True)
        single_quoted_string.setForeground(brush)
        rule = HighlightingRule(pattern, single_quoted_string)
        self.highlightingRules.append(rule)

    def highlightBlock(self, text):
        for rule in self.highlightingRules:
            expression = QRegExp(rule.pattern)
            index = expression.indexIn(text)
            # print("in for: " + text)
            while index >= 0:
                length = expression.matchedLength()
                self.setFormat(index, length, rule.format)
                index = expression.indexIn(text, index + length)
        self.setCurrentBlockState(0)


class HighlightingRule:
    def __init__(self, pattern, format):
        self.pattern = pattern
        self.format = format
