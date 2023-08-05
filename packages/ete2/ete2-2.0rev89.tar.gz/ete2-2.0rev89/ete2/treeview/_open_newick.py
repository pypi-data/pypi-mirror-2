# #START_LICENSE###########################################################
#
# Copyright (C) 2009 by Jaime Huerta Cepas. All rights reserved.  
# email: jhcepas@gmail.com
#
# This file is part of the Environment for Tree Exploration program (ETE). 
# http://ete.cgenomics.org
#  
# ETE is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#  
# ETE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#  
# You should have received a copy of the GNU General Public License
# along with ETE.  If not, see <http://www.gnu.org/licenses/>.
#
# #END_LICENSE#############################################################
__VERSION__="ete2-2.0rev89" 
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_newick.ui'
#
# Created: Mon Sep 14 11:11:49 2009
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

try:
    from PyQt4 import QtCore, QtGui
except ImportError:
    import QtCore, QtGui

class Ui_OpenNewick(object):
    def setupUi(self, OpenNewick):
        OpenNewick.setObjectName("OpenNewick")
        OpenNewick.resize(569, 353)
        self.comboBox = QtGui.QComboBox(OpenNewick)
        self.comboBox.setGeometry(QtCore.QRect(460, 300, 81, 23))
        self.comboBox.setObjectName("comboBox")
        self.widget = QtGui.QWidget(OpenNewick)
        self.widget.setGeometry(QtCore.QRect(30, 10, 371, 321))
        self.widget.setObjectName("widget")

        self.retranslateUi(OpenNewick)
        QtCore.QMetaObject.connectSlotsByName(OpenNewick)

    def retranslateUi(self, OpenNewick):
        OpenNewick.setWindowTitle(QtGui.QApplication.translate("OpenNewick", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
