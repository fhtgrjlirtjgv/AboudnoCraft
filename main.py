from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

sky = Sky()
ground = Entity(model='plane',collider='box', scale=300, texture='grass', texture_scale=(4,4), position=(0,-2,0))
player = FirstPersonController()


block = Entity(model='cube', texture='grass', position=(2,5,0), scale=0.5)

app.run()