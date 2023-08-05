from pyprocessing import *
import math
import OpenGL.GL as gl

def cubelist ():
    "Creates a cube vertex list"
    v = []
    for x in -1,1: 
        for y in -1,1:
            for z in -1,1:
                v+=[(x,y,z)]
    p,n = [],[] 
    for f in [(0,1,3,2),(5,4,6,7),(5,1,0,4),(2,3,7,6),(2,6,4,0),(1,5,7,3)]:
        for fv in f: p+=v[fv]
    for fn in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
        n += fn*4
    return pyglet.graphics.vertex_list(24,('v3f', p),('n3f', n))
    
def spherelist (nslices,nstacks):
    """Creates an indexed vertex list to display a sphere of radius 
    1 with (nstacks+1)*(nslices+1) points"""
    
    def vpos(islice,istack):
        """Returns the vertex position for the given stack/slice"""
        a = math.pi*2*islice/nslices
        costheta,sintheta = math.cos(a),math.sin(a)
        b = math.pi*istack/nstacks
        cosphi,sinphi = math.cos(b),math.sin(b)
        return (sinphi*costheta,cosphi,sinphi*sintheta)
    
    def vindex(islice,istack):
        """Returns the index for the vertex at the given stack/slice"""
        return islice*(nstacks+1)+istack
        
    # First build a matrix of vertices (and normals)
    vtx = []
    for islice in range(nslices+1): 
        for istack in range(nstacks+1):
            assert (vindex(islice,istack)==len(vtx)/3)
            vtx.extend(vpos(islice,istack))
            
    # Then build indices to a big quadstrip running up and down slices
    idx = []
    for islice in range (nslices):
        # handle separately odd and even slices
        if islice%2==0: 
            for istack in range (nstacks+1): 
                idx.append(vindex(islice,istack))
                idx.append(vindex(islice+1,istack))
        else:
            for istack in range(nstacks,-1,-1):
                idx.append(vindex(islice+1,istack))
                idx.append(vindex(islice,istack))
    # Return an indexed vertex list
    return pyglet.graphics.vertex_list_indexed(len(vtx)/3,idx,('v3f',vtx),('n3f',vtx))
                
def setup():
    size(200,200)
    global vlist,slist
    vlist = cubelist()
    slist = spherelist(20,10)
    
def draw(): 
    # clear the whole screen
    background(200)
    lights()
    noStroke()
    background(200)
    pushMatrix()
    fill(255,255,0)
    translate(130,130)
    rotate(PI/10,1,1,0)
    scale(50)
    vlist.draw(pyglet.gl.GL_QUADS)
    #slist.draw(pyglet.gl.GL_QUAD_STRIP)
    #box(50)
    popMatrix()
    fill(255,0,255)
    translate(60, 50)
    vlist.draw(pyglet.gl.GL_QUADS)
    
    
run()
