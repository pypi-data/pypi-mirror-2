#!/usr/bin/env python

#############################################################################
##
## This file is part of Taurus, a Tango User Interface Library
## 
## http://www.tango-controls.org/static/taurus/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Taurus is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Taurus is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Taurus.  If not, see <http://www.gnu.org/licenses/>.
##
###########################################################################

"""
This Wizard provide functionality of creation of configuration file 
for constructing a GUI based on TaurusGUI  

The configuration file determines the default, permanent, pre-defined
contents of the GUI. While the user may add/remove more elements at run
time and those customizations will also be stored, this file defines what a
user will find when launching the GUI for the first time.
"""

import os, sys
from PyQt4 import Qt
import taurus.qt.qtgui.resource
import taurus.qt.qtgui.panel
import taurus.qt.qtgui.taurusgui.paneldescriptionwizard
import taurus.qt.qtgui.input
import copy
from taurus.core.util import etree
        

        
class BooleanWidget(Qt.QWidget):
    """
        This class represents the simple boolean widget with two RadioButtons
        true and false. The default value of the widget is true.
        It change the value by using getValue and setValue methods
    """
    
    def __init__(self, parent=None):
        Qt.QWidget.__init__(self,parent)
        self._formLayout = Qt.QHBoxLayout(self)
        self.trueButton = Qt.QRadioButton(self)
        self._formLayout.addWidget(self.trueButton)
        self.falseButton = Qt.QRadioButton(self)
        self._formLayout.addWidget(self.falseButton)
        self.trueButton.setText("Yes")
        self.falseButton.setText("No")
        Qt.QObject.connect(self.trueButton, Qt.SIGNAL("clicked()"), self.valueChanged)
        Qt.QObject.connect(self.falseButton, Qt.SIGNAL("clicked()"), self.valueChanged)
        self.setValue(self.getDefaultValue(), undo=False)

    def valueChanged(self):
        if not (self.trueButton.isChecked() == self._actualValue):
            self.emit(Qt.SIGNAL("valueChanged"),self._actualValue,not self._actualValue)
        self._actualValue = self.trueButton.isChecked()
    
    def setValue(self, value, undo=False):
        if value is None:
            value = self.getDefaultValue()
        self.trueButton.setChecked(value)
        self.falseButton.setChecked(not value)
        self._actualValue = value
       
    def getValue(self):
        return self.trueButton.isChecked()
    
    @classmethod 
    def getDefaultValue(self):
        return False


class BasePage(Qt.QWizardPage):
    """
        This class represents the base page for all of the pages in the wizard
    """
    
    def __init__(self, parent = None):
        Qt.QWizardPage.__init__(self, parent)
        self._item_funcs = {}
        self._layout = Qt.QGridLayout()  
        self.setLayout(self._layout)
        self._setupUI()
        
    def initializePage(self):
        Qt.QWizardPage.initializePage(self)
        self.checkData()
    
    def _setupUI(self):
        pass
        
    def __setitem__(self, name, value):
        self._item_funcs[name] = value

    def __getitem__(self, name):
        return self._item_funcs[name]
        
    def checkData(self):
        self._valid = True
        self.emit(Qt.SIGNAL('completeChanged()'))
        
    def isComplete(self):
        return self._valid

    def _markRed(self, label):
        """
            Set the color of the given label to red
        """
        palette = label.palette()
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.red)
        label.update()
        
    def _markBlack(self, label):
        """
            Set the color of the given label to black
        """
        palette = label.palette()
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.black)
        label.update()

    def setStatusLabelPalette(self, label):
        """
            Set the label look as as status label
        """
        label.setAutoFillBackground(True)
        palette = label.palette()
        gradient = Qt.QLinearGradient(0, 0, 0, 15)
        gradient.setColorAt(0.0, Qt.QColor.fromRgb( 60, 150, 255))
        gradient.setColorAt(0.5, Qt.QColor.fromRgb(  0,  85, 227))
        gradient.setColorAt(1.0, Qt.QColor.fromRgb( 60, 150, 255))
        gradient.setSpread(Qt.QGradient.RepeatSpread)
        palette.setBrush(Qt.QPalette.Window, Qt.QBrush(gradient))
        palette.setBrush(Qt.QPalette.WindowText, Qt.Qt.white)

    def __setitem__(self, name, value):
        self._item_funcs[name] = value

    def __getitem__(self, name):
        return self._item_funcs[name]
  
    def setNextPageId(self, id):
        self._nextPageId = id


class IntroPage(Qt.QWizardPage):
    """
        Introduction page
    """
    
    def __init__(self, parent = None):
        Qt.QWizardPage.__init__(self, parent)
    
        self.setTitle('Introduction')
        self.setPixmap(Qt.QWizard.WatermarkPixmap, taurus.qt.qtgui.resource.getThemeIcon("document-properties").pixmap(120,120))
        label = Qt.QLabel(self.getIntroText())
        label.setWordWrap(True)
        label.setAlignment(Qt.Qt.Alignment(Qt.Qt.AlignJustify))
        self._layout = Qt.QVBoxLayout()
        self._layout.addWidget(label)
        self._spacerItem1 = Qt.QSpacerItem(10, 200, Qt.QSizePolicy.Minimum, Qt.QSizePolicy.Fixed)  
        self._layout.addItem(self._spacerItem1)
        self.setLayout(self._layout)
        
    def getIntroText(self):
       return """
       
       
           This wizard will guide you through the process of creation a configuration file to construct a GUI based on TaurusGUI.
       
       This configuration file determines the default, permanent, pre-defined contents of the GUI. While the user may add/remove more elements at run time and those customizations will also be stored, this file defines what a user will find when launching the GUI for the first time."""
    
    def setNextPageId(self, id):
        self._nextPageId = id
        
        
class GeneralSettings(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self.setTitle('General settings')
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("guiName",self._getGUIName)
        self.wizard().__setitem__("organizationName",self._getOrganizationName)
        
    def _getGUIName(self):
        return str(self._guiNameLineEdit.text())
    
    def _getOrganizationName(self):
        if len(self._organizationCombo.currentText())>0:
            return str(self._organizationCombo.currentText())
        else:
            return None
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self._guiNameLabel = Qt.QLabel("GUI name:")
        font = Qt.QFont() #set bigger font 
        font.setPointSize(14)
        
        self._label = Qt.QLabel()
        self._layout.addWidget(self._label,0,0,1,2,Qt.Qt.AlignRight)
        
        self._guiNameLineEdit = Qt.QLineEdit()
        self._guiNameLineEdit.setFont(font)
        self._guiNameLineEdit.setMinimumSize(150, 30)
        self._layout.addWidget(self._guiNameLabel,1,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._guiNameLineEdit,1,1,1,1,Qt.Qt.AlignRight)
        self._organizationNameLabel = Qt.QLabel("Organization name:")
        self._organizationCombo = Qt.QComboBox()
        self._organizationCombo.addItems(self._getOrganizationNames())
        self._organizationCombo.setMinimumSize(150, 25)
        self._organizationCombo.setEditable(True)
        self._layout.addWidget(self._organizationNameLabel,2,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._organizationCombo,2,1,1,1,Qt.Qt.AlignRight)

        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel()
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,3)
        
        Qt.QObject.connect(self._guiNameLineEdit, Qt.SIGNAL("textChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._organizationCombo, Qt.SIGNAL("editTextChanged(const QString&)"), self.checkData)
        Qt.QObject.connect(self._organizationCombo, Qt.SIGNAL("currentIndexChanged(const QString&)"), self.checkData)
        
    def _getOrganizationNames(self):
        return ["TAURUS","ALBA", "DESY", "elettra", "ESRF", "MAX-lab", "SOLEIL", "XFEL"]         

    def checkData(self):
        self._valid = True
        if not len(self._guiNameLineEdit.text()):
            self._valid = False
            self._markRed(self._guiNameLabel)
        else:
            self._markBlack(self._guiNameLabel)
            
        self.emit(Qt.SIGNAL('completeChanged()'))
        
        if not self._valid:
            self._setStatus("Please type the name of the GUI")
        else:
            self._setStatus("Press next button to continue")   

    def _setStatus(self,text):
        self._status_label.setText(text)
        

class CustomLogoPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("customLogo",self._getCustomLogo)
    
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Custom logo')
        self._label = Qt.QLabel("\nIf you want to have a custom logo inside your application panel, please select the image file. \n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,4) 
        self._customLogoLabel = Qt.QLabel("Custom logo:")
        self._customLogoLineEdit = Qt.QLineEdit()
        self._customLogoLineEdit.setMinimumSize(150, 25)
        self._customLogoLineEdit.setReadOnly(True)
        self._customLogoButton = Qt.QPushButton("Browse")
        self._customLogoButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("logo"))
        self._customLogoButton.setMaximumSize(80, 25)
        self._spacerItem1 = Qt.QSpacerItem(30, 30, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)  
        self._customLogo = Qt.QLabel(self)
        self._customLogo.setAlignment(Qt.Qt.AlignCenter)
        self._customLogo.setMinimumSize(120, 120)
        self._customLogoRemoveButton = Qt.QPushButton("Remove")
        self._customLogoRemoveButton.setMaximumSize(80, 25)
        self._customLogoRemoveButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/emblems/emblem-unreadable.svg"))
        
        self._layout.addWidget(self._customLogoLabel,2,0,Qt.Qt.AlignRight)
        self._layout.addWidget(self._customLogoLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._customLogoButton,2,2,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._customLogoRemoveButton,2,3,Qt.Qt.AlignLeft) 
        self._layout.addItem(self._spacerItem1,3,2)
        self._layout.addWidget(self._customLogo,4,1,2,2,Qt.Qt.AlignHCenter)
        
             
        self._setNoImage()

        
        Qt.QObject.connect(self._customLogoButton, Qt.SIGNAL("clicked()"), self._selectImage)
        Qt.QObject.connect(self._customLogoRemoveButton, Qt.SIGNAL("clicked()"), self._setNoImage)
        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,4)
        
    def _setNoImage(self):
        self._customLogoLineEdit.setText(":/logo.png") 
        pixmap = taurus.qt.qtgui.resource.getIcon(":/logo.png").pixmap(40,40)
        self._customLogo.setPixmap(pixmap)
        self._customLogoRemoveButton.hide()
    
    def _getCustomLogo(self):
        return str(self._customLogoLineEdit.text())
                
    def _selectImage(self):
            fileName = Qt.QFileDialog.getOpenFileName(self, self.tr("Open File"),"/home", self.tr("Images (*.png *.xpm *.jpg *.jpeg)"))
            image = Qt.QImage()
            if len(fileName):                    
                if not image.load(fileName): 
                    self._setStatus("Selected file is not an image, please select another.")
                    self._setNoImage()
                else:
                    if self._setImage(image):
                        self._customLogoLineEdit.setText(fileName)
                        self._customLogoRemoveButton.show()
                        self._customLogo.show()
                        self._setStatus("Press next button to continue.")
                    else:
                        self._setStatus("Selected file is not an image, please select another.")
                        self._setNoImage()      
            self.checkData()
        
    def _setImage(self, image):
        if type(image)==Qt.QPixmap:
            self._customLogo.setPixmap(image.scaled(200,200))
            return True
        elif type(image)==Qt.QImage:
            self._customLogo.setPixmap(Qt.QPixmap().fromImage(image).scaled(200,200))
            return True
        else:
            self._customLogo.setPixmap(taurus.qt.qtgui.resource.getThemePixmap("image-missing").scaled(50,50))
            return False
        
        self.checkData()
        
    def _setStatus(self,text):
        self._status_label.setText(text)
        

class SynopticPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
    
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("synoptic",self._getSynoptic)
    
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Synoptic')
        self._label = Qt.QLabel("\nIf you want to have a main synoptic panel, set the SYNOPTIC variable to the file name of a .jdraw file. If a relative path is given, the directory containing this configuration file will be used as root. \n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,4) 
        self._synopticLabel = Qt.QLabel("Synoptic:")
        self._synopticLineEdit = Qt.QLineEdit()
        self._synopticLineEdit.setMinimumSize(150, 25)
        self._synopticLineEdit.setReadOnly(True)
        self._synopticButton = Qt.QPushButton("Browse")
        self._synopticButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("system-search"))
        self._synopticButton.setMaximumSize(80, 25)
        self._synopticRemoveButton = Qt.QPushButton("Remove")
        self._synopticRemoveButton.setMaximumSize(80, 25)
        self._synopticRemoveButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/emblems/emblem-unreadable.svg"))     
        self._layout.addWidget(self._synopticLabel,2,0,Qt.Qt.AlignRight)
        self._layout.addWidget(self._synopticLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._synopticButton,2,2,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._synopticRemoveButton,2,3,Qt.Qt.AlignLeft)
        Qt.QObject.connect(self._synopticButton, Qt.SIGNAL("clicked()"), self._selectSynoptic)
        Qt.QObject.connect(self._synopticRemoveButton, Qt.SIGNAL("clicked()"), self._clearSynoptic)
        self._synopticRemoveButton.hide()

        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,4)
        
    
    def _clearSynoptic(self):
        self._synopticLineEdit.clear()
        self._synopticRemoveButton.hide()
    
    def _getSynoptic(self):
        return str(self._synopticLineEdit.text())
        
    def _selectSynoptic(self):
            fileName = Qt.QFileDialog.getOpenFileName(self, self.tr("Open File"),"/home", self.tr("JDW (*.jdw );; All files (*)")  )
            if len(fileName):
                self._synopticLineEdit.setText(fileName)
                self._synopticRemoveButton.show()                    
                    
            self.checkData()      
    
    def _setStatus(self,text):
        self._status_label.setText(text)
            
            
class InstrumentsPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("instruments",self._getInstruments)
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Instruments from Pool:')
        self._label = Qt.QLabel("Set the value to True for enabling auto-creation of instrument panels based on the Pool Instrument information\n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,3)
        
        self._instrumentsLabel = Qt.QLabel("Instruments from pool:")
        self._intstrumentsBoolean = BooleanWidget()
        self._intstrumentsBoolean.setMinimumSize(150, 25)
        self._layout.addWidget(self._instrumentsLabel,5,0,1,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._intstrumentsBoolean,5,1,1,1,Qt.Qt.AlignRight)
        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,3)
        
    def _getInstruments(self):
        return str(self._intstrumentsBoolean.getValue())
        
    def checkData(self):
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)
        
    
class PanelsPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._panels = []
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("panels",self._getPanels)
        self._refreshPanelList()
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Panels editor')
        self._label = Qt.QLabel("If you want extra panels add them to this list\n")
        self._layout.addWidget(self._label,0,0)
        self.setLayout(self._layout)
        self._panelGroupBox = Qt.QGroupBox()
        self._panelGroupBox.setCheckable(False)
        self._panelGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._panelGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._layout.addWidget(self._panelGroupBox,2,0,1,1)
        self._horizontalLayout = Qt.QHBoxLayout(self._panelGroupBox)
        self._panelList = Qt.QListWidget(self._panelGroupBox)
        self._horizontalLayout.addWidget(self._panelList)
        self._verticalLayout = Qt.QVBoxLayout()
        self._addButton = Qt.QPushButton("Add Panel")
        self._addButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._addButton)
        self._removeButton = Qt.QPushButton("Remove Panel")
        self._removeButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._removeButton)
        self._upButton = Qt.QPushButton("Move Up")
        self._upButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._upButton)
        self._downButton = Qt.QPushButton("Move Down")
        self._downButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._downButton)
        self._horizontalLayout.addLayout(self._verticalLayout)
        self._addButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-add"))
        self._removeButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-remove"))
        self._upButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-up"))
        self._downButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-down"))
        Qt.QObject.connect(self._addButton, Qt.SIGNAL("clicked()"), self._addPanel)
        Qt.QObject.connect(self._removeButton, Qt.SIGNAL("clicked()"), self._removePanel)
        Qt.QObject.connect(self._upButton, Qt.SIGNAL("clicked()"), self._moveUp)
        Qt.QObject.connect(self._downButton, Qt.SIGNAL("clicked()"), self._moveDown)
        Qt.QObject.connect(self._panelList, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self._editPanel) 
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
    
    def _addPanel (self):
        paneldesc,ok = taurus.qt.qtgui.taurusgui.paneldescriptionwizard.PanelDescriptionWizard.getDialog(self)
        if ok:
            w = paneldesc.getWidget()
            self._panels.append((paneldesc.name,paneldesc.toXml()))
            
        self._refreshPanelList()
        
    def _editPanel (self):
        # edit
        self._refreshPanelList()
            
    def _removePanel(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            self._panels.remove(self._panels[self._panel_id])
            self._refreshPanelList()
            
    def _moveUp(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            if self._panel_id > 0:
                tmp =  self._panels[self._panel_id]
                self._panels[self._panel_id]=self._panels[self._panel_id-1]
                self._panels[self._panel_id-1]=tmp
                self._refreshPanelList()
                self._panelList.setCurrentIndex(self._panelList.indexFromItem(self._panelList.item(self._panel_id-1) ))
                
    def _moveDown(self):
        if len(self._panelList.selectedIndexes())>0:
            self._panel_id=self._panelList.selectedIndexes()[0].row()
            if self._panel_id < self._panelList.count()-1:
                tmp =  self._panels[self._panel_id]
                self._panels[self._panel_id]=self._panels[self._panel_id+1]
                self._panels[self._panel_id+1]=tmp
                self._refreshPanelList()
                self._panelList.setCurrentIndex(self._panelList.indexFromItem(self._panelList.item(self._panel_id+1) ))
              
    def _refreshPanelList(self):
        self._panelList.clear()
        for panel in self._panels:
            name,xml = panel
            self._panelList.addItem(name)
            
    def _getPanels(self):
        if len(self._panels)<=0:
            return None
        else:
            return self._panels
        
    def checkData(self):
        BasePage.checkData(self)          
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)
        
        
class ExternalAppEditor(Qt.QDialog):
    def __init__(self, parent = None):
        Qt.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle('External Application Editor')
        
        self._dlgBox = Qt.QDialogButtonBox(Qt.QDialogButtonBox.Ok| Qt.QDialogButtonBox.Cancel)
        
        self._layout = Qt.QVBoxLayout()
        self._layout1 = Qt.QGridLayout()
        self._layout2 = Qt.QHBoxLayout()
        self._layout.addLayout(self._layout1)
        self._layout.addLayout(self._layout2)
        self._layout.addWidget(self._dlgBox)
        self.setLayout(self._layout)
        
        self._icon = None
        self._label = Qt.QLabel("\n On this page you can define an external application. \n")
        self._label.setWordWrap(True)
        self._layout1.addWidget(self._label,0,0,1,4) 
        self._execFileLabel = Qt.QLabel("Command:")
        self._execFileLineEdit = Qt.QLineEdit()
        self._execFileLineEdit.setMinimumSize(150, 25)
        #self._execFileLineEdit.setReadOnly(True)
        self._execFileButton = Qt.QPushButton("Browse")
        self._execFileButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("system-search"))
        self._execFileButton.setMaximumSize(80, 25)
        self._layout1.addWidget(self._execFileLabel,2,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._execFileLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._execFileButton,2,2,Qt.Qt.AlignLeft)
        self._paramsLabel = Qt.QLabel("Parameters:")
        self._paramsLineEdit = Qt.QLineEdit()
        self._paramsLineEdit.setMinimumSize(150, 25)
        self._layout1.addWidget(self._paramsLabel,3,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._paramsLineEdit,3,1,Qt.Qt.AlignRight)
        self._textLabel = Qt.QLabel("Text:")
        self._textLineEdit = Qt.QLineEdit()
        self._textLineEdit.setMinimumSize(150, 25)
        self._layout1.addWidget(self._textLabel,4,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._textLineEdit,4,1,Qt.Qt.AlignRight)
        
        self._iconLabel = Qt.QLabel("Icon:")
        self._iconLogo = Qt.QPushButton()
        self._iconLogo.setIcon(Qt.QIcon(taurus.qt.qtgui.resource.getThemePixmap("image-missing") ) )
        self._iconLogo.setIconSize(Qt.QSize(60,60))
        self._iconLogo.setStyleSheet(" QPushButton:flat { border: none; /* no border for a flat push button */} ")
        self._iconLogo.setFlat(True)
        self._layout1.addWidget(self._iconLabel,5,0,Qt.Qt.AlignRight)
        self._layout1.addWidget(self._iconLogo,5,1,Qt.Qt.AlignCenter)
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout1.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
             
        #connections
        Qt.QObject.connect(self._execFileButton, Qt.SIGNAL("clicked()"), self._selectExecFile)
        Qt.QObject.connect(self._execFileLineEdit, Qt.SIGNAL("textChanged(const QString&)"), self._setDefaultText)
        Qt.QObject.connect(self._iconLogo, Qt.SIGNAL("clicked()"), self._selectIcon)
        self.connect(self._dlgBox,Qt.SIGNAL('accepted()'), self.accept)
        self.connect(self._dlgBox,Qt.SIGNAL('rejected()'), self.reject)
        
    def _getExecFile(self):
        return self._execFileLineEdit.text()
    
    def checkData(self):
        if len(self._execFileLabel.text())>0:
            self._dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(True)
        else:
            self._dlgBox.button(Qt.QDialogButtonBox.Ok).setEnabled(False)
        
    
    def _setDefaultText(self):
        fileName = self._execFileLineEdit.text().split('/')[-1]
        index = str(fileName).rfind(".")
        if (index>0):
            self._textLineEdit.setText ( str(fileName)[0:index] )
        else:
            self._textLineEdit.setText(fileName)
        
    def _selectExecFile(self):
            filePath = Qt.QFileDialog.getOpenFileName(self, self.tr("Open File"),"/home", self.tr("All files (*)")  )
            if len(filePath):
                self._execFileLineEdit.setText(filePath)
                self._setDefaultText()
             
    def _selectIcon(self):
        iconNameList=[]
        pixmapList={}
        rowIconName = []
        #rowPixmap=[]
        rowSize = 7
        r=0
        i=0
        
        progressBar = Qt.QProgressDialog  ("Loading icons...", "Abort", 0, len(taurus.qt.qtgui.resource.getThemeMembers().items()), self)
        progressBar.setModal(True)
        progressBar.setMinimumDuration(0)
                
        for k,v in taurus.qt.qtgui.resource.getThemeMembers().items():
            progressBar.setValue(progressBar.value()+1)
            progressBar.setLabelText(k)
            for iconName in v:
                if (not progressBar.wasCanceled()):
                    rowIconName.append(iconName)
                    pixmapList[iconName] = taurus.qt.qtgui.resource.getThemePixmap(iconName)
                    i=i+1
                    if r == rowSize-1:
                        r=0
                        iconNameList.append(rowIconName)
                        rowIconName=[]
                    else:
                        r=r+1
                    
        if (len (rowIconName)>0) and not (progressBar.wasCanceled()):
            iconNameList.append(rowIconName)
        
        if not progressBar.wasCanceled():
            progressBar.close()
            name,ok = taurus.qt.qtgui.input.GraphicalChoiceDlg.getChoice(parent=None, title= 'Panel chooser', msg='Choose the type of Panel:', choices=iconNameList, pixmaps=pixmapList, iconSize=60)            
            if ok:
                if taurus.qt.qtgui.resource.getThemePixmap(name).width()!=0:
                    self._iconLogo.setIcon(Qt.QIcon(taurus.qt.qtgui.resource.getThemePixmap(name) ) )
                    self._iconLogo.setIconSize(Qt.QSize(60,60))
                    self._iconLogo.setText("")
                    self._icon = name
                else:
                    self._iconLogo.setText(name)
                    self._icon = name
        else:
            progressBar.close()
    
    def _getExecFile(self):
        return str(self._execFileLineEdit.text())
    
    def _getParams(self):
        return str(self._paramsLineEdit.text())
        #return str(self._paramsLineEdit.text()).split()
    
    def _getText(self):
        return str(self._textLineEdit.text())
    
    def _getIcon(self):
        return str(self._icon)
      
    def _toXml(self):
        root = etree.Element("externalApp")
        command = etree.SubElement(root, "command")
        command.text = self._getExecFile()
        params = etree.SubElement(root, "params")
        params.text = self._getParams()
        text = etree.SubElement(root, "text")
        text.text = self._getText()
        icon = etree.SubElement(root, "icon")
        icon.text = self._getIcon()
        
        return etree.tostring(root)

    @staticmethod    
    def getDialog():
        dlg = ExternalAppEditor()
        dlg.exec_()
        return dlg._getExecFile(), dlg._toXml() , (dlg.result() == dlg.Accepted)   
    
        
class ExternalAppPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._externalApps = []
        
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("externalApps",self._getExternalApps)
        self._refreshApplicationList()
        
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('External Applications')
        self._label = Qt.QLabel("The GUI may include shortcuts to external applications. You can add them now.\n")
        self._layout.addWidget(self._label,0,0)
        self.setLayout(self._layout)
        self._externalAppGroupBox = Qt.QGroupBox()
        self._externalAppGroupBox.setCheckable(False)
        self._externalAppGroupBox.setAlignment(Qt.Qt.AlignLeft)
        self._externalAppGroupBox.setStyleSheet(" QGroupBox::title {  subcontrol-position: top left; padding: 5 5px; }")
        self._layout.addWidget(self._externalAppGroupBox,2,0,1,1)
        self._horizontalLayout = Qt.QHBoxLayout(self._externalAppGroupBox)
        self._externalAppList = Qt.QListWidget(self._externalAppGroupBox)
        self._horizontalLayout.addWidget(self._externalAppList)
        self._verticalLayout = Qt.QVBoxLayout()
        self._addButton = Qt.QPushButton("Add Application")
        self._addButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._addButton)
        self._removeButton = Qt.QPushButton("Remove Application")
        self._removeButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._removeButton)
        self._upButton = Qt.QPushButton("Move Up")
        self._upButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._upButton)
        self._downButton = Qt.QPushButton("Move Down")
        self._downButton.setStyleSheet("text-align: left;")
        self._verticalLayout.addWidget(self._downButton)
        self._horizontalLayout.addLayout(self._verticalLayout)
        self._addButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-add"))
        self._removeButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("list-remove"))
        self._upButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-up"))
        self._downButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("go-down"))
        Qt.QObject.connect(self._addButton, Qt.SIGNAL("clicked()"), self._addApplication)
        Qt.QObject.connect(self._removeButton, Qt.SIGNAL("clicked()"), self._removeApplication)
        Qt.QObject.connect(self._upButton, Qt.SIGNAL("clicked()"), self._moveUp)
        Qt.QObject.connect(self._downButton, Qt.SIGNAL("clicked()"), self._moveDown)
        Qt.QObject.connect(self._externalAppList, Qt.SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self._editApplication) 
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,1)
        
    
    def _addApplication (self):
        name, xml, ok = ExternalAppEditor.getDialog()
        if ok:
            self._externalApps.append((name,xml))
            
        self._refreshApplicationList()
        
    def _editApplication (self):
        # edit
        self._refreshApplicationList()
            
    def _removeApplication(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            self._externalApps.remove(self._externalApps[self._app_id])
            self._refreshApplicationList()
            
    def _moveUp(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            if self._app_id > 0:
                tmp =  self._externalApps[self._app_id]
                self._externalApps[self._app_id]=self._externalApps[self._app_id-1]
                self._externalApps[self._app_id-1]=tmp
                self._refreshApplicationList()
                self._externalAppList.setCurrentIndex(self._externalAppList.indexFromItem(self._externalAppList.item(self._app_id-1) ))
                
    def _moveDown(self):
        if len(self._externalAppList.selectedIndexes())>0:
            self._app_id=self._externalAppList.selectedIndexes()[0].row()
            if self._app_id < self._externalAppList.count()-1:
                tmp =  self._externalApps[self._app_id]
                self._externalApps[self._app_id]=self._externalApps[self._app_id+1]
                self._externalApps[self._app_id+1]=tmp
                self._refreshApplicationList()
                self._externalAppList.setCurrentIndex(self._externalAppList.indexFromItem(self._externalAppList.item(self._app_id+1) ))
              
    def _refreshApplicationList(self):
        self._externalAppList.clear()
        for panel in self._externalApps:
            name,xml = panel
            self._externalAppList.addItem(name)
            
    def _getExternalApps(self):
        if len(self._externalApps)<=0:
            return None
        else:
            return self._externalApps
        
    def checkData(self):
        BasePage.checkData(self)          
        self._valid=True
    
    def _setStatus(self,text):
        self._status_label.setText(text)     


class MonitorPage(BasePage):
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
    
    def initializePage(self):
        BasePage.initializePage(self)
        self.wizard().__setitem__("monitor",self._getMonitor)
    
    def _setupUI(self):
        BasePage._setupUI(self)
        self.setTitle('Monitor List')
        self._label = Qt.QLabel("\nIf you want to monitor some attributes, add them to the monitor list. \n")
        self._label.setWordWrap(True)
        self._layout.addWidget(self._label,0,0,1,4) 
        self._monitorLabel = Qt.QLabel("Monitor List:")
        self._monitorLineEdit = Qt.QLineEdit()
        self._monitorLineEdit.setToolTip("Comma-separated list of attribute names")
        self._monitorLineEdit.setMinimumSize(300, 25)
        self._monitorLineEdit.setReadOnly(False)
        self._monitorButton = Qt.QPushButton("Browse")   
        #self._monitorButton.setIcon(taurus.qt.qtgui.resource.getThemeIcon("system-search"))
        self._monitorButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/designer/devs_tree.png"))     
        self._monitorButton.setMaximumSize(80, 25)
        self._monitorClearButton = Qt.QPushButton("Clear")
        self._monitorClearButton.setMaximumSize(80, 25)
        self._monitorClearButton.setIcon(taurus.qt.qtgui.resource.getIcon(":/actions/edit-clear.svg"))     
        self._layout.addWidget(self._monitorLabel,2,0,Qt.Qt.AlignRight)
        self._layout.addWidget(self._monitorLineEdit,2,1,Qt.Qt.AlignRight)
        self._layout.addWidget(self._monitorButton,2,2,Qt.Qt.AlignLeft)
        self._layout.addWidget(self._monitorClearButton,2,3,Qt.Qt.AlignLeft)
        Qt.QObject.connect(self._monitorButton, Qt.SIGNAL("clicked()"), self._selectMonitor)
        Qt.QObject.connect(self._monitorClearButton, Qt.SIGNAL("clicked()"), self._clearMonitor)
        #self._synopticClear.hide()

        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,8,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Press next button to continue")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,9,0,1,4)
        
    
    def _clearMonitor(self):
        self._monitorLineEdit.clear()
        #self._monitorClearButton.hide()
    
    def _getMonitor(self):
        return str(self._monitorLineEdit.text())
        
    def _selectMonitor(self):
            models, ok = taurus.qt.qtgui.panel.TaurusModelChooser.modelChooserDlg(host=None)
            if ok:
                self._monitorLineEdit.setText(",".join(models))
            self.checkData()      
    
    def _setStatus(self,text):
        self._status_label.setText(text)

        
class OutroPage(BasePage):
    
    def __init__(self, parent = None):
        BasePage.__init__(self, parent)
        self._valid = True
        self.setTitle('Confirmation Page')
        #self.setPixmap(Qt.QWizard.WatermarkPixmap, taurus.qt.qtgui.resource.getIcon(":/categories/applications-system.svg").pixmap(60,60))
        self._label = Qt.QLabel("XML configuration file:")
        self._label.setWordWrap(True)
        self._label.setAlignment(Qt.Qt.Alignment(Qt.Qt.AlignJustify))
        self._layout.addWidget(self._label,0,0,2,1)
        self._spacerItem1 = Qt.QSpacerItem(20, 20, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Fixed)  
        self._layout.addItem(self._spacerItem1,1,0,1,1)
        self._xml = Qt.QTextEdit()
        self._xml.setMinimumHeight(200)
        self._xml.setMinimumWidth(200)
        self._xml.setSizePolicy(Qt.QSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding))
        self._layout.addWidget(self._xml,2,0,1,2)
#        
        self._spacerItem1 = Qt.QSpacerItem(10, 0, Qt.QSizePolicy.Fixed, Qt.QSizePolicy.Expanding)
        self._layout.addItem(self._spacerItem1,4,0,1,1,Qt.Qt.AlignCenter)
        self._status_label = Qt.QLabel("Write it to file on Finish")
        self.setStatusLabelPalette(self._status_label)
        self._layout.addWidget(self._status_label,5,0,1,2)
        
        
    def _createConfigFile(self):
        if True:
            return True
        else:
            return False
        
    def initializePage(self):
        Qt.QWizardPage.initializePage(self)
        self.wizard().setOption (Qt.QWizard.NoCancelButton , True)
        self._xml.setText(self._toXml())
        
    def setNextPageId(self, id):
        self._nextPageId = id
    
    def _toXml(self):
        root = etree.Element("application")
        guiName = etree.SubElement(root, "guiName")
        guiName.text = self.wizard().__getitem__("guiName")
        organizationName = etree.SubElement(root, "organizationName")
        organizationName.text = self.wizard().__getitem__("organizationName")
        customLogo = etree.SubElement(root, "customLogo")
        customLogo.text = self.wizard().__getitem__("customLogo")
        synoptic = etree.SubElement(root, "synoptic")
        synoptic.text = self.wizard().__getitem__("synoptic")
        instruments = etree.SubElement(root, "instruments")
        instruments.text = str(self.wizard().__getitem__("instruments"))

        panelList = self.wizard().__getitem__("panels")
        if panelList:
            panels = etree.SubElement(root, "panels")
            for panel in panelList:
                name,xml = panel
                item = etree.fromstring(xml)
                panels.append(item)
            
        externalAppList = self.wizard().__getitem__("externalApps")
        if externalAppList:
            externalApps = etree.SubElement(root, "externalApps")
            for externalApp in externalAppList:
                name,xml = externalApp
                item = etree.fromstring(xml)
                externalApps.append(item)
       
        monitor = etree.SubElement(root, "monitor")
        monitor.text = self.wizard().__getitem__("monitor")
        
        return  etree.tostring(root, pretty_print=True)


class AppSettingsWizard(Qt.QWizard):
    
    def __init__(self, parent=None, jdrawCommand='jdraw'):
        Qt.QWizard.__init__(self, parent)
        self._item_funcs = {}
        self._pages = {}
        self._jdrawCommand = jdrawCommand

    def __setitem__(self, name, value):
        self._item_funcs[name] = value
        
    def __getitem__(self, name):
        for id in self.getPages():
            p = self.page(id)
            if isinstance(p, BasePage):
                try:
                    return p[name]()
                except Exception,e:
                    pass
        return self._item_funcs[name]()
        return None

    
    def addPage(self, page):
        id = Qt.QWizard.addPage(self, page)
        self._pages[id] = page

    def setPage(self, id, page):
        Qt.QWizard.setPage(self, id, page)
        self._pages[id] = page
        
    def getPages(self):
        return self._pages
    
