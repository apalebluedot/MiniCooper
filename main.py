from __future__ import division
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kiv.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.clock import Clock
import mini_geometry

class MainFrame(Widget):
	def __init__(self, *larg, **kw):
		self.canvas=RenderContext(compute_normal_mat=False)
		super(MainFrame, self).__init__(*larg, **kw)
		with self.canvas:
			self.cb=Callback(self.setup_gl_context)
			PushMatrix()
			self.setup_scene()
			self.cb=Callback(self.reset_gl_context)
		self.mini=mini_geometry.Mini_geometry()
		Clock.schedule_interval(self.step, 1 / 30.)

	def setup_gl_context(self, *args):
		glEnable(GL_DEPTH_TEST)

	def reset_gl_context(self, *args):
		glDisable(GL_DEPTH_TEST)

	def update_glsl(self, *largs):
		asp=self.width/float(self.height)
		proj=Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
		self.canvas['projection_mat']=proj
		self.canvas['diff_light']=(1.0, 1.0, 0.8)
		self.canvas['amb_light']=(0.1, 0.1, 0.1)

	def setup_scene(self):
		Color(1,1,1,1)
		PushMatrix()
		Translate(0,0,-3)
		self.rot=Rotate(1,0,1,0)
		m=self.scene.objects.values()[0]
		UpdateNormalMatrix()
		self.mesh=(
			vertices=self.mini.vertexdata,
			indices=self.mini.indices,
			fmt=m.vertex_format,
			mode='triangles',
		)
		PopMatrix()

class MiniApp(App):
	def build(self):
		root=MainFrame()
		return root

if __name__='main':
		MiniApp().run()

