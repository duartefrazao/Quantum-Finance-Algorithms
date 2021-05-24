from qiskit import BasicAer
from qiskit.aqua import aqua_globals, QuantumInstance
from qiskit.aqua.algorithms import QAOA, NumPyMinimumEigensolver,VQE
from qiskit.circuit.parameter import Parameter
from qiskit.optimization.algorithms import MinimumEigenOptimizer, RecursiveMinimumEigenOptimizer,GroverOptimizer
from qiskit.optimization import QuadraticProgram

from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.aqua import QuantumInstance
from qiskit.finance.applications.ising import portfolio
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.finance.data_providers import RandomDataProvider
from qiskit.aqua.algorithms import VQE, QAOA, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import COBYLA
import numpy as np
import matplotlib.pyplot as plt
import datetime
import math as math
from math import sin,cos
from itertools import combinations
from qiskit.aqua.operators import  PrimitiveOp, SummedOp
from qiskit.quantum_info.operators import Pauli,Operator
from qiskit import QuantumCircuit
from qiskit.extensions import HamiltonianGate
from qiskit.aqua.operators import (OperatorBase, Swap,X, I,Y, H, CircuitStateFn,
                                   EvolutionFactory, LegacyBaseOperator)
aqua_globals.massive = True

def qaoa(qubo,num_assets,num_assets_wanted, alternating):
    num_ancila_qubits = 2
    ansatz = ((X^num_assets_wanted)^(I^(num_assets-num_assets_wanted)))#^(I^num_ancila_qubits)
    mixer_iterations = math.ceil((num_assets/2))
    """     print(mixer_iterations)
    mixer = QuantumCircuit(num_assets+ 1)
    theta = Parameter('θ')
    
    cos = math.cos(theta / 2)
    sin = math.sin(theta / 2)
    np.array([[cos, -1j * sin],
                        [-1j * sin, cos]], dtype=dtype)
    op = Operator(op)
    for i in range(num_assets-1):
        mixer.unitary(iswap_op, [i, i+1], label='iswap') """
    
    """ num_qubits = num_assets + 2
    mixer = QuantumCircuit(num_qubits)
    num_iterations = math.ceil((num_assets) /2) - 1
    theta = Parameter('θ1')

    mixer.rx(theta,0)
    mixer.rx(theta,1)
    for iteration in range(num_iterations):
        ancila = 0
        for i in range(0,num_qubits - 3,+2):
            mixer.cswap(num_qubits-1,i,i+1)
        for i in range(1,num_qubits - 3,+2):
            mixer.cswap(num_qubits-1,i,i+1)
        if num_qubits%2 == 1:
            mixer.cswap(num_qubits-1,num_qubits-3,0)
        for i in range(3,num_qubits-1,+2):
            mixer.cswap(0 + ancila%2,i,i+1)
            ancila = ancila + 1
        for i in range(2,num_qubits-1,+2):
            mixer.cswap(0 + ancila%2,i,i+1)
            ancila = ancila + 1
        if num_qubits%2 == 1:
            mixer.cswap(0 + ancila%2,num_qubits-1,2)
    mixer.rx(-theta,0)
    mixer.rx(-theta,1) """
    #mixer = I^num_qubits
    quantum_instance = QuantumInstance(BasicAer.get_backend('qasm_simulator'),
                                    seed_simulator=aqua_globals.random_seed,
                                    seed_transpiler=aqua_globals.random_seed,
                                    shots=4096)#,basis_gates=['iswap','cx','swap','unitary','u1','u2','u3'])
                                    
    #qaoa_mes = QAOA(quantum_instance=quantum_instance, p=1, initial_state=ansatz,optimizer=COBYLA(rhobeg=(np.pi/4),maxiter=4000), num_mixer_params = mixer_iterations)
    #qaoa_mes = QAOA(mixer=mixer,quantum_instance=quantum_instance, p=1, initial_state=ansatz,optimizer=COBYLA(rhobeg=(np.pi/4),maxiter=4000), num_mixer_params = mixer_iterations)
    
    p = 1

    if alternating:
        qaoa_mes = QAOA(quantum_instance=quantum_instance,p=p,initial_state=ansatz,optimizer=COBYLA(rhobeg=(np.pi/4)), alternating=alternating)
    else:
        qaoa_mes = QAOA(quantum_instance=quantum_instance,p=p,optimizer=COBYLA(rhobeg=(np.pi/4)))
    #qaoa_mes = QAOA(quantum_instance=quantum_instance)

    #qaoa_mes = QAOA(quantum_instance=quantum_instance, initial_state=ansatz,p=1, optimizer=COBYLA(), num_mixer_params = mixer_iterations)
    #qaoa_mes = QAOA(quantum_instance=quantum_instance,p=1, optimizer=COBYLA(), num_mixer_params = 1)
    qaoa = MinimumEigenOptimizer(qaoa_mes)   
    qaoa_result = qaoa.solve(qubo)
    return qaoa_result

def vqe(qubo):
    quantum_instance = QuantumInstance(BasicAer.get_backend('statevector_simulator'),
                                    seed_simulator=aqua_globals.random_seed,
                                    seed_transpiler=aqua_globals.random_seed)
    vqe_mes = VQE(quantum_instance=quantum_instance, initial_point=[0., 0.])
    vqe = MinimumEigenOptimizer(vqe_mes)   
    vqe_result = vqe.solve(qubo)
    return vqe_result

def grover_optimizer(qubo,num_stocks):
    quantum_instance = QuantumInstance(BasicAer.get_backend('statevector_simulator'),
                                    seed_simulator=aqua_globals.random_seed,
                                    seed_transpiler=aqua_globals.random_seed)
    grover_mes =GroverOptimizer(6, quantum_instance=quantum_instance)
    grover_result = grover_mes.solve(qubo)
    return grover_result

def minimum_eigen(qubo):
    quantum_instance = QuantumInstance(BasicAer.get_backend('statevector_simulator'),
                                    seed_simulator=aqua_globals.random_seed,
                                    seed_transpiler=aqua_globals.random_seed)
    exact_mes = NumPyMinimumEigensolver()
    exact = MinimumEigenOptimizer(exact_mes) 
    exact_result = exact.solve(qubo)
    return exact_result