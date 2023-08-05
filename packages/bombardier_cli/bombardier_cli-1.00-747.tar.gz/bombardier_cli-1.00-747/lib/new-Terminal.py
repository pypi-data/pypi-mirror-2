#!/usr/bin/python
# BSD License
# Copyright (c) 2009, Peter Banka et al
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the GE Security nor the names of its contributors may
#   be used to endorse or promote products derived from this software without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

'''A [PinshCmd] command which allows a user to configure the terminal'''


import PinshCmd
from bombardier_core.static_data import OK
from bombardier_core.static_data import LOG_LEVEL_LOOKUP
from MultipleChoice import MultipleChoice
from SystemStateSingleton import SystemState
system_state = SystemState()

class Terminal(PinshCmd.PinshCmd):
    '''
       bomsh# set log-level debug
       [OK, ['Logging output set to debug']]
       bomsh# set log-level info
       [OK, ['Logging output set to info']]
    '''
    def __init__(self):
        "set up the command"
        PinshCmd.PinshCmd.__init__(self, "terminal", "configure the terminal")
        log_level = PinshCmd.PinshCmd("log-level")
        log_level.help_text = "set degree of logging to display to terminal"
        choices = ["debug", "info", "warning", "error", "critical"]
        choice_help = ["Maximum debugging", "Normal amounts of logs",
                       "Reduced logging", "Much reduced logging",
                       "Minimum logging"]
        choice_field = MultipleChoice(choices=choices, help_text=choice_help)
        log_level.children = [choice_field]
        self.children = [log_level]
        self.level = 0
        self.cmd_owner = 1

    def cmd(self, tokens, no_flag):
        """
        tokens -- all of the keywords passed in the command string, parsed
        no_flag -- whether the 'no' keyword was used in the command string
        """
        setting = tokens[1]
        if setting == "log-level":
            new_log_level = LOG_LEVEL_LOOKUP[tokens[2].upper()]
            system_state.log_level = new_log_level
            return [OK, ["Logging output set to %s" % tokens[2]]]
