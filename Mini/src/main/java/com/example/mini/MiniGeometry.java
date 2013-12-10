package com.example.mini;
/*Geometry for the Mini Cooper model.

The Cooper model is formed of various groups. Each group has a name (the
"part") that determines which part it belongs to. For example, the "Roof" part
possesses geometry that belongs to the roof of the car. To get the
starting and ending indices of the faces belonging to the part, use the group
function; this can be used to render only that face:
    mini = MiniGeometry()
    <load vertex buffer and index buffer from mini.vertexdata & mini.indices>
    for part in mini.parts:   
        start, end = mini.group(part)
        offset = sizeof(GLushort) * mini.indicesPerFace * start
        count = mini.indicesPerFace * (end - start)
        glDrawElements(GL_TRIANGLES, count, GL_UNSIGNED_SHORT, offset)
        
*/

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;

import android.text.*;

public class MiniGeometry{
    //A class that loads and stores the Mini geometry.
    public static int _numVertices;
    public static int _numFaces;
    public static ArrayList _data;
    public MiniGeometry(){
        this(false);
    }

    public MiniGeometry(boolean adjacency){
        /*****************************************************************
         Read in geometry
         Format:
         numVertices
         vx vy vz nx ny nz tu tv
         ...
         numFaces
         vertexIndex0 vertexIndex1 ... vertexIndexN (3 or 6 if adjacency)
         ...
         numGroups
         faceStart faceEnd name
         *******************************************************************/
        String fileName;
        if (adjacency){
            fileName = new String("Assets/mini_geometry.txt");
        }
        else{
            fileName = new String("Assets/mini_geometry_adjacency.txt");
        }
        try{
            BufferedReader file = new BufferedReader( new FileReader(fileName));
            try{
              _numVertices = Integer.parseInt(file.readLine());
            } catch(IOException e){
                System.out.println("End of file");
            }
            try{

            }

        }catch (FileNotFoundException e){
            System.out.println("Bad File loc");
        }





    }
}