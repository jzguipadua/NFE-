import pandas as pd
import bifrost
import os

FILE = pd.read_excel(f'{bifrost.MY_USER}//OneDrive//PowerBi//Recursos//pedidos.xlsm',engine='openpyxl')

nf = pd.DataFrame(FILE["NOTA  FISCAL"].dropna())
bnf = pd.DataFrame(FILE["NF BONIFICAÇÃO"].dropna())

nf["Tipo NF"] = "NOTA  FISCAL"
bnf["Tipo NF"] = "NF BONIFICAÇÃO"



def run():
    
    print(bnf)

run()