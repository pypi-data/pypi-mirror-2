from sympy import I, Matrix, symbols

from sympy.physics.quantum import hbar, represent, Commutator
from sympy.physics.quantum import qapply
from sympy.physics.quantum.spin import (J2, Rotation, Jplus, JzKet, Jminus,
        Jx, Jy, Jz)


def test_represent():
    assert represent(Jz) == hbar*Matrix([[1,0],[0,-1]])/2
    assert represent(Jz, j=1) == hbar*Matrix([[1,0,0],[0,0,0],[0,0,-1]])

def test_jplus():
    assert Commutator(Jplus, Jminus).doit() == 2*hbar*Jz
    assert qapply(Jplus*JzKet(1,1)) == 0
    assert Jplus.matrix_element(1,1,1,1) == 0
    assert Jplus.rewrite('xyz') == Jx + I*Jy

def test_rotation():
    assert Rotation.d(1,1,1,0) == 1

def test_j2():
    j, m = symbols('j m')
    assert Commutator(J2, Jz).doit() == 0
    assert qapply(J2*JzKet(1,1)) == 2*hbar**2*JzKet(1,1)
    assert qapply(J2*JzKet(j,m)) == j**2*hbar**2*JzKet(j,m)+j*hbar**2*JzKet(j,m)
    assert J2.matrix_element(1,1,1,1) == 2*hbar**2

