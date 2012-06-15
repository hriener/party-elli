import logging
from interfaces.automata import to_dot
from interfaces.smt_model import SmtModel
from synthesis.states_extender import extend_self_looped_rejecting_states
from synthesis.smt_encoder import Encoder
from synthesis.z3 import Z3

_logger = None

def _get_logger():
    global _logger
    if _logger is None:
        _logger = logging.getLogger(__name__)
    return _logger


def search(automaton, inputs, outputs, size, bound, z3solver, logic):
    assert bound > 0

    logger = _get_logger()

    logger.info("searching the model of size {0}".format(('<=' + str(bound)) if size is None else size))

    model_sizes = range(1, bound + 1) if size is None else range(size, size + 1)
    for current_bound in model_sizes:
        logger.info('trying model size = %i', current_bound)

        automaton_wo_rejecting_states = extend_self_looped_rejecting_states(automaton, current_bound)
        assert len(automaton_wo_rejecting_states.rejecting_nodes) == 0

#        _logger.debug('original automaton nodes: ' + to_dot(automaton))
#        _logger.debug('preprocessed automaton nodes: ' + to_dot(automaton_wo_rejecting_states))

#        _logger.debug('(raw format) original automaton nodes: ' + str(automaton))
#        _logger.debug('(raw format) preprocessed automaton nodes: ' + str(automaton_wo_rejecting_states))

        encoder = Encoder(automaton_wo_rejecting_states, inputs, outputs, logic)
        smt_str = encoder.encode(current_bound)

        z3solver.solve(smt_str)

        if z3solver.get_state() == Z3.UNSAT:
            logger.info('unsat..')
        elif z3solver.get_state() == Z3.SAT:
            logger.info('sat!')
            model = SmtModel(z3solver.get_model())
            return model
        else:
            logger.warning('solver status is unknown')

    return None
