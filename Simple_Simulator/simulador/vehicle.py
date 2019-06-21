import numpy as np

# La clase representa al vehiculo simulado
# debera adaptarse para modelar el comportamiento fisico
# del vehiculo particular considerando inercias y en especial
# radios y velocidades de giro.
class Vehicle:

    _position = (0, 0)
    _phisical = None
    _orientation = 0 # rotacion

    def __init__(self,initial_position, phisical_properties):
        self._position = tuple(initial_position)
        self._phisical = phisical_properties


    # mueve el vehiculo basado en la desviacion indicada.
    # @param desviation : desviacion angular.
    #                        > 0 => girar a la izquierda
    #                        = 0 => no desviar
    #                        < 0 => girar a la derecha
    def move(self, desviation):
        self._orientation = self._orientation+desviation
        xi,yi= self._pol2cart(self._phisical.vel,np.radians(self._orientation))
        self._position = (self._position[0]+xi, self._position[1]+yi)

    def get_position(self):
        return self._position

    def _pol2cart(self,rho, phi):
        x = rho * np.cos(phi)
        y = rho * np.sin(phi)
        return (int(x), int(y))


# propiedades fisicas del vehiculo. tambien se puede extender
# de esta clase para mejorar el modelado
class VehicleProps:
    def __init__(self, width, long, vel=10, v_max=100, a_max=100):
        self.shape = (width,long)
        self.vel = vel
        self.v_max = v_max
        self.a_max = a_max

