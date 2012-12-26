from parsing.helpers import Visitor
from parsing.interface import BinOp, UnaryOp, Signal, Number


class SignalsChecker(Visitor):
    def __init__(self, known_signals):
        self._known_signals = known_signals
        self.unknown_signal = None

    def visit_binary_op(self, binary_op:BinOp):
        if not self.unknown_signal:
            self.dispatch(binary_op.arg1)
        if not self.unknown_signal:
            self.dispatch(binary_op.arg2)

    def visit_unary_op(self, unary_op:UnaryOp):
        self.dispatch(unary_op.arg)

    def visit_bool(self, bool_const):
        return

    def visit_signal(self, signal:Signal):
        if signal not in self._known_signals:
            self.unknown_signal = signal

    def visit_number(self, number:Number):
        return


def check_unknown_signals_in_properties(property_asts, known_signals):
    signals_checker = SignalsChecker(known_signals)
    for a in property_asts:
        signals_checker.dispatch(a)
        if signals_checker.unknown_signal:
            return 'found unknown signal "{signal}" in property "{ast}"'.format(
                signal = str(signals_checker.unknown_signal),
                ast = str(a))