import matplotlib.pyplot as plt
import numpy as np

def generate_solution_label(result,stocks):
    res_str = ""
    i = 0
    for allocation in result:
        res_str+= str(allocation)[:4] + "_" + stocks[i] + "  "
        i+=1
    return res_str.replace("0.0","0")


def graph(stocks,optimum_sol,quantum_sol,brute_force_sol):

    fig, ax = plt.subplots()  # Create a figure and an axes.

    brute = {"returns" : [],"risk":[]}

    for solution in brute_force_sol["info"]:
        brute['returns'].append(solution['returns'])
        brute['risk'].append(solution['risk'])


    if optimum_sol["info"]["risk"]:
        ax.scatter(optimum_sol["info"]["risk"],optimum_sol["info"]["returns"], label=optimum_sol['name'],marker=">",s=[120]) 
    for solution in quantum_sol:
        info = solution['info']
        if solution["qaoa"] :
            ax.scatter(info["risk"],info["returns"], label=solution["name"],marker="<",s=[120])  
        else:
            ax.scatter(info["risk"],info["returns"], label=solution["name"],marker="^",s=[120])  

    ax.scatter(brute["risk"],brute["returns"], label=brute_force_sol['name'],marker="x",color="black") 

    #x,y=quantum_sol[0]["info"]["risk"],quantum_sol[0]["info"]["returns"]

    #annotation = 'Qiskit Solution = ' + generate_solution_label(quantum_sol[0]["info"]["result"],stocks)
    #plt.figtext(0.5, 0.05, annotation, fontsize=8,ha='center')
    plt.subplots_adjust(bottom=0.2)
    ax.set_xlabel('% Portfolio Variance') 
    ax.set_ylabel('% Expected returns')
    ax.set_title("Plot of results") 

    plt.legend( loc='upper left') 
    ax.plot()
    plt.show()
