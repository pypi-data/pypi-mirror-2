# -*- coding: utf-8 -*-
"""
neuroshareio
==================

Classe for wrapping neuroshare dlls.
neuroshare is C API for reading neural data.
Neuroshare provide also a Matlab and a python API on top of that.
The python API has been completly rewritten using ctypes here.

Neurohare is a open source API but each dll is provided directly by the vendor.
We provide here some of them that downlable in vendors web site.

This io run only on win32 platforms.
For some vendors (Spike2/CED , Clampfit/Abf) , neo.io provide also a pure python
readers, you should prefer them.



@author : sgarcia

"""







#from baseio import BaseIO
from neo.io import BaseIO
from neo.core import *
from numpy import *
import re
import os, sys
import datetime
import ctypes
from ctypes import byref, c_char_p, c_uint32, c_char, c_double, c_int16, c_int32 , c_ulong
from numpy import *


class NeuroshareIO(BaseIO):
    """
    Base Classe for reading with neuroshare API.
    """
    
    is_readable        = True
    is_writable        = False

    supported_objects            = [Segment , AnalogSignal, Event, SpikeTrain ]
    readable_objects    = [Segment]
    writeable_objects    = []  
    
    has_header         = False
    is_streameable     = False
    
    read_params        = { Segment : [] }
    write_params       = { Segment : [] }
    
    name               = 'neurohare'
    
    def __init__(self , dllname = '') :
        """
        
        **Arguments**
        
        """
        self.dllname = dllname
        BaseIO.__init__(self)


    def read(self , **kargs):
        """
        Read the file.
        Return a neo.Segment
        See read_segment for detail.
        """
        return self.read_segment( **kargs)
    
    def read_segment(self):
        """
        **Arguments**
            
        
        """
        seg = Segment()
        
        #neuroshare = ctypes.windll.LoadLibrary(self.dllname)
        # FIXME : is that coreect or an ugly solution
        neuroshare = ctypes.windll.LoadLibrary(os.path.join(os.path.dirname(__file__),self.dllname))
        
        
        # API version
        info = ns_LIBRARYINFO()
        neuroshare.ns_GetLibraryInfo(byref(info) , ctypes.sizeof(info))
        print 'API ver' , info.dwAPIVersionMaj, '.',info.dwAPIVersionMin
        
        # open file
        hFile = c_uint32(0)
        neuroshare.ns_OpenFile(c_char_p(self.filename) ,byref(hFile))
        fileinfo = ns_FILEINFO()
        neuroshare.ns_GetFileInfo(hFile, byref(fileinfo) , ctypes.sizeof(fileinfo))
        print fileinfo.dwEntityCount
        # read all entities
        for dwEntityID in range(fileinfo.dwEntityCount):
            print 'dwEntityID' , dwEntityID 
            entityInfo = ns_ENTITYINFO()
            neuroshare.ns_GetEntityInfo( hFile, dwEntityID,
                                        byref(entityInfo), ctypes.sizeof(entityInfo))
            print 'type', entityInfo.dwEntityType,entity_types[entityInfo.dwEntityType], 'count', entityInfo.dwItemCount
            print  entityInfo.szEntityLabel 

            # EVENT
            if entity_types[entityInfo.dwEntityType] == 'ns_ENTITY_EVENT': 
                pEventInfo = ns_EVENTINFO()
                neuroshare.ns_GetEventInfo ( hFile,  dwEntityID, 
                                            byref(pEventInfo), ctypes.sizeof(pEventInfo))
                print pEventInfo.szCSVDesc, pEventInfo.dwEventType, pEventInfo.dwMinDataLength, pEventInfo.dwMaxDataLength
                
                if pEventInfo.dwEventType == 0: #TEXT
                    pData = ctypes.create_string_buffer(pEventInfo.dwMaxDataLength)
                elif pEventInfo.dwEventType == 1:#CVS
                    pData = ctypes.create_string_buffer(pEventInfo.dwMaxDataLength)
                elif pEventInfo.dwEventType == 2:# 8bit
                    pData = ctypes.c_byte(0)
                elif pEventInfo.dwEventType == 3:# 16bit
                    pData = ctypes.c_int16(0)
                elif pEventInfo.dwEventType == 4:# 32bit
                    pData = ctypes.c_int32(0)
                pdTimeStamp  = c_double(0.)
                pdwDataRetSize = c_uint32(0)
                for dwIndex in range(entityInfo.dwItemCount ):
                    neuroshare.ns_GetEventData ( hFile, dwEntityID, dwIndex,
                                        byref(pdTimeStamp), byref(pData),
                                        ctypes.sizeof(pData), byref(pdwDataRetSize) )
                    #print 'dwIndex' , dwIndex , pdTimeStamp, pData , pdwDataRetSize
                    event = Event(time = pdTimeStamp.value)
                    #event.label = 
                    #event.type = 'channel %d' % channel_num
                    event.type = entityInfo.szEntityLabel
                    # TODO event.type
                    seg._events.append(event)
                    
            # analog
            if entity_types[entityInfo.dwEntityType] == 'ns_ENTITY_ANALOG': 
                pAnalogInfo = ns_ANALOGINFO()
                neuroshare.ns_GetAnalogInfo( hFile, dwEntityID,
                                        byref(pAnalogInfo),
                                        ctypes.sizeof(pAnalogInfo) )
                print 'dSampleRate' , pAnalogInfo.dSampleRate , pAnalogInfo.szUnits
                dwStartIndex = c_uint32(0)
                dwIndexCount = entityInfo.dwItemCount
                #dwIndexCount = 999
                # FIXME
                pdwContCount = c_uint32(0)
                pData = zeros( (entityInfo.dwItemCount,), dtype = 'f8')
                ns_RESULT = neuroshare.ns_GetAnalogData ( hFile,  dwEntityID,  dwStartIndex,
                                 dwIndexCount, byref( pdwContCount) , pData.ctypes.data)
                print 'ns_RESULT' , ns_RESULT
                pszMsgBuffer  = ctypes.create_string_buffer(" "*256)
                neuroshare.ns_GetLastErrorMsg(byref(pszMsgBuffer), 256)
                print 'pszMsgBuffer' , pszMsgBuffer.value
                
                print 'pdwContCount', pdwContCount, dwIndexCount
                #sig = pData[:pdwContCount.value]
                #print sig.shape
                dwIndex = 0
                pdTime = c_double(0)
                neuroshare.ns_GetTimeByIndex( hFile,  dwEntityID,  dwIndex, byref(pdTime))
                print 'pdTime' , pdTime.value
                anaSig = AnalogSignal(sampling_rate = pAnalogInfo.dSampleRate,
                                    signal = pData[:pdwContCount.value],
                                    t_start = pdTime.value)
                seg._analogsignals.append( anaSig )
                
            
            #segment
            if entity_types[entityInfo.dwEntityType] == 'ns_ENTITY_SEGMENT': 
                
                pdwSegmentInfo = ns_SEGMENTINFO()
                ns_RESULT = neuroshare.ns_GetSegmentInfo( hFile,  dwEntityID,
                                                 byref(pdwSegmentInfo), ctypes.sizeof(pdwSegmentInfo) )
                print 'ns_RESULT' , ns_RESULT
                pszMsgBuffer  = ctypes.create_string_buffer(" "*256)
                neuroshare.ns_GetLastErrorMsg(byref(pszMsgBuffer), 256)
                print 'pszMsgBuffer' , pszMsgBuffer.value
                
                print 'pdwSegmentInfo.dwSourceCount' , pdwSegmentInfo.dwSourceCount
                for dwSourceID in range(pdwSegmentInfo.dwSourceCount) :
                    pSourceInfo = ns_SEGSOURCEINFO()
                    neuroshare.ns_GetSegmentSourceInfo( hFile,  dwEntityID, dwSourceID,
                                    byref(pSourceInfo), ctypes.sizeof(pSourceInfo) )
                
                pdTimeStamp  = c_double(0.)
                
                dwDataBufferSize = pdwSegmentInfo.dwMaxSampleCount*pdwSegmentInfo.dwSourceCount
                pData = zeros( (dwDataBufferSize), dtype = 'f8')
                pdwSampleCount = c_uint32(0)
                pdwUnitID= c_uint32(0)
                for dwIndex in range(entityInfo.dwItemCount ):
                    ns_RESULT = neuroshare.ns_GetSegmentData ( hFile,  dwEntityID,  dwIndex,
                            byref(pdTimeStamp), pData.ctypes.data,
                             dwDataBufferSize, byref(pdwSampleCount),
                            byref(pdwUnitID ) )
                    
                    #print 'dwDataBufferSize' , dwDataBufferSize,pdwSampleCount , pdwUnitID
                    nsample ,nsource = pdwSampleCount.value,pdwSegmentInfo.dwSourceCount
                    print 'nsample ,nsource' , nsample ,nsource
                    waveform = pData[:nsample*nsource].reshape(nsample ,nsource)
#                    print waveform.shape , pdwSegmentInfo.dSampleRate , waveform
                    
                    event = Event(time = pdTimeStamp.value)
                    event.waveform = waveform
                    event.sampling_rate = pdwSegmentInfo.dSampleRate #FIXME
                    event.type = entityInfo.szEntityLabel
                    seg._events.append(event)
                    
                    
            # neuralevent
            if entity_types[entityInfo.dwEntityType] == 'ns_ENTITY_NEURALEVENT': 
                
                pNeuralInfo = ns_NEURALINFO()
                neuroshare.ns_GetNeuralInfo ( hFile,  dwEntityID,
                                 byref(pNeuralInfo), ctypes.sizeof(pNeuralInfo))
                print pNeuralInfo.dwSourceUnitID , pNeuralInfo.szProbeInfo
                pData = zeros( (entityInfo.dwItemCount,), dtype = 'f8')
                dwStartIndex = 0
                dwIndexCount = entityInfo.dwItemCount
                neuroshare.ns_GetNeuralData( hFile,  dwEntityID,  dwStartIndex,
                                                 dwIndexCount,  pData.ctypes.data)
                print pData.shape
                spikeTr = SpikeTrain(spike_times = pData)
                seg._spiketrains.append(spikeTr)
        
        # close
        neuroshare.ns_CloseFile(hFile)
        return seg





class NeuroshareSpike2IO(NeuroshareIO):
    """
    Class for reading CED with neuroshare API.
    """
    name               = 'Spike 2 CED neuroshare'
    extensions          = [ 'smr' ]
    def __init__(self , filename = None) :
        """
        Class for reading CED with neuroshare API.
        
        **Arguments**
            filename : the filename to read
        """        
        NeuroshareIO.__init__(self, dllname = 'NSCEDSON')
        self.filename = filename

        


class NeurosharePlexonIO(NeuroshareIO):
    """
    Classe for reading plexon with neuroshare API.
    """
    name               = 'Plexon neuroshare'
    extensions          = [ 'nex' ]
    def __init__(self , filename = None) :
        """
         Classe for reading plexon with neuroshare API.
        
        **Arguments**
            filename : the filename to read
        """        
        NeuroshareIO.__init__(self, dllname = 'nsPlxLibrary')
        self.filename = filename


class NeuroshareAlphaOmegaIO(NeuroshareIO):
    """
    Classe for reading alpha omega with neuroshare API.
    """
    name               = 'AlphaOmega neuroshare'
    extensions          = [ 'map' ]
    def __init__(self , filename = None) :
        """
        Classe for reading alpha omega with neuroshare API.
        **Arguments**
            filename : the filename to read
        """      
        NeuroshareIO.__init__(self, dllname = 'nsAOLibrary')
        self.filename = filename


class NeuroshareTdtIO(NeuroshareIO):
    """
    Classe for reading  tdt with neuroshare API.
    """
    name               = 'TDT neuroshare'
    extensions          = [ 'tank' ]
    def __init__(self , filename = None) :
        """
        Classe for reading  tdt with neuroshare API.
        **Arguments**
            filename : the filename to read
        """      
        NeuroshareIO.__init__(self, dllname = 'nsTDTLib')
        self.filename = filename



# neuroshare structures

class ns_FILEDESC(ctypes.Structure):
    _fields_ = [('szDescription', c_char*32),
                ('szExtension', c_char*8),
                ('szMacCodes', c_char*8),
                ('szMagicCode', c_char*32),
                ]


class ns_LIBRARYINFO(ctypes.Structure):
    _fields_ = [('dwLibVersionMaj', c_uint32),
                ('dwLibVersionMin', c_uint32),
                ('dwAPIVersionMaj', c_uint32),
                ('dwAPIVersionMin', c_uint32),
                ('szDescription', c_char*64),
                ('szCreator',c_char*64),
                ('dwTime_Year',c_uint32),
                ('dwTime_Month',c_uint32),
                ('dwTime_Day',c_uint32),
                ('dwFlags',c_uint32),
                ('dwMaxFiles',c_uint32),
                ('dwFileDescCount',c_uint32),
                ('FileDesc',ns_FILEDESC*16),
                ]

class ns_FILEINFO(ctypes.Structure):
    _fields_ = [('szFileType', c_char*32),
                ('dwEntityCount', c_uint32),
                ('dTimeStampResolution', c_double),
                ('dTimeSpan', c_double),
                ('szAppName', c_char*64),
                ('dwTime_Year',c_uint32),
                ('dwTime_Month',c_uint32),
                ('dwReserved',c_uint32),
                ('dwTime_Day',c_uint32),
                ('dwTime_Hour',c_uint32),
                ('dwTime_Min',c_uint32),
                ('dwTime_Sec',c_uint32),
                ('dwTime_MilliSec',c_uint32),
                ('szFileComment',c_char*256),
                ]

class ns_ENTITYINFO(ctypes.Structure):
    _fields_ = [('szEntityLabel', c_char*32),
                ('dwEntityType',c_uint32),
                ('dwItemCount',c_uint32),
                ]

entity_types = { 0 : 'ns_ENTITY_UNKNOWN' ,
                    1 : 'ns_ENTITY_EVENT' ,
                    2 : 'ns_ENTITY_ANALOG' ,
                    3 : 'ns_ENTITY_SEGMENT' ,
                    4 : 'ns_ENTITY_NEURALEVENT' ,
                    }

class ns_EVENTINFO(ctypes.Structure):
    _fields_ = [
                ('dwEventType',c_uint32),
                ('dwMinDataLength',c_uint32),
                ('dwMaxDataLength',c_uint32),
                ('szCSVDesc', c_char*128),
                ]

class ns_ANALOGINFO(ctypes.Structure):
    _fields_ = [
                ('dSampleRate',c_double),
                ('dMinVal',c_double),
                ('dMaxVal',c_double),
                ('szUnits', c_char*16),
                ('dResolution',c_double),
                ('dLocationX',c_double),
                ('dLocationY',c_double),
                ('dLocationZ',c_double),
                ('dLocationUser',c_double),
                ('dHighFreqCorner',c_double),
                ('dwHighFreqOrder',c_uint32),
                ('szHighFilterType', c_char*16),
                ('dLowFreqCorner',c_double),
                ('dwLowFreqOrder',c_uint32),
                ('szLowFilterType', c_char*16),
                ('szProbeInfo', c_char*128),
            ]


class ns_SEGMENTINFO(ctypes.Structure):
    _fields_ = [
                ('dwSourceCount',c_uint32),
                ('dwMinSampleCount',c_uint32),
                ('dwMaxSampleCount',c_uint32),
                ('dSampleRate',c_double),
                ('szUnits', c_char*32),
                ]

class ns_SEGSOURCEINFO(ctypes.Structure):
    _fields_ = [
                ('dMinVal',c_double),
                ('dMaxVal',c_double),
                ('dResolution',c_double),
                ('dSubSampleShift',c_double),
                ('dLocationX',c_double),
                ('dLocationY',c_double),
                ('dLocationZ',c_double),
                ('dLocationUser',c_double),
                ('dHighFreqCorner',c_double),
                ('dwHighFreqOrder',c_uint32),
                ('szHighFilterType', c_char*16),
                ('dLowFreqCorner',c_double),
                ('dwLowFreqOrder',c_uint32),
                ('szLowFilterType', c_char*16),
                ('szProbeInfo', c_char*128),                
                ]

class ns_NEURALINFO(ctypes.Structure):
    _fields_ = [
                ('dwSourceEntityID',c_uint32),
                ('dwSourceUnitID',c_uint32),
                ('szProbeInfo',c_char*128),
                ]


