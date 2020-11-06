"""
    This example shows adds 3d object to the scene by loading
    it from file and moving/scaling it to be aligned correctly.
    In this case the object is a .stl file of the mouse skull,
    but it could be anything, including experimental and recording devices.

    Note that the mouse skull and brain meshes come from different sources
    so that's why they don't match perfectly.
"""


import brainrender
from vedo import Cylinder
import pandas as pd
import numpy as np

brainrender.SHADER_STYLE = "cartoon"
brainrender.ROOT_ALPHA = 0.5
brainrender.WHOLE_SCREEN = False
brainrender.SHOW_AXES = False
brainrender.DISPLAY_INSET = False

from brainrender.scene import Scene

def add_skull(scene):

    # Load skull from file
    skull = scene.add_from_file("Examples/example_files/skull.stl")
    skull.c("ivory").alpha(0.5)

    # Align skull and brain (scene.root)
    skull_com = skull.centerOfMass()
    root_com = scene.root.centerOfMass()

    skull.origin(skull.centerOfMass())
    skull.rotateY(90).rotateX(180)
    skull.x(root_com[0] - skull_com[0])
    skull.y(root_com[1] - skull_com[1])
    skull.z(root_com[2] - skull_com[2])
    skull.x(3500)
    skull.rotateZ(-25)
    skull.y(7800)
    skull.scale([1300, 1500, 1200])

    # Cut skull actor to show brain inside
    scene.cut_actors_with_plane("sagittal", actors=skull)

    # Improve looks
    scene.add_silhouette(scene.root, lw=3)
    scene.add_silhouette(skull, lw=3)

def add_probe(scene, xrot, zrot, convergence_point):

    # Load shank model from file
    probe = scene.add_from_file("Examples/example_files/probe_shank.stl")
    probe.c("black").alpha(1.0)

    probe_com = probe.centerOfMass()

    # Scale and rotate to default location
    probe.scale(40)
    probe.rotateX(-90)

    # Add custom rotations
    probe.rotateX(xrot)
    probe.rotateZ(zrot)

    # Add custom translation
    probe.x(convergence_point[0])
    probe.y(convergence_point[1])
    probe.z(convergence_point[2])

    return probe.bounds()



def add_odd_arc(zrot, xrotations = (32, 16, 0)):

    """ Adds an "odd" arc of probes (5 probes across one arc)

    # Required global variables:
        scene - brainrender.scene
        convergence point - list of x, y, z points
        probe_bounds - list of object boundaries

    Inputs:
    =======
    zrot - int or float
        defines the rotation of the arc
        -48 = most anterior
        +48 = most posterior

    xrotations - (optional) list or tuple of ints or floats
        defines the rotation of the slot
        +32 = most lateral (right hemisphere)
        -32 = most lateral (left hemisphere)

    Outputs:
    ========

    Appends the boundaries of each probe to the 'probe_bounds' list

    """

    for xrot in xrotations:
        probe_bounds.append(add_probe(scene, xrot, zrot, convergence_point))

def add_even_arc(zrot, xrotations = (40, 24, 8)):

    """ Adds an "even" arc of probes (6 probes across one arc)

    # Required global variables:
        scene - brainrender.scene
        convergence point - list of x, y, z points
        probe_bounds - list of object boundaries

    Inputs:
    =======
    zrot - int or float
        defines the rotation of the arc
        -48 = most anterior
        +48 = most posterior

    xrotations - (optional) list or tuple of ints or floats
        defines the rotation of the slot
        +32 = most lateral (right hemisphere)
        -32 = most lateral (left hemisphere)

    Outputs:
    ========

    Appends the boundaries of each probe to the 'probe_bounds' list
    """

    for xrot in xrotations:
        probe_bounds.append(add_probe(scene, xrot, zrot, convergence_point))

def get_structures_for_probe(bounds, npoints=10):

    """
    Prints out the structures along a given probe trajectory

    Inputs:
    =======
    bounds - list of 6 values
        min/max bounds for x, y, and z axes

    npoints - (optional) int
        number of points along each probe trajectory

    """

    structures = []

    xpts = np.linspace(bounds[0], bounds[1], npoints)
    ypts = np.linspace(bounds[2], bounds[3], npoints)
    zpts = np.linspace(bounds[4], bounds[5], npoints)

    for i in range(len(xpts)):
        try:
            structures.append(scene.atlas.structure_from_coords(
                coords = [xpts[i],
                         ypts[i],
                         zpts[i]],
                microns=True,
                as_acronym=True))
        except KeyError:
            pass
        except IndexError:
            pass

    print(structures)


scene = Scene()

add_skull(scene)

probe_bounds = []


#####################################################

# MODIFY THIS SECTION

scene.add_brain_regions(["P","MRN"], alpha=0.4) # select brain regions to highlight

convergence_point = [12000, 7000, 5700] # for pons

add_odd_arc(-48)

#convergence_point = [6500, 8500, 5700] # default central location

#add_even_arc(-32)

#add_odd_arc(-16)

#add_even_arc(0)

#add_odd_arc(16)

#add_even_arc(32)

#add_odd_arc(48)

######################################################


[get_structures_for_probe(bounds) for bounds in probe_bounds]

scene.render()
