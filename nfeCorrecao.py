import os
import shutil
import bifrost
import shutil
import pandas as pd
from progress.bar import Bar

bifrost.goto(
    r'PATH GOES HERE'
)


FRAME_LIST = []

DICT_LIST = []


def mk_dicts(list):
    for file in list:
        d = bifrost.open_xml(file)
        DICT_LIST.append(d["procEventoNFe"])


def mk_frames(list):
    d = {}
    l = []
    with Bar(f'Atualizando Dataframe de cartas de correção', max=len(list), fill='#') as bar:
        for dict in list:
            d = {
                "KEY": dict["evento"]["infEvento"]["chNFe"],
                "CNPJ": dict["evento"]["infEvento"]["CNPJ"],
                "STATUS": dict["evento"]["infEvento"]["detEvento"]["descEvento"],
                "MOTIVO": dict["evento"]["infEvento"]["detEvento"]["xCorrecao"],
            }
            l.append(d)
            bar.next()
    df = pd.DataFrame(l)
    bar.finish()
    df.to_csv(
        r'PATH GOES HERE/NFE/correcoes/cartas_de_correcao.csv',
        sep=";",
        encoding="utf8",
    )


def exportCancelFiles():

    bifrost.goto(
        r'C:/Users/supor/OneDrive/PowerBi/NFE/correcoes'
    )

    f = bifrost.filter_list(bifrost.list_files(), "-procEventoNfe.xml")
    gd = os.getcwd()
    td = bifrost.p_join(
        bifrost._split(gd, 1), "pending"
    )
    with Bar(f'Exportando cartas de correção', max=len(f), fill='#') as bar:
        for file in f:
            shutil.copy(f'{gd}/{file}', f'{td}/{file}')
            bar.next()
    bar.finish()


def run():

    exportCancelFiles()
    bifrost.goto(r'C:/Users/supor/OneDrive/PowerBi/NFE/pending')
    FILES_LIST = bifrost.filter_list(bifrost.list_files(), "-procEventoNfe.xml")

    def move_files():
        ppd = r'PATH GOES HERE/NFE/pending'
        ccd = r'PATH GOES HERE/NFE/correcoes'
        with Bar(f'Importando cartas de correção', max=len(FILES_LIST), fill='#') as bar:
            for files in FILES_LIST:
                shutil.copy(f'{ppd}/{files}', f'{ccd}/{files}')
                os.remove(f'{ppd}/{files}')
                bar.next()
        bar.finish()

    mk_dicts(FILES_LIST)
    mk_frames(DICT_LIST)
    move_files()

run()




 
