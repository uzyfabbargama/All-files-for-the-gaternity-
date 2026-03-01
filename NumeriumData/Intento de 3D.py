from ursina import *

app = Ursina()

cube = Entity(model='cube',
color = color.azure, scale=2)
app.run()