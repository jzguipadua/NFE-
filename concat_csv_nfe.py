from os import listdir, getcwd, chdir, path
import pandas as pd
import time
from progress.bar import Bar
import math
import numpy as np

TARGET_FOLDERS = ['_SX COSMETICS','_BEAUTY SUPPLY','_BEAUTY BRAZIL','_COFERLY COSMETICA LTDA','_QUIOSQUE HIGIENOPOLIS','_QUIOSQUE MORUMBI']
REF_FOLDERS = ['Total','Produtos']
EXTENSION_PREF = {'Total':'-tot','Produtos':'-prod'}
NFEPATH = 'OneDrive/PowerBi/NFE'

def df_csv(df, name):
    df.to_csv(name,sep='|', encoding='utf8')

def goto_nfe_folder():
    cur_user = path.expanduser('~')
    setPath_nfe = path.join(cur_user,NFEPATH)
    chdir(setPath_nfe)



def split_frame(df, file_name):
    size = len(df.index)
    print(size)
    sz_control = 50000
   
    if size > sz_control:
        print(f'Target folder dataframe splited accordind to preset value: {sz_control}')
        
        print(getcwd())
        chdir(path.join(getcwd(),'Base'))
        _df = df.reset_index()
        df_split = np.array_split(_df,math.ceil(size/sz_control))

        for i in range(len(df_split)):
            df_csv(df_split[i],f'{i}_{file_name}')
        
        _ = path.split(getcwd())
        chdir(_[0])
    else:
        print('Split method was not used')
        print(getcwd())
        chdir(path.join(getcwd(),'Base'))
        df_csv(df,file_name)
        _ = path.split(getcwd())
        chdir(_[0])


def mkframe(extention, folder_name):
    l = listdir()
    files = []
    df_lst = []
    extention = extention + '.csv'
    for f in l:
        if extention in f:
            
            files.append(f)
        else: pass

    with Bar(f'Building Csv {folder_name} {extention}',max=len(files) ,fill='#')as bar:
        for i in files:
            df_lst.append(pd.read_csv(i,sep='|', index_col='Unnamed: 0',encoding='utf8'))
            bar.next()
    bar.finish()
    o = pd.concat(df_lst)
    
    file_name = folder_name + extention
    split_frame(o, file_name)





def run_into_folders():
    goto_nfe_folder()
    lsDir = listdir()
    
    for target in lsDir:
            if target in TARGET_FOLDERS:
                
                chdir(path.join(getcwd(),target))
                
                # ! ;;;;;;;;;;;;;
                lsDir_ref = listdir()
                for ref in lsDir_ref:
                    
                    if ref in REF_FOLDERS:
                        chdir(path.join(getcwd(),ref))
                        # todo AQUI QUE VAI O CÓDIGO DO MKFRAME
                        mkframe(EXTENSION_PREF[ref],target)
                       
                        _ = path.split(getcwd())
                        chdir(_[0])
                        

                        
                        time.sleep(0.015)
                    else:
                        pass

            goto_nfe_folder()
    
    
            
run_into_folders()           

