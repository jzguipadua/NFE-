

import bifrost
import pandas as pd
from bifrost import goto, list_files, nice_p

typez = bifrost.types().sufix

class Dac(object):

    def __init__(self, ref=bifrost.open_json("dac.json")):
        self.ref = ref

    def get(obj, arg):
        if arg not in obj.ref:
            print(
                f"GET ERROR [Argument not found in dac list: {arg}] \nUse ref.keys() method to see a valid comand.")
        else:
            goto(obj.ref[arg]["path"])
            f = bifrost.find(arg)
            return bifrost.frame_xls(f,obj.ref[arg]["target"][0])
            


