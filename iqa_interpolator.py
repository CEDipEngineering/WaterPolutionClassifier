import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# for k,i in indicators.items():
#     plt.plot(i[0],i[1])
#     plt.title(k)
#     plt.show()


class IQA_Interpolator():
    #['pH', 'Temperatura da Água', 'Sólido Dissolvido Total', 'Oxigênio Dissolvido', 'Turbidez', 'Nitrogênio-Nitrito', 'Nitrogênio-Nitrato', 'Nitrogênio Amoniacal', 'Fósforo Total', 'DBO (5, 20)', 'Coliformes Termotolerantes']

    def __init__(self):
        self.indicators = {}
        self.indicators['Coliformes Termotolerantes'] = pd.read_csv('csv_iqa\COLIFORMESCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators['pH'] = pd.read_csv('csv_iqa/PHCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators['DBO (5, 20)'] = pd.read_csv('csv_iqa\DEMANDACSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators['Nitrogênio-Nitrato'] = pd.read_csv('csv_iqa/NITROGENIOCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators['Fósforo Total'] = pd.read_csv('csv_iqa/fosforo.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Temperatura da Água'] = pd.read_csv('csv_iqa/temperatura.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Turbidez'] = pd.read_csv('csv_iqa/turbidez.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Sólido Dissolvido Total'] = pd.read_csv('csv_iqa/residuo.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Oxigênio Dissolvido'] = pd.read_csv('csv_iqa/o2dissolvido.csv', delimiter=',', decimal='.', header=None)
        self.indicatorFunctions = {}
        self.indicatorFunctions['Coliformes Termotolerantes'] = lambda x: np.interp(x, self.indicators['Coliformes Termotolerantes'][0], self.indicators['Coliformes Termotolerantes'][1])
        self.indicatorFunctions['pH'] = lambda x: np.interp(x, self.indicators['pH'][0], self.indicators['pH'][1])
        self.indicatorFunctions['DBO (5, 20)'] = lambda x: np.interp(x, self.indicators['DBO (5, 20)'][0], self.indicators['DBO (5, 20)'][1])
        self.indicatorFunctions['Nitrogênio-Nitrato'] = lambda x: np.interp(x, self.indicators['Nitrogênio-Nitrato'][0], self.indicators['Nitrogênio-Nitrato'][1])
        self.indicatorFunctions['Fósforo Total'] = lambda x: np.interp(x, self.indicators['Fósforo Total'][0], self.indicators['Fósforo Total'][1])
        self.indicatorFunctions['Temperatura da Água'] = lambda x: np.interp(x, self.indicators['Temperatura da Água'][0], self.indicators['Temperatura da Água'][1])
        self.indicatorFunctions['Turbidez'] = lambda x: np.interp(x, self.indicators['Turbidez'][0], self.indicators['Turbidez'][1])
        self.indicatorFunctions['Sólido Dissolvido Total'] = lambda x: np.interp(x, self.indicators['Sólido Dissolvido Total'][0], self.indicators['Sólido Dissolvido Total'][1])
        self.indicatorFunctions['Oxigênio Dissolvido'] = lambda x: np.interp(x, self.indicators['Oxigênio Dissolvido'][0], self.indicators['Oxigênio Dissolvido'][1])
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
    print(Interpolator.IQA_Result({'Coliformes Termotolerantes':5, 'pH':7, 'DBO (5, 20)':2, 'Temperatura da Água':0, 'Turbidez':10, 'Nitrogênio-Nitrato':0, 'Fósforo Total': 0, 'Sólido Dissolvido Total': 50, 'Oxigênio Dissolvido':100}))
    print(Interpolator.indicatorWeights)
if __name__ == "__main__":
    main()