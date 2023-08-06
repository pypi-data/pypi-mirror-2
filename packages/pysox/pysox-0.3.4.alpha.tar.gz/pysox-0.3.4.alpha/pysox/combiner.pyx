#
# Python objects wrapping the c implementation
#
# $Id: sox.pyx 9 2011-03-19 22:13:46Z patrick $
#
# Copyright 2011 Patrick Atamaniuk
#
# This source code is freely redistributable and may be used for
# any purpose.  This copyright notice must be maintained.
# Patrick Atamaniuk and Contributors are not responsible for
# the consequences of using this software.
#
import sys
from cython.operator cimport dereference as deref
from cpython cimport PY_MAJOR_VERSION
cimport pysox.csox as csox
from sox cimport CEffect, CSoxStream, toCharP, SoxSampleBuffer

ctypedef struct pysoxtransportheader_t:
    char magic[4]
    csox.sox_signalinfo_t signalinfo

DEF SOX_SUCCESS = 0
DEF SOX_EOF = -1

cdef class MixerBase(CEffect):
    """Virtual object to replace the internal input effect of sox
    """
    cdef object inputnames
    cdef object inputs
    cdef csox.sox_effect_handler_t *handler
    cdef int currentInput
    
    def __dealloc__(self):
        #print 'concatenate dealloc'
        if self.handler:
            csox.free(self.handler)
            
    cdef create(self, name, arguments):
        self.name = name
        self.inputnames = arguments
        self.effect = csox.sox_create_effect(self._setup_handler());
        self.effect.priv = <void *>self

        self.inputs = [] #these need to contain sox_format_t thingies
        for name in self.inputnames:
            #print name
            inf = CSoxStream(name, 'r')
            #print repr(inf)
            self.inputs.append(inf)

        self.currentInput = 0 

        cdef csox.sox_signalinfo_t * insignal = (<CSoxStream>self.inputs[self.currentInput]).cget_signal()
        cdef csox.sox_encodinginfo_t * inencoding = (<CSoxStream>self.inputs[self.currentInput]).cget_encoding()
      
        self.effect.in_signal = deref(insignal) 
        self.effect.out_signal = deref(insignal) 
        self.effect.in_encoding = inencoding
        self.effect.out_encoding = inencoding
        
    cdef csox.sox_effect_handler_t * _setup_handler(self):
        self.handler = <csox.sox_effect_handler_t *>csox.malloc(sizeof(csox.sox_effect_handler_t))
        #print 'creating handler'
        self.handler.name = toCharP(self.name)
        self.handler.flags = csox.SOX_EFF_MCHAN + csox.SOX_EFF_LENGTH
        self.handler.drain = __combiner_mixerbase_cb_drain
        self.handler.start = __combiner_mixerbase_cb_start
        self.handler.stop = __combiner_mixerbase_cb_stop
        self.handler.kill = __combiner_mixerbase_cb_kill
        self.handler.priv_size = 0
        return self.handler;

    cdef int start(self):
        """start is called within chain.sox_add_effect, and at that point,
        our effect in_signal and out_signal are set,
        our effect in_encoding is chain->in_enc, out_encoding is chain->out_enc,
        
        Returns:
            SOX_SUCCESS to indicate readiness
            otherwise, to indicate a failure in setup
        """
        return SOX_SUCCESS
    
    cdef int stop(self):
        return 0 #return number of clippings

    cdef int kill(self):
        return 0 #return value ignored

    cdef int drain(self, csox.sox_sample_t * obuf, size_t * osamp):
        """same as flow but without input"""
        return SOX_EOF

    cdef int flow(self, csox.sox_sample_t *ibuf, csox.sox_sample_t *obuf, size_t *isamp, size_t *osamp):
        """Run effect on all channels at once, or
        flow multiple times, once per channel
        Returns:
            SOX_SUCCESS: can continue
            SOX_EOF: request stop for end of data
        """
        return SOX_EOF

cdef int __combiner_mixerbase_cb_start(csox.sox_effect_t * effp):
    obj = <MixerBase>effp.priv # class ConcatenateFiles
    return obj.start()

cdef int __combiner_mixerbase_cb_stop(csox.sox_effect_t * effp):
    obj = <MixerBase>effp.priv # class ConcatenateFiles
    return obj.stop()

cdef int __combiner_mixerbase_cb_kill(csox.sox_effect_t * effp):
    obj = <MixerBase>effp.priv # class ConcatenateFiles
    obj.kill()
    effp.priv=NULL #need to void the pointer to the python object since sox_delete_effect would otherwise free it
    return 0

cdef int __combiner_mixerbase_cb_drain(csox.sox_effect_t * effp, csox.sox_sample_t * obuf, size_t * osamp):
    obj = <MixerBase>effp.priv # class ConcatenateFiles
    return obj.drain(obuf, osamp)

cdef int __combiner_mixerbase_cb_flow(csox.sox_effect_t * effp, csox.sox_sample_t *ibuf, csox.sox_sample_t *obuf, size_t *isamp, size_t *osamp):
    obj = <MixerBase>effp.priv # class ConcatenateFiles
    return obj.flow(ibuf, obuf, isamp, osamp)

cdef class ConcatenateFiles(MixerBase):
    """ConcatenateFiles("input", ["test1.wav", "test2.wav"])
    
    Input effect provider for CEffectChain in order to concatenate multiple input files.
    This effect replaces the sox internal input effect.

    All audio data must be the same format (bitrate, channels, precision)
    The output's length is the total length of all combined signals.
    """
    cdef create(self, name, arguments):
        print("ConcatenateFiles::create")
        MixerBase.create(self, name, arguments)
        self.effect.out_signal.length = self.effect.in_signal.length*2

    cdef int drain(self, csox.sox_sample_t * obuf, size_t * osamp):
        cdef csox.sox_format_t * ft
        cdef size_t nread
        if self.currentInput >= len(self.inputs):
            return SOX_EOF #last one reached
        ft = (<CSoxStream>self.inputs[self.currentInput]).get_ft()
        nread = 1024
        nread = csox.sox_read(ft, obuf, nread);
        #sys.stdout.write('.')
        osamp[0] = nread
        if nread > 0:
            return SOX_SUCCESS

        #advance
        (<CSoxStream>self.inputs[self.currentInput]).close()
        self.currentInput +=1
        if self.currentInput >= len(self.inputs):
            return SOX_EOF #last one reached
        #print 'advanced to',self.currentInput
        return self.drain(obuf, osamp)

#
#
#
DEF MIXFILES_BUFSIZE = 1024

cdef class MixFiles(MixerBase):
    """MixFiles("input", ["test1.wav", "test2.wav"])
    
    Input effect provider for CEffectChain in order to mix multiple input files.
    This effect replaces the sox internal input effect.
    
    Volumes are mixed down by 1/n where n is the number of inputs.
    
    Clipping probably will not occur with this method, but the signal appears to be
    less loud than the originals.
    
    The input files signals must be equal, meaning bitrate and channels must be equal.
    The signal's length can be different, the output will get the length of the longest signal.
    """
    cdef csox.sox_sample_t * mixbuffer
    cdef csox.sox_sample_t * readbuffer
    cdef float volume
    
    cdef float __calc_volume(self):
        self.volume = 1.0/len(self.inputs)
        
    cdef create(self, name, arguments):
        cdef size_t bufsize
        bufsize = MIXFILES_BUFSIZE * sizeof(csox.sox_sample_t)
#        print("Mix::create")
        MixerBase.create(self, name, arguments)
        self.mixbuffer = <csox.sox_sample_t *>csox.malloc(bufsize)
        self.readbuffer = <csox.sox_sample_t *>csox.malloc(bufsize)
        csox.bzero(self.mixbuffer, bufsize)
        csox.bzero(self.readbuffer, bufsize)
        #self.effect.out_signal.length = self.effect.in_signal.length #no change
        self.__calc_volume()
        
    cdef int start(self):
        return SOX_SUCCESS

    cdef int kill(self):
        if not self.mixbuffer is NULL:
            csox.free(self.mixbuffer)
            self.mixbuffer = NULL
        if not self.readbuffer is NULL:
            csox.free(self.readbuffer)
            self.readbuffer = NULL
        return 0 #return value ignored

    #mixer function, this will create quite optimal c code.
    cdef size_t do_mix(self, csox.sox_sample_t *inb, csox.sox_sample_t *outb, size_t len, float factor):
        cdef csox.sox_sample_t i=0
        while i < len:
            outb[i] = outb[i] + <csox.sox_sample_t>(inb[i]*factor)
            i +=1
        return len

    cdef int drain(self, csox.sox_sample_t * obuf, size_t * osamp):
        cdef size_t bufsize
        bufsize = MIXFILES_BUFSIZE * sizeof(csox.sox_sample_t)
        cdef csox.sox_format_t * ft
        cdef size_t nread
        cdef size_t max_nread
        cdef int ninputs

        ninputs = len(self.inputs)   
        self.currentInput = 0
        max_nread = 0
        csox.bzero(self.mixbuffer, bufsize)
        while self.currentInput < ninputs:
            ft = (<CSoxStream>self.inputs[self.currentInput]).get_ft()
            nread = MIXFILES_BUFSIZE
            csox.bzero(self.readbuffer, bufsize)
            nread = csox.sox_read(ft, self.readbuffer, nread);
            if nread:
                self.do_mix(self.readbuffer, self.mixbuffer, nread, self.volume)
                max_nread = max(nread, max_nread)
            self.currentInput +=1
            
        osamp[0] = max_nread
        if max_nread > 0: # can read again in next iteration
            csox.bcopy(self.mixbuffer, obuf, max_nread * sizeof(csox.sox_sample_t));
            return SOX_SUCCESS

        return SOX_EOF #last one reached

import math
cdef class PowerMixFiles(MixFiles):
    """PowerMixFiles("input", ["test1.wav", "test2.wav"])
    
    Input effect provider for CEffectChain in order to mix multiple input files.
    This effect replaces the sox internal input effect.
    
    Volumes are mixed down by 1/sqrt(n) where n is the number of inputs.
    
    Clipping might occur here, but in most cases distortions are not susceptible.
    """
    cdef float __calc_volume(self):
        self.volume = 1.0/math.sqrt(len(self.inputs))

cdef class SocketOutput(MixerBase):
    """SocketOutput("output",[connection])
    
    Output the chain data to a multiprocess socket. Used as output effect at the end of a chain.
    
    Args:
        connection: multiprocessing Pipe of a process child
    """
    cdef object conn
    cdef create(self, name, arguments):
        self.name = name
        # not calling MixerBase.create(self, name, arguments)
        self.effect = csox.sox_create_effect(self._setup_handler());
        self.effect.priv = <void *>self
        self.conn = arguments[0]

    cdef csox.sox_effect_handler_t * _setup_handler(self):
        self.handler = <csox.sox_effect_handler_t *>csox.malloc(sizeof(csox.sox_effect_handler_t))
        #print 'creating handler'
        self.handler.name = toCharP(self.name)
        self.handler.flags = csox.SOX_EFF_MCHAN + csox.SOX_EFF_LENGTH
        self.handler.flow = __combiner_mixerbase_cb_flow
        self.handler.drain = NULL
        self.handler.start = __combiner_mixerbase_cb_start
        self.handler.stop = __combiner_mixerbase_cb_stop
        self.handler.kill = __combiner_mixerbase_cb_kill
        self.handler.priv_size = 0
        return self.handler;

    cdef int flow(self, csox.sox_sample_t *ibuf, csox.sox_sample_t *obuf, size_t *isamp, size_t *osamp):
#        print("SocketOutput flow ", deref(isamp))
        cdef char *s
        cdef bytes b
        cdef size_t length
        osamp[0] = 0
        try:
            if self.conn:
                if not deref(isamp): #nothing to send
                    return SOX_SUCCESS
                if PY_MAJOR_VERSION >= 3:
                    inbuf = SoxSampleBuffer()
                    inbuf.set_buffer(ibuf, deref(isamp))
                    self.conn.send_bytes(inbuf)
                else:
                    length = deref(isamp)*4 #FIXME use self.effect.in_signal.precision
                    s = <char *>ibuf
                    b=s[:length] #will make a copy to a python bytes() object
                    self.conn.send_bytes(b, 0, length)
                return SOX_SUCCESS
        except Exception as e:
#            print("Exception",e)
            import traceback
            traceback.print_exc()
            return SOX_EOF
        return SOX_SUCCESS #0 samples put in obuf, we are end of chain

    cdef int send_header(self):
        cdef csox.sox_signalinfo_t * isig
        cdef pysoxtransportheader_t header
        cdef char * chead
        cdef bytes bhead
        if not self.conn:
            return 0
        cdef length = sizeof(pysoxtransportheader_t)
        csox.bcopy(b'.PYS', header.magic, 4)
        csox.bcopy(&self.effect.in_signal, &header.signalinfo, sizeof(self.effect.out_signal))
        
        chead = <char *>&header
        bhead = chead[:length]
        self.conn.send_bytes(bytes(bhead), 0, length)
        return 0
    
    cdef int start(self):
        """send signal info header"""
#        print 'sending',self.get_out_signal()
        self.send_header()
        return 0
    
    cdef int stop(self):
        if self.conn:
            self.conn.send_bytes(b'')
            self.conn.close()
            self.conn = None
        return 0
    
cdef class MixSockets(MixFiles):
    """Mix multiple signals from multiprocess socket"""
    cdef object conns
    cdef object initialdata

    cdef float __calc_volume(self):
        self.volume = 1.0/len(self.conns)

    cdef create(self, name, arguments):
        cdef size_t bufsize
        bufsize = MIXFILES_BUFSIZE * sizeof(csox.sox_sample_t)

        self.name = name
        # not calling MixerBase.create(self, name, arguments)
        self.effect = csox.sox_create_effect(self._setup_handler());
        self.effect.priv = <void *>self
        self.conns = arguments
#        print("Mix::create")
#        MixerBase.create(self, name, arguments)
        self.mixbuffer = <csox.sox_sample_t *>csox.malloc(bufsize)
        self.readbuffer = <csox.sox_sample_t *>csox.malloc(bufsize)
        csox.bzero(self.mixbuffer, bufsize)
        csox.bzero(self.readbuffer, bufsize)
        self.__calc_volume()
    
    cdef int receive_header(self):
        cdef int nconns = len(self.conns)
        cdef pysoxtransportheader_t header
        cdef length = sizeof(pysoxtransportheader_t)
        cdef bytes data
        cdef int i=0
        self.initialdata = [b'' for x in range(nconns)]
        for conn in self.conns:
            self.initialdata[i] = b''
            
            data = conn.recv_bytes()
            csox.bcopy(<char *>data, <char *>&header, length)
#            print("got header from %d"%i)
#            print(header.magic)
            #FIXME to checking if the formats match
            csox.bcopy((<char *>&header)+4, &self.effect.in_signal, length-4) 
            csox.bcopy((<char *>&header)+4, &self.effect.out_signal, length-4) 
            
            if len(data) > length:
                self.initialdata[i] = data[length:]
                print("Got successive data while reading header",len(self.initialdata[i]))
            i +=1
        return SOX_SUCCESS
    
    cdef int start(self):
        """send signal info header"""
        self.receive_header()
#        print "got signalinfo",self.get_in_signal()
#        print "got signalinfo",self.get_out_signal()
        return SOX_SUCCESS

    cdef int drain(self, csox.sox_sample_t * obuf, size_t * osamp):
#        if self.initialdata:
#            for id in self.initialdata:
#                if len(id):
#                    pass
#                    #FIXME do it
#            osamp[0]=0
#            return SOX_SUCCESS
        
        #else receive
        cdef int i = 0
        cdef bytes data
        cdef char * cdata
        cdef size_t length=0
        cdef float factor = 0.5
        max_nread = 0
        cdef size_t bufsize
        bufsize = MIXFILES_BUFSIZE * sizeof(csox.sox_sample_t)
        csox.bzero(self.mixbuffer, bufsize)
        for conn in self.conns:
            try:
                data = conn.recv_bytes()
            except EOFError:
                print('IEffr EOF')
                i += 1
                continue
            length = len(data)
            #print("td",type(data), length, data)
            if not data or not length:
                print("IEffr data is None, channel %s is finished"%self.currentInput)
            else:
                # MIX the stuff
                nread = MIXFILES_BUFSIZE
                csox.bzero(self.readbuffer, bufsize)
                nread = len(data) / sizeof(csox.sox_sample_t)
                if nread:
                    cdata = data
                    self.do_mix(<csox.sox_sample_t *>cdata, self.mixbuffer, nread, self.volume)
                    max_nread = max(nread, max_nread)

            i += 1
        osamp[0] = max_nread
        if max_nread > 0: # can read again in next iteration
            csox.bcopy(self.mixbuffer, obuf, max_nread * sizeof(csox.sox_sample_t));
            return SOX_SUCCESS

        return SOX_EOF #last one reached


