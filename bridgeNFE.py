import nfe
import nfeCan
import nfeCorrecao
import concat_csv_nfe
import updatexlsQueries
import os
def exec():
    THISUSER = os.path.expanduser("~")
    NFEPATH = os.path.join(THISUSER, "OneDrive/Powerbi/NFE/pending")
    os.chdir(NFEPATH)
    nfe.run()
    nfeCan.run()
    nfeCorrecao.run()
    concat_csv_nfe.run_into_folders()
    updatexlsQueries.run()

exec()