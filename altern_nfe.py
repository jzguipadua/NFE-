#
#todo                              UTILIZADO NO MOMENTO PARA GERAR MATRIZ DE NFE DAS NOTAS ALTERNATIVAS 
#!                                 ESTE MÓDULO NÃO SE APLICA PARA NOTAS DE ENTRADA
from logging import exception
from types import NoneType
import bifrost
import shutil
import json
import os
import xmltodict
import time
from pprint import pprint
from progress.bar import Bar
import pandas as pd


class BRAE(object):
    __slot__ = "companies"

    def get_companyFile():
        file_list = os.listdir()
        for file in file_list:
            if ".json" in file:
                try:
                    with open(file, "r") as file:
                        tyb = json.load(file)
                        if "empresa" in tyb.keys():
                            return tyb
                except:
                    pass

    def __init__(self, companies=get_companyFile()):
        self.companies = companies


EMPRESAS = BRAE().companies
THISUSER = os.path.expanduser("~")
NFEPATH = os.path.join(THISUSER, "OneDrive/Powerbi/NFE")
bifrost.nfe_pendingFolder()
PENDING_FILES = bifrost.filter_list(bifrost.list_files(), 'xml')


print(EMPRESAS)


class Nfe:
    def __init__(self, file):
        def obj(file):
            with open(file, 'r', encoding='utf8') as file:
                return json.loads(json.dumps(xmltodict.parse(file.read())))

        self.file = obj(file)

    def params(obj):
        dest = obj.file["CFe"]["infCFe"]["dest"]
        if isinstance(dest, NoneType):
            dest = [{"xNome":"CLIENTE QUIOSQUE","CNPJ":"00000000"}]
        else:
            dest = [obj.file["CFe"]["infCFe"]["dest"]]

        return {
            "Id": obj.file["CFe"]["infCFe"]["@Id"],
            "Identificação": [obj.file["CFe"]["infCFe"]["ide"]],
            "Emitente": [obj.file["CFe"]["infCFe"]["emit"]],            
            "Destinatário": dest,    
            "Total": [obj.file["CFe"]["infCFe"]["total"]],
            "Pagamento": [obj.file["CFe"]["infCFe"]["pgto"]]
        }

    def prods(obj):
        if isinstance(obj.file["CFe"]["infCFe"]["det"], dict):
            prods_single = [obj.file["CFe"]["infCFe"]["det"]]
        else:
            prods = obj.file["CFe"]["infCFe"]["det"]

        try:

            df = {i["@nItem"]: [i] for i in prods}
            nip = []
            vlk = {}
            arq = {}
            # todo
            for i in df:
                arq[i] = df[i][0]['imposto']
            for item in arq:
                #! item por nota
                # print(arq[item])
                for key in arq[item]:
                    # print(arq[item][key])
                    vlk[item] = arq[item]
                    for subkey in arq[item][key]:
                        # print(arq[item][key][subkey])
                        #  print(type(arq[item][key][subkey]))
                        # keyFname = key +'_'+subkey #!sem ramificação
                        try:
                            for inkey in arq[item][key][subkey]:
                                if isinstance(arq[item][key][subkey], dict):
                                    # print(f'{key}_{inkey}')
                                    n_kName = key + "_" + inkey
                                    # print(arq[item][key][subkey][inkey])
                                    nip.append(({
                                        '@nItem':
                                        item,
                                        n_kName:
                                        arq[item][key][subkey][inkey]
                                    }))

                                else:
                                    # print(f'{key}_{subkey}')
                                    n_kName = key + "_" + subkey
                                    # print(arq[item][key][subkey])
                                    nip.append(({
                                        '@nItem': item,
                                        n_kName: arq[item][key][subkey]
                                    }))

                                    break
                        except:
                            pass

            xdf = pd.DataFrame(nip).set_index('@nItem').fillna('')
            ts = xdf.groupby(xdf.index).sum()
            ndf = ts.to_dict(orient='index')
            # pprint(ndf)
            for skey in ndf:

                # pprint(df[skey][0]['@nItem'])
                # print('=====================')

                df[skey][0]['imposto'] = ndf[skey]

# todo
#!

        except:

            df = {i["@nItem"]: [i] for i in prods_single}
            #!

            nip = []
            vlk = {}
            arq = {}
            # todo
            for i in df:
                arq[i] = df[i][0]['imposto']
            for item in arq:
                #! item por nota
                # print(arq[item])
                for key in arq[item]:
                    # print(arq[item][key])
                    vlk[item] = arq[item]
                    for subkey in arq[item][key]:
                        # print(arq[item][key][subkey])
                        #  print(type(arq[item][key][subkey]))
                        # keyFname = key +'_'+subkey #!sem ramificação
                        try:
                            for inkey in arq[item][key][subkey]:
                                if isinstance(arq[item][key][subkey], dict):
                                    # print(f'{key}_{inkey}')
                                    n_kName = key + "_" + inkey
                                    # print(arq[item][key][subkey][inkey])
                                    nip.append(({
                                        '@nItem':
                                        item,
                                        n_kName:
                                        arq[item][key][subkey][inkey]
                                    }))

                                else:
                                    # print(f'{key}_{subkey}')
                                    n_kName = key + "_" + subkey
                                    # print(arq[item][key][subkey])
                                    nip.append(({
                                        '@nItem': item,
                                        n_kName: arq[item][key][subkey]
                                    }))

                                    break
                        except:
                            pass

            xdf = pd.DataFrame(nip).set_index('@nItem').fillna('')
            ts = xdf.groupby(xdf.index).sum()
            ndf = ts.to_dict(orient='index')
            # pprint(ndf)
            for skey in ndf:

                # pprint(df[skey][0]['@nItem'])
                # print('=====================')

                df[skey][0]['imposto'] = ndf[skey]


#!

        return df

    def emissao(obj):
        df = {
            'data': obj.file["CFe"]["infCFe"]["ide"]['dEmi'],
            'cnpj': obj.file["CFe"]["infCFe"]["emit"]['CNPJ']
        }
        return df


def delay(x):
    time.sleep(x)


def retify(dict, key):
    df = {}
    for d in dict:
        d.update(d.pop(key, {}))

    return dict


def ramification_level(param):

    paramKeys = param.keys()
    RAMIFICATION = {}

    for key in paramKeys:
        RAMIFICATION[key] = ([], [])

    for key in param:

        if type(param[key]) == "str":
            RAMIFICATION[key][1].append(0)

        else:

            for subkey in param[key][0]:

                try:
                    RAMIFICATION[key][1].append(
                        len(param[key][0][subkey].keys()))
                except:
                    RAMIFICATION[key][1].append(0)

        for subkey in param[key][0]:
            if type(param[key][0]) == type("str"):
                RAMIFICATION[key][0].append(key)

            else:
                RAMIFICATION[key][0].append(subkey)

    return RAMIFICATION


def alignDF(param):
    ramification = ramification_level(param)

    for key in ramification:

        for i in range(len(ramification[key][1])):
            if ramification[key][1][i] > 0:

                level = ramification[key][0][i]
                dic = param[key]
                retify(dic, level)

            else:
                pass
    return param


def try_to_retify(df):

    level = ramification_level(df)
    for key in level:
        while sum(level[key][1]) != 0:
            tyb = alignDF(df)
            refresh = ramification_level(tyb)
            level = refresh
            # print(level[key][1])
    return tyb


def destiny_folder(param):
    date = param['data']
    company = ""
    if param['cnpj'] in EMPRESAS['empresa']:
        company = EMPRESAS['empresa'][param['cnpj']]
    else:
        company = "CnD"

    return company, date


def set_file_loc(param):
    company, date = destiny_folder(param)

    def f_date(date):
        if len(date) > 8:
            date = date.replace('-', '').replace('/', '')
        else:
            pass
        return f'{date[:4]}/{date[4:6]}'

    def moveTodir(company, date):
        # ? CODING HERE
        os.chdir(NFEPATH)
        file_path = os.path.join(company, date)
        try:
            os.chdir(file_path)
        except:
            os.makedirs(file_path)
            os.chdir(file_path)

        return os.getcwd()

    if company == "CnD":
        print('>> Bifrost system - WARNING!')
        print(
            'Could not resolve Company name. CNPJ from Emit field return Cnd [Company not Defined]'
        )
        delay(1)
        print(
            'Check if appears in your local company.json or even if this .xml is valid'
        )
        delay(1)
        print('This file will be allocated in NOTRESOLVED folders scheme.')
        company = 'NOTRESOLVED'
    else:
        pass

    return moveTodir(company, f_date(date))


def nfe_conversion(nota):
    PARAM = alignDF(nota.params())
    PRODS = try_to_retify(nota.prods())

    idken = pd.DataFrame(PARAM, columns=['Id'], index=[0])
    iden = pd.DataFrame(PARAM['Identificação'][0], index=['Identificação'])
    emitin = pd.DataFrame(PARAM['Emitente'][0], index=['Emitente'])
    destn = pd.DataFrame(PARAM['Destinatário'][0], index=['Destinatário'])
    totaln = pd.DataFrame(PARAM['Total'][0], index=['Totais'])
    

    df_nfe = [iden, emitin, destn, totaln]
    c_df_nfe = pd.concat(df_nfe).fillna('')
    c_df_nfe.insert(0, 'ID', idken['Id'][0])

    o = []
    for key in PRODS:
        o.append(pd.DataFrame(PRODS[key][0], index=['']))

    prods = pd.concat(o)
    prods.insert(0, 'ID', idken['Id'][0])

    return c_df_nfe, prods


def main():
    NOTA = ''

    # len(PENDING_FILES)
    
    def copy_files(path, file):
        dest1 = os.path.join(path, file)
        # print(dest1)
        file_path = os.path.join(NFEPATH, "pending")
        n_file_path = os.path.join(file_path, file)

        upFolder = os.path.join(NFEPATH, "uploaded")
        n_upFolder = os.path.join(upFolder, file)
        # print(upFolder)
        shutil.copy(n_file_path, dest1)
        shutil.copy(n_file_path, n_upFolder)

    def returnTopends():
        file_path = os.path.join(NFEPATH, "pending")
        os.chdir(file_path)

    def save_csv(total, prods, obj):
        def mkcompany_path(obj, param):
            if obj not in EMPRESAS['empresa']:
                return os.path.join(NFEPATH, '_NOTRESOLVED/' + param)
            else:
                return os.path.join(
                    NFEPATH, '_' + EMPRESAS['empresa'][obj] + '/' + param)

        delay(0.025)

        def validatePath(file_path):
            try:
                if file_path in os.listdir():
                    pass
                else:
                    os.makedirs(file_path)
            except:
                pass

        validatePath(mkcompany_path(obj.emissao()['cnpj'], 'Total'))
        validatePath(mkcompany_path(obj.emissao()['cnpj'], 'Produtos'))
        files_dir = [
            mkcompany_path(obj.emissao()['cnpj'], 'Total'),
            mkcompany_path(obj.emissao()['cnpj'], 'Produtos')
        ]
        dFrames = (total, prods)
        final_file = ('-tot', '-prod')
        # print(NOTA.params()['KEYN'])
        os.chdir(NFEPATH)

        for i in range(len(files_dir)):

            if os.path.isdir(files_dir[i]):

                fName = files_dir[i] + "/" + \
                    obj.params()['Id']+final_file[i]+'.csv'
                dFrames[i].to_csv(fName, encoding='utf-8-sig', sep='|')
                # print(files_dir[i]+' csv file succeed')

            else:
                os.mkdir(files_dir[i])
                fName = files_dir[i] + "/" + \
                    obj.params()['Id']+final_file[i]+'.csv'
                dFrames[i].to_csv(fName, encoding='utf-8-sig', sep='|')
                # print(files_dir[i]+' csv file succeed')

    with Bar(f'Processando dados...', max=len(PENDING_FILES), fill='#') as bar:
        for file in range(len(PENDING_FILES)):
            
            try:
                NOTA = Nfe(PENDING_FILES[file])
               
                total, prods = nfe_conversion(NOTA)
                file_path = set_file_loc(NOTA.emissao())
                save_csv(total, prods, NOTA)

                # print(PENDING_FILES[file])
                returnTopends()
                copy_files(file_path, PENDING_FILES[file])
                os.remove(PENDING_FILES[file])
                bar.next()
            except Exception as e:
                print(e)
                bar.next()
                pass
                #! BUILD REPORT CSV

    bar.finish()


main()
