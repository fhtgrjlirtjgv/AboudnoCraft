from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from models import *

app = Ursina()

sky = Sky()

map = Map()
map.genetator()


player = FirstPersonController()
app.run()