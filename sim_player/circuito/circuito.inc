define floorplan model
(
  # sombre, sensible, artistic
  color "gray30"

  # most maps will need a bounding box
  boundary 0

  gui_nose 1
  gui_grid 0
  gui_move 0
  gui_outline 0
  gripper_return 0
  fiducial_return 0
  ranger_return 1
)

floorplan
(
   bitmap "circuito.png"
   size [32 12 1]    
)