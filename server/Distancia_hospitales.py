import pandas as pd
from math import sin,cos,sqrt,asin,pi

class Distancia_hospitales:

    def __init__(self, data, lat_p, long_p):
        # Recuperamos solo los datos que nos interesan
        self.data = data
        # Cogemos solo los hospitales y 
        # Guardamos la ubicación del paciente
        self.lat_p = lat_p
        self.long_p = long_p

        # Constantes necesarias para el cálculo de la función distancia_puntos
        self.r = 6371000 #radio terrestre medio, en metros
        self.c = pi/180 #constante para transformar grados en radianes
   

    # Función que recibe dos puntos (lat,long) y devuelve la distancia entre ambos
    # con la fórmula de Haversine.
    # _p hace referencia a la persona
    # _h hace referencia al Hospital
    def distancia_puntos(self, lat_h, long_h):
        d = 2*self.r*asin(sqrt(sin(self.c*(lat_h-self.lat_p)/2)**2 + \
        cos(self.c*self.lat_p)*cos(self.c*lat_h)*sin(self.c*(long_h-self.long_p)/2)**2))
        return d


    def calculo_distancias(self):
        # Lista para guardar las distancias de todos los hospitales
        lista_dist = []
        for i in range(self.data.shape[0]):
            lat_h = self.data.iloc[i]['LATITUD']
            long_h = self.data.iloc[i]['LONGITUD']
            d = self.distancia_puntos(self.lat_p, self.long_p, lat_h, long_h)
            lista_dist.append(d)
        return lista_dist



    def dict_cercanos(self, cant):
        lista_distancias = self.calculo_distancias(self.lat_p,self.long_p)
        self.data['DISTANCIA'] = lista_distancias
        self.data.sort_values(by='DISTANCIA',inplace=True)
        self.data['DISTANCIA'] = self.data['DISTANCIA'].apply(lambda x: x/1000)
        df_fin = self.data.iloc[0:cant]
        return df_fin.to_dict()
