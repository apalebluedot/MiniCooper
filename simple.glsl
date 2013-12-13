---VERTEX SHADER-------------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3  v_pos;
attribute vec3  v_normal;
attribute vec2  v_tc0;

uniform mat4 modelview_mat;
uniform mat4 projection_mat;
varying vec3 colors;
varying vec4 frag_color;
varying vec2 uv_vec;
varying vec4 normal_vec;
varying vec4 vertex_pos;


void main (void) {
    vec4 pos = modelview_mat * vec4(v_pos,1.0);
    vertex_pos = pos;
    normal_vec =vec4(v_normal,0.0);
    uv_vec=v_tc0;
    gl_Position = projection_mat * pos;
    uv_vec = v_tc0;
}


---FRAGMENT SHADER-----------------------------------------------------
#ifdef GL_ES
    precision highp float;
#endif

//varying vec4 frag_color;
varying vec2 uv_vec;
varying vec4 normal_vec;
varying vec4 vertex_pos;
varying vec3 colors;

uniform sampler2D tex;
uniform mat4 normal_mat;

void main (void){
    vec4 v_normal = normalize( normal_mat * normal_vec );
    vec4 v_light = normalize( vec4(0,0,0,1) - vertex_pos );
    vec4 color = texture2D(tex, uv_vec);
    //float theta = clamp(dot(v_normal, v_light), 0,0, 1.0);
    float theta = clamp(dot(v_normal, v_light), 0.0, 1.0);
    //vec4 color = vec4(1.0,1.0,1.0,1.0);
    vec4 light = vec4(theta,theta,theta,1.0);
    //if(colors[0]==0 && colors[1]==0 && colors[2]==0){
        gl_FragColor = light*color;
    /*}
    else{
        gl_FragColor=light*vec4(colors,1.0);
    //}*/
}