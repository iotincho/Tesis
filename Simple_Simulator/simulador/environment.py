import cv2
import numpy as np

# Esta clase mantiene el entorno de simulacion donde se mueve el rover.
# levanta un mapa 2D con obstaculos desde una imagen
class Environment:
    _POINTS=[]
    _ENV_SIZE = (0,0)
    def __init__(self,map_image):
        self.load_map(map_image)

    # carga la imagen, extrae el contorno de los obstaculos binarizando
    # y extrae los puntos de interes para un procesamiento mas agil
    def load_map(self,map_image):
        gray_map = cv2.cv2.imread(map_image, cv2.IMREAD_GRAYSCALE)
        blur_map = cv2.blur(gray_map, (5, 5))
        _, binarized_map = cv2.threshold(blur_map, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(image=binarized_map, mode=cv2.RETR_LIST, method=cv2.CHAIN_APPROX_NONE)
        self._POINTS = self._get_all_points(contours)
        self._ENV_SIZE = binarized_map.shape

    # convierte todos los contornos en una lista de puntos
    def _get_all_points(self,contours):
        pts = []
        for a in contours:
            for c in a:
                for p in c:
                    pts.append(np.array(p))
        return pts

    # funcion de redondeo hacia un valor particular
    # xq no existe un metodo asi en python
    def _myround(self,x, base=1):
        return base * round(x / base)


    # devielve un diccionario {angulo:distancia}
    # observando el entorno desde 'point'.
    # graficamente se ve como los puntos obtenidos por un lidar360
    # @param point : coordenada (x,y) en el mapa,
    #                actualmente las coordenadas estan como coordenadas de imagen
    # @param angulo : resolucion angular de cada zona. actualmente solo puede ser entero
    # @param radio  : alcance maximo de percepcion
    def get_perception(self,point, angulo=1, radio=10000):
        point = np.array(point)
        space = {0:radio}
        for i in range(-180,181,angulo):
            space[i] = radio
        for p in self._POINTS:
            x = p[0] - point[0]
            y = p[1] - point[1]
            tita = self._myround(180 * np.arctan2(y, x) / np.pi, angulo)
            space[tita] = min(space[tita], np.sqrt(x**2 + y**2))
        return space

    # devuelve una imagen del entorno base para testeo
    def get_env_mat(self):
        mat = np.zeros((self._ENV_SIZE[0],self._ENV_SIZE[1], 3), dtype=np.uint8)
        for p in self._POINTS:
            cv2.circle(mat,tuple(p),2,(0,0,200),-1)
        return mat

