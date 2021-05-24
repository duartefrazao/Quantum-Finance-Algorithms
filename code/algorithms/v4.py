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

sector_dictinary = {
    "tech":["AAPL","MSFT"],
    "automotive":["TSLA","GM"],
    "consumer":["JWN","NKE"]
}


def portfolio_optimization(assets,sectors_to_favour,mu,sigma,num_assets_portfolio,risk_aversion,penalty):

    if len(mu) != sigma.shape[0] or len(mu) != sigma.shape[1] or len(mu) != len(assets):
        raise IncompatibleArguments("Sigma, mu and assets need to be equal in size")
    if not 0 <= risk_aversion <= 1:
        raise IncompatibleArguments("Risk aversion needs to be in [0,1]")
    if not 0 < num_assets_portfolio <= len(assets):
        raise IncompatibleArguments("Number of assets to include in the portfolio needs to be smaller or equal to the number of assets passed")

    #Join dictionary stocks to make lookup easy
    stocks_in_sectors_to_favour = []
    for sector in sector_dictinary:
        if sector in sectors_to_favour:
            stocks_in_sectors_to_favour = stocks_in_sectors_to_favour + sector_dictinary[sector]

    #Initialize binary variable array
    mdl = AdvModel('docplex model')
    mdl.init_numpy()
    decision_vars = np.array([])

    to_favour_sector = np.zeros(len(assets))

    for i in range(len(assets)):
        curr_asset = assets[i]
        if curr_asset in stocks_in_sectors_to_favour:
            to_favour_sector[i]=1
        decision_vars = np.append(decision_vars,[mdl.binary_var(str(curr_asset))])
  

    #Terms
    vec_ones = np.ones(len(decision_vars)) #helper vector
    num_assets_chosen = np.matmul(vec_ones.T,decision_vars) 
    num_stocks_chosen_from_sectors_to_favour = np.matmul(to_favour_sector.T,decision_vars)
    expected_returns_portfolio = np.matmul(mu.T,decision_vars)
    variance_portfolio = np.matmul(decision_vars.T,np.dot(sigma,decision_vars)) / 2

    #Objective function
    mdl.minimize(- expected_returns_portfolio 
    + (risk_aversion * variance_portfolio) 
    - penalty * num_stocks_chosen_from_sectors_to_favour 
    + penalty * (num_assets_chosen - num_assets_portfolio)**2)


    qubo = QuadraticProgram()
    qubo.from_docplex(mdl)

    return qubo


