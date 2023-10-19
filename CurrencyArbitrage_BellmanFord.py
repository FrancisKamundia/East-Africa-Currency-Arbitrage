#import packages
import math
from typing import Tuple, List
from math import log
import pandas as pd
import numpy as np

#Import the currency Matrix
df = pd.read_excel("Currencies_Matrix.xlsx")
print(df)
#Drop the 1st column
df_1 = df.iloc[:, 1:]
# Extract currencies names
currencies = list(df_1.columns)
# Extract the rates
rates = df_1[:].values


#BELLMAN FORD ALGORITHM

#Start by calculating the negative logs
def negate_logarithm_convertor(graph: Tuple[Tuple[float]]) -> List[List[float]]:
    """log of each rate in graph and negate it"""
    result = [[-log(edge) for edge in row] for row in graph]
    return result

#Calculate the arbitrage

def arbitrage(currency_tuple: tuple, rates_matrix: Tuple[Tuple[float, ...]]):
    ''' Calculates arbitrage situations and prints out the details of this calculations'''

    trans_graph = negate_logarithm_convertor(rates_matrix)

    # Pick any source vertex -- we can run Bellman-Ford from any vertex and get the right result

    source = 0
    n = len(trans_graph)
    min_dist = [float('inf')] * n

    pre = [-1] * n
    
    min_dist[source] = source

    # 'Relax edges |V-1| times'
    for _ in range(n-1):
        for source_curr in range(n):
            for dest_curr in range(n):
                if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                    min_dist[dest_curr] = min_dist[source_curr] + trans_graph[source_curr][dest_curr]
                    pre[dest_curr] = source_curr

    # if we can still relax edges, then we have a negative cycle
    for source_curr in range(n):
        for dest_curr in range(n):
            if min_dist[dest_curr] > min_dist[source_curr] + trans_graph[source_curr][dest_curr]:
                # negative cycle exists, and use the predecessor chain to print the cycle
                print_cycle = [dest_curr, source_curr]
                # Start from the source and go backwards until you see the source vertex again or any vertex that already exists in print_cycle array
                while pre[source_curr] not in  print_cycle:
                    print_cycle.append(pre[source_curr])
                    source_curr = pre[source_curr]
                print_cycle.append(pre[source_curr])
                arbi = ([currencies[p] for p in print_cycle[::-1]])
    return arbi



#Run the algorithm with data
print("Arbitrage Opportunity: \n\n", " --> " .join([p for p in arbitrage(currencies, rates)]))


#CALCULATE AMOUNT GAINED USING ARBITRAGE OPPORTUNITY

#Set the currency column to be index
df_2= df.set_index(["Currencies"])
#list of arbitrage opportunity
arbiOppotunity = arbitrage(currencies, rates)

#extract values from data
list_1 = []
for i in range(len(arbiOppotunity)-1):
    list_1.append(df_2.loc[arbiOppotunity[i]][arbiOppotunity[i+1]])

#multiply function
def multiplyList(myList):
     
    # Multiply elements one by one
    result = 1
    for x in myList:
        result = result * x
    return result

#Amount gained using arbitrage opportunity
print("Amount gained using arbitrage : ", multiplyList(list_1))

