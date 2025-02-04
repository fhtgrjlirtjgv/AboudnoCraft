from ursina import *

app = Ursina()

from models import *

sky = Sky()

map = Map()
map.genetator()


player = Player()

window.fullscreen = True
app.run()
