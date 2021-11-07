from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
import psd_tools
import os
window.title = "Testing Game"
window.exit_button_visible = True
window.fps_counter_enabled = True 
window.fullscreen = True
ftime = time.time()
def start():
  global info
  info = Text(text="A Game Made By Elston", size = 1400, x=-.24, enabled = False)
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
  if held_keys['left arrow']:
    spaceship.position -= (time.dt, 0, 0)
  if held_keys['up arrow']:
    if time.time()-before <= 1:
      return
    projectile = Entity(model="quad", scale = 0.1, y = -2.4, x = spaceship.x)
    projectile.collider = "box"
    projectiles.append(projectile)
    before = time.time()

def projectileUpdate():
  global projectiles
  toDelete = []
  count = 0
  for projectile in projectiles:
    projectile.position += (0, time.dt, 0)
    hitInfo = projectile.intersects()
    if hitInfo.hit:
      hitInfo.entities[0].disable()
      projectile.disable()
      toDelete.append(count)
    count += 1
  for i in reversed(toDelete):
    del projectiles[i]

    


startingcheck = True
secondcheck = False
lastcheck = False
endscreen = False
def update(): 
  global lastcheck, secondcheck, endscreen
  if startingcheck : starting()
  if secondcheck : lastcheck = checkonekey()
  if lastcheck and not endscreen:
    secondcheck = False
    main()

def clearaliens():
  global aliens
  for i in aliens:
    for alien in i:
      alien.disable()


def lose():
  clearaliens()
  text = Text("You lost!", scale = 6, y = 0.3, x = -0.3)
  text2 = Text("You did not kill the alien octopuses fast enough!", scale = 2, x = -0.5)

def win():
  global wintext
  print('won')
  scene.clear()
  wintext = Text("You've won!", scale = 6, y=0.4, x=-0.38)
  loadnext()

def loadnext():
  global level, lastcheck, secondcheck, endscreen, cleared, projectiles, lvlcomplete, nextlvl
  lvlcomplete = Text(f"Level {level} completed!", scale = 3, y = 0.2, x = -0.29)
  level += 1
  nextlvl = Text(f"Press any button to move on to level {level}", scale = 2, x = -0.4)
  lastcheck = False
  secondcheck = True
  endscreen = False
  cleared = 0
  projectiles = []
  time.sleep(1.5)




def checkwin():
  global endscreen
  if time.perf_counter()-sleveltime >= rtime:
    endscreen = True
    lose()
  elif not any([any(i) for i in [map(lambda x: x.enabled, i) for i in aliens]]):
    endscreen = True
    win()
    


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

def level1():
  global aliens, spaceship, sleveltime, rtime
  rtime = 60
  sleveltime = time.perf_counter()
  spaceship = Entity(model="quad", scale = 2, texture="spaceship.png")
  spaceship.position = (0, -3.3, 0)
  alienscale = 1.5
  basex = -4.5
  aliens = [[Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=3, collider = "box") for i in range(0, 12, 2)], [Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=0.9, collider = "box") for i in range(0, 12,2)]]

def level2():
  global aliens, spaceship, sleveltime, rtime
  rtime = 70
  sleveltime = time.perf_counter()
  spaceship = Entity(model="quad", scale = 2, texture = "spaceship.png")
  spaceship.position = (0, -3.3, 0)
  alienscale = 0.9
  basex = -4.5
  aliens = [[Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=3, collider = "box") for i in range(0, 12, 2)], [Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y=1.9, collider = "box") for i in range(0, 12,2)], [Entity(model="quad", scale = alienscale, texture = "squid.png", x=basex+i, y = 0.8, collider = "box") for i in range(0, 12, 2)]]


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
sceneclear = 0
def main():
  global cleared, sceneclear
  if not sceneclear:
    scene.clear()
    sceneclear += 1
  if not cleared:
    camera.position = (0, 0, -20)
    if level > 1:
      wintext.disable()
      nextlvl.disable()
      lvlcomplete.disable()
    exec(f"level{level}()")
    cleared = 1
  leftright(aliens)
  spaceshipmovement()
  projectileUpdate()
  checkwin()
  
level = 1
#cube = Entity(model='cube', color=color.red, scale=(5,5,5))
Text.default_resolution = 1080 * Text.size
cube = Entity(model='cube', color = color.red, scale = (5,5,5), texture = "brick")
app = Ursina()
s= Sky()
app.run()
