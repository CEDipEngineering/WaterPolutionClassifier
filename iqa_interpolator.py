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
        self.indicatorFunctions['Coliformes Termotolerantes'] = lambda x: np.interp(x, self.indicators['Coliformes Termotolerantes'][0], self.indicators['Coliformes Termotolerantes'][1]) if x <= 1e5 else 3 
        self.indicatorFunctions['pH'] = self.handlerPH
        self.indicatorFunctions['DBO (5, 20)'] = lambda x: np.interp(x, self.indicators['DBO (5, 20)'][0], self.indicators['DBO (5, 20)'][1]) if x <= 30 else 2
        self.indicatorFunctions['Nitrogênio-Nitrato'] = lambda x: np.interp(x, self.indicators['Nitrogênio-Nitrato'][0], self.indicators['Nitrogênio-Nitrato'][1]) if x <= 100 else 1
        self.indicatorFunctions['Fósforo Total'] = lambda x: np.interp(x, self.indicators['Fósforo Total'][0], self.indicators['Fósforo Total'][1]) if x <= 10 else 1
        self.indicatorFunctions['Temperatura da Água'] = self.handlerTemp
        self.indicatorFunctions['Turbidez'] = lambda x: np.interp(x, self.indicators['Turbidez'][0], self.indicators['Turbidez'][1]) if x <= 100 else 5
        self.indicatorFunctions['Sólido Dissolvido Total'] = lambda x: np.interp(x, self.indicators['Sólido Dissolvido Total'][0], self.indicators['Sólido Dissolvido Total'][1]) if x <= 500 else 32
        self.indicatorFunctions['Oxigênio Dissolvido'] = lambda x: np.interp(x, self.indicators['Oxigênio Dissolvido'][0], self.indicators['Oxigênio Dissolvido'][1]) if x <= 140 else 47
        self.indicatorList = list(self.indicators.keys())
        self.indicatorWeights = {a:b for a,b in zip(self.indicatorList, [0.15, 0.12, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.17])}
       
    def handlerPH(self, value):
        if value<2:
            return 2
        elif value>12:
            return 3
        return np.interp(value, self.indicators['pH'][0], self.indicators['pH'][1])

    def handlerTemp(self, value):
        if value<-5:
            return self.handlerTemp(-5)
        elif value>15:
            return 9
        return np.interp(value, self.indicators['Temperatura da Água'][0], self.indicators['Temperatura da Água'][1])

    def IQA_Result(self, valuesDict: dict):
        keys = valuesDict.keys()
        result = 1
        for key in keys:
            if key in self.indicatorList:
                result*= self.indicatorFunctions[key](valuesDict[key])**self.indicatorWeights[key]
        return result


def main():
    Interpolator = IQA_Interpolator()
    print(Interpolator.IQA_Result({'Coliformes Termotolerantes': 14000.0, 'pH': 6.2, 'DBO (5, 20)': 4.0, 'Temperatura da Água': 25.0, 'Turbidez': 40.0, 'Nitrogênio-Nitrato': 0.16, 'Fósforo Total': 0.155, 'Sólido Dissolvido Total': 142.0, 'Oxigênio Dissolvido': 1.2}))
    print(Interpolator.indicatorWeights)
if __name__ == "__main__":
    main()