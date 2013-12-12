
---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec3  v_normal;
attribute vec2  v_uv;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;

varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec2 fragTexcoord;



void main (void) {
    //compute vertex position in eye_space and normalize normal vector
	
    vec4 pos = modelview_mat * vec4(v_pos,1.0);
    vertex_pos=pos;
    normal_vec=vec4(v_normal,0.0);
    gl_Position = projection_mat * pos;
    fragTexcoord=v_uv;
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec2 fragTexcoord;

uniform mat4 normal_mat;
uniform sampler2D texture1;

void main (void){

    vec4 v_normal = normalize( normal_mat * normal_vec ) ;
    vec4 v_light = normalize( vec4(0,0,0,1) - vertex_pos );
    float theta = clamp(dot(v_normal, v_light), 0.0, 1.0);
    gl_FragColor = texture2D(texture1,fragTexcoord);//*vec4(theta,theta,theta,1.0);
    //gl_FragColor=vec4(0.5,0.5,0.5,0.5)
}
