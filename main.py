from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.core.image import Image as Image
import mini_geometry


colormap = {
    "Body":(0.05, 0.05, 0.54),
    "Body Chrome":(0.95, 0.96, 0.93),
    "Roof":(0.85, 0.85, 0.85),
    "Headlights":(0.95, 0.96, 0.93),
    "Mirrors":(0.85, 0.85, 0.85),
    "Brakelights":(0.54, 0.22, 0.22),
    "Undercarriage":(0.2, 0.2, 0.2),
    "Antenna":(0.2, 0.2, 0.2),
    "Driver Blinker":(0.9, 0.5, 0.1),
    "Passenger Blinker":(0.9, 0.5, 0.1),
    "Exhaust":(0.95, 0.96, 0.93),
    "Upper Driver Wiper":(0.2, 0.2, 0.2),
    "Upper Passenger Wiper":(0.2, 0.2, 0.2),
    "Lower Driver Wiper":(0.2, 0.2, 0.2),
    "Lower Passenger Wiper":(0.2, 0.2, 0.2),
    "Rear Wiper":(0.2, 0.2, 0.2),
    "Vents":(0.1, 0.1, 0.1),
    "License":(0.94, 0.64, 0.19),
    "Front Driver Rim":(0.75, 0.75, 0.75),
    "Front Passenger Rim":(0.75, 0.75, 0.75),
    "Rear Driver Rim":(0.75, 0.75, 0.75),
    "Rear Passenger Rim":(0.75, 0.75, 0.75),
    "Front Driver Tire":(0.1, 0.1, 0.1),
    "Front Passenger Tire":(0.1, 0.1, 0.1),
    "Rear Driver Tire":(0.1, 0.1, 0.1),
    "Rear Passenger Tire":(0.1, 0.1, 0.1),
    "Brakes":(0.75, 0.75, 0.75),
    "Rear View Mirror":(0.8, 0.8, 0.8),
    "Interior":(0.4, 0.4, 0.0),
    "Driver":(0.9, 0.9, 0.9),
    "Chair":(0.55, 0.27, 0.075),
    "Windows":(0.5, 0.5, 0.5),
}
nocolor={"nope":(0,0,0)}

'''EXAMPLES BORROWED FROM KIVY 3DRENDERING 
    https://github.com/kivy/kivy/blob/master/examples/3Drendering/main.py
'''
class Renderer(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('simple.glsl')
        self.scene =  mini_geometry.MiniGeometry()
        self._tloc=resource_find('mini-diffuse.png')
        self.texture=Image("mini-diffuse.png").texture
        with self.canvas:
            glEnable(GL_DEPTH_TEST)
            BindTexture(texture=self.texture, index=1)
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        self.canvas['tex']=1
        super(Renderer, self).__init__(**kwargs)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)


    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)


    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(0, self.width, 0, self.height, 1, 900, 0)
        self.canvas['projection_mat']=proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
        self.rot.angle += 1

    def setup_scene(self):
        PushMatrix()
        Translate(300, 340, -30)
        self.rot = Rotate(1, 1, 1, 0)

        vertex_format=[
            ('v_pos', 3, 'float'),
            ('v_normal', 3, 'float'),
            ('v_tc0', 2, 'float')
        ]

        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=self.scene.vertexdata.tolist(),
            indices=self.scene.indices.tolist(),
            fmt=vertex_format,
            mode='triangles',
        )
        colored=["Front Passenger Tire","Front Driver Tire", "Rear Driver Tire", "Rear Passenger Tire", "Windows", "Vents", "License", "Front Driver Rim", "Front Passenger Rim", "Rear Passenger Rim", "Rear Driver Rim", "Rear Wiper"]
        for part in self.scene.parts:
            start,end=self.scene.group(part)
            count=self.scene.indicesPerFace*(end-start)
            if part in colored:
                self.canvas['colors']=colormap[part]
            else:
                self.canvas['colors']=nocolor["nope"]

        PopMatrix()

    
class RendererApp(App):
    def build(self):
        return Renderer()

if __name__ == "__main__":
    RendererApp().run()
