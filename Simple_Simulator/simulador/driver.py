
from .environment import Environment
from .vehicle import Vehicle
from abc import  ABC, abstractmethod

class Driver(ABC):
    # esta clase toma las deciciones en cuanto al
    # control del vehiculo sobre el entorno.
    # contiene los algoritmos de obstacle avoidance
    # y debe ser adaptada para cada algoritmo que se
    # desee simular
    _target=(0,0)
    _environment = None
    _vehicle = None

    def __init__(self,image_map,vehicle,target):
        self._environment = Environment(image_map)
        self._vehicle = vehicle
        self._target = tuple(target)

    # da un paso en la simulacion
    def step(self):
        position = self._vehicle.get_position()
        env = self._environment.get_perception(position)
        direction = self._drive_to(env)
        self._vehicle.move(direction)

    # funcion a implementar para que el algoritmo decida
    # hacia donde avanzar
    # @param lidar_env : es un diccionario {angulo:distancia}
    #                    tal como lo obtendria un mapeo con lidar
    # @retun angulo de desviacion en GRADOS
    @abstractmethod
    def _drive_to(self, lidar_env):
        pass
    # @return una imagen de opencv (np.array((x,y,3),np.uint8)
    #         del entorno de simulacion para poder visualizarla
    #         y graficar lo necesario encima
    def get_env(self):
        return self._environment



