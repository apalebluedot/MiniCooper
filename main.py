from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
import mini_geometry


class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        self.scene = mini_geometry.MiniGeometry()
        super(Renderer, self).__init__(**kwargs)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
        self.rot.angle += 1

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -3)
        self.rot = Rotate(1, 0, 1, 0)
        vertex_format=[
            ('v_pos', 3, 'float'),  # <--- These are GLSL shader variable names.
            ('v_normal', 3, 'float'),
            ('v_uv', 2, 'float'),
        ]
        UpdateNormalMatrix()
        #vertices=[]
        #for i in range(self.scene._numVertices):
        	#vertices.append(self._mini.vertexdata[8*i])
        	#vertices.append(self._mini.vertexdata[8*i+1])
        	#vertices.append(self._mini.vertexdata8*i+2])
        #	vertices.append(self.scene.vertexdata[8*i:8*i+3])
        

        self.mesh = Mesh(
            vertices=self.scene.vertexdata.tolist(),
            indices=self.scene.indices.tolist(),
            fmt=vertex_format,
            mode='triangles',
        )
        PopMatrix()


class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
