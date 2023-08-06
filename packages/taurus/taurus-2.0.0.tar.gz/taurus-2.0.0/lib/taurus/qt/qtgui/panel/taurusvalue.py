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
#############################################################################

"""
taurusvalue.py: 
"""

__all__ = ["TaurusValue", "TaurusValuesFrame", "DefaultTaurusValueCheckBox", "DefaultLabelWidget",
           "DefaultUnitsWidget", "TaurusPlotButton", "TaurusArrayEditorButton",
           "TaurusValuesTableButton", "TaurusDevButton", "TaurusStatusLabel"]

__docformat__ = 'restructuredtext'

from PyQt4 import Qt
import PyTango
import taurus.core

from taurus.qt.qtcore.mimetypes import TAURUS_ATTR_MIME_TYPE, TAURUS_DEV_MIME_TYPE
from taurus.qt.qtcore.configuration import BaseConfigurableClass
from taurus.qt.qtgui.base import TaurusBaseWidget
from taurus.qt.qtgui.container import TaurusFrame
from taurus.qt.qtgui.display import TaurusValueLabel, TaurusConfigLabel
from taurus.qt.qtgui.display import TaurusStateLed, TaurusBoolLed, TaurusLed
from taurus.qt.qtgui.input import TaurusValueSpinBox, TaurusValueCheckBox
from taurus.qt.qtgui.input import TaurusWheelEdit, TaurusValueLineEdit
from taurus.qt.qtgui.button import TaurusLauncherButton
from taurus.qt.qtgui.util import TaurusWidgetFactory

from taurus.qt.qtgui.resource import getIcon


class DefaultTaurusValueCheckBox(TaurusValueCheckBox):
    def __init__(self,*args):
        TaurusValueCheckBox.__init__(self,*args)
        self.setShowText(False)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None
    
class DefaultLabelWidget(TaurusConfigLabel):
    def __init__(self,*args):
        TaurusConfigLabel.__init__(self,*args)
        self.setAlignment(Qt.Qt.AlignRight)
        self.setSizePolicy(Qt.QSizePolicy.Preferred,Qt.QSizePolicy.Maximum)
        self.setStyleSheet('border-style: solid; border-width: 1px; border-color: transparent; border-radius: 4px;')
    def setModel(self, model):
        try: config = self.taurusValueBuddy.getLabelConfig()
        except Exception: config = 'label'
        if self.taurusValueBuddy.getModelClass() == taurus.core.TaurusAttribute:
            config = self.taurusValueBuddy.getLabelConfig()
            TaurusConfigLabel.setModel(self, model + "?configuration=%s"%config)
        else:
            TaurusConfigLabel.setModel(self, model + "/state?configuration=dev_alias")
    def sizeHint(self):
        return Qt.QSize(Qt.QLabel.sizeHint(self).width(), 18)
    def contextMenuEvent(self,event):   
        """ The label widget will be used for handling the actions of the whole TaurusValue
        
        see :meth:`QWidget.contextMenuEvent`"""
        menu = Qt.QMenu(self)  
        menu.addMenu(taurus.qt.qtgui.util.ConfigurationMenu(self.taurusValueBuddy)) #@todo: This should be done more Taurus-ish 
        if self.taurusValueBuddy.isModifiableByUser():
            cr_action = menu.addAction("Change Read Widget",self.taurusValueBuddy.onChangeReadWidget)
            cw_action = menu.addAction("Change Write Widget",self.taurusValueBuddy.onChangeWriteWidget)
            cw_action.setEnabled(not self.taurusValueBuddy.isReadOnly()) #disable the action if the taurusValue is readonly
        menu.exec_(event.globalPos())
        event.accept()
    def mousePressEvent(self, event):
        '''reimplemented to provide drag events'''
        Qt.QLabel.mousePressEvent(self, event)
        if event.button() == Qt.Qt.LeftButton:
            self.dragStartPosition = event.pos()
    def mouseMoveEvent(self, event):
        '''reimplemented to provide drag events'''
        if not event.buttons() & Qt.Qt.LeftButton:
            return
        mimeData = Qt.QMimeData()
        if self.taurusValueBuddy.getModelClass() == taurus.core.TaurusDevice:
            mimeData.setData(TAURUS_DEV_MIME_TYPE, self.taurusValueBuddy.getModelName())
        elif self.taurusValueBuddy.getModelClass() == taurus.core.TaurusAttribute:
            mimeData.setData(TAURUS_ATTR_MIME_TYPE, self.taurusValueBuddy.getModelName())
        mimeData.setText(self.text())
        drag = Qt.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())
        dropAction = drag.start(Qt.Qt.CopyAction)

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class DefaultUnitsWidget(TaurusConfigLabel):
    def __init__(self,*args):
        TaurusConfigLabel.__init__(self,*args)
        self.setNoneValue('')
        self.setSizePolicy(Qt.QSizePolicy.Preferred,Qt.QSizePolicy.Maximum)
    def setModel(self, model):
        TaurusConfigLabel.setModel(self, model + "?configuration=unit")
    def sizeHint(self):
        #print "UNITSSIZEHINT:",Qt.QLabel.sizeHint(self).width(), self.minimumSizeHint().width(), Qt.QLabel.minimumSizeHint(self).width()
        return Qt.QSize(Qt.QLabel.sizeHint(self).width(), 24)
 
    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusPlotButton(TaurusLauncherButton):
    '''A button that launches a TaurusPlot'''
    def __init__(self, parent = None, designMode = False):
        import taurus.qt.qtgui.plot
        TaurusPlot = taurus.qt.qtgui.plot.TaurusPlot
        TaurusLauncherButton.__init__(self, parent = parent, designMode = designMode, widget = TaurusPlot(), icon=getIcon(':/designer/qwtplot.png'), text = 'Show')

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusArrayEditorButton(TaurusLauncherButton):
    '''A button that launches a TaurusArrayEditor'''
    def __init__(self, parent = None, designMode = False):
        import taurus.qt.qtgui.plot
        TaurusArrayEditor = taurus.qt.qtgui.plot.TaurusArrayEditor
        TaurusLauncherButton.__init__(self, parent = parent, designMode = designMode, widget = TaurusArrayEditor(), icon=getIcon(':/designer/arrayedit.png'), text = 'Edit')

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusValuesTableButton(TaurusLauncherButton):
    '''A button that launches a TaurusValuesTable'''
    def __init__(self, parent = None, designMode = False):
        import taurus.qt.qtgui.table
        TaurusValuesTable = taurus.qt.qtgui.table.TaurusValuesTable
        TaurusLauncherButton.__init__(self, parent = parent, designMode = designMode, widget = TaurusValuesTable(), icon=getIcon(':/designer/table.png'), text = 'Show')

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusDevButton(TaurusLauncherButton):
    '''A button that launches a TaurusPlot'''
    def __init__(self, parent = None, designMode = False):
        from taurus.qt.qtgui.panel.taurusform import TaurusAttrForm 
        TaurusLauncherButton.__init__(self, parent = parent, designMode = designMode, widget = TaurusAttrForm(), icon=getIcon(':/places/folder-remote.svg'), text = 'Show Device')

    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusStatusLabel(TaurusValueLabel):
    '''just a taurusVaueLabel but showing the state as its background by default'''
    def __init__(self, parent = None, designMode = False, background = 'state'):
        TaurusValueLabel.__init__(self, parent = parent, designMode = designMode, background = background)
        
    @classmethod
    def getQtDesignerPluginInfo(cls):
        return None


class TaurusValue(Qt.QWidget, TaurusBaseWidget):
    
    __pyqtSignals__ = ("modelChanged(const QString &)",)
    
    def __init__(self, parent = None, designMode = False):
        name = self.__class__.__name__
        self.call__init__wo_kw(Qt.QWidget, parent)
        self.call__init__(TaurusBaseWidget, name, designMode=designMode)
        
        self.__modelClass = None
        self._designMode=designMode
        self._customWidget = None
        
        self._customWidgetMap = {}
        
        #This is a hack to show something usable when in designMode
        if self._designMode:
            layout = Qt.QHBoxLayout(self)
            dummy = TaurusConfigLabel()
            layout.addWidget(dummy)
            dummy.setUseParentModel(True)
            dummy.setModel("?configuration=attr_fullname") 
            dummy.setPrefixText("< TaurusValue: ")
            dummy.setSuffixText(" >")
        else:    
            self.setVisible(False)
            self.setFixedSize(1,1)

        self._parentLayout=None
        
        self._labelWidget = None
        self._readWidget = None
        self._writeWidget = None
        self._unitsWidget = None
        
        self.labelWidgetClassID = 'Auto'
        self.readWidgetClassID = 'Auto'
        self.writeWidgetClassID = 'Auto'
        self.unitsWidgetClassID = 'Auto'
        self.customWidgetClassID = 'Auto'
        self.setPreferredRow(-1)
        self._row = None
        
        self._allowWrite = True
        self._minimumHeight = None
        self._labelConfig = 'label'
        self.setModifiableByUser(False)
        
        if parent is not None:
            self.setParent(parent)
    
    def labelWidget(self):
        return self._labelWidget
    
    def readWidget(self):
        return self._readWidget
    
    def writeWidget(self):
        return self._writeWidget
    
    def unitsWidget(self):
        return self._unitsWidget
    
    def customWidget(self):
        return self._customWidget
    
    def setParent(self, parent):
   
        #make sure that the parent has a QGriLayout
        pl=parent.layout()
        if pl is None:
            pl = Qt.QGridLayout(parent) #creates AND sets the parent layout
        if not isinstance(pl, Qt.QGridLayout):
            raise ValueError('layout must be a QGridLayout (got %s)'%type(pl))
        self._parentLayout = pl
        
        if self._row is None:
            self._row = self.getPreferredRow()  #@TODO we should check that the Preferred row is empty in self._parentLayout
            if self._row < 0:
                self._row = self._parentLayout.rowCount()
        #print 'ROW:',self, self.getRow()
        
        #insert self into the 0-column
        self._parentLayout.addWidget(self, self._row, 0) #this widget is invisible (except in design mode)
        
        #Create/update the subwidgets (this also inserts them in the layout)
        if not self._designMode:  #in design mode, no subwidgets are created
            self.updateLabelWidget()
            self.updateReadWidget()
            self.updateWriteWidget()
            self.updateUnitsWidget()
        
#        self.updateCustomWidget()
        
        #do the base class stuff too    
        Qt.QWidget.setParent(self,parent)
        
    def getAllowWrite(self):
        return self._allowWrite
    
    @Qt.pyqtSignature("setAllowWrite(bool)")
    def setAllowWrite(self, mode):
        self._allowWrite = mode
    
    def resetAllowWrite(self):
        self._allowWrite = True
    
    def getPreferredRow(self):
        return self._preferredRow
    
    @Qt.pyqtSignature("setPreferredRow(int)")
    def setPreferredRow(self,row):
        self._preferredRow=row
        
    def resetPreferredRow(self):
        self.setPreferredRow(-1)
        
    def getRow(self):
        return self._row
    
    def setMinimumHeight(self, minimumHeight):
        self._minimumHeight = minimumHeight
        
    def minimumHeight(self):
        return self._minimumHeight
    
    def getDefaultLabelWidgetClass(self):
#        if self._customWidget is not None: return None
        return DefaultLabelWidget
     
    def getDefaultReadWidgetClass(self, returnAll=False):
        '''
        Returns the default class (or classes) to use as read widget for the
        current model.
        
        :param returnAll: (bool) if True, the return value is a list of valid
                          classes instead of just one class
        
        :return: (class or list<class>) the default class  to use for the read
                 widget (or, if returnAll==True, a list of classes that can show
                 the attribute ). If a list is returned, it will be loosely
                 ordered by preference, being the first element always the
                 default one.
        '''
#        if self._customWidget is not None: return None
        modelobj = self.getModelObj()
        if modelobj is None: 
            if returnAll: return [TaurusValueLabel]
            else: return TaurusValueLabel
        
        if self.getModelClass() == taurus.core.TaurusAttribute:
            ##The model is an attribute
            config = modelobj.getConfig()
            #print "---------ATTRIBUTE OBJECT:----------\n",modelobj.read()
            try: configType = config.getType()
            except: configType = None            
            if config.isScalar():
                if  configType == PyTango.ArgType.DevBoolean:
                    result = [TaurusLed, TaurusBoolLed, TaurusValueLabel]
                elif configType == PyTango.ArgType.DevState:
                    result = [TaurusStateLed, TaurusValueLabel]
                elif str(self.getModel()).lower().endswith('/status'):
                    result = [TaurusStatusLabel, TaurusValueLabel]
                else:
                    result = [TaurusValueLabel]
            elif config.isSpectrum():
                if PyTango.is_numerical_type(configType):
                    result = [TaurusPlotButton, TaurusValueLabel]
                else:
                    result = [TaurusValuesTableButton, TaurusValueLabel]
            elif config.isImage():
                result = [TaurusValuesTableButton, TaurusValueLabel]
            else:
                self.warning('Unsupported attribute type %s'%configType)
                result = None
        else:  
            ##The model is a device           
            result = [TaurusDevButton]
            
        if returnAll: return result
        else: return result[0]
        
    def getDefaultWriteWidgetClass(self, returnAll=False):
        '''
        Returns the default class (or classes) to use as write widget for the
        current model.
        
        :param returnAll: (bool) if True, the return value is a list of valid
                          classes instead of just one class
        
        :return: (class or list<class>) the default class  to use for the write
                 widget (or, if returnAll==True, a list of classes that can show
                 the attribute ). If a list is returned, it will be loosely
                 ordered by preference, being the first element always the
                 default one.
        '''
#        if self._customWidget is not None: return None
        if self.isReadOnly() or self.getModelClass() != taurus.core.TaurusAttribute: 
            if returnAll: return []
            else: return None
        modelobj = self.getModelObj()
        if modelobj is None:
            if returnAll: return [TaurusValueLineEdit]
            else: return TaurusValueLineEdit
        config = modelobj.getConfig()
        if config.isScalar():
            configType = config.getType() 
            if configType == PyTango.ArgType.DevBoolean:
                result = [DefaultTaurusValueCheckBox, TaurusValueLineEdit]
            #elif PyTango.is_numerical_type(configType ):
            #    result = TaurusWheelEdit
            else:
                result = [TaurusValueLineEdit, TaurusValueSpinBox, TaurusWheelEdit]
        elif config.isSpectrum():
            result = [TaurusArrayEditorButton, TaurusValueLineEdit]
        else:
            self.debug('Unsupported attribute type for writting: %s'% str(config.getType()))
            result = [None]
            
        if returnAll: return result
        else: return result[0]
    
    def getDefaultUnitsWidgetClass(self):
#        if self._customWidget is not None: return None
        if self.getModelClass() != taurus.core.TaurusAttribute:
            return None
        return DefaultUnitsWidget
    
    def getDefaultCustomWidgetClass(self):
        if self.getModelClass() == taurus.core.TaurusAttribute:
            return None
        try:
            key = self.getModelObj().getHWObj().info().dev_class
        except:
            return None
        return self.getCustomWidgetMap().get(key, None)
            
    def setCustomWidgetMap(self, cwmap):
        '''Sets a map map for custom widgets.
        
        :param cwmap: (dict<str,Qt.QWidget>) a dictionary whose keys are device
                      class strings (see :class:`PyTango.DeviceInfo`) and
                      whose values are widget classes to be used
        '''
        self._customWidgetMap = cwmap
        
    def getCustomWidgetMap(self):
        '''Returns the map used to create custom widgets.
        
        :return: (dict<str,Qt.QWidget>) a dictionary whose keys are device
                 type strings (i.e. see :class:`PyTango.DeviceInfo`) and whose
                 values are widgets to be used
        '''
        return self._customWidgetMap
    
    def onChangeReadWidget(self):
        classnames = ['None', 'Auto']+[c.__name__ for c in self.getDefaultReadWidgetClass(returnAll=True)]
        cname, ok = Qt.QInputDialog.getItem(self, 'Change Read Widget', 'Choose a new read widget class', classnames, 1, True)
        if ok:
            self.setReadWidgetClass(str(cname))
            
    def onChangeWriteWidget(self):
        classnames = ['None', 'Auto']+[c.__name__ for c in self.getDefaultWriteWidgetClass(returnAll=True)]
        cname, ok = Qt.QInputDialog.getItem(self, 'Change Write Widget', 'Choose a new write widget class', classnames, 1, True)
        if ok:
            self.setWriteWidgetClass(str(cname))
        
    def _newSubwidget(self, oldWidget, newClass):
        '''eliminates oldWidget and returns a new one.
        If newClass is None, None is returned
        If newClass is the same as the olWidget class, nothing happens'''
        if oldWidget.__class__ == newClass: return oldWidget
        if oldWidget is not None:
            oldWidget.hide()
            oldWidget.setParent(None)
            oldWidget.destroy()
        if newClass is None: result = None
        else: result = newClass()
        return result

    def labelWidgetClassFactory(self, classID):
        if self._customWidget is not None: return None
        if classID is None or classID is 'None': return None
        if isinstance(classID, type): return classID
        elif str(classID) == 'Auto': return self.getDefaultLabelWidgetClass()
        else: return TaurusWidgetFactory().getTaurusWidgetClass(classID)

    def readWidgetClassFactory(self, classID):
        if self._customWidget is not None: return None
        if classID is None or classID is 'None': return None
        if isinstance(classID, type): return classID
        elif str(classID) == 'Auto': return self.getDefaultReadWidgetClass()
        else: return TaurusWidgetFactory().getTaurusWidgetClass(classID)
    
    def writeWidgetClassFactory(self, classID):
        if self._customWidget is not None: return None
        if classID is None or classID is 'None': return None
        if isinstance(classID, type): return classID
        elif str(classID) == 'Auto': return self.getDefaultWriteWidgetClass()
        else: return TaurusWidgetFactory().getTaurusWidgetClass(classID)
        
    def unitsWidgetClassFactory(self, classID):
        if self._customWidget is not None: return None
        if classID is None or classID is 'None': return None
        if isinstance(classID, type): return classID
        elif str(classID) == 'Auto': return self.getDefaultUnitsWidgetClass()
        else: return TaurusWidgetFactory().getTaurusWidgetClass(classID)
        
    def customWidgetClassFactory(self, classID):
        if classID is None or classID is 'None': return None
        if isinstance(classID, type): return classID
        elif str(classID) == 'Auto': return self.getDefaultCustomWidgetClass()
        else: return TaurusWidgetFactory().getTaurusWidgetClass(classID)
        
    def updateLabelWidget(self):
        #get the class for the widget and replace it if necessary
        klass = self.labelWidgetClassFactory(self.labelWidgetClassID)
        self._labelWidget = self._newSubwidget(self._labelWidget, klass)
        
        #take care of the layout
        self.addLabelWidgetToLayout() 
        
        if self._labelWidget is not None:
            #give the new widget a reference to its buddy TaurusValue object
            self._labelWidget.taurusValueBuddy = self
            
            #tweak the new widget
            if self.minimumHeight() is not None:
                self._labelWidget.setMinimumHeight(self.minimumHeight())
            
            #set the model for the subwidget
            if hasattr(self._labelWidget,'setModel'):
                self._labelWidget.setModel(self.getModelName())
            
    def updateReadWidget(self):
        #get the class for the widget and replace it if necessary
        klass = self.readWidgetClassFactory(self.readWidgetClassID)
        self._readWidget = self._newSubwidget(self._readWidget, klass)
        
        #take care of the layout
        self.addReadWidgetToLayout() 
        
        if self._readWidget is not None:
            #give the new widget a reference to its buddy TaurusValue object
            self._readWidget.taurusValueBuddy = self
            
            #tweak the new widget
            if self.minimumHeight() is not None:
                self._readWidget.setMinimumHeight(self.minimumHeight())
            
            #set the model for the subwidget
            if hasattr(self._readWidget,'setModel'):
                self._readWidget.setModel(self.getModelName())

    def updateWriteWidget(self):
        #get the class for the widget and replace it if necessary
        klass = self.writeWidgetClassFactory(self.writeWidgetClassID)
        self._writeWidget = self._newSubwidget(self._writeWidget, klass)
        
        #take care of the layout
        self.addReadWidgetToLayout() #this is needed because the writeWidget affects to the readWritget layout
        self.addWriteWidgetToLayout()
        
        if self._writeWidget is not None:
            #give the new widget a reference to its buddy TaurusValue object
            self._writeWidget.taurusValueBuddy = self
            
            #tweak the new widget
            ##hide getPendingOperations of the writeWidget so that containers don't get duplicate lists
            #self._writeWidget._getPendingOperations = self._writeWidget.getPendingOperations 
            #self._writeWidget.getPendingOperations = lambda : [] 
            self.connect(self._writeWidget, Qt.SIGNAL('valueChanged'),self.updatePendingOpsStyle)
            self._writeWidget.setDangerMessage(self.getDangerMessage())
            self._writeWidget.setForceDangerousOperations(self.getForceDangerousOperations())
            if self.minimumHeight() is not None:
                self._writeWidget.setMinimumHeight(self.minimumHeight())
            
            #set the model for the subwidget
            if hasattr(self._writeWidget,'setModel'):
                self._writeWidget.setModel(self.getModelName())
        
    def updateUnitsWidget(self):
        #get the class for the widget and replace it if necessary
        klass = self.unitsWidgetClassFactory(self.unitsWidgetClassID)
        self._unitsWidget = self._newSubwidget(self._unitsWidget, klass)
        
        #take care of the layout
        self.addUnitsWidgetToLayout() 
        
        if self._unitsWidget is not None:
            #give the new widget a reference to its buddy TaurusValue object
            self._unitsWidget.taurusValueBuddy = self
            #tweak the new widget
            if self.minimumHeight() is not None:
                self._unitsWidget.setMinimumHeight(self.minimumHeight())
            
            #set the model for the subwidget
            if hasattr(self._unitsWidget,'setModel'):
                self._unitsWidget.setModel(self.getModelName())
                
    def updateCustomWidget(self):
        #get the class for the widget and replace it if necessary
        klass = self.customWidgetClassFactory(self.customWidgetClassID)
        self._customWidget = self._newSubwidget(self._customWidget, klass)
        
        #take care of the layout
#        self.addReadWidgetToLayout() 
#        self.addWriteWidgetToLayout()
        self.addCustomWidgetToLayout()
        
        if self._customWidget is not None:            
            #set the model for the subwidget
            if hasattr(self._customWidget,'setModel'):
                self._customWidget.setModel(self.getModelName())
                
                
    def addLabelWidgetToLayout(self):
        if self._labelWidget is not None:
            self._parentLayout.addWidget(self._labelWidget, self._row, 1)
    
    def addReadWidgetToLayout(self):
        if self._readWidget is not None: 
            if self._writeWidget is None:
                self._parentLayout.addWidget(self._readWidget, self._row, 2,1,2)
            else:
                self._parentLayout.addWidget(self._readWidget, self._row, 2)
    
    def addWriteWidgetToLayout(self):
        if self._writeWidget is not None:
            self._parentLayout.addWidget(self._writeWidget, self._row, 3)
    
    def addUnitsWidgetToLayout(self):
        if self._unitsWidget is not None:
            self._parentLayout.addWidget(self._unitsWidget, self._row, 4)
            
    def addCustomWidgetToLayout(self):
        if self._customWidget is not None:
            self._parentLayout.addWidget(self._customWidget, self._row, 1,1,-1)

    @Qt.pyqtSignature("parentModelChanged(const QString &)")
    def parentModelChanged(self, parentmodel_name):
        """Invoked when the parent model changes
        
        :param parentmodel_name: (str) the new name of the parent model
        """
        TaurusBaseWidget.parentModelChanged(self, parentmodel_name)
        if not self._designMode:     #in design mode, no subwidgets are created
            self.updateLabelWidget()
            self.updateReadWidget()
            self.updateWriteWidget()
            self.updateUnitsWidget()

    @Qt.pyqtSignature("setLabelWidget(QString)")
    def setLabelWidgetClass(self,classID):
        '''substitutes the current widget by a new one. classID can be one of:
        None, 'Auto', a TaurusWidget class name, or any class'''
        self.labelWidgetClassID = classID
        self.updateLabelWidget()
            
    def getLabelWidgetClass(self):
        return self.labelWidgetClassID
    
    def resetLabelWidgetClass(self):
        self.labelWidgetClassID = 'Auto'
    
    @Qt.pyqtSignature("setReadWidget(QString)")
    def setReadWidgetClass(self,classID):
        '''substitutes the current widget by a new one. classID can be one of:
        None, 'Auto', a TaurusWidget class name, or any class'''
        self.readWidgetClassID = classID
        self.updateReadWidget()
            
    def getReadWidgetClass(self):
        return self.readWidgetClassID
    
    def resetReadWidgetClass(self):
        self.readWidgetClassID = 'Auto'
        
    @Qt.pyqtSignature("setWriteWidget(QString)")
    def setWriteWidgetClass(self,classID):
        '''substitutes the current widget by a new one. classID can be one of:
        None, 'Auto', a TaurusWidget class name, or any class'''
        self.writeWidgetClassID = classID
        self.updateWriteWidget()
    
    def getWriteWidgetClass(self):
        return self.writeWidgetClassID
    
    def resetWriteWidgetClass(self):
        self.writeWidgetClassID = 'Auto'
        
    @Qt.pyqtSignature("setUnitsWidget(QString)")
    def setUnitsWidgetClass(self,classID):
        '''substitutes the current widget by a new one. classID can be one of:
        None, 'Auto', a TaurusWidget class name, or any class'''
        self.unitsWidgetClassID = classID
        self.updateUnitsWidget()
    
    def getUnitsWidgetClass(self):
        return self.unitsWidgetClassID
    
    def resetUnitsWidgetClass(self):
        self.unitsWidgetClassID = 'Auto'
    
    @Qt.pyqtSignature("setCustomWidget(QString)")
    def setCustomWidgetClass(self,classID):
        '''substitutes the current widget by a new one. classID can be one of:
        None, 'Auto', a TaurusWidget class name, or any class'''
        self.customWidgetClassID = classID
        self.updateCustomWidget()
    
    def getCustomWidgetClass(self):
        return self.customWidgetClassID
    
    def resetCustomWidgetClass(self):
        self.customWidgetClassID = 'Auto'
        
    def isReadOnly(self):
        if not self.getAllowWrite(): return True 
        modelObj = self.getModelObj()
        if modelObj is None: return False 
        return not modelObj.isWritable()

    def getModelClass(self):
        return self.__modelClass
    
    def destroy(self):
        if not self._designMode:
            for w in [self._labelWidget, self._readWidget, self._writeWidget, self._unitsWidget]:
                if isinstance(w,Qt.QWidget):
                    w.setParent(self)   #reclaim the parental rights over subwidgets before destruction
        Qt.QWidget.setParent(self,None)
        Qt.QWidget.destroy(self)

    def createConfig(self, allowUnpickable=False):
        '''
        extending  :meth:`TaurusBaseWidget.createConfig` to store also the class names for subwidgets
               
        :param alllowUnpickable:  (bool) 
        
        :return: (dict<str,object>) configurations (which can be loaded with :meth:`applyConfig`).
        
        .. seealso: :meth:`TaurusBaseWidget.createConfig`, :meth:`applyConfig` 
        '''
        configdict = TaurusBaseWidget.createConfig(self, allowUnpickable=allowUnpickable)
        #store the subwidgets classIDs and configs
        for key in ('LabelWidget', 'ReadWidget', 'WriteWidget', 'UnitsWidget', 'CustomWidget'):
            classID = getattr(self, 'get%sClass'%key)() # calls self.getLabelWidgetClass, self.getReadWidgetClass,...
            if isinstance(classID, (str, Qt.QString)) or allowUnpickable:
                #configdict[key] = classID
                configdict[key] = {'classid':classID}
                widget = getattr(self, key[0].lower()+key[1:])()
                if isinstance(widget, BaseConfigurableClass):
                    configdict[key]['delegate'] = widget.createConfig()
            else:
                self.info('createConfig: %s not saved because it is not Pickable (%s)'%(key, str(classID)))

        return configdict
    
    def applyConfig(self, configdict, **kwargs):
        """extending :meth:`TaurusBaseWidget.applyConfig` to restore the subwidget's classes
        
        :param configdict: (dict)
        
        .. seealso:: :meth:`TaurusBaseWidget.applyConfig`, :meth:`createConfig`
        """
        #first do the basic stuff...
        TaurusBaseWidget.applyConfig(self, configdict, **kwargs)
        #restore the subwidgets classIDs
        for key in ('LabelWidget', 'ReadWidget', 'WriteWidget', 'UnitsWidget', 'CustomWidget'):
            if key in configdict:
                widget_configdict = configdict[key]
                getattr(self, 'set%sClass'%key)(widget_configdict.get('classid', None))
                if widget_configdict.has_key('delegate'):
                    widget = getattr(self, key[0].lower()+key[1:])()
                    if isinstance(widget, BaseConfigurableClass):
                        widget.applyConfig(widget_configdict['delegate'], **kwargs)
                
        
    @Qt.pyqtSignature("setModel(QString)")
    def setModel(self, model):
        try:
            taurus.Attribute(model)
            self.__modelClass = taurus.core.TaurusAttribute
        except:
            self.__modelClass = taurus.core.TaurusDevice
        model = str(model)
        TaurusBaseWidget.setModel(self,model)
        if not self._designMode:     #in design mode, no subwidgets are created
            self.updateCustomWidget()
            self.updateLabelWidget()
            self.updateReadWidget()
            self.updateWriteWidget()
            self.updateUnitsWidget()
#        
#    def _setDevModel(self, model):
#        self.__modelClass = taurus.core.TaurusDevice
#        model = str(model)
#        TaurusBaseWidget.setModel(self,model)
#        if not self._designMode:
#            self.setReadWidgetClass(None)
#            self.setReadWidgetClass(None)
#            self.setReadWidgetClass(None)
#            self.setReadWidgetClass(None)
#        
#    def _setAttrModel(self, model):
#        self.__modelClass = taurus.core.TaurusAttribute
#        model = str(model)
#        TaurusBaseWidget.setModel(self,model)
#        if not self._designMode:     #in design mode, no subwidgets are created
#            self.updateLabelWidget()
#            self.updateReadWidget()
#            self.updateWriteWidget()
#            self.updateUnitsWidget()
#        
    def isValueChangedByUser(self):
        try:
            return self._writeWidget.isValueChangedByUser()
        except AttributeError:
            return False
    
    def setDangerMessage(self, dangerMessage=None):
        TaurusBaseWidget.setDangerMessage(self, dangerMessage)
        try:
            return self._writeWidget.setDangerMessage(dangerMessage)
        except AttributeError:
            pass
    
    def setForceDangerousOperations(self, yesno):
        TaurusBaseWidget.setForceDangerousOperations(self, yesno)
        try:
            return self._writeWidget.setForceDangerousOperations(yesno)
        except AttributeError:
            pass
        
    def hasPendingOperations(self):
        '''self.getPendingOperations will alwaysd return an empty list, but still
        self.hasPendingOperations will look at the writeWidget's operations.
        If you want to ask the TaurusValue for its pending operations, call
        self.writeWidget().getPendingOperations()'''
        w = self.writeWidget()
        if w is None: return []
        return w.hasPendingOperations()
        
    
    def updatePendingOpsStyle(self):
        if self._labelWidget is None: return
        if self.hasPendingOperations():
            self._labelWidget.setStyleSheet(
                'border-style: solid ; border-width: 1px; border-color: blue; color: blue; border-radius:4px;')
        else:
            self._labelWidget.setStyleSheet(
                'border-style: solid; border-width: 1px; border-color: transparent; color: black;  border-radius:4px;')
            
    def getLabelConfig(self):
        return self._labelConfig
    
    @Qt.pyqtSignature("setLabelConfig(QString)")
    def setLabelConfig(self, config):
        self._labelConfig = config
        self.updateLabelWidget()
        
    def resetLabelConfig(self):
        self._labelConfig = 'label'
        self.updateLabelWidget()
    
    @classmethod
    def getQtDesignerPluginInfo(cls):
        ret = TaurusBaseWidget.getQtDesignerPluginInfo()
        ret['module'] = 'taurus.qt.qtgui.panel'
        ret['icon'] = ":/designer/label.png"
        return ret
        
    ########################################################
    ## Qt properties (for designer)
    model = Qt.pyqtProperty("QString", TaurusBaseWidget.getModel,  setModel, TaurusBaseWidget.resetModel)
    preferredRow = Qt.pyqtProperty("int", getPreferredRow, setPreferredRow, resetPreferredRow)
    labelWidgetClass = Qt.pyqtProperty("QString", getLabelWidgetClass, setLabelWidgetClass, resetLabelWidgetClass)
    readWidgetClass = Qt.pyqtProperty("QString", getReadWidgetClass, setReadWidgetClass, resetReadWidgetClass)
    writeWidgetClass = Qt.pyqtProperty("QString", getWriteWidgetClass, setWriteWidgetClass, resetWriteWidgetClass)
    unitsWidgetClass = Qt.pyqtProperty("QString", getUnitsWidgetClass, setUnitsWidgetClass, resetUnitsWidgetClass)
    labelConfig = Qt.pyqtProperty("QString", getLabelConfig, setLabelConfig, resetLabelConfig)
    allowWrite = Qt.pyqtProperty("bool", getAllowWrite, setAllowWrite, resetAllowWrite)
    modifiableByUser = Qt.pyqtProperty("bool", TaurusBaseWidget.isModifiableByUser, TaurusBaseWidget.setModifiableByUser, TaurusBaseWidget.resetModifiableByUser)

class TaurusValuesFrame(TaurusFrame):
    '''This is a container specialiced into containing TaurusValue widgets.
    It should be used Only for TaurusValues'''
    
    _model = Qt.QStringList()
    @Qt.pyqtSignature("setModel(QStringList)")    
    def setModel(self, model):
        self._model = model
        for tv in self.getTaurusValues():
            tv.destroy()
        for m in self._model:
            taurusvalue = TaurusValue(self, self.designMode)
            taurusvalue.setMinimumHeight(20)
            taurusvalue.setModel(str(m))
            taurusvalue.setModifiableByUser(self.isModifiableByUser())
    def getModel(self):
        return self._model
                
    def resetModel(self):
        self.setModel(Qt.QStringList())
    
    def getTaurusValueByIndex(self, index):
        '''returns the TaurusValue item at the given index position'''
        return self.getTaurusValues()[index]
    
    def getTaurusValues(self):
        '''returns the list of TaurusValue Objects contained by this frame'''
        return [obj for obj in self.children() if isinstance(obj,TaurusValue)]
    
    @classmethod
    def getQtDesignerPluginInfo(cls):
        '''we don't want this widget in designer'''
        return None  
    

    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # QT properties 
    #-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
   
    model = Qt.pyqtProperty("QStringList", getModel, setModel, resetModel)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if __name__ == "__main__":
    
    import sys

    app = Qt.QApplication(sys.argv)
    form = Qt.QMainWindow()
    #ly=Qt.QVBoxLayout(form)
    #container=Qt.QWidget()
#    container = TaurusValuesFrame()
    from taurus.qt.qtgui.panel import TaurusForm
    container = TaurusForm()
    #ly.addWidget(container)
    form.setCentralWidget(container)

    try:
        from taurus.qt.qtgui.extra_pool import PoolMotorSlim, PoolChannel
        container.setCustomWidgetMap({'SimuMotor':PoolMotorSlim,
                                'Motor':PoolMotorSlim,
                                'PseudoMotor':PoolMotorSlim,
                                'PseudoCounter':PoolChannel,
                                'CTExpChannel':PoolChannel,
                                'ZeroDExpChannel':PoolChannel,
                                'OneDExpChannel':PoolChannel,
                                'TwoDExpChannel':PoolChannel})
    except:
        pass
    
    ##set a model list  
    if len(sys.argv)>1:
        models=sys.argv[1:]
        container.setModel(models)
    else:
        models = []
        
    #models assigned for debugging.... comment out when releasing
    #models=['bl97/pc/dummy-01/Current','bl97/pysignalsimulator/1/value1','bl97/pc/dummy-02/RemoteMode','bl97/pc/dummy-02/CurrentSetpoint','bl97/pc/dummy-02/Current']
    #models=['bl97/pc/dummy-01/Current']
    #models=['bl97/pc/dummy-01/CurrentSetpoint','bl97/pc/dummy-02/Current','bl97/pc/dummy-02/RemoteMode','bl97/pysignalsimulator/1/value1']
    #models=['bl97/pc/dummy-01/CurrentSetpoint','bl97/pc/dummy-02/RemoteMode']
    #container.setModel(models)
    
    #container.getTaurusValueByIndex(0).writeWidget().setDangerMessage('BOOO') #uncomment to test the dangerous operation support
    #container.getTaurusValueByIndex(0).readWidget().setShowState(True)
    #container.getTaurusValueByIndex(0).setWriteWidgetClass(TaurusValueLineEdit)
    #container.setModel(models)
    

    container.setModifiableByUser(True)
    form.show()

        
    
    #show an Attributechooser dialog if no model was given
    if models == []:
        from taurus.qt.qtgui.panel import TaurusModelChooser
        modelChooser = TaurusModelChooser()
        form.connect(modelChooser, Qt.SIGNAL("updateModels"), container.setModel)
        modelChooser.show()
    
    sys.exit(app.exec_())
