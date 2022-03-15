import time
import nfe
import nfeCan
import nfeCorrecao
import concat_csv_nfe
import updatexlsQueries
import os
print(""" 
  ____    _    __                        _                           _                      
 | __ )  (_)  / _|  _ __    ___    ___  | |_     ___   _   _   ___  | |_    ___   _ __ ___  
 |  _ \  | | | |_  | '__|  / _ \  / __| | __|   / __| | | | | / __| | __|  / _ \ | '_ ` _ \ 
 | |_) | | | |  _| | |    | (_) | \__ \ | |_    \__ \ | |_| | \__ \ | |_  |  __/ | | | | | |
 |____/  |_| |_|   |_|     \___/  |___/  \__|   |___/  \__, | |___/  \__|  \___| |_| |_| |_|
                                                       |___/                                """ )
time.sleep(0.5)
print("Notas fiscais")

def mainMenu():
    print("Menu Principal")
    def opcoes():
       return input(""" 
1 - Atualizar base completa
2 - Atualizar notas canceladas
3 - Atualizar cartas de correção
4 - Atualizar planilhas
5 - Sair
""")
    r = opcoes()
    
    exec(r)
    
def exec(resp):
    if resp == '1':
        THISUSER = os.path.expanduser("~")
        NFEPATH = os.path.join(THISUSER, "OneDrive/Powerbi/NFE/pending")
        os.chdir(NFEPATH)        
        nfe.run()
        nfeCan.run()
        nfeCorrecao.run()
        concat_csv_nfe.run_into_folders()
        updatexlsQueries.run()
        mainMenu()
    elif resp == '2':
        nfeCan.run()
        mainMenu()
    elif resp == '3':
        nfeCorrecao.run()
        mainMenu()
    elif resp == '4':
        updatexlsQueries.run()
        mainMenu()
    elif resp == '5':
        exit()
    else:
        mainMenu()

mainMenu()