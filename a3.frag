// A3 fragment shader
// Not much to do here other than set the color
#version 150
#ifdef GL_ES
    precision highp float;
#endif


// Any uniforms you have go here
//uniform fragColor2
uniform vec3 car;
uniform sampler2D carTexture;

// Interpolated inputs. Only if you created some in your vertex program
uniform vec3 Color;
in vec2 fragTexcoord;
// The output. Always a color
out vec4 fragColor;

void main() 
{  
    // Output the assigned color
    if(Color[0]==0 && Color[1]==0 && Color[2]==0){
      fragColor=texture(carTexture, fragTexcoord);  
    }
    else{
      fragColor=vec4(Color,1.0);
    }
}