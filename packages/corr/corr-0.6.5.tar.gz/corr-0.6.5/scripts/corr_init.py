#! /usr/bin/env python
""" 
Script for initialising casper_n correlators. Requires X engine version 330 and F engine 310 or greater.

Author: Jason Manley
"""
"""
Revisions:
2011-02-11  JRM Added commandline option to skip clock check.
2010-12-13  JRM Stop data transmission before initialising anything.\n
2010-11-08  JRM Update to include f engines that output 10GbE\n
2010-08-08  JRM Changed order of execution to match dataflow.\n
2010-08-05  JRM Mods at GMRT for int time, feng clock, vacc sync checks etc.\n
2010-07-20  JRM Mods to use ROACH based F engines.\n 
2010-04-02  JCL Removed base_ant0 software register from Xengines, moved it to Fengines, and renamed it to use ibob_addr0 and ibob_data0.  Use function write_ibob() from corr_functions.py to set antenna offsets on Fengines
2010-01-06  JRM Added output control and self-check after primary init.
2009-12-02  JRM Re-enabled acc_len config.\n
2009-11-20: JRM Hardcoded 10GbE configuration call.\n
2009-11-10: JRM Added EQ config.\n
2009-07-02: JRM Switch to use corr_functions.\n
2009-06-15  JRM New 10GbE config scheme for ROACH.\n
2009-05-25  JRM Switched to KATCP.\n
2008-10-30  JRM Removed loopback flush since this has been fixed in hardware\n
2008-09-12  JRM Added support for different numbers of X and F engines\n
2008-02-20  JRM Now uses UDP borphserver\n
                New ibob address/data communication scheme\n
2008-02-14  JRM Fixed gbe_config for >1 BEE\n
2008-01-09  JRM DESIGNED FOR Cn rev 308b and upwards\n
                New loopback_mux flush\n
                Now grabs config settings from global corr.conf file \n
"""
import corr, time, sys, numpy, os, logging, katcp, socket, struct

def exit_fail():
    print 'FAILURE DETECTED. Log entries:\n',lh.printMessages()
    print "Unexpected error:", sys.exc_info()
    try:
        c.disconnect_all()
    except: pass
    if verbose:
        raise
    exit()

def exit_clean():
    try:
        c.disconnect_all()
    except: pass
    exit()

if __name__ == '__main__':
    from optparse import OptionParser

    p = OptionParser()
    p.set_usage('%prog [options] CONFIG_FILE')
    p.set_description(__doc__)
    p.add_option('-r', '--n_retries', dest='n_retries', type='int', default=40, 
        help='Number of times to try after an error before giving up. Default: 40')
    p.add_option('-p', '--skip_prog', dest='prog_fpga',action='store_false', default=True, 
        help='Skip FPGA programming (assumes already programmed).  Default: program the FPGAs')
    p.add_option('-e', '--skip_eq', dest='prog_eq',action='store_false', default=True, 
        help='Skip configuration of the equaliser in the F engines.  Default: set the EQ according to config file.')
    p.add_option('-c', '--skip_core_init', dest='prog_10gbe_cores',action='store_false', default=True, 
        help='Skip configuring the 10GbE cores (ie starting tgtap drivers).  Default: start all drivers')
    p.add_option('-o', '--skip_output_config', dest='config_output',action='store_false', default=True, 
        help='Do not begin outputting packetised data.  Default: start the output.')
    p.add_option('-k', '--clk_chk', dest='clk_chk',action='store_false', default=True, 
        help='Skip the F engine clock checks.')
    p.add_option('-v', '--verbose', dest='verbose',action='store_true', default=False, 
        help='Be verbose about errors.')
    p.add_option('-s', '--spead', dest='spead',action='store_false', default=True, 
        help='Do not send SPEAD metadata and data descriptor packets. Default: send all SPEAD info.')

    opts, args = p.parse_args(sys.argv[1:])

    if args==[]:
        print 'Please specify a configuration file! \nExiting.'
        exit()
    verbose=opts.verbose
    prog_fpga=opts.prog_fpga
    check_clocks = opts.clk_chk

lh=corr.log_handlers.DebugLogHandler(35)

try:
    print 'Connecting...',
    c=corr.corr_functions.Correlator(args[0],lh)
    if opts.verbose:
        for logger in c.floggers+c.xloggers: logger.setLevel(logging.DEBUG)
    else:
        for logger in c.floggers+c.xloggers: logger.setLevel(logging.INFO)
    print 'done'

    print '\n======================'
    print 'Initial configuration:'
    print '======================'

    if prog_fpga:
        print ''' Clearing the FPGAs...''',
        sys.stdout.flush()
        c.deprog_all()
        time.sleep(1)
        print 'done.'

        # PROGRAM THE DEVICES
        print ''' Programming the Fengines with %s and the Xengines with %s...'''%(c.config['bitstream_f'],c.config['bitstream_x']),
        sys.stdout.flush()
        c.prog_all()
        print 'done.'
    else: print ' Skipped programming FPGAs.'

    print ' Stopping transmission of data...',
    c.tx_stop()
    print 'done.'

    # Disable 10GbE cores until the network's been setup and ARP tables have settled. 
    # Need to do a reset here too to flush buffers in the core. But must be careful; resets are asynchronous and there must be no activity on the core (fifos) when they are reset.
    #DO NOT RESET THE 10GBE CORES SYNCHRONOUSLY... Packets will be routed strangely!
    print('\n Pausing 10GbE data exchange...'),
    sys.stdout.flush()
    if c.config['feng_out_type'] == '10gbe':
        print "Pausing Fengs...",
        c.feng_ctrl_set_all(gbe_enable=False, gbe_rst=False)
        c.feng_ctrl_set_all(gbe_enable=False, gbe_rst=True)
        c.syslogger.info("Holding F engine 10GbE cores in reset.")

    print "Pausing Xengs...",
    c.xeng_ctrl_set_all(gbe_enable=False, gbe_rst=False)
    c.xeng_ctrl_set_all(gbe_enable=False, gbe_rst=True)
    c.syslogger.info("Holding X engine 10GbE cores in reset.")
    print 'done.'


    print ''' Syncing the F engines...''',
    sys.stdout.flush()
    trig_time=c.arm()
    print 'Armed. Expect trigg at %s local (%s UTC).'%(time.strftime('%H:%M:%S',time.localtime(trig_time)),time.strftime('%H:%M:%S',time.gmtime(trig_time))),
    print 'SPEAD packet sent.'

    print(''' Checking F engine clocks...'''),
    sys.stdout.flush()
    if check_clocks:
        if c.check_feng_clks(): print 'ok'
        else: 
            print ('FAILURES detected!')
            raise RuntimeError("System doesn't work with broken clocks!")
    else: print 'skipped.'

    print(''' Setting the board indices...'''),
    sys.stdout.flush()
    c.feng_brd_id_set()
    if c.config['feng_out_type'] == '10gbe': c.xeng_brd_id_set()
    print ('''done''')

    if c.config['adc_type'] == 'katadc':
        print(''' Setting the RF gain stages on the KATADC...'''),
        sys.stdout.flush()
        c.rf_gain_set_all()
        print ('''done''')

    print(''' Setting the FFT shift schedule to 0x%X...'''%c.config['fft_shift']),
    sys.stdout.flush()
    c.fft_shift_set_all()
    print ('''done''')

    print ' Configuring EQ...',
    sys.stdout.flush()
    if opts.prog_eq:
        c.eq_set_all()
        print 'done'
    else: print 'skipped.'


    # Configure the 10 GbE cores and load tgtap drivers
    print(''' Configuring the 10GbE cores...'''),
    sys.stdout.flush()
    if opts.prog_10gbe_cores:
        c.config_roach_10gbe_ports()
        print 'done'

        print(''' Waiting for ARP to complete...'''),
        sys.stdout.flush()
        sleep_time=((c.config['10gbe_ip']&255 + c.config['n_xeng']*c.config['n_xaui_ports_per_xfpga'])*0.1)
        c.syslogger.info("Waiting %i seconds for ARP to complete."%sleep_time)
        time.sleep(sleep_time)
        print '''done'''

    else: print 'skipped'

    # Restart 10GbE data exchange (had to wait until the network's been setup and ARP tables have settled).
    # need to be careful about resets. these are asynchronous.
    print(' Starting 10GbE data exchange...'),
    sys.stdout.flush()
    if c.config['feng_out_type'] == '10gbe':
        c.feng_ctrl_set_all(gbe_enable=False, gbe_rst=False)
        c.feng_ctrl_set_all(gbe_enable=True, gbe_rst=False)
        print 'F engines re-enabled.',
    c.xeng_ctrl_set_all(gbe_enable=False,gbe_rst=False)
    c.xeng_ctrl_set_all(gbe_enable=True,gbe_rst=False)
    print 'X engines re-enabled.'
    
    if c.config['feng_out_type'] == 'xaui':
        print(' Flushing loopback muxs...'),
        sys.stdout.flush()
        c.xeng_ctrl_set_all(loopback_mux_rst=True,gbe_enable=False)
        time.sleep(2)
        c.xeng_ctrl_set_all(loopback_mux_rst=False,gbe_enable=True)
        print 'done.'

    print '\n=================================='
    print 'Verifying correct data exchange...'
    print '=================================='

    wait_time=len(c.xfpgas)/2
    print(''' Wait %i seconds for system to stabalise...'''%wait_time),
    sys.stdout.flush()
    time.sleep(wait_time)
    print '''done'''

    print(''' Resetting error counters...'''),
    sys.stdout.flush()
    c.rst_cnt()
    print '''done'''

    time.sleep(1)

    if c.config['feng_out_type'] == 'xaui':
        print(""" Checking that all XAUI links are working..."""),
        sys.stdout.flush()
        if c.check_xaui_error(): print 'ok'
        else: 
            print ('FAILURES detected!')
            exit_fail()

        print(""" Checking that the same timestamp F engine data is arriving at all X boards within a sync period..."""),
        if c.check_xaui_sync(): print 'ok'
        else: 
            print ('FAILURE! ')
            print "Check your 1PPS, clock source, XAUI links, clock on this computer (should be NTP sync'd for reliable arming) and KATCP network links."
            exit_fail()


    print(''' Checking that FPGAs are sending 10GbE packets...'''),
    sys.stdout.flush()
    if c.check_10gbe_tx(): print 'ok'
    else: 
        print ('FAILURES detected!')
        exit_fail()

    print(''' Checking that all X engine FPGAs are receiving 10GbE packets...'''),
    sys.stdout.flush()
    if c.check_10gbe_rx(): print 'ok'
    else: 
        print ('FAILURES detected!')
        exit_fail()

    if c.config['feng_out_type'] == 'xaui':
        print(''' Waiting for loopback muxes to sync...'''),
        sys.stdout.flush()
        loopback_ok=c.check_loopback_mcnt()
        loop_retry_cnt=0
        while (not loopback_ok) and (loop_retry_cnt< opts.n_retries):
            time.sleep(1)
            loop_retry_cnt+=1
            print '%i...'%loop_retry_cnt,
            sys.stdout.flush()
            loopback_ok=c.check_loopback_mcnt()
        if c.check_loopback_mcnt(): print 'ok'
        else: 
            print ('FAILURES detected!')
            exit_fail()


    print ''' Checking that all X engines are receiving all their packets...''',
    sys.stdout.flush()
    time.sleep(1)
    c.rst_cnt()
    if c.check_x_miss(): print 'ok'
    else: 
        print ('FAILURES detected!')
        c.check_x_miss(verbose=True)
        exit_fail()

    print (''' Setting the number of accumulations to %i (%5.3f seconds) and syncing VACCs...'''%(c.config['n_accs'],c.config['int_time'])),
    sys.stdout.flush()
    c.acc_time_set()
    c.rst_cnt()
    print 'done'

    print(''' Checking vector accumulators...'''),
    sys.stdout.flush()
    print "Waiting for an integration to finish...",
    sys.stdout.flush()
    time.sleep(c.config['int_time']+0.1)
    print('''done. Checking...'''),
    sys.stdout.flush()
    if c.check_vacc(): print 'ok'
    else: 
        print ('FAILURES detected!')
        exit_fail()
    
    print ' Sending SPEAD metatdata and data descriptors to %s:%i...'%(c.config['rx_meta_ip_str'],c.config['rx_udp_port']),
    sys.stdout.flush()
    if opts.spead:
        c.spead_static_meta_issue()
        c.spead_eq_meta_issue()
        c.spead_time_meta_issue()
        c.spead_data_descriptor_issue()
        print 'done'
    else: print 'skipped.'

    print ' Configuring output to %s:%i...'%(c.config['rx_udp_ip_str'],c.config['rx_udp_port']),
    sys.stdout.flush()
    if opts.config_output and (c.config['out_type'] == '10gbe'): 
        c.config_udp_output()
        print 'done'
    else: print 'skipped.'

    print ' Starting transmission of data...',
    sys.stdout.flush()
    if opts.config_output: 
        c.tx_start()
        print 'done'
    else: print 'skipped.'

    print(''' Resetting error counters...'''),
    sys.stdout.flush()
    c.rst_cnt()
    print '''done'''

    print(''' Enabling KITT...'''),
    sys.stdout.flush()
    c.kitt_enable()
    print '''done'''

except KeyboardInterrupt:
    exit_clean()
except:
    exit_fail()
