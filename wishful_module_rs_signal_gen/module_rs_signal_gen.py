import logging
import random
import wishful_upis as upis
import wishful_agent as wishful_module

__author__ = "Piotr Gawlowicz, Anatolij Zubow"
__copyright__ = "Copyright (c) 2015, Technische Universität Berlin"
__version__ = "0.1.0"
__email__ = "{gawlowicz, zubow}@tkn.tu-berlin.de"


@wishful_module.build_module
class RsSignalGen(wishful_module.AgentUpiModule):
    def __init__(self, agentPort=None):
        super(RsSignalGen, self).__init__(agentPort)
        self.log = logging.getLogger('wifi_module.main')
        self.power = 1

    @wishful_module.bind_function(upis.radio.set_power)
    def set_power(self, power):
        self.log.debug("RsSignalGen sets power: {} on interface: {}".format(power, self.interface))
        self.power = power
        return {"SET_POWER_OK_value" : power}

    @wishful_module.bind_function(upis.radio.get_power)
    def get_power(self):
        self.log.debug("RsSignalGen gets power on interface: {}".format(self.interface))
        return self.power

