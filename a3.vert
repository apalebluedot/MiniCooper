// A3 vertex shader
// Transform position into clip coordinates
#version 150

// TODO: Define any uniforms you need here
/*uniform float theta;
uniform float scale;*/

in vec3 normal;
uniform mat4 matrix;
uniform mat4 perspective;

//uniform bool reset;
// For A3, the only vertex attribute you need is the position. If you added
// any more, they go here
in vec3 position;
in vec2 texcoord;

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
	
	gl_Position=perspective * viewMatx* matrix* vec4(position, 1.0);
	fragTexcoord=texcoord;


}
