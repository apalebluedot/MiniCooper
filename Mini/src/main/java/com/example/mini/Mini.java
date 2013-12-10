/*
 * Copyright (C) 2011 The Android Open Source Project
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.example.mini;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.FloatBuffer;
import java.util.ArrayList;
import java.util.HashMap;

import android.opengl.GLES20;

/**
 * A two-dimensional triangle for use as a drawn object in OpenGL ES 2.0.
 */
public class Mini {
    /*HashMap<String, ArrayList<Double>> colormap = new HashMap<String, ArrayList<Item>>();*/

    /*public synchronized void addToList(String mapKey, Item myItem) {
        List<Item> itemsList = items.get(mapKey);

        // if list does not exist create it
        if(itemsList == null) {
            itemsList = new ArrayList<Item>();
            itemsList.add(myItem);
            items.put(mapKey, itemsList);
        } else {
            // add if item is not already in list
            if(!itemsList.contains(myItem)) itemsList.add(myItem);
        }
    }*/

    /*colormap.addToList("Body",(0.05, 0.05, 0.54));
    colormap.addToList("Body Chrome",(0.95, 0.96, 0.93));
    colormap.addToList("Roof",(0.85, 0.85, 0.85));
    colormap.addToList("Headlights",(0.95, 0.96, 0.93));
    colormap.addToList("Mirrors",(0.85, 0.85, 0.85));
    colormap.addToList("Brakelights",(0.54, 0.22, 0.22));
    colormap.addToList("Undercarriage",(0.2, 0.2, 0.2));
    colormap.addToList("Antenna",(0.2, 0.2, 0.2));
    colormap.addToList("Driver Blinker",(0.9, 0.5, 0.1));
    colormap.addToList("Passenger Blinker",(0.9, 0.5, 0.1));
    colormap.addToList("Exhaust",(0.95, 0.96, 0.93));
    colormap.addToList("Upper Driver Wiper",(0.2, 0.2, 0.2));
    colormap.addToList("Upper Passenger Wiper",(0.2, 0.2, 0.2));
    colormap.addToList("Lower Driver Wiper",(0.2, 0.2, 0.2));
    colormap.addToList("Lower Passenger Wiper",(0.2, 0.2, 0.2));
    colormap.addToList("Rear Wiper",(0.2, 0.2, 0.2));
    colormap.addToList("Vents",(0.1, 0.1, 0.1));
    colormap.addToList("License",(0.94, 0.64, 0.19));
    colormap.addToList("Front Driver Rim",(0.75, 0.75, 0.75));
    colormap.addToList("Front Passenger Rim",(0.75, 0.75, 0.75));
    colormap.addToList("Rear Driver Rim",(0.75, 0.75, 0.75));
    colormap.addToList("Rear Passenger Rim",(0.75, 0.75, 0.75));
    colormap.addToList("Front Driver Tire",(0.1, 0.1, 0.1));
    colormap.addToList("Front Passenger Tire",(0.1, 0.1, 0.1));
    colormap.addToList("Rear Driver Tire",(0.1, 0.1, 0.1));
    colormap.addToList("Rear Passenger Tire",(0.1, 0.1, 0.1));
    colormap.addToList("Brakes",(0.75, 0.75, 0.75));
    colormap.addToList("Rear View Mirror",(0.8, 0.8, 0.8));
    colormap.addToList("Interior",(0.4, 0.4, 0.0));
    colormap.addToList("Driver",(0.9, 0.9, 0.9));
    colormap.addToList("Chair",(0.55, 0.27, 0.075));
    colormap.addToList("Windows",(0.5, 0.5, 0.5));
    */
    private final String vertexShaderCode =
            // This matrix member variable provides a hook to manipulate
            // the coordinates of the objects that use this vertex shader
            "in vec3 normal;" +
                    "uniform mat4 matrix;" +
                    "uniform mat4 perspective;" +
                    "in vec3 position;"+
                    "in vec2 texcoord;"+
                    "out vec2 fragTexcoord;"+
                    "void main() {" +
                    "mat4 identity = mat4(\n" +
                    "\t\tvec4(1.0, 0.0, 0.0, 0.0),\n" +
                    "\t\tvec4(0.0, 1.0, 0.0, 0.0),\n" +
                    "\t\tvec4(0.0, 0.0, 1.0, 0),\n" +
                    "\t\tvec4(0.0, 0.0, 0.0, 1.0));\n" +
                    "\n" +
                    "\tmat4 viewMat=transpose(mat4(\n" +
                    "\t\tvec4(1,0,0,-300),\n" +
                    "\t\tvec4(0,1,0,-300),\n" +
                    "\t\tvec4(0,0,1,-300),\n" +
                    "\t\tvec4(0,0,0,1)));\n" +
                    "\tmat4 viewMatx=mat4(\n" +
                    "\t\tvec4(1, 0, 0, 0),\n" +
                    "\t\tvec4(0, cos(45), -sin(45), 0),\n" +
                    "\t\tvec4(0, sin(45), cos(45), 0),\n" +
                    "\t\tvec4(0, 0, -400, 1));\n" +
                    "\t\n" +
                    "\tgl_Position=perspective * viewMatx* matrix* vec4(position, 1.0);\n" +
                    "\tfragTexcoord=texcoord;"+
                    "}";

    private final String fragmentShaderCode =
                    "// A3 fragment shader\n" +
                            "// Not much to do here other than set the color\n" +
                            "#version 150\n" +
                            "\n" +
                            "// Any uniforms you have go here\n" +
                            "//uniform fragColor2\n" +
                            "uniform vec3 car;\n" +
                            "uniform sampler2D carTexture;\n" +
                            "\n" +
                            "// Interpolated inputs. Only if you created some in your vertex program\n" +
                            "uniform vec3 Color;\n" +
                            "in vec2 fragTexcoord;\n" +
                            "// The output. Always a color\n" +
                            "out vec4 fragColor;\n" +
                            "\n" +
                            "void main() \n" +
                            "{  \n" +
                            "    // Output the assigned color\n" +
                            "    if(Color[0]==0 && Color[1]==0 && Color[2]==0){\n" +
                            "      fragColor=texture(carTexture, fragTexcoord);  \n" +
                            "    }\n" +
                            "    else{\n" +
                            "      fragColor=vec4(Color,1.0);\n" +
                            "    }\n" +
                            "}";

    private final FloatBuffer vertexBuffer;
    private final int mProgram;
    private int mPositionHandle;
    private int mColorHandle;
    private int mMVPMatrixHandle;

    // number of coordinates per vertex in this array
    static final int COORDS_PER_VERTEX = 3;
    static float triangleCoords[] = {
            // in counterclockwise order:
            0.0f,  0.622008459f, 0.0f,   // top
            -0.5f, -0.311004243f, 0.0f,   // bottom left
            0.5f, -0.311004243f, 0.0f    // bottom right
    };
    private final int vertexCount = triangleCoords.length / COORDS_PER_VERTEX;
    private final int vertexStride = COORDS_PER_VERTEX * 4; // 4 bytes per vertex

    float color[] = { 0.63671875f, 0.76953125f, 0.22265625f, 0.0f };

    /**
     * Sets up the drawing object data for use in an OpenGL ES context.
     */
    public Mini() {
        // initialize vertex byte buffer for shape coordinates
        ByteBuffer bb = ByteBuffer.allocateDirect(
                // (number of coordinate values * 4 bytes per float)
                triangleCoords.length * 4);
        // use the device hardware's native byte order
        bb.order(ByteOrder.nativeOrder());

        // create a floating point buffer from the ByteBuffer
        vertexBuffer = bb.asFloatBuffer();
        // add the coordinates to the FloatBuffer
        vertexBuffer.put(triangleCoords);
        // set the buffer to read the first coordinate
        vertexBuffer.position(0);

        // prepare shaders and OpenGL program
        int vertexShader = MyGLRenderer.loadShader(
                GLES20.GL_VERTEX_SHADER, vertexShaderCode);
        int fragmentShader = MyGLRenderer.loadShader(
                GLES20.GL_FRAGMENT_SHADER, fragmentShaderCode);

        mProgram = GLES20.glCreateProgram();             // create empty OpenGL Program
        GLES20.glAttachShader(mProgram, vertexShader);   // add the vertex shader to program
        GLES20.glAttachShader(mProgram, fragmentShader); // add the fragment shader to program
        GLES20.glLinkProgram(mProgram);                  // create OpenGL program executables

    }

    public void createBuffers(){

    }

    /**
     * Encapsulates the OpenGL ES instructions for drawing this shape.
     *
     * @param mvpMatrix - The Model View Project matrix in which to draw
     * this shape.
     */
    public void draw(float[] mvpMatrix) {
        // Add program to OpenGL environment
        GLES20.glUseProgram(mProgram);

        // get handle to vertex shader's vPosition member
        mPositionHandle = GLES20.glGetAttribLocation(mProgram, "vPosition");

        // Enable a handle to the triangle vertices
        GLES20.glEnableVertexAttribArray(mPositionHandle);

        // Prepare the triangle coordinate data
        GLES20.glVertexAttribPointer(
                mPositionHandle, COORDS_PER_VERTEX,
                GLES20.GL_FLOAT, false,
                vertexStride, vertexBuffer);

        // get handle to fragment shader's vColor member
        mColorHandle = GLES20.glGetUniformLocation(mProgram, "vColor");

        // Set color for drawing the triangle
        GLES20.glUniform4fv(mColorHandle, 1, color, 0);

        // get handle to shape's transformation matrix
        mMVPMatrixHandle = GLES20.glGetUniformLocation(mProgram, "uMVPMatrix");
        MyGLRenderer.checkGlError("glGetUniformLocation");

        // Apply the projection and view transformation
        GLES20.glUniformMatrix4fv(mMVPMatrixHandle, 1, false, mvpMatrix, 0);
        MyGLRenderer.checkGlError("glUniformMatrix4fv");

        // Draw the triangle
        GLES20.glDrawArrays(GLES20.GL_TRIANGLES, 0, vertexCount);

        // Disable vertex array
        GLES20.glDisableVertexAttribArray(mPositionHandle);
    }
    public void loadTexture(String filename, int texUnit){

        GLES20.glActiveTexture(GLES20.GL_TEXTURE0 + texUnit);
    }

}
