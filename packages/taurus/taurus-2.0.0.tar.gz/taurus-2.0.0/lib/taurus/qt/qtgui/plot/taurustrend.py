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
taurustrend.py: Generic trend widget for Taurus
"""
__all__=["ScanTrendsSet", "TaurusTrend", "TaurusTrendsSet"]

import copy
from datetime import datetime
import time
import numpy
import re
from PyQt4 import Qt, Qwt5

import taurus.core
from taurus.core.util import CaselessDict, CaselessList, ArrayBuffer
from taurus.qt.qtgui.base import TaurusBaseComponent
from taurus.qt.qtgui.plot import TaurusPlot
import PyTango

def getArchivedTrendValues(*args, **kwargs):
    try:
        import PyTangoArchiving
        return PyTangoArchiving.getArchivedTrendValues(*args, **kwargs)
    except:
        return []

from taurus.qt.qtcore.tango.macroserver import QDoor

def stripShape(s):
    '''
    returns a shape (a list) based on the given one. The returned shape will
    have all dimensions with length 1 removed, and it will be a list regardless
    of the input shape
    '''
    return [e for e in s if e!=1]

class TaurusTrendsSet(Qt.QObject, TaurusBaseComponent):
    """A collection of TaurusCurves generated from a Taurus Attribute.
    
    If the attribute is a scalar, The Trend Set consists of only one curve
    representing the evolution of the value of the attribute. If the attribute
    is a SPECTRUM, as many curves as the length of the spectrum are created,
    each representing the evolution of the value of a component of the array.
       
    When an event is received, all curves belonging to a TaurusTrendSet are updated.
    
    TaurusTrendSet objects can be considered as containers of (sorted) curves. As
    such, the curves contained by them can be accessed with item notation, as in
    the following example::
    
        attrname = 'a/b/c/d'       #consider this attribute is a SPECTRUM of 3 elements
        ts=TaurusTrendSet(attrname)
        ...                        # wait for a Taurus Event arriving so that the curves are created
        n_curves = len(ts)         #ncurves will be 3 (assuming the event already arrived)
        curve0 = ts[0]             #you can access the curve by index
        curve1 = ts['a/b/c/d[1]']  #and also by name

    
    Note that internally each curve is treated as a RawData curve (i.e., it is
    not aware of events by itself, but it relies on the TaurusTrendSet object to
    update its values)
    
    """
    def __init__(self, name, parent = None, curves=None):
        self._parent = parent #@todo: maybe this should be converted to a weakref?
        Qt.QObject.__init__(self, parent)
        self.call__init__(TaurusBaseComponent, self.__class__.__name__)
        self._history = []
        self.__xBuffer = None
        self.__yBuffer = None
        self.ForcedReadingTimer = None
        try: self.__maxBufferSize = self._parent.getMaxDataBufferSize()
        except: self.__maxBufferSize = 1048576 #(1M= 2**20)
        if curves is None:
            self._curves = {}
            self._orderedCurveNames = []
        else:
            self._curves = curves
            self._orderedCurveNames = curves.keys()
        self.setModel(name)
        
    def __getitem__(self, key):
        if isinstance(key, int):
            key = self._orderedCurveNames[key]
        return self._curves[key]
        
    def __len__(self):
        return len(self._orderedCurveNames)
        
    def __contains__(self, k):
        return self._curves.__contains__(k)
        
    def index(self, curveName):
        '''Returns the index in the trend for the given curve name. It gives an
        exception if the curve is not in the set.
        
        :param curveName: (str) the curvename to find
        
        :return: (int) The index associated to the given curve in the TrendSet
        '''
        return self.getCurveNames().index(curveName)
    
    def setTitleText(self, basetitle):
        '''Sets the title text of the trends this trendset. The name will be
        constructed by appending "[%i]" to the basetitle, where %i is the index
        position of the trend in the trendset. As a particular case, nothing is
        appended if the trendset consists of only one trend.
        
        :param basetitle: (str) The title text to use as a base for constructing
                          the title of each trend belonging to this trendset. It
                          may contain placeholders as those used in
                          :meth:`TaurusCurve.setTitleText`
        
        .. seealso:: :meth:`TaurusCurve.setTitleText`
        '''
        self._titleText = basetitle
        titles = self.compileTitles(basetitle)
        for t,(n,c) in zip(titles, self.getCurves()):
            c.setTitleText(t)
    
    def compileTitles(self, basetitle):
        '''Return a list of titles. Each title corresponds to a trend of the
        trendset (ordered). Substitution of known placeholders is performed.
        
        :param basetitle: (str) A string to be used as base title. It may
                          contain any of the following placeholders (which will
                          be substituted by their corresponding value):
            
            - <label> the attribute label (default)
            - <model> the model name
            - <attr_name> attribute name
            - <attr_full_name> full attribute name
            - <dev_alias> device alias
            - <dev_name> device name
            - <dev_full_name> full device name
            - <current_title> The current title
            - <trend_index> The index of the trend in the trendset
            - <[trend_index]> Same as: `"[<trend_index>]" if Ntrends>1 else ""`
        
        :return: (string_list) a list of title strings that correspond to the
                 list of trends in the set. 
        
        .. seealso:: :meth:`compileBaseTile`
        '''
        basetitle = self.compileBaseTile(basetitle)
        ntrends = len(self._curves)
        if '<trend_index>' in basetitle:
            ret = [basetitle.replace('<trend_index>', "%i"%i) for i in xrange(ntrends)]
        else:
            ret = [basetitle]*ntrends
        return ret
    
    def compileBaseTile(self, basetitle):
        '''Return a base tile for a trend in whichs substitution of known
        placeholders has been performed.
        
        :param basetitle: (str) String on which the substitutions will be
                          performed. The following placeholders are supported:
            
            - <label> the attribute label (default)
            - <model> the model name
            - <attr_name> attribute name
            - <attr_full_name> full attribute name
            - <dev_alias> device alias
            - <dev_name> device name
            - <dev_full_name> full device name
            - <current_title> The current title
            - <[trend_index]> Same as: `"[<trend_index>]" if Ntrends>1 else ""`
        
        **Note** that <trend_index> itself is not substituted!
        
        :return: (str) the compiled base title.
        
        .. seealso:: :meth:`compileTitles`
        '''
        attr = self.getModelObj()
        basetitle = basetitle.replace('<current_title>',self._titleText)
        basetitle = basetitle.replace('<model>',self.getModel())
        if isinstance(attr, taurus.core.TaurusAttribute):
            basetitle = basetitle.replace('<label>',attr.label or '---')
            basetitle = basetitle.replace('<attr_name>',attr.name or '---')
            basetitle = basetitle.replace('<attr_full_name>',attr.getFullName() or '---')
            basetitle = basetitle.replace('<dev_alias>',attr.dev_alias or '---')
            basetitle = basetitle.replace('<dev_name>',attr.dev_name or '---')
        
        dev = attr.getParentObj()
        if dev is not None:
            basetitle = basetitle.replace('<dev_full_name>',dev.getFullName() or '---')

        if len(self._curves)==1: basetitle = basetitle.replace('<[trend_index]>','')
        else: basetitle = basetitle.replace('<[trend_index]>','[<trend_index>]')    
            
        return basetitle
        
    def addCurve(self, name, curve):
        '''add a curve (with the given name) to the internal curves dictionary of this TaurusTrendSet
        
        :param name: (str) the name of the curve
        :param curve: (TaurusCurve) the curve object to be added
        '''  
        self._curves[name] = curve
        self._orderedCurveNames.append(name)
        
    def getCurves(self):
        '''returns an iterator of (curveName,curveObject) tuples associated to
        this TaurusTrendSet. The curves will always be returned in the order they
        were added to the set
        
        :return: (iterator<str,TaurusCurve>)
        '''
        return iter([(n,self._curves[n]) for n in self._orderedCurveNames])
    
    def getCurveNames(self):
        '''returns a list of the names of the curves associated to this
        TaurusTrendSet. The curve names will always be returned in the order they
        were added to the set
        
        :return: (list<str>) the names of the curves
        '''
        return self._orderedCurveNames
        
    def getModelClass(self):
        '''see :meth:`TaurusBaseComponent.getModelClass`'''
        return taurus.core.TaurusAttribute

    def registerDataChanged(self,listener,meth):
        '''see :meth:`TaurusBaseComponent.registerDataChanged`'''
        listener.connect(self, Qt.SIGNAL("dataChanged(const QString &)"), meth)
        
    def unregisterDataChanged(self,listener,meth):
        '''see :meth:`TaurusBaseComponent.unregisterDataChanged`'''
        listener.disconnect(self, Qt.SIGNAL("dataChanged(const QString &)"), meth)

    def _updateHistory(self,model, value):
        '''Update the history data buffers using the latest value from the event
        
        :param model: (str) the source of the event (needed to retrieve data from archiving)
        :param value: (PyTango.DeviceAttribute) the value from the event
        
        :return: (tuple<numpy.ndarray, numpy.ndarray>) Tuple of two arrays
                 containing the X data and Y data, respectively, from the
                 history buffers:
                 - The dtype of both arrays is "double".
                 - The X array will contain timestamps if the parent is in
                   XisTime mode, and a sequential event number otherwise.
                 - The Y array may be two-dimensional if the attribute value is
                   a spectrum
                   
        **Example of return values:** Consider history of 10 events for a
        SPECTRUM attribute with dim_x=8. Then the return value will be (X,Y)
        where X.shape=(10,) and Y.shape=(10,8); X.dtype = Y.dtype = <dtype('float64')>
        '''
        if self.__xBuffer is None:
            self.__xBuffer = ArrayBuffer(numpy.zeros(128, dtype='d'), maxSize=self.__maxBufferSize )
        if self.__yBuffer is None:
            self.__yBuffer = ArrayBuffer(numpy.zeros((128, value.dim_x),dtype='d'), maxSize=self.__maxBufferSize )
        
        self.__yBuffer.append(value.value)
        
        if self._parent.getXIsTime():
            #add the timestamp to the x buffer
            self.__xBuffer.append(value.time.totime())
            ##Adding archiving values
            if self._parent.getUseArchiving():
                if self._parent.getXDynScale() or not self._parent.axisAutoScale(Qwt5.QwtPlot.xBottom): #Do not open a mysql connection for autoscaled plots
                    startdate = self._parent.axisScaleDiv(Qwt5.QwtPlot.xBottom).lowerBound()
                    stopdate = self.__xBuffer[0] #Older value already read
                    try:
                        archived = getArchivedTrendValues(self,model,startdate,stopdate)
                        del(archived[:-self.__xBuffer.remainingSize()]) #limit the archived values according to the maximum size of the buffer
                        t = numpy.zeros(len(archived), dtype=float)
                        y = numpy.zeros((len(archived), value.dim_x), dtype=float)#self.__yBuffer.dtype)
                        for i,v in enumerate(archived):
                            t[i]=v.time.totime()
                            y[i]=v.value
                        self.__xBuffer.extendLeft(t)
                        self.__yBuffer.extendLeft(y)
                    except Exception,e:
                        self.trace('%s: reading from archiving failed: %s'%(datetime.now().isoformat('_'),str(e)))     
        else:
            #add the event number to the x buffer
            try:
                self.__xBuffer.append(1.+self.__xBuffer[-1]) 
            except IndexError: #this will happen when the x buffer is empty
                self.__xBuffer.append(0) 
        
        return self.__xBuffer.contents(), self.__yBuffer.contents()

    
    def handleEvent(self, evt_src, evt_type, evt_value):
        ''' processes Change (and Periodic) Taurus Events: updates the data of all
        curves in the set according to the value of the attribute.
        
        For documentation about the parameters of this method, see
        :meth:`TaurusBaseComponent.handleEvent`'''
        if evt_type == taurus.core.TaurusEventType.Config:
            self.setTitleText(self._parent.getDefaultCurvesTitle())
            return
        
        if evt_type == taurus.core.TaurusEventType.Error:
            return
        
        model = evt_src if evt_src is not None else self.getModelObj()
        if model is None: return
        
        value = evt_value if isinstance(evt_value, PyTango.DeviceAttribute) else self.getModelValueObj()
        if value is None or value.value is None: return
        
        #Check that the data dimensions are consistent with what was plotted before
        ntrends = value.dim_x
        if ntrends != len(self._curves):
            #clean previous curves
            for subname in self.getCurveNames():
                self._parent.detachRawData(subname)
            self._curves = {}
            self._orderedCurveNames = []
            #clean history Buffers
            self.__xBuffer = None
            self.__yBuffer = None
            #create as many curves as the dim_x of the given model and add them to the TrendSet
            name = self.getModelName()
            rawdata = {'x':numpy.zeros(0), 'y':numpy.zeros(0)}
            for i in xrange(ntrends):
                subname = "%s[%i]"%(name,i)
                self._parent.attachRawData(rawdata,id=subname)
                self.addCurve(subname, self._parent.curves[subname])
            self.setTitleText(self._parent.getDefaultCurvesTitle())
            self._parent.autoShowYAxes()

        #get the data from the event
        self._xValues, self._yValues = self._updateHistory(model=model,value=value)

        #assign xvalues and yvalues to each of the curves in self._curves
        for i,(n,c) in enumerate(self.getCurves()):
            c._xValues, c._yValues = self._xValues, self._yValues[:,i]
            
            #update min/max markers
            if c.isVisible():
                if c._showMaxPeak:
                    try: maxpoint = [c._xValues[c._yValues.argmax()],c._yValues.max()]
                    except: maxpoint = [0, 0]
                    c._maxPeakMarker.setValue(*maxpoint)
                    label = c._maxPeakMarker.label()
                    label.setText("Max. " + n + " " + repr(maxpoint[1]) + ' at x = ' + repr(maxpoint[0]))
                    c._maxPeakMarker.setLabel(label)
                if c._showMinPeak:
                    try: minpoint = [c._xValues[c._yValues.argmin()],c._yValues.min()]
                    except: minpoint = [0,0]
                    c._minPeakMarker.setValue(*minpoint)
                    label = c._minPeakMarker.label()
                    label.setText("Max. " + n + " " + repr(minpoint[1]) + ' at x = ' + repr(minpoint[0]))
                    c._minPeakMarker.setLabel(label)

        self.emit(Qt.SIGNAL("dataChanged(const QString &)"), Qt.QString(self.getModel()))
        
    def isReadOnly(self):
        return True
    
    def setMaxDataBufferSize(self, maxSize):
        '''sets the maximum number of events that are stored in the internal
        buffers of the trend. Note that this sets the maximum amount of memory
        used by the data in this trend set to:
        
            ~(1+ntrends)*2*8*maxSize bytes
        
        (the data is stored as float64, and two copies of it are kept: one at
        the x and y buffers and another at the QwtPlotCurve.data)
        
        :param maxSize: (int) the maximum limit
        '''
        self.__xBuffer.setMaxSize(maxSize)
        self.__yBuffer.setMaxSize(maxSize)
        self.__maxBufferSize = maxSize
        
    def maxDataBufferSize(self):
        return self.__maxBufferSize

    def setForcedReadingPeriod(self, msec):
        '''
        Forces periodic reading of the subscribed attribute in order to show
        get new points even if no events are received. It will create fake events as
        needed with the read value. Note that setting a period may yield
        unwanted results when the x axis is set to show event numbers
        (xIsTime==False)since there is no way of distinguishing the real from
        the fake events.
        
        :param msec: (int ) period in milliseconds. Use msec=-1 to stop the
                     forced periodic reading
        '''
        if self.ForcedReadingTimer is None:
            self.ForcedReadingTimer = Qt.QTimer()
            self.connect(self.ForcedReadingTimer, Qt.SIGNAL('timeout()'),self.forceReading)
        self.ForcedReadingTimer.stop()
        if msec >= 0:
            self.ForcedReadingTimer.start(msec)
        
    def forceReading(self, cache=False):
        '''Forces a read of the attribute and generates a fake event with it. 
        By default it ignores the cache
        
        :param cache: (bool) set to True to do cache'd reading (by default is False)
        '''
        self.fireEvent(self.getModelObj(), taurus.core.TaurusEventType.Change, self.getModelValueObj(cache=cache))


class ScanTrendsSet(TaurusTrendsSet):
    """
    An specialized TaurusTrendSet that instead of being updated via events, it
    receives new data directly via a PyQt slot
    
    receives signal containing record data from a scan.
       
    When an event is received, all curves belonging to a TaurusTrendSet are updated.
        
    Note that internally each curve is treated as a RawData curve (i.e., it is
    not aware of events by itself, but it relies on the ScanTrendSet object to
    update its values)
    
    .. seealso:: :class:`TaurusTrendSet`
    """
    def __init__(self, name, parent = None):
        TaurusTrendsSet.__init__(self, None, parent=parent, curves=None)
        self.setModel(name)
        
    def scanDataReceived(self, packet):
        '''
        packet is a dict with {type:str, "data":object} and the accepted types are: data_desc, record_data, record_end
        and the data objects are: seq<ColumnDesc.Todict()>, record.data dict and dict , respectively
        '''
        id,packet = packet
        pcktype = packet.get("type","__UNKNOWN_PCK_TYPE__")
        if pcktype == "data_desc": 
            self._createTrends(packet["data"])
        elif pcktype == "record_data": 
            self._scanLineReceived(packet["data"])
        elif pcktype == "record_end":
            pass
        else:
            self.debug("Ignoring packet of type %s"%repr(pcktype))
        
    def _createTrends(self, datadesc):
        '''
        Creates the needed curves using the information from the DataDesc
        
        For now, it only creates trends for those "columns" containing scalar values
        
        :param datadesc: (seq<dict>) each dict is a ColumnDesc.toDict()
        '''
        self.__datadesc = datadesc
        #clean previous curves
        for subname in self.getCurveNames():
            self._parent.detachRawData(subname)
        self._curves = {}
        self._orderedCurveNames = []
        #clean history Buffers
        self.__xBuffer = None
        self.__yBuffer = None
        #create as many curves as columns containing scalars
        rawdata = {'x':numpy.zeros(0), 'y':numpy.zeros(0)}
        for dd in self.__datadesc:
            if len(stripShape(dd['shape']))== 0:
                label = dd["label"]
                rawdata["title"] = label
                curve = self._parent.attachRawData(rawdata)
                self.addCurve(label, curve)
        self._parent.autoShowYAxes()
        self.emit(Qt.SIGNAL("dataChanged(const QString &)"), Qt.QString(self.getModel()))
    
    def _scanLineReceived(self, recordData):
        '''Receives a recordData dictionary and updates the curves associated to it
        
        .. seealso:: <Sardana>/MacroServer/scan/scandata.py:Record.data
        
        '''
        ##I assume that recordData is a dictionary as the one described for <Sardana>/MacroServer/scan/scandata.py:Record.data
        curvenames = self.getCurveNames()
        
        #update history
        if self.__xBuffer is None:
            self.__xBuffer = ArrayBuffer(numpy.zeros(128, dtype='d'), maxSize=self.maxDataBufferSize() )
        if self.__yBuffer is None:
            self.__yBuffer = ArrayBuffer(numpy.zeros((128, len(curvenames)),dtype='d'), maxSize=self.maxDataBufferSize() )
        
        self.__xBuffer.append(recordData['point_nb'])
                
        y = numpy.array([recordData.get(n,numpy.NaN) for n in curvenames])
        self.__yBuffer.append(y)
        
        self._xValues, self._yValues = self.__xBuffer.contents(), self.__yBuffer.contents()

        #assign xvalues and yvalues to each of the curves in self._curves
        for i,(n,c) in enumerate(self.getCurves()):
            c._xValues, c._yValues = self._xValues, self._yValues[:,i]
        
        #update min/max markers
        if c.isVisible():
            if c._showMaxPeak:
                try: maxpoint = [c._xValues[c._yValues.argmax()],c._yValues.max()]
                except: maxpoint = [0, 0]
                c._maxPeakMarker.setValue(*maxpoint)
                label = c._maxPeakMarker.label()
                label.setText("Max. " + n + " " + repr(maxpoint[1]) + ' at x = ' + repr(maxpoint[0]))
                c._maxPeakMarker.setLabel(label)
            if c._showMinPeak:
                try: minpoint = [c._xValues[c._yValues.argmin()],c._yValues.min()]
                except: minpoint = [0,0]
                c._minPeakMarker.setValue(*minpoint)
                label = c._minPeakMarker.label()
                label.setText("Max. " + n + " " + repr(minpoint[1]) + ' at x = ' + repr(minpoint[0]))
                c._minPeakMarker.setLabel(label)

        self.emit(Qt.SIGNAL("dataChanged(const QString &)"), Qt.QString(self.getModel()))
        
    def connectWithQDoor(self, qdoor):
        '''connects this ScanTrendsSet to a QDoor
        
        :param qdoor: (QDoor or str) either a QDoor instance or the QDoor name
        '''
        if not isinstance(qdoor, QDoor): qdoor = taurus.Device(qdoor)
        self.connect(qdoor, Qt.SIGNAL("recordDataUpdated"), self.scanDataReceived)
    
    def getModel(self):
        return self.__model 
    def setModel(self, model):
        self.__model = model
    
           
class TaurusTrend(TaurusPlot):
    '''
    A :class:`TaurusPlot` -derived widget specialised in plotting trends (i.e.,
    evolution of parameters).

    .. image:: /_static/taurustrend01.png
       :align: center

    TaurusTrend inherits all the features from TaurusPlot (zooming,
    exporting/importing, data inspection,...) and also provides some specific
    features (e.g. fixed-range X scale mode and Archiving support).
    
    For an overview of the features from an user point of view, see the
    :ref:`TaurusTrend User's Interface Guide <trend_ui>`.
    
    You can also see some code that exemplifies the use of TaurusTrend in :ref:`the
    TaurusTrend coding examples <examples_taurustrend>`
    
    Note: if you pass a model that is a Tango SPECTRUM attribute (instead of a
    scalar), TaurusTrend will interpret it as a collection of scalar values and
    will plot a separate trend line for each.
    
    Note 2: As an special case, you can pass a model of the type
    scan://doorname. This will link the TaurusTrend to the given Taurus door and will 
    listen to it for scan record events, which will be plotted.


    
    .. seealso:: :class:`TaurusPlot`,
                 :ref:`TaurusTrend User's Interface Guide <trend_ui>`, 
                 :ref:`The TaurusTrend coding examples <examples_taurustrend>`
    '''
    def __init__(self, parent = None, designMode = False):
        TaurusPlot.__init__(self, parent = parent, designMode = designMode)
        self.trendSets = CaselessDict()
        self._supportedConfigVersions = ["ttc-1"]        
        self._xDynScaleSupported = True
        self._useArchiving = False
        self._usePollingBuffer = False
        self.setDefaultCurvesTitle('<label><[trend_index]>')
        self._maxDataBufferSize = 1048576 #(=2**20, i.e., 1M events))
        self.__qdoorname = None
        self.__initActions()
        self._startingTime = time.time()
        self._archivingWarningLocked = False
        self._forcedReadingPeriod = None
        #Use a rotated labels x timescale by default
        self.setXIsTime(True)
        rotation = -45
        alignment = self.getDefaultAxisLabelsAlignment(self.xBottom, rotation)
        self.setAxisLabelRotation(self.xBottom, rotation)
        self.setAxisLabelAlignment(self.xBottom, alignment)
        #use dynamic scale by default
        self.setXDynScale(True)
        
    
    def __initActions(self):
        '''Create TaurusTrend actions'''
        self._useArchivingAction = Qt.QAction("Use Archiver", None)
        self._useArchivingAction.setCheckable(True)
        self._useArchivingAction.setChecked(self.getUseArchiving())
        self.connect(self._useArchivingAction, Qt.SIGNAL("toggled(bool)"), self._onUseArchivingAction)
        self._usePollingBufferAction = Qt.QAction("Use Polling Buffer", None)
        self._usePollingBufferAction.setCheckable(True)
        self._usePollingBufferAction.setChecked(self.getUsePollingBuffer())
        self.connect(self._usePollingBufferAction, Qt.SIGNAL("toggled(bool)"), self.setUsePollingBuffer)
    
    def setXIsTime(self, enable, axis=Qwt5.QwtPlot.xBottom):
        if enable:
            self.setAxisScale(self.xBottom, self._startingTime-60, self._startingTime)#Set a range of 1 min
        else:
            self.setAxisScale(self.xBottom, 0, 10) #Set a range of 10 events   
        self._useArchivingAction.setEnabled(enable)
        TaurusPlot.setXIsTime(self, enable, axis=axis)
    
    def setScanDoor(self, qdoorname):
        '''
        sets the door to which This TrendSet will listen for scans.
        This removes any previous scan set usinfg this method, but respects scans set with setModel
        '''
        if self.__qdoorname is not None: 
            self.removeModels(["scan://%s"%self.__qdoorname])
        self.addModels(["scan://%s"%qdoorname])
        self.__qdoorname=qdoorname
    
    def updateCurves(self, names):
        '''Defines the curves that need to be plotted. For a TaurusTrend, the
        models can refer to:
        
        - PyTango.SCALARS: they are to be plotted in a trend
        - PyTango.SPECTRUM: each element of the spectrum is considered
          independently as in a)
        
        Note that passing an attribute for X values makes no sense in this case
        
        Internally, every curve is grouped in a TaurusTrendSet. For each SPECTRUM
        attribute, a TrendSet is created, containing as many curves as the
        lenght of the spectrum For eacha SCALAR attribute, a TrendSet containing
        just one curve is created.
        
        :param names: (sequence<str>) a sequence of model names
        
        .. note:: Adding/removing a model will add/remove a whole set. No
                  sub-set adding/removing is allowed.
                  Still, each curve will be independent regarding its
                  properties, and can be hidden/shown independently.
        
        .. seealso:: :meth:`TaurusPlot.updateCurves`
        '''
        self.curves_lock.acquire()
        try:
            # For it to work properly, 'names' must be a CaselessList, just as
            # self.trendSets is a CaselessDict
            del_sets = [ name for name in self.trendSets.keys() if name not in names]
            
            for name in names:
                name = str(name)
                if "|" in name: raise ValueError('composed ("X|Y") models are not supported by TaurusTrend')
                #create a new TrendSet if not already there
                if not self.trendSets.has_key(name):
                    matchScan = re.search(r"scan:\/\/(.*)", name) #check if the model name is of scan type and provides a door
                    if matchScan:
                        tset = ScanTrendsSet(name, parent=self)
                        qdoor = matchScan.group(1) #the name of the door
                        tset.connectWithQDoor(qdoor)
                    else:
                        tset = TaurusTrendsSet(name, parent=self)
                        if self._forcedReadingPeriod is not None: 
                            tset.setForcedReadingPeriod(self._forcedReadingPeriod)
                    self.trendSets[name] = tset
                    tset.registerDataChanged(self, self.curveDataChanged)
            # Trend Sets to be removed
            for name in del_sets:
                name = str(name)
                tset = self.trendSets.pop(name)
                tset.unregisterDataChanged(self, self.curveDataChanged)
                for subname in tset.getCurveNames():
                    self.detachRawData(subname)
            if del_sets:        
                self.autoShowYAxes()
                
            # legend
            self.showLegend(len(self.curves) > 1, forever=False)
            self.replot()
            
        finally:
            self.curves_lock.release()
        
    def getTrendSetNames(self):
        '''returns the names of all TrendSets attached to this TaurusTrend.
        
        :return: (list<str>) a copy of self.trendSets.keys()
        '''
        self.curves_lock.acquire()
        try:
            ret = copy.deepcopy(self.trendSets.keys())
        finally:
            self.curves_lock.release()
        return ret
    
    def getTrendSet(self, name):
        '''gets a trend set object by name.
        
        **Important**: Note that the TrendSet object is not thread safe.
        Therefore, if you access it you must do it protected by the
        TaurusTrend.curves_lock reentrant lock.
        
        :param name: (str) the trend set name
        
        :return: (TaurusTrendSet) the trend set object corresponding to name
        '''
        self.curves_lock.acquire()
        try:
            ret = self.trendSets.get(str(name))
        finally:
            self.curves_lock.release()
        return ret
    
    def changeCurvesTitlesDialog(self, curveNamesList=None):
        '''Shows a dialog to set the curves titles (it will change the current
        curves titles and the default curves titles)
                
        :param curveNamesList: (string_sequence or string_iterator) names of the
                               curves to which the title will be changed (if
                               None given , it will apply to all the TrendsSets
                               and it will also be used as default for newly
                               created ones)
        
        :return: (caselessDict<str,QString> or None) The return value will be
                 `None` if `curveNamesList` is None. Otherwise it will be a
                 dictionary with key=curvename and value=newtitle. 
        
        .. seealso:: :meth:`setCurvesTitle`, :meth:`setDefaultCurvesTitle`
        '''
        newTitlesDict = None
        titletext, ok = Qt.QInputDialog.getText( self,
                                                'New Title for Curves',
                                                'New text to be used for the curves.'\
                                                'You can use any of the following placeholders:\n'\
                                                '<label>, <model>, <attr_name>, <attr_full_name>,'\
                                                '<dev_alias>, <dev_name>, <dev_full_name>,' \
                                                '<current_title>, <trend_index>, <[trend_index]>',
                                                Qt.QLineEdit.Normal,
                                                self._defaultCurvesTitle)
        if ok:
            titletext = str(titletext)
            if curveNamesList is None:
                self.setDefaultCurvesTitle(titletext)
                self.setTrendSetsTitles(titletext)
            else:
                self.curves_lock.acquire()
                try:
                    newTitlesDict = CaselessDict() 
                    for curveName in curveNamesList:
                        curvetitle = titletext
                        for ts in self.trendSets.itervalues():
                            if curveName in ts:
                                curvetitle = ts.compileBaseTile(curvetitle)
                                curvetitle = curvetitle.replace('<trend_index>', "%i"%ts.index(curveName))
                                break
                        curve = self.curves.get(curveName)
                        curve.setTitleText(curvetitle)
                        newTitlesDict[curveName] = curve.title().text()
                    self.updateLegend(self.legend())
                    return newTitlesDict
                finally:
                    self.curves_lock.release()
        return newTitlesDict
    
    def setTrendSetsTitles(self, basetitle, setNames=None):
        '''Calls setTitleText(basetitle) for each Trend Set set in setNames
        
        :param basetitle: (str) the base title
        :param setNames: (sequence<str> or iterator<str>) names of the sets to be changed
        
        See: TaurusTrendsSet.setTitleText
        '''
        self.curves_lock.acquire()
        try:
            if setNames is None: setNames = self.trendSets.iterkeys()
            for tname in setNames:
                if tname in self.trendSets:
                    self.trendSets[tname].setTitleText(basetitle)
        finally:
            self.curves_lock.release()
        self.updateLegend(self.legend())

    @Qt.pyqtSignature("dataChanged(const QString &)")
    def curveDataChanged(self, name):
        '''slot that is called whenever a curve emits a dataChanged signal
        
        :emits: "dataChanged(const QString &)"
        
        :param name: (str) curve name
        '''
        name=str(name)
        self.curves_lock.acquire()
        try:
            for n,curve in self.trendSets[name].getCurves():
                curve.setData(curve._xValues,curve._yValues)
            #self._zoomer.setZoomBase()
            if self.getXDynScale() and len(curve._xValues)>0: #keep the scale width constant, but translate it to get the last value
                max= curve._xValues[-1]
                min=max-self.getXAxisRange() 
                self.setAxisScale(Qwt5.QwtPlot.xBottom, min, max)
        finally:
            self.curves_lock.release()
        self.emit(Qt.SIGNAL("dataChanged(const QString &)"), Qt.QString(name))
        self.replot()
    
    def setPaused(self, paused = True):
        '''Pauses itself and other listeners (e.g. the trendsets) depending on it
        
        .. seealso:: :meth:`TaurusBaseComponent.setPaused`
        '''
        for ts in self.trendSets.itervalues():
            ts.setPaused(paused)
        self._isPaused = paused
    
    def createConfig(self, curvenames=None, **kwargs):
        '''Returns a pickable dictionary containing all relevant information
        about the current plot.
        For Tango attributes it stores the attribute name and the curve properties
        For raw data curves, it stores the data as well.
        
        Hint: The following code allows you to serialize the configuration
        dictionary as a string (which you can store as a QSetting, or as a Tango
        Attribute)::
        
            import pickle
            c = pickle.dumps(taurusplot.createConfig())  #c is a string that can be stored
                
        :param names:  (sequence<str>) a sequence of TrendSet names for which the
                       configuration will be stored (all by default).
        
        :return: (dict) configurations (which can be loaded with applyConfig)
        '''
        configdict = TaurusPlot.createConfig(self, curvenames=curvenames) #use the superclass configdict as a starting point
        if curvenames is None: curvenames = CaselessList(self.trendSets.keys())
        configdict.pop("TangoCurves") #delete the TangoCurves key since it is meaningless in a TaurusTrend
        tsetsdict = CaselessDict()
        rawdatadict = CaselessDict(configdict["RawData"])
        self.curves_lock.acquire()
        try:
            for tsname,ts in self.trendSets.iteritems():
                if tsname in curvenames:
                    tsetsdict[tsname] = tsname #store a dict containing just model names (key and value are the same)
                for cname in CaselessList(ts.getCurveNames()):
                    rawdatadict.pop(cname)#clean the rawdatadict of rawdata curves that come from trendsets (but we keep the properties!)                
        finally:
            self.curves_lock.release()
        configdict["TrendSets"] = tsetsdict
        configdict["RawData"] = rawdatadict
        return configdict
        
    def applyConfig(self, configdict, **kwargs):
        """applies the settings stored in a configdict to the current plot.
        
        :param configdict: (dict)
        
        .. seealso:: :meth:`createConfig`
        """
        if not self.checkConfigVersion(configdict): return
        #attach the curves
        for rd in configdict["RawData"].values(): self.attachRawData(rd)
        models = configdict["TrendSets"].values()
        self.addModels(models)
        for m in models:
            tset = self.trendSets[m]
            tset.fireEvent(None, taurus.core.TaurusEventType.Change, None) #a fake event to force generating the curves
        #set curve properties
        self.setCurveAppearanceProperties(configdict["CurveProp"])
        self.updateLegend(force=True)
        #set the axes
        self.applyAxesConfig(configdict["Axes"])
        #set other misc configurations
        self.applyMiscConfig(configdict["Misc"])

    @classmethod
    def getQtDesignerPluginInfo(cls):
        """Returns pertinent information in order to be able to build a valid
        QtDesigner widget plugin
        
        :return: (dict) a map with pertinent designer information"""
        return {
            'module'    : 'taurus.qt.qtgui.plot',
            'group'     : 'Taurus Display Widgets',
            'icon'      : ':/designer/qwtplot.png',
            'container' : False }
                
    def setEventFilters(self, filters=None, tsetnames=None):
        '''propagates a list of taurus filters to the trendsets given by tsetnames.
        See :meth:`TaurusBaseComponent.setEventFilters`
        '''
        if tsetnames is None: tsetnames=self.trendSets.keys()
        self.curves_lock.acquire()
        try:
            for name in tsetnames:
                self.trendSets[name].setEventFilters(filters)
        finally:
            self.curves_lock.release()
             
    def setUsePollingBuffer(self, enable):
        '''enables/disables looking up in the PollingBuffer for data
        
        :param enable: (bool) if True, PollingBuffer values will be used if available
        '''
        self._usePollingBuffer = enable
        self.replot()

    def getUsePollingBuffer(self):
        '''whether TaurusTrend is looking for data in the PollingBuffer
        
        :return: (bool)
        
        .. seealso:: :meth:`setUsePollingBuffer`
        '''
        return self._usePollingBuffer

    def resetUsePollingBuffer(self):
        '''Same as setUsePollingBuffer(True)'''
        self.setUsePollingBuffer(True)   
    
    def setUseArchiving(self, enable):
        '''enables/disables looking up in the archiver for data stored before
        the Trend was started
        
        :param enable: (bool) if True, archiving values will be used if available
        '''
        if not self.getXIsTime():
            self.info('ignoring setUseArchiving. Reason: not in X time scale')
        self._useArchivingAction.setChecked(enable)
        
    def getUseArchiving(self):
        '''whether TaurusTrend is looking for data in the archiver when needed
        
        :return: (bool)
        
        .. seealso:: :meth:`setUseArchiving`
        '''
        return self._useArchiving

    def resetUseArchiving(self):
        '''Same as setUseArchiving(True)'''
        self.setUseArchiving(True)   
    
    def _onUseArchivingAction(self, enable):
        '''slot being called when toggling the useArchiving action
        
        .. seealso:: :meth:`setUseArchiving`
        '''
        if enable:
            self._archivingWarningThresshold = self._startingTime - 600 #10 min before the widget was created
            self.connect(self.axisWidget(self.xBottom), Qt.SIGNAL("scaleDivChanged ()"), self._scaleChangeWarning)
        else:
            self.disconnect(self.axisWidget(self.xBottom), Qt.SIGNAL("scaleDivChanged ()"), self._scaleChangeWarning)
            self._archivingWarningThresshold = None
        self._useArchiving = enable
        self.replot()

    def _scaleChangeWarning(self):
        '''slot that may be called when the x axis changes the scale'''
        sdiv = self.axisScaleDiv(self.xBottom)
        min = sdiv.lowerBound()
        if min < self._archivingWarningThresshold:
            self.showArchivingWarning()
            self._archivingWarningThresshold = min-2*sdiv.range() #lower the thresshold by twice the current range 
    
    def showArchivingWarning(self):
        '''shows a dialog warning of the potential isuues with 
        archiving performance. It offers the user to disable archiving retrieval'''
        #stop the scale change notification temporally (to avoid duplicate warnings)
        self.disconnect(self.axisWidget(self.xBottom), Qt.SIGNAL("scaleDivChanged ()"), self._scaleChangeWarning)
        #show a dialog
        dlg = Qt.QDialog(self)
        dlg.setLayout(Qt.QVBoxLayout())
        dlg.setWindowTitle('Archiving warning')
        msg = 'Archiving retrieval is enabled.\n'+\
              'Rescaling to previous date/times may cause performance loss.\n'+\
              '\nDisable archiving retrieval?\n'            
        dlg.layout().addWidget(Qt.QLabel(msg))
        rememberCB = Qt.QCheckBox('Do not ask again')
        buttonbox = Qt.QDialogButtonBox()
        buttonbox.addButton(Qt.QPushButton('&Keep enabled'), buttonbox.RejectRole)
        buttonbox.addButton(Qt.QPushButton('&Disable'), buttonbox.AcceptRole)
        dlg.layout().addWidget(buttonbox)
        dlg.connect(buttonbox, Qt.SIGNAL('accepted()'), dlg.accept)
        dlg.connect(buttonbox, Qt.SIGNAL('rejected()'), dlg.reject)
        dlg.layout().addWidget(rememberCB)
        dlg.exec_()
        #disable archiving if the user said so
        if dlg.result() == dlg.Accepted:
            self.setUseArchiving(False)
        #restore the scale change notification only if the user chose to keep archiving AND did not want to disable warnings
        elif not rememberCB.isChecked(): 
            self.connect(self.axisWidget(self.xBottom), Qt.SIGNAL("scaleDivChanged ()"), self._scaleChangeWarning) 
    
    def setMaxDataBufferSize(self, maxSize):
        '''sets the maximum number of events that can be plotted in the trends
        
        :param maxSize: (int) the maximum limit
        
        .. seealso:: :meth:`TaurusTrendSet.setMaxDataBufferSize`
        '''
        self.curves_lock.acquire()
        try:
            for ts in self.trendSets.itervalues():
                ts.setMaxDataBufferSize(maxSize)
        finally:
            self.curves_lock.release()
        self._maxDataBufferSize = maxSize
        
    def getMaxDataBufferSize(self):
        '''returns the maximum number of events that can be plotted in the trend
        
        :return: (int)
        '''
        return self._maxDataBufferSize
            
    def resetMaxDataBufferSize(self):
        '''Same as setMaxDataBufferSize(1048576)  (i.e. 1M of events)'''
        self.setMaxDataBufferSize(1048576)
    
    def _canvasContextMenu(self):
        ''' see :meth:`TaurusPlot._canvasContextMenu` '''
        menu = TaurusPlot._canvasContextMenu(self)
        menu.insertAction(self._setCurvesTitleAction, self._useArchivingAction)
        menu.insertAction(self._setCurvesTitleAction, self._usePollingBufferAction)
        return menu
    
    def setForcedReadingPeriod(self, msec, tsetnames=None):
        '''Sets the forced reading period for the trend sets given by tsetnames.
        
        :param msec: (int) period in milliseconds
        :param tsetnames: (seq<str> or None) names of the curves for which the forced 
                          reading is set. If None passed, this will be set for all 
                          present *and future* curves added to this trend
    
        .. seealso: :meth:`TaurusTrendSet.setForcedReadingPeriod`
        '''
        if tsetnames is None: 
            tsetnames=self.trendSets.keys()
            self._forcedReadingPeriod = msec
        self.curves_lock.acquire()
        try:
            for name in tsetnames:
                self.trendSets[name].setForcedReadingPeriod(msec)
        finally:
            self.curves_lock.release()
    
    useArchiving = Qt.pyqtProperty("bool", getUseArchiving, setUseArchiving, resetUseArchiving)
    usePollingBuffer = Qt.pyqtProperty("bool", getUsePollingBuffer, setUsePollingBuffer, resetUsePollingBuffer)
    maxDataBufferSize = Qt.pyqtProperty("int", getMaxDataBufferSize, setMaxDataBufferSize, resetMaxDataBufferSize)
    

def main():
    import sys
    import taurus.qt.qtgui.application
    import taurus.core.util.argparse
    
    parser = taurus.core.util.argparse.get_taurus_parser()
    parser.usage = "%prog [options] [<model1> [<model2>] ...]"
    parser.add_option("-x", "--x-axis-mode", dest="x_axis_mode", default='t', metavar="t|e",
                  help="interprete X values as either timestamps (t) or event numbers (e). Accepted values: t|e")
    parser.add_option("--config", "--config-file", dest="config_file", default=None,
                  help="use the given config file for initialization")
    parser.add_option("--export", "--export-file", dest="export_file", default=None,
                  help="use the given file to as output instead of showing the plot")
    parser.add_option("-r", "--forced-read", dest="forced_read_period", type="int", default=-1, metavar="PERIOD",
                  help="force Tautrend to re-read the attributes every PERIOD milliseconds")
    parser.add_option("-a", "--use-archiving", action="store_true", dest="use_archiving", default=False)

    
    
    app = taurus.qt.qtgui.application.TaurusApplication(cmd_line_parser=parser)
    args = app.get_command_line_args()
    options = app.get_command_line_options()
    if options.x_axis_mode.lower() not in ['t', 'e']:
        parser.print_help(sys.stderr)
        sys.exit(1)

    models = args
    
    w = TaurusTrend()
    w.setWindowTitle('TaurusTrend')
    
    #xistime option
    w.setXIsTime(options.x_axis_mode.lower() == 't')
    #configuration file option
    if options.config_file is not None: w.loadConfig(options.config_file)
    #set models 
    if models: w.setModel(models)
    #export option
    if options.export_file is not None:
        curves = dict.fromkeys(w.trendSets.keys(),0)        
        def exportIfAllCurves(curve,trend=w,counters=curves):
            curve = str(curve)
            print '*'*10 + ' %s: Event received for %s  '%(datetime.now().isoformat(),curve) +'*'*10        
            if curve in counters:
                counters[curve]+=1
                if all(counters.values()):
                    trend.exportPdf(options.export_file)
                    print '*'*10 + ' %s: Exported to : %s  '%(datetime.now().isoformat(),options.export_file) +'*'*10        
                    trend.close()
            return
        if not curves: w.close()
        else:
            for ts in w.trendSets.values():
                Qt.QObject.connect(ts, Qt.SIGNAL("dataChanged(const QString &)"), exportIfAllCurves)
        sys.exit(app.exec_()) #exit without showing the widget
    
    # period option
    if options.forced_read_period >=0:
        w.setForcedReadingPeriod(options.forced_read_period)
    
    #archiving option     
    w.setUseArchiving(options.use_archiving)
    
    #show the widget
    w.show()
    
    #if no models are passed, show the data import dialog
    if len(models) == 0 and options.config_file is None:
        w.showDataImportDlg()
    
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()    

