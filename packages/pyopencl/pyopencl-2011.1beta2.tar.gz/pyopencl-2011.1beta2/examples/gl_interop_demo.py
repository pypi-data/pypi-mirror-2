from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.raw.GL.VERSION.GL_1_5 import glBufferData as rawGlBufferData
from OpenGL import platform, GLX, WGL
import pyopencl as cl


n_vertices = 10000

src = """

__kernel void generate_sin(__global float2* a)
{
    int id = get_global_id(0);
    int n = get_global_size(0);
    float r = (float)id / (float)n;
    float x = r * 16.0f * 3.1415f;
    a[id].x = r * 2.0f - 1.0f;
    a[id].y = native_sin(x);
}

"""

def initialize():
    plats = cl.get_platforms()
    ctx_props = cl.context_properties

    props = [(ctx_props.PLATFORM, plats[0]), 
            (ctx_props.GL_CONTEXT_KHR, platform.GetCurrentContext())]

    import sys
    if sys.platform == "linux2":
        props.append(
                (ctx_props.GLX_DISPLAY_KHR, 
                    GLX.glXGetCurrentDisplay()))
    elif sys.platform == "win32":
        props.append(
                (ctx_props.WGL_HDC_KHR, 
                    WGL.wglGetCurrentDC()))
    ctx = cl.Context(properties=props)

    glClearColor(1, 1, 1, 1)
    glColor(0, 0, 1)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    rawGlBufferData(GL_ARRAY_BUFFER, n_vertices * 2 * 4, None, GL_STATIC_DRAW)
    glEnableClientState(GL_VERTEX_ARRAY)
    glVertexPointer(2, GL_FLOAT, 0, None)
    coords_dev = cl.GLBuffer(ctx, cl.mem_flags.READ_WRITE, int(vbo))
    prog = cl.Program(ctx, src).build()
    queue = cl.CommandQueue(ctx)
    cl.enqueue_acquire_gl_objects(queue, [coords_dev])
    prog.generate_sin(queue, (n_vertices,), None, coords_dev)
    cl.enqueue_release_gl_objects(queue, [coords_dev])
    queue.finish()
    glFlush()

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glDrawArrays(GL_LINE_STRIP, 0, n_vertices)
    glFlush()

def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

if __name__ == '__main__':
    import sys
    glutInit(sys.argv)
    if len(sys.argv) > 1:
        n_vertices = int(sys.argv[1])
    glutInitWindowSize(800, 160)
    glutInitWindowPosition(0, 0)
    glutCreateWindow('OpenCL/OpenGL Interop Tutorial: Sin Generator')
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    initialize()
    glutMainLoop()
