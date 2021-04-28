import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# for k,i in indicators.items():
#     plt.plot(i[0],i[1])
#     plt.title(k)
#     plt.show()


class IQA_Interpolator():

    def __init__(self):
        self.indicators = {}
        self.indicators["coliformes"] = pd.read_csv('csv_iqa\COLIFORMESCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators["PH"] = pd.read_csv('csv_iqa/PHCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators["dbo"] = pd.read_csv('csv_iqa\DEMANDACSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators["N2"] = pd.read_csv('csv_iqa/NITROGENIOCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators["P"] = pd.read_csv('csv_iqa/fosforo.csv', delimiter=',', decimal='.', header=None)
        self.indicators["temp"] = pd.read_csv('csv_iqa/temperatura.csv', delimiter=',', decimal='.', header=None)
        self.indicators["turbidez"] = pd.read_csv('csv_iqa/turbidez.csv', delimiter=',', decimal='.', header=None)
        self.indicators["residuo"] = pd.read_csv('csv_iqa/residuo.csv', delimiter=',', decimal='.', header=None)
        self.indicators["O2"] = pd.read_csv('csv_iqa/o2dissolvido.csv', delimiter=',', decimal='.', header=None)
        self.indicatorFunctions = {}
        self.indicatorFunctions["coliformes"] = lambda x: np.interp(x, self.indicators["coliformes"][0], self.indicators["coliformes"][1])
        self.indicatorFunctions["PH"] = lambda x: np.interp(x, self.indicators["PH"][0], self.indicators["PH"][1])
        self.indicatorFunctions["dbo"] = lambda x: np.interp(x, self.indicators["dbo"][0], self.indicators["dbo"][1])
        self.indicatorFunctions["N2"] = lambda x: np.interp(x, self.indicators["N2"][0], self.indicators["N2"][1])
        self.indicatorFunctions["P"] = lambda x: np.interp(x, self.indicators["P"][0], self.indicators["P"][1])
        self.indicatorFunctions["temp"] = lambda x: np.interp(x, self.indicators["temp"][0], self.indicators["temp"][1])
        self.indicatorFunctions["turbidez"] = lambda x: np.interp(x, self.indicators["turbidez"][0], self.indicators["turbidez"][1])
        self.indicatorFunctions["residuo"] = lambda x: np.interp(x, self.indicators["residuo"][0], self.indicators["residuo"][1])
        self.indicatorFunctions["O2"] = lambda x: np.interp(x, self.indicators["O2"][0], self.indicators["O2"][1])
        self.indicatorList = list(self.indicators.keys())
        self.indicatorWeights = {a:b for a,b in zip(self.indicatorList, [0.15, 0.12, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.17])}
       
    def IQA_Result(self, valuesDict: dict):
        keys = valuesDict.keys()
        result = 1
        for key in keys:
            if key in self.indicatorList:
                result*= self.indicatorFunctions[key](valuesDict[key])**self.indicatorWeights[key]
        return result


def main():
    Interpolator = IQA_Interpolator()
    print(Interpolator.IQA_Result({'coliformes':5,'PH':7,'dbo':2, 'temp':25, 'turbidez':10, 'N2':0, 'P': 0, 'residuo': 50, 'O2':100}))
    print(Interpolator.indicatorWeights)
if __name__ == "__main__":
    main()