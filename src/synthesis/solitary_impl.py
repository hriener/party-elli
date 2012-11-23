from synthesis.blank_impl import BlankImpl
from synthesis.func_description import FuncDescription

class SolitaryImpl(BlankImpl):
    def __init__(self, automaton, inputs, outputs, nof_local_states, sys_state_type):
        super().__init__()

        self._state_type = sys_state_type
        self._tau_name = 'tau'

        self.automaton = automaton
        self.nof_processes = 1

        self.init_states = [(0,)]
        self.proc_states_descs = self._get_proc_descs(nof_local_states)

        self.orig_inputs = [inputs]
        self.aux_func_descs = []

        self.all_outputs =  [outputs]
        self.all_outputs_descs = self._get_all_outputs_descs(outputs)

        self.taus_descs = self._get_taus_descs(inputs)
        self.model_taus_descs = self.taus_descs


    def _get_all_outputs_descs(self, outputs):
        descs = []
        for o in outputs:
            argname_to_type = {'state': self._state_type}

            description = FuncDescription(str(o), argname_to_type, set(), 'Bool', None)

            descs.append(description)

        return [descs]

    def _get_taus_descs(self, inputs):
        tau_desc = FuncDescription('tau',
            dict([('state', self._state_type)] + list(map(lambda i: (str(i), 'Bool'), inputs))),
            set(),
            self._state_type,
            None)

        return [tau_desc]

    def _get_proc_descs(self, nof_local_states):
        return list(map(lambda proc_i: (self._state_type, list(map(lambda s: 't'+str(s), range(nof_local_states)))),
            range(self.nof_processes)))
