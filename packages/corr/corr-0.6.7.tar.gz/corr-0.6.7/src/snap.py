import numpy,time,struct,construct
from construct import *

def snapshots_get(fpgas,dev_names,man_trig=False,man_valid=False,wait_period=-1,offset=-1,circular_capture=False):
    """Fetches data from multiple snapshot devices. fpgas and dev_names are lists of katcp_wrapper.FpgaClient,and 'snapshot_device_name', respectively.
        This function triggers and retrieves data from the snap block devices. The actual captured length and starting offset is returned with the dictionary of data for each FPGA (useful if you've done a circular capture and can't calculate this yourself).\n
        \tdev_names: list of strings, names of the snap block corresponding to FPGA list. Can optionally be 1-D, in which case name is used for all FPGAs.\n
        \tman_trig: boolean, Trigger the snap block manually.\n
        \toffset: integer, wait this number of valids before beginning capture. Set to zero if your hardware doesn't support this or the circular capture function. Set to negative if you've got a modern snap block with end-of-capture detect but actually want to start at     offset zero.\n
        \tcircular_capture: boolean, Enable the circular capture function.\n
        \twait_period: integer, wait this number of seconds between triggering and trying to read-back the data. Make it negative to wait forever.\n
        \tRETURNS: dictionary with keywords: \n
        \t\tlengths: list of integers matching number of valids captured off each fpga.\n
        \t\toffset: optional (depending on snap block version) list of number of valids elapsed since last trigger on each fpga.
        \t\t{brams}: list of data from each fpga for corresponding bram.\n
        """
    # 2011-06-24 JRM first write. 
    if isinstance(dev_names,str):
        dev_names=[dev_names for f in fpgas]

    if offset >=0:
        for fn,fpga in enumerate(fpgas):
            fpga.write_int(dev_names[fn]+'_trig_offset',offset)

    for fn,fpga in enumerate(fpgas):
        fpga.write_int(dev_names[fn]+'_ctrl',(0 + (man_trig<<1) + (man_valid<<2) + (circular_capture<<3)))
        fpga.write_int(dev_names[fn]+'_ctrl',(1 + (man_trig<<1) + (man_valid<<2) + (circular_capture<<3)))

    done=False
    start_time=time.time()
    while not done and ((time.time()-start_time)<wait_period or (wait_period < 0)): 
        addr      = [fpga.read_uint(dev_names[fn]+'_status') for fn,fpga in enumerate(fpgas)]
        done_list = [not bool(i & 0x80000000) for i in addr]
        if (done_list == [True for i in fpgas]): done=True

    bram_dmp=dict()
    bram_dmp['data']=[]
    bram_dmp['lengths']=[i&0x7fffffff for i in addr]
    bram_dmp['offsets']=[0 for fn in fpgas]
    for fn,fpga in enumerate(fpgas):
        now_status=bool(fpga.read_uint(dev_names[fn]+'_status')&0x80000000)
        now_addr=fpga.read_uint(dev_names[fn]+'_status')&0x7fffffff
        if (bram_dmp['lengths'][fn] != now_addr) or (bram_dmp['lengths'][fn]==0) or (now_status==True):
            #if address is still changing, then the snap block didn't finish capturing. we return empty.  
            raise RuntimeError("A snap block logic error occurred on capture #%i. It reported capture complete but the address is either still changing, or it returned 0 bytes captured after the allotted %2.2f seconds. Addr at stop time: %i. Now: Still running :%s, addr: %i."%(fn,wait_period,bram_dmp['lengths'][fn],{True:'yes',False:'no'}[now_status],now_addr))
            bram_dmp['lengths'][fn]=0
            bram_dmp['offsets'][fn]=0

        if circular_capture:
            bram_dmp['offsets'][fn]=fpga.read_uint(dev_names[fn]+'_tr_en_cnt') - bram_dmp['lengths'][fn]
        else: 
            bram_dmp['offsets'][fn]=0

        if bram_dmp['lengths'][fn] == 0:
            bram_dmp['data'].append([])
        else:
            bram_dmp['data'].append(fpga.read(dev_names[fn]+'_bram',bram_dmp['lengths'][fn]))

    bram_dmp['offsets']=numpy.add(bram_dmp['offsets'],offset)
    
    for fn,fpga in enumerate(fpgas):
        if (bram_dmp['offsets'][fn]<0): 
            bram_dmp['offsets'][fn]=0

    return bram_dmp

#def unpack_snapshot(data, bitmap, word_width=32):
#    """Unpacks data from a snap block. data is the raw binary (string). bitmap is a dictionary of form {yourvariablename: (bitfield_length,bitfield_start_pos,dtype)}. dtype should be a numpy type (eg numpy.int8, numpy.int16, numpy.uint32 etc). Bitfields with length of 1 are automatically unpacked as binary values (True/False). Word width should reflect your snap hardware block's databus width."""
#    if word_width==8:
#        req_dtype=numpy.uint8
#    elif word_width==16:
#        req_dtype=numpy.uint16
#    elif word_width==32:
#        req_dtype=numpy.uint32
#    elif word_width==64:
#        req_dtype=numpy.uint64
#    elif word_width==128:
#        req_dtype=numpy.uint128
#
#    unpacked_data = numpy.fromstring(data,dtype=numpy.int8)        
#    for key,value in bitmap.iteritems():
#   INCOMPLETE. use construct instead.


def get_adc_snapshots(correlator,ant_strs=[],trig_level=-1,sync_to_pps=True):
    """Fetches multiple ADC snapshots from hardware. Set trig_level to negative value to disable triggered captures."""

    if correlator.config['adc_n_bits'] !=8: 
        raise RuntimeError('This function is hardcoded to work with 8 bit ADCs. According to your config file, yours is %i bits.'%correlator.config['adc_n_bits'])

    fpgas=[]
    dev_names=[]
    for ant_str in ant_strs:    
        (ffpga_n,xfpga_n,fxaui_n,xxaui_n,feng_input) = correlator.get_ant_str_location(ant_str)
        fpgas.append(correlator.ffpgas[ffpga_n])
        dev_names.append('adc_snap%i'%feng_input)

    if trig_level>=0:
        [fpga.write_int('trig_level',trig_level) for fpga in fpgas]
        raw=snapshots_get(fpgas,dev_names,wait_period=-1,circular_capture=True,man_trig=(not sync_to_pps))
        ready=((int(time.time()*10)%10)==5)
        while not ready:
            time.sleep(0.05)
            ready=((int(time.time()*10)%10)==5)
    else:
        raw=snapshots_get(fpgas,dev_names,wait_period=2,circular_capture=False,man_trig=(not sync_to_pps))

    rv={}
    for ant_n,ant_str in enumerate(ant_strs):    
        rv[ant_str]={'data':numpy.fromstring(raw['data'][ant_n],dtype=numpy.int8),'offset':raw['offsets'][ant_n],'length':raw['lengths'][ant_n]}
    
    if (sync_to_pps==True) or (trig_level>=0):
        for ant_n,ant_str in enumerate(ant_strs):    
            rv[ant_str]['timestamp']=fpgas[ant_n].read_uint(dev_names[ant_n]+'_val')

    return rv
       
    #return numpy.fromstring(self.ffpgas[ffpga_n].snapshot_get('adc_snap%i'%feng_input,man_trig=False,circular_capture=True,wait_period=-1)['data'],dtype=numpy.int8)        

def get_quant_snapshot(correlator,ant_str,n_spectra=1):
    """Fetches a quantiser snapshot from hardware for a given antenna."""
    if correlator.config['feng_bits'] !=4:
        raise RuntimeError('Sorry, this function is currently hard-coded to unpack 4 bit values')
    (ffpga_n,xfpga_n,fxaui_n,xxaui_n,feng_input) = correlator.get_ant_str_location(ant_str)
    ns=0
    unpacked_vals = []
    while ns < n_spectra:
        bram_dmp = correlator.ffpgas[ffpga_n].snapshot_get('quant_snap%i'%feng_input, man_trig = False, wait_period = 2)
        pckd_8bit = numpy.fromstring(bram_dmp['data'],dtype=numpy.uint8)
        for val in pckd_8bit:
            #get the right 4 bit values:
            pol_r_bits = (val & ((2**8) - (2**4))) >> 4
            pol_i_bits = (val & ((2**4) - (2**0)))
            #cast up to signed numbers:
            unpacked_vals.append(float(((numpy.int8(pol_r_bits << 4)>> 4))) + 1j * float(((numpy.int8(pol_i_bits << 4)>> 4))))
        ns = len(unpacked_vals)/correlator.config['n_chans']
    rv=numpy.array(unpacked_vals)
    if len(rv)%correlator.config['n_chans'] != 0:
        raise RuntimeError('Retrieved data is not a multiple of n_chans. Something is wrong.')
    rv.shape=(len(unpacked_vals)/correlator.config['n_chans'],correlator.config['n_chans'])
    if n_spectra==0:
        return rv[0]
    else:
        return rv[0:n_spectra,:]

def Swapped(subcon):
    """swaps the bytes of the stream, prior to parsing"""
    return Buffered(subcon,
        encoder = lambda buf: buf[::-1],
        decoder = lambda buf: buf[::-1],
        resizer = lambda length: length
    )

def get_rx_snapshot(correlator,xeng_ids):
    "Grabs a snapshot of the decoded incomming packet stream. xeng_ids is a list of integers (xeng core numbers)."
    for xeng_n in xeng_ids:    
        (xfpga_n,xeng_core) = correlator.get_xeng_location(xeng_n)
        fpgas.append(correlator.xfpgas[xfpga_n])
        dev_names.append('snap_rx%i'%xeng_core)
    raw=snapshots_get(fpgas,dev_names,wait_period=2,circular_capture=False,man_trig=False)
    
    rx_bf=construct.BitStruct("oob",
        BitField("ant",15),
        BitField("mcnt",28),
        Flag("loop_ack"),
        Flag("gbe_ack"),
        Flag("valid"),
        Flag("eof"),
        Flag("flag"),
        BitField("ip_addr",16),
        BitField("data", 64),
        )

    unp_rpt = construct.GreedyRepeater(rx_bf)
    unpacked=unp_rpt.parse(raw['data'][0])

def get_gbe_rx_snapshot(correlator,xeng_ids):
    for xeng_n in xeng_ids:    
        (xfpga_n,xeng_core) = correlator.get_xeng_location(xeng_n)
        fpgas.append(correlator.xfpgas[xfpga_n])
        dev_names.append('snap_gbe_rx%i'%xeng_core)
    raw=snapshots_get(fpgas,dev_names,wait_period=2,circular_capture=False,man_trig=False)

    rx_bf=construct.BitStruct("oob",
        Flag("led_up"),
        Flag("led_rx"),
        Flag("eof"),
        Flag("bad_frame"),
        Flag("overflow"),
        Flag("valid"),
        Flag("ack"),
        BitField("ip_addr",32),
        BitField("data", 64),
        )

    unp_rpt = construct.GreedyRepeater(rx_bf)
    unpacked=unp_rpt.parse(raw['data'][0])


def get_gbe_tx_snapshot(correlator,xeng_ids):
    for xeng_n in xeng_ids:    
        (xfpga_n,xeng_core) = correlator.get_xeng_location(xeng_n)
        fpgas.append(correlator.xfpgas[xfpga_n])
        dev_names.append('snap_gbe_tx%i'%xeng_core)
    raw=snapshots_get(fpgas,dev_names,wait_period=2,circular_capture=False,man_trig=False)

    rx_bf=construct.BitStruct("oob",
        Flag("eof"),
        Flag("link_up"),
        Flag("led_tx"),
        Flag("tx_full"),
        Flag("tx_over"),
        Flag("valid"),
        BitField("ip_addr",32),
        BitField("data", 64),
        )

    unp_rpt = construct.GreedyRepeater(rx_bf)

    for xeng_n,data in enumerate(raw['data']):
        unpacked=unp_rpt.parse(raw['data'][0])


