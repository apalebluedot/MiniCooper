from __future__ import absolute_import
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.shader import *
from kivy.graphics.opengl import *
from kivy.graphics import *
from math import pi




class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        self._tpath = resource_find('mini-diffuse.png')
        self.canvas.shader.source = resource_find('simple.glsl')

        super(Renderer, self).__init__(**kwargs)
        with self.canvas:
            PushMatrix()
            self.setup_scene()
            PopMatrix()
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def update_glsl(self, *largs):
        proj = Matrix().view_clip(0, self.width, 0, self.height, 1, 100, 0)
        self.canvas['projection_mat'] = proj

    def setup_scene(self):
        PushMatrix()

        indices = [0, 1, 2, 3, 0, 2]
        vertex_format = [
            ('v_pos', 3, 'float'),  # <--- These are GLSL shader variable names.
            ('v_color', 4, 'float'),
            ('v_uv', 2, 'float'),
        ]
        vertices = [
          10.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0,
          10.0, 200.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 1.0,
          200.0, 200.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
          200.0, 10.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0,
        ]

        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=vertices,
            indices=indices,
            fmt=vertex_format,
            mode='triangles',
        )
        self.mesh.texture = Image(self._tpath).texture
        PopMatrix()


class RendererApp(App):
    def build(self):
        return Renderer()


def main():
  RendererApp().run()