---VERTEX SHADER---
// A3 vertex shader
// Transform position into clip coordinates
#ifdef GL_ES
    precision highp float;
#endif

// TODO: Define any uniforms you need here
/*uniform float theta;
uniform float scale;*/

in vec3 normal;
uniform mat4 modelview_mat;
uniform mat4 projection_mat

//uniform bool reset;
// For A3, the only vertex attribute you need is the position. If you added
// any more, they go here
attribute vec3 v_pos;
attribute vec2 v_uv;
attribute vec4 v_uv

out vec2 fragTexcoord;

// For A3, the only out varying we need is the gl_Position. We could generate
// the color here if desired. Out variables go here if any.

void main(void)
{
    // TODO: Transform your point here. You may specify color here or in the 
    // fragment shader
	mat4 identity = mat4(
		vec4(1.0, 0.0, 0.0, 0.0),
		vec4(0.0, 1.0, 0.0, 0.0),
		vec4(0.0, 0.0, 1.0, 0),
		vec4(0.0, 0.0, 0.0, 1.0));

	mat4 viewMat=transpose(mat4(
		vec4(1,0,0,-300),
		vec4(0,1,0,-300),
		vec4(0,0,1,-300),
		vec4(0,0,0,1)));
	mat4 viewMatx=mat4(
		vec4(1, 0, 0, 0),
		vec4(0, cos(45), -sin(45), 0),
		vec4(0, sin(45), cos(45), 0),
		vec4(0, 0, -400, 1));
	
	/*gl_Position=perspective * viewMatx* matrix* vec4(position, 1.0);
	fragTexcoord=texcoord;*/

	vec4 pos = modelview_mat * vec4(v_pos,1.0);
	gl_Position=projection_mat * pos;
	frag_color=vec4(1,1,1,1);
	uv_vec=v_uv;


}

---FRAGMENT SHADER---
// A3 fragment shader
// Not much to do here other than set the color
#ifdef GL_ES
    precision highp float;
#endif


// Any uniforms you have go here
//uniform fragColor2
varying vec4 frag_color;
varying vec2 uv_vec;

uniform sampler2D tex;

// Interpolated inputs. Only if you created some in your vertex program
uniform vec3 Color;
in vec2 fragTexcoord;
// The output. Always a color
out vec4 frag_color;

void main() 
{  
    /*// Output the assigned color
    if(Color[0]==0 && Color[1]==0 && Color[2]==0){
      fragColor=texture(carTexture, fragTexcoord);  
    }
    else{
      fragColor=vec4(Color,1.0);
    }*/
    vec4 color = texture2D(tex, uv_vec)*frag_color;
    gl_FragColor=color;
}
