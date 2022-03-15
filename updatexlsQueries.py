import bifrost
import os
from bifrost import delay


def run():
    print('Running update from xls macro files')
    delay(0.15)
    try:
        bifrost.goto(
        bifrost.p_join(bifrost._split(
                __file__,1
            ),'vbs')
        )


        f = bifrost.filter_list(
            bifrost.list_files(),'vbs'
        )

        for file in  f:
            os.system(file)
            delay(2)

        print("Done")
    except Exception as e:
        print(e)

