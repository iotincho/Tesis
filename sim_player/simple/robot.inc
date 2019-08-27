

# definicion de los sensores, en este caso los sensores son ultrasonicos
define robot_sonar sensor
(
    # define the size of each transducer [xsize ysize zsize] in meters
    size [0.02 0.05 0.01 ]
    # define the range bounds [min max]
    range [0.15 3.0]
    # define the angular field of view in degrees
    fov 22.5
    # define the color that ranges are drawn in the gui
    color_rgba [ 1 0 0 1 ]
)

# creo los ranger que seran attachados al robot sensores y se indica donde estan ubicados sobre el
# las cordenadas de posicion son relativas al centro de rotacion defido en [origin]
define robot_sonars ranger
(

  # one line for each sonar [xpos ypos zpos heading]
  robot_sonar( pose [ 0 0 -0.5 -80])
  robot_sonar( pose [ 0 0 -0.5 -60])
  robot_sonar( pose [ 0 0 -0.5 -40])
  robot_sonar( pose [ 0 0 -0.5 -20])
  robot_sonar( pose [ 0 0 -0.5  0])
  robot_sonar( pose [ 0 0 -0.5  20])
  robot_sonar( pose [ 0 0 -0.5  40])
  robot_sonar( pose [ 0 0 -0.5  60])
  robot_sonar( pose [ 0 0 -0.5  80])


)


#defino los lasers
define robotLaser sensor
(
      size [0.025 0.025 0.025]
      range [0.1 10]            # max = dist between teeth in m
      fov 2                    # does not need to be big
      color_rgba [ 0.5 0 1 0.5]
      samples 180               # number of ranges measured
)
define robot_lasers ranger
(
      robotLaser( pose [ 0 0 0 0]) # left corner
#      robot_laser( pose [ 0.25 -0.5 0 -45]) # right corner
)



# definiconi del robot con su forma y algunos parametros fisicos
define robot_base position
(
      #define el tamaño del robot,
      #escala las dimensiones normalizadas[block]
      size [ 0.5 0.5 1]

      # define el centro de rotacion, por defecto utiliza
      #el centro geometrico basado en el paramentro anterior [size]
      origin [0 0 0 0]
#      gui_nose 1
#      ranger_return 0.5
      #define la forma con dimensiones normalizadas
      block
      (
            points 6
            point[0] [0.75 0]
            point[1] [1 0.25]
            point[2] [1 0.75]
            point[3] [0.75 1]
            point[4] [0 1]
            point[5] [0 0]
            z [0 1.0]
      )

      #forma de manejo del robot, 'diff' significa que gira por diferencia de velocidad en las ruedas
      drive "diff"

      #attach de sensores al modelo
      robot_sonars()

)

#define robot_with_sonar robot_base
#{
#  robot_sonars()
#}
