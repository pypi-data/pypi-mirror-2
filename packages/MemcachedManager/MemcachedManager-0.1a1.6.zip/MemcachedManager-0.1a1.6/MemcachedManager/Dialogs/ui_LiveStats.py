# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LiveStats.ui'
#
# Created: Wed Jul 14 20:48:53 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_liveStatsDialog(object):
    def setupUi(self, liveStatsDialog):
        liveStatsDialog.setObjectName("liveStatsDialog")
        liveStatsDialog.resize(694, 628)
        self.verticalLayout = QtGui.QVBoxLayout(liveStatsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtGui.QScrollArea(liveStatsDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtGui.QWidget(self.scrollArea)
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 651, 877))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gbConnections = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbConnections.setMinimumSize(QtCore.QSize(0, 250))
        self.gbConnections.setObjectName("gbConnections")
        self.horizontalLayout = QtGui.QHBoxLayout(self.gbConnections)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lblTotalConnectionsGraph = QtGui.QLabel(self.gbConnections)
        self.lblTotalConnectionsGraph.setMinimumSize(QtCore.QSize(275, 250))
        self.lblTotalConnectionsGraph.setObjectName("lblTotalConnectionsGraph")
        self.horizontalLayout.addWidget(self.lblTotalConnectionsGraph)
        self.lblConnectionsGraph = QtGui.QLabel(self.gbConnections)
        self.lblConnectionsGraph.setMinimumSize(QtCore.QSize(275, 250))
        self.lblConnectionsGraph.setObjectName("lblConnectionsGraph")
        self.horizontalLayout.addWidget(self.lblConnectionsGraph)
        self.verticalLayout_4.addWidget(self.gbConnections)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gbGetsSets = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbGetsSets.setObjectName("gbGetsSets")
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.gbGetsSets)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblGetsGraph = QtGui.QLabel(self.gbGetsSets)
        self.lblGetsGraph.setMinimumSize(QtCore.QSize(270, 250))
        self.lblGetsGraph.setObjectName("lblGetsGraph")
        self.verticalLayout_5.addWidget(self.lblGetsGraph)
        self.horizontalLayout_2.addWidget(self.gbGetsSets)
        self.gbHitsMisses = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbHitsMisses.setObjectName("gbHitsMisses")
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.gbHitsMisses)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblHitsMissesGraph = QtGui.QLabel(self.gbHitsMisses)
        self.lblHitsMissesGraph.setMinimumSize(QtCore.QSize(270, 250))
        self.lblHitsMissesGraph.setObjectName("lblHitsMissesGraph")
        self.verticalLayout_7.addWidget(self.lblHitsMissesGraph)
        self.horizontalLayout_2.addWidget(self.gbHitsMisses)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.gbMemoryUsage = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.gbMemoryUsage.setObjectName("gbMemoryUsage")
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.gbMemoryUsage)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lblMemoryGraph = QtGui.QLabel(self.gbMemoryUsage)
        self.lblMemoryGraph.setMinimumSize(QtCore.QSize(550, 250))
        self.lblMemoryGraph.setObjectName("lblMemoryGraph")
        self.verticalLayout_2.addWidget(self.lblMemoryGraph)
        self.verticalLayout_4.addWidget(self.gbMemoryUsage)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)

        self.retranslateUi(liveStatsDialog)
        QtCore.QMetaObject.connectSlotsByName(liveStatsDialog)

    def retranslateUi(self, liveStatsDialog):
        liveStatsDialog.setWindowTitle(QtGui.QApplication.translate("liveStatsDialog", "Live Stats", None, QtGui.QApplication.UnicodeUTF8))
        self.gbConnections.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Active Connections", None, QtGui.QApplication.UnicodeUTF8))
        self.lblTotalConnectionsGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Total Connections Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.lblConnectionsGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Connections Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbGetsSets.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Gets && Sets", None, QtGui.QApplication.UnicodeUTF8))
        self.lblGetsGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Gets & Sets Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbHitsMisses.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Hits vs. Misses", None, QtGui.QApplication.UnicodeUTF8))
        self.lblHitsMissesGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Hits vs. Misses Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.gbMemoryUsage.setTitle(QtGui.QApplication.translate("liveStatsDialog", "Memory Usage", None, QtGui.QApplication.UnicodeUTF8))
        self.lblMemoryGraph.setText(QtGui.QApplication.translate("liveStatsDialog", "Memory Usage Graph", None, QtGui.QApplication.UnicodeUTF8))

