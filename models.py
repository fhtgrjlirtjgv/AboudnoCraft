from ursina import *
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor
import random
import os

block_textures = []
BASE_DIR = os.getcwd()
BLOCK_DIR = os.path.join(BASE_DIR, 'assets/blocks')

file_list = os.listdir(BLOCK_DIR)

for image in file_list:
    texture = load_texture('assets/blocks'+ os.sep + image)
    block_textures.append(texture)

class Tree(Entity):
    def __init__(self, pos, **kwargs):
        super().__init__(
            parent=scene,
            model='assets/minecraft_tree/scene.gltf',
            position=pos,
            scale=5,
            collider='box',
            origin_y=0.5,
            color=color.color(0,0, random.uniform(0.9, 1)),
            shader=basic_lighting_shader,
            **kwargs
        
        )


class Block(Entity):
    current = 0
    def __init__(self, block_type, pos, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            texture=block_textures[block_type],
            position=pos,
            scale=1,
            collider='box',
            origin_y=-0.5,
            color=color.color(0,0, random.uniform(0.9, 1)),
            shader=basic_lighting_shader,
            **kwargs
        
        )


class Map(Entity):
    def __init__(self, **kwargs):
        super().__init__(model=None, collider=None, **kwargs)
        self.bedrock = Entity(model='plane',collider='box', scale=300, texture='grass', texture_scale=(4,4), position=(0,-2,0))
        self.blocks = {}
        self.noise = PerlinNoise(octaves=2, seed=1488)

    def genetator(self):
        for x in range(50):
            for z in range(50):
                y = floor(self.noise([x/24, z/24])*6)
                block = Block(Block.current, (x,y,z))
                rand_num=random.randint(1,100)
                if rand_num ==40:
                    Tree((x,y+1,z))


class Player(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.speed = 20
        self.jump_height = 3
        self.hand_block = Entity(parent = camera.ui, model='cube', texture=block_textures[Block.current],scale =0.2, position=(0.6, -0.42),
                                 shader=basic_lighting_shader, rotation = Vec3(30,-30,10))

    def input(self, key):
        super().input(key)

        if key =='scroll up':
            Block.current += 1
            if Block.current >=len(block_textures):
                Block.current = 0
            self.hand_block.texture = block_textures[Block.current]

        if key =='scroll down':
            Block.current -= 1
            if Block.current <0:
                Block.current = len(block_textures) - 1
            self.hand_block.texture = block_textures[Block.current]



        if key == "left mouse down" and mouse.hovered_entity:
            destroy(mouse.hovered_entity)
        if key == "right mouse down" and mouse.hovered_entity:
            hit_info = raycast(camera.world_position, camera.forward,distance = 15 )
            if hit_info.hit:
                Block(Block.current, hit_info.entity.position + hit_info.normal)




    def update(self):
        super().update()
        if held_keys['control']:
            self.speed = 10
        else:
            self.speed = 5

        if held_keys["shift"]:
            self.speed = 3
            self.height = 1
        else:
            self.height = 2

