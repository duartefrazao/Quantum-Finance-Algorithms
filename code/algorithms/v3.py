from qiskit import Aer
from qiskit.circuit.library import TwoLocal
from qiskit.aqua import QuantumInstance
from qiskit.optimization.applications.ising.common import sample_most_likely
from qiskit.aqua.algorithms import VQE, QAOA, NumPyMinimumEigensolver
from qiskit.aqua.components.optimizers import COBYLA
from aux_functions import IncompatibleArguments
import numpy as np
import matplotlib.pyplot as plt

# initialization
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile

# import basic plot tools
from qiskit.visualization import plot_histogram

#Quadratic
from qiskit.optimization import QuadraticProgram
from docplex.mp.advmodel import AdvModel


def portfolio_optimization3(assets,assets_to_include,mu,sigma,num_assets_portfolio,risk_aversion,penalty):

    if len(mu) != sigma.shape[0] or len(mu) != sigma.shape[1] or len(mu) != len(assets):
        raise IncompatibleArguments("Sigma, mu and assets need to be equal in size")
    if not 0 <= risk_aversion <= 1:
        raise IncompatibleArguments("Risk aversion needs to be in [0,1]")
    if not 0 < num_assets_portfolio <= len(assets):
        raise IncompatibleArguments("Number of assets to include in the portfolio needs to be smaller or equal to the number of assets passed")
    if len(assets_to_include) > num_assets_portfolio:
        raise IncompatibleArguments("Can't include stocks mentioned, they are more than the number of assets to include")


    for asset in assets_to_include:
        if not asset in assets:
            raise IncompatibleArguments("Asset " + asset + " not contained in asset list")

    #Initialize binary variable array
    mdl = AdvModel('docplex model')
    mdl.init_numpy()
    decision_vars = np.array([])

    to_choose_assets = np.zeros(len(assets))

    for i in range(len(assets)):
        curr_asset = assets[i]
        if curr_asset in assets_to_include:
            to_choose_assets[i]=1
        decision_vars = np.append(decision_vars,[mdl.binary_var(str(curr_asset))])
  

    #Terms
    vec_ones = np.ones(len(decision_vars)) #helper vector
    num_assets_chosen = np.matmul(vec_ones.T,decision_vars) 
    num_necessary_assets_chosen = np.matmul(to_choose_assets.T,decision_vars)
    expected_num_assets_chosen = len(assets_to_include)
    expected_returns_portfolio = np.matmul(mu.T,decision_vars)
    variance_portfolio = np.matmul(decision_vars.T,np.dot(sigma,decision_vars)) / 2

    #Objective function
    mdl.minimize(
        - expected_returns_portfolio 
        + (risk_aversion * variance_portfolio) 
        + penalty * ((expected_num_assets_chosen - num_necessary_assets_chosen)**2) 
        + penalty*(num_assets_chosen - num_assets_portfolio)**2)


    qubo = QuadraticProgram()
    qubo.from_docplex(mdl)

    if DEBUG:
        print(mdl.export_as_lp_string())
    
    return qubo


