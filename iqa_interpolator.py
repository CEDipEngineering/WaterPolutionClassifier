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
        self.indicators['Nitrogênio Total'] = pd.read_csv('csv_iqa/NITROGENIOCSV.csv', delimiter=';', decimal=',', header=None)
        self.indicators['Fósforo Total'] = pd.read_csv('csv_iqa/fosforo.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Temperatura'] = pd.read_csv('csv_iqa/temperatura.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Turbidez'] = pd.read_csv('csv_iqa/turbidez.csv', delimiter=',', decimal='.', header=None)
        self.indicators['Sólido Dissolvido Total'] = pd.read_csv('csv_iqa/residuo.csv', delimiter=',', decimal='.', header=None)
        self.indicators['pctO2'] = pd.read_csv('csv_iqa/o2dissolvido.csv', delimiter=',', decimal='.', header=None)
        self.indicatorFunctions = {}
        self.indicatorFunctions['Coliformes Termotolerantes'] = lambda x: np.interp(x, self.indicators['Coliformes Termotolerantes'][0], self.indicators['Coliformes Termotolerantes'][1]) if x <= 1e5 else 3 
        self.indicatorFunctions['pH'] = self.handlerPH
        self.indicatorFunctions['DBO (5, 20)'] = lambda x: np.interp(x, self.indicators['DBO (5, 20)'][0], self.indicators['DBO (5, 20)'][1]) if x <= 30 else 2
        self.indicatorFunctions['Nitrogênio Total'] = lambda x: np.interp(x, self.indicators['Nitrogênio Total'][0], self.indicators['Nitrogênio Total'][1]) if x <= 100 else 1
        self.indicatorFunctions['Fósforo Total'] = lambda x: np.interp(x, self.indicators['Fósforo Total'][0], self.indicators['Fósforo Total'][1]) if x <= 10 else 1
        self.indicatorFunctions['Temperatura'] = self.handlerTemp
        self.indicatorFunctions['Turbidez'] = lambda x: np.interp(x, self.indicators['Turbidez'][0], self.indicators['Turbidez'][1]) if x <= 100 else 5
        self.indicatorFunctions['Sólido Dissolvido Total'] = lambda x: np.interp(x, self.indicators['Sólido Dissolvido Total'][0], self.indicators['Sólido Dissolvido Total'][1]) if x <= 500 else 32
        self.indicatorFunctions['pctO2'] = lambda x: np.interp(x, self.indicators['pctO2'][0], self.indicators['pctO2'][1]) if x <= 140 else 47
        self.indicatorList = list(self.indicators.keys())
        self.indicatorWeights = {a:b for a,b in zip(self.indicatorList, [0.15, 0.12, 0.1, 0.1, 0.1, 0.1, 0.08, 0.08, 0.17])}
        self.tempToPercent = [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                              [14.6, 14.2, 13.8, 13.5, 13.1, 12.8, 12.5, 12.2, 11.9, 11.6, 11.3, 11.1, 10.9, 10.6, 10.4, 10.2, 10.0, 9.8, 9.6, 9.4, 9.2, 9.0, 8.9, 8.7, 8.6, 8.4, 8.2, 8.1, 7.9, 7.8, 7.7]]
       
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
        return np.interp(value, self.indicators['Temperatura'][0], self.indicators['Temperatura'][1])

    def IQA_Result(self, valuesDict: dict):
        keys = valuesDict.keys()
        result = 1
        for key in keys:
            if key in self.indicatorList:
                result*= self.indicatorFunctions[key](valuesDict[key])**self.indicatorWeights[key]
        return result

    def getMaxSolubility(self, temp):
        return np.interp(temp, self.tempToPercent[0], self.tempToPercent[1])

def main():
    Interpolator = IQA_Interpolator()
    # print(Interpolator.IQA_Result({'Coliformes Termotolerantes': 14000.0, 'pH': 6.2, 'DBO (5, 20)': 4.0, 'Temperatura': 25.0, 'Turbidez': 40.0, 'Nitrogênio Total': 0.16, 'Fósforo Total': 0.155, 'Sólido Dissolvido Total': 142.0, 'Oxigênio Dissolvido': 1.2}))
    # print(Interpolator.indicatorWeights)
if __name__ == "__main__":
    main()