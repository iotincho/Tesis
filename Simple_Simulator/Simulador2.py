from simulador.driver import Driver
from simulador.vehicle import *
import cv2


class MyDriver(Driver):
    def _drive_to(self, lidar_env):
        return -10


if __name__ == '__main__':
    vehicle_props = VehicleProps(width=15,
                                 long=20,
                                 vel=10)
    vehicle = Vehicle(tuple([50, 50]), vehicle_props)
    driver = MyDriver(image_map='image2.jpg',
                      vehicle=vehicle,
                      target=(400, 400))

    mat = driver.get_env().get_env_mat()

    while True:
        cv2.circle(img=mat, center=vehicle.get_position(), radius=5, color=(0,255,0))
        cv2.imshow('map', mat)
        driver.step()
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

