from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import psd_tools
import os
print(os.getcwd())
window.title = "Testing Game"
window.exit_button_visible = True
window.fps_counter_enabled = True 
window.fullscreen = True
ftime = time.time()
def start():
  print('debug')
  global info
  info = Text(text="A Game Made By Elston", size = 1400, x=-.23, enabled = False)
  info.scale = 2
  info.appear(speed=0.25, delay=1)

def checkonekey():
  for i in held_keys:
    if held_keys[i]:
      return True 

projectiles = []
before = 0
def spaceshipmovement():
  global projectiles, before
  if held_keys['right arrow']:
    spaceship.position += (time.dt, 0, 0)
  elif held_keys['left arrow']:
    spaceship.position -= (time.dt, 0, 0)
  elif held_keys['up arrow']:
    if time.time()-before <= 0.8:
      return
    projectile = Entity(model="quad", scale = 0.1, y = -2.4, x = spaceship.x)
    projectile.collider = "box"
    projectiles.append(projectile)
    before = time.time()

def projectileUpdate():
  global projectiles
  count = 0
  for projectile in projectiles:
    projectile.position += (0, time.dt, 0)
    hitInfo = projectile.intersects()
    if hitInfo.hit:
      hitInfo.entities[0].disable()
      projectile.disable()
      del projectiles[count]
    count += 1
    

def debug(obj):
  if held_keys['right arrow']:
    for i in obj:
      for j in i:
        j.position += (time.dt*5, 0, 0)
    print(obj[1][5].position)
  elif held_keys['left arrow']:
    for i in obj:
      for j in i:
        j.position -= (time.dt*5, 0, 0)
    print(obj[0][0].position)

startingcheck = True
secondcheck = False
lastcheck = False
def update(): 
  global lastcheck, secondcheck
  if startingcheck : starting()
  if secondcheck : lastcheck = checkonekey()
  if lastcheck:
    secondcheck = False
    main()



_ = True
check = True 
def starting():
  global ftime, info, _, check, startingcheck, secondcheck
  if _:
    start()
    _ = False
  cube.rotation_y += time.dt*10
  cube.rotation_x += time.dt*10
  stime = time.time()
  if stime-ftime >= 9 and stime-ftime<27: 
    camera.position -= (0, time.dt, 0)
    info.position += (0, time.dt*0.098)
  elif stime-ftime >= 27 and check:
    text2 = Text(text="Galaxy Intruders", scale = 6, enabled = False, position = (-0.55, 0.5, 0))
    text2.appear(speed=0.25, delay = 0.5)
    text3 = Text(text = "A Knockoff Space Invaders Game", scale = 2, enabled = False, position = (-0.35, -0.19, 0), scale_override = 1)
    text3.appear(speed=0.3, delay = 1)
    text3.enable()
    squid = Entity(model='quad', scale = 3, texture='squid.png')
    squid.position = (0, -18.3, 0)
    check = False
  elif stime-ftime >= 33:
    startText = Text(text="Press Any Button To Play!", scale = 4, enabled=False, position = (-0.55, -0.3, 0))
    startText.appear(speed=0.2, delay = 0)
    startingcheck = False
    secondcheck = True

def mainsetup():
  global aliens, spaceship
  spaceship = Entity(model="quad", scale = 2, texture="spaceship.png")
  spaceship.position = (0, -3.3, 0)
  alienscale = 1.5
  basex = -4.5
  aliens = [[Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=3, collider = "box") for i in range(0, 12, 2)], [Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=0.9, collider = "box") for i in range(0, 12,2)]]


neg = False
def leftright(arrAliens):
  global neg
  """
  The left and right movement for the aliens
  """
  if neg:
    dx = -time.dt
  else:
    dx = time.dt
  if arrAliens[0][5].x >= 6.4:
    neg = True
  elif arrAliens[0][0].x <= -6.5:
    neg = False
  for arr in arrAliens:
    for alien in arr:
      alien.position += (dx, 0, 0)


cleared = 0
def main():
  global cleared
  if not cleared:
    scene.clear()
    camera.position = (0, 0, -20)
    mainsetup()
    cleared = 1
  leftright(aliens)
  spaceshipmovement()
  projectileUpdate()
  

#cube = Entity(model='cube', color=color.red, scale=(5,5,5))
Text.default_resolution = 1080 * Text.size
cube = Entity(model='cube', color = color.red, scale = (5,5,5), texture = "brick")
app = Ursina()
s= Sky()
app.run()
