import logging
import random
import wishful_upis as upis
import wishful_framework as wishful_module
from wishful_framework.classes import exceptions
import inspect
import subprocess
import platform
import os

__author__ = "Piotr Gawlowicz, Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, zubow}@tkn.tu-berlin.de"

"""
Implementation of UPI_R and UPI_N interfaces for the R&S signal generator.
"""

@wishful_module.build_module
class RsSignalGenModule(wishful_module.AgentModule):
    def __init__(self):
        super(RsSignalGenModule, self).__init__()
        self.log = logging.getLogger('RsSignalGenModule')

    @wishful_module.bind_function(upis.radio.play_waveform)
    def play_waveform(self, iface, freq, power_lvl, **kwargs):
        self.log.debug('playWaveform()')

        try:
            # set the center frequency
            exec_file = 'rs_siggen_etherraw'
            args = iface + ' \"FREQ ' + freq + 'MHz\"'

            command = exec_file + ' ' + args
            self.log.debug('playWaveform on iface %s ... set frequency' % (iface))
            self.log.info('exec %s' % command)

            [rcode, sout, serr] = self.run_command(command)

            # set power level
            args = iface + ' \":POW ' + str(power_lvl) + '\"'

            command = exec_file + ' ' + args
            self.log.debug('playWaveform on iface %s ... set power level to %s' % (iface, str(power_lvl)))
            self.log.info('exec %s' % command)

            [rcode, sout, serr] = self.run_command(command)

            # power on
            args = iface + ' \"OUTP ON\"'

            command = exec_file + ' ' + args
            self.log.debug('playWaveform on iface %s ... power on' % (iface))
            self.log.info('exec %s' % command)

            [rcode, sout, serr] = self.run_command(command)

            return True
        except Exception as e:
            self.log.fatal("Failed to play waveform, err_msg:%s" % (str(e)))
            raise exceptions.FunctionExecutionFailedException(
                func_name=inspect.currentframe().f_code.co_name,
                err_msg='Failed to play waveform: ' + str(e))


    @wishful_module.bind_function(upis.radio.stop_waveform)
    def stop_waveform(self, iface, **kwargs):
        self.log.debug('stopWaveform()')

        try:
            exec_file = str(os.path.join(self.getPlatformPath())) + '/rs_siggen_etherraw'
            # power off
            args = iface + '\"OUTP OFF\"'

            command = exec_file + ' ' + args
            self.log.debug('stopWaveform on iface %s ... power off' % (iface))
            self.log.debug('exec %s' % command)

            [rcode, sout, serr] = self.run_command(command)

            return True
        except Exception as e:
            self.log.fatal("Failed to stop waveform, err_msg:%s" % (str(e)))
            raise exceptions.FunctionExecutionFailedException(
                func_name=inspect.currentframe().f_code.co_name,
                err_msg='Failed to stop waveform: ' + str(e))

    def run_command(self, command):
        """
            Method to start the shell commands and get the output as iterater object
        """

        sp = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        out, err = sp.communicate()

        if False:
            if out:
                self.log.debug("standard output of subprocess:")
                self.log.debug(out)
            if err:
                self.log.debug("standard error of subprocess:")
                self.log.debug(err)

        if err:
            raise Exception("An error occurred in RsSignalGenModule: %s" % err)

        return [sp.returncode, out.decode("utf-8"), err.decode("utf-8")]

