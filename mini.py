#!/usr/bin/env pythonw
# Transform assignment
# Name:
# NetID:
from __future__ import division

import platform
from ctypes import * 

import pyglet

# Required for my darwin patch

import numpy
from math import cos, sin 
import sys
import Image
import kivy.graphics.opengl
import mini_geometry

##################################################################
# Map of part names to colors

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
##################################################################
# pyglet window
def loadTexture(filename, texUnit):
        # Activate the texture unit (starting at 0); need 1 per texture
        glActiveTexture(GL_TEXTURE0 + texUnit)
        texture = GLuint()
        glGenTextures(1, byref(texture))
        glBindTexture(GL_TEXTURE_2D, texture)
        
        # Texture does not wrap
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        # How is the image sampled?
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        
        # Load the image using PIL
        image = Image.open(filename)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.size[0], image.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, image.tostring("raw", "RGBX", 0, -1))

    
class Window(pyglet.window.Window):
    def __init__(self):
        # Create an OpenGL 3.2 context; initialize with that
        '''config = pyglet.gl.Config(double_buffer = True, 
                                  depth_size = 24, 
                                  major_version=3, 
                                  minor_version=2, 
                                  forward_compatible = True)

        super(Window, self).__init__(caption ="Gfx Assignment 3",
                                     width = 600, height = 600, 
                                     resizable = True,
                                     config = config)'''
        # The mini model
        self._mini = mini_geometry.MiniGeometry()
        # TODO: Define any other member variables you need here
        # Initialize GL state: Enable depth testing
        #glClearColor(1, 1, 1, 1)
        #glEnable(GL_DEPTH_TEST)
        self.theta=180
        self.near=200
        self.far=600
        self.left=-300
        self.right=300
        self.top=300
        self.bottom=-300
        self.transMat=numpy.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]])
        self.identity=numpy.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1]])
        self.translate=numpy.matrix([
        [1,0,0,0],
        [0,1,0,35],
        [0,0,1,0],
        [0,0,0,1]])
        self.flipTrans=numpy.matrix([
        [1,0,0,0],
        [0,1,0,-35],
        [0,0,1,0],
        [0,0,0,1]])
        self.perspective=numpy.matrix([[2*self.near/(self.right-self.left), 0, -(self.right+self.left)/(self.right-self.left), 0],
                                    [0, (2*self.near)/(self.top-self.bottom), -(self.top+self.bottom)/(self.top-self.bottom), 0],
                                    [0, 0, -(self.far+self.near)/(self.far-self.near), -(2*self.far*self.near)/(self.far-self.near)],
                                    [0, 0, -1.0, 0]])
        self.rotMatx=numpy.matrix([[1, 0, 0, 0],
            [0, cos(180), -sin(180), 0],
            [0, sin(180), cos(180), 0],
            [0, 0, 0, 1]
            ])
        self.skewMat=numpy.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,540,0,1]])
        theta=self.theta
        print self.perspective
        print self.translate
        print self.flipTrans
        print self.transMat

        self.rotMatz=numpy.matrix([[cos(theta), -sin(theta), 0, 1],
            [sin(theta), cos(theta), 0, 1],
            [0, 0, 1, 1],
            [0, 0, 0, 1]])

        # Initialize OpenGL data 
        loadTexture("mini-diffuse.png", 0)        
        self.createBuffers()
        self.createShaders()
        

    ##################################################################
    # Buffer management
    
    def createBuffers(self):
        # TODO: Create, load, and bind your vertex & index buffers. Also
        # setup any vertex attributes. Note that the geometry stores 8
        # values per vertex (position x,y,z; normal x,y,z; texcoord u,v)
        # as floats in that order. You only need vertices for this assignment.
        # Your positions must be stored in vertex attribute 0.
        self.arrayID=GLuint()
        self.bufferID=GLuint()

        indices=(GLshort*len(self._mini.indices))(*self._mini.indices)
        data=(GLfloat*len(self._mini.vertexdata))(*self._mini.vertexdata)

        glGenVertexArrays(3, byref(self.arrayID))
        glBindVertexArray(self.arrayID)

        glGenBuffers(1, byref(self.bufferID))
        glBindBuffer(GL_ARRAY_BUFFER, self.bufferID)
        sVertex=sizeof(GLfloat) * len(self._mini.vertexdata)
        glBufferData(GL_ARRAY_BUFFER, sVertex, data, GL_STATIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), 0)
        #glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), 3*sizeof(GLfloat))
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 8*sizeof(GLfloat), 6*sizeof(GLfloat))

        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glEnableVertexAttribArray(2)

        self.indexBufferID=GLuint()
        sIndex=sizeof(GLshort)*len(self._mini.vertexdata)
        glGenBuffers(1, byref(self.indexBufferID))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.indexBufferID)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, sIndex, indices, GL_STATIC_DRAW)

    def destroyBuffers(self):
        # TODO: Clean up your vertex & index buffers
        glDisableVertexAttribArray(0)
        glDisableVertexAttribArray(1)
        glDisableVertexAttribArray(2)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glDeleteBuffers(2, byref(self.bufferID))
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER,0)
        glDeleteBuffers(1,self.indexBufferID)
        glBindVertexArray(0)
        glDeleteVertexArrays(3, byref(self.arrayID))
    ##################################################################
    # Shader management
    def projectionMatrix(self):
        projectionMatrix=numpy.array([[2*self.near/(self.right-self.left), 0, -(self.right+self.left)/(self.right-self.left), 0],
                                    [0, (2*self.near)/(self.top-self.bottom), -(self.top+self.bottom)/(self.top-self.bottom), 0],
                                    [0, 0, -(self.far+self.near)/(self.far-self.near), -(2*self.far*self.near)/(self.far-self.near)],
                                    [0, 0, -1, 0]])
        return projectionMatrix
    def rotMatx(self):
        rotMatx=numpy.array([[1, 0, 0, 1],
            [0, cos(180), -sin(180), 1],
            [0, sin(180), cos(180), 1],
            [0, 0, 0, 1]
            ])
        return rotMatx

    def rotMatz(self):
        theta=self.theta
        rotMatz=numpy.array([[cos(theta), -sin(theta), 0, 1],
            [sin(theta), cos(theta), 0, 1],
            [0, 0, 1, 1],
            [0, 0, 0, 1]])
        return rotMatz

    
    def createShaders(self):
        # Create, load, and compile the vertex shader.
        # Requires an ugly ctypes cast, unfortunately 
        with open('a3.vert') as vertexFile:
            vertexShader = vertexFile.read()
        self.vertexShaderID = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.vertexShaderID, 1, 
                       cast(pointer(c_char_p(vertexShader)),
                            POINTER(POINTER(c_char))),
                       None)
        glCompileShader(self.vertexShaderID)
        
        # Print an error log
        length = GLsizei()
        log = (c_char_p)(" " * 1023)
        glGetShaderInfoLog(self.vertexShaderID, 1023, byref(length), log)
        print "Vertex Log:", log.value
        
        # Create, load, and compile the fragment shader
        # Requires an ugly ctypes cast, unfortunately 
        with open('a3.frag') as fragFile:
            fragShader = fragFile.read()
        self.fragShaderID = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.fragShaderID, 1, 
                       cast(pointer(c_char_p(fragShader)), 
                            POINTER(POINTER(c_char))),
                       None)
        glCompileShader(self.fragShaderID)
        
        # Print an error log
        length = GLsizei()
        log = (c_char_p)(" " * 1023)
        glGetShaderInfoLog(self.fragShaderID, 1023, byref(length), log)
        print "Frag Log:", log.value
        
        # Create the final program
        self.programID = glCreateProgram()
        glAttachShader(self.programID, self.vertexShaderID)
        glAttachShader(self.programID, self.fragShaderID)
        
        # Associate the vertex shader with the vertex attributes:
        #   Attrib array 0 stores the vertices
        glBindAttribLocation(self.programID, 0, "position")
        glBindAttribLocation(self.programID, 1, "texcoord")
        
        # Link and enable the program
        glLinkProgram(self.programID)
        glUseProgram(self.programID)
        
        texUnit=glGetUniformLocation(self.programID, "carTexture")
        glUniform1i(texUnit, 0)
        # TODO: Get and set the uniform variable values as needed
        # Store their locations as member variables for later

        transformed=(GLfloat* 16)(*self.transMat.flat)
        newperspective=(GLfloat* 16)(*self.perspective.flat)
        matrixLoc=glGetUniformLocation(self.programID, "matrix")
        perspectiveloc=glGetUniformLocation(self.programID, "perspective")
        glUniformMatrix4fv(matrixLoc, 1, GL_TRUE, transformed)
        glUniformMatrix4fv(perspectiveloc, 1, GL_TRUE, newperspective)
        self.colloc=glGetUniformLocation(self.programID, "car")
        
    def destroyShaders(self):
        # Disable the current program
        glUseProgram(0)
     
        # Detach the shaders
        glDetachShader(self.programID, self.vertexShaderID)
        glDetachShader(self.programID, self.fragShaderID)
        
        # Destroy the shaders
        glDeleteShader(self.vertexShaderID)
        glDeleteShader(self.fragShaderID)
        
        # Destroy the program
        glDeleteProgram(self.programID)
    ##################################################################
    # Window events
    
    # Window closed
    def on_close(self):
        self.destroyShaders()
        self.destroyBuffers()
        super(Window, self).on_close()
    
    # Window resized
    def on_resize(self, width, height):
        # Update the viewport and associated shader variable
        self.left=-(width/2)
        self.right=width/2
        self.top=height/2
        self.bottom=-(height/2)
        glViewport(0, 0, width, height)
        
        # TODO: Update any projection matrix/info you need
        
        
        # Always redraw
        self.on_draw()
        pass

    # Draw the window
    def on_draw(self):
        # Handles glClear calls
        self.clear()
        colored=["Front Passenger Tire","Front Driver Tire", "Rear Driver Tire", "Rear Passenger Tire", "Windows", "Vents", "License", "Front Driver Rim", "Front Passenger Rim", "Rear Passenger Rim", "Rear Driver Rim", "Rear Wiper"]

        for part in self._mini.parts:   
            start, end = self._mini.group(part)
            offset = sizeof(GLushort) * self._mini.indicesPerFace * start
            count = self._mini.indicesPerFace * (end - start)
            if(part in colored):
                self.colloc=glGetUniformLocation(self.programID, "Color")
                glUniform3f(self.colloc, *colormap[part])
            else:
                self.colloc=glGetUniformLocation(self.programID, "Color")
                glUniform3f(self.colloc, *nocolor["nope"])
            glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_SHORT, offset)
        

        
    def on_key_release(self, keycode, modifiers):
 
        if keycode == key.RIGHT:
            self.theta+=0.5
            self.transMat=self.transMat* self.rotMatz
            print self.transMat
            
        elif keycode == key.LEFT:
            self.theta-=0.5
            self.transMat=self.transMat* self.rotMatz
  
        elif keycode == key.H:
            self.transMat=self.identity
        elif keycode == key.DOWN:
            self.transMat=self.transMat* self.translate
        elif keycode == key.UP:
            self.transMat=self.transMat* self.flipTrans
        elif keycode == key.S:
            self.transMat=self.transMat * self.skewMat
        matrixLoc=glGetUniformLocation(self.programID, "matrix")
        mat=(GLfloat*16)(*self.transMat.flat)
        glUniformMatrix4fv(matrixLoc, 1, GL_TRUE, mat)
        # Always redraw after keypress
        self.on_draw()
# Run the actual application
#if __name__ == "__main__":
#    window = Window()
#    pyglet.app.run()