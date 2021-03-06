from helpers.spec_helper import *
from interfaces.spec import Spec

rs1, r1 = sig_prop('r1')
gs1, g1 = sig_prop('g1')

rs2, r2 = sig_prop('r2')
gs2, g2 = sig_prop('g2')

inputs = [rs1,rs2]
outputs = [gs1,gs2]

# formula = ~g1 & ~g2 & \
#           AG((r1 >> F(g1)) & (r2 >> F(g2))) & \
#           AG(((~g1 & r1) >> F(g1)) & ((~g2 & r2) >> F(g2))) & \
#           AG(~(g1&g2))

formula = ~g1 & ~g2 & \
          AG((r1 >> F(g1)) & (r2 >> F(g2))) & \
          AG(~(g1&g2)) & \
          AG(EF(~g1 & r1 & X(r1 & ~g1 & X(~g1)))) & \
          AG(EF(~g2 & r2 & X(r2 & ~g2 & X(~g2))))
spec = Spec(inputs, outputs, formula)
