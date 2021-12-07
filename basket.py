import bpy
import math
from mathutils import Matrix

# -----------------------------------------------------------------------------
# Settings

name = 'Basket'

# Origin point transformation settings
mesh_offset = (0, 0, 0)
origin_offset = (0, 0, 0)

# Matrices settings
translation = (0, 0, 0)
scale_factor = 1
scale_axis = (1, 1, 1)
rotation_angle = math.radians(0)
rotation_axis = 'X'


# -----------------------------------------------------------------------------
# Utility Functions

def vert(x, y, z):
    """ Make a vertex """

    return (x + origin_offset[0], y + origin_offset[1], z + origin_offset[2])


# -----------------------------------------------------------------------------
# Basket Code

basket_x = 1
basket_y = 1
basket_z = 0.6
basket_scale = 1.0
wall_thickness_factor = 0.25
wall_thickness = wall_thickness_factor*basket_scale

verts = [vert(basket_x*basket_scale, basket_y*basket_scale, basket_z*-basket_scale),  # cube
         vert(basket_x*basket_scale, basket_y*- \
              basket_scale, basket_z*-basket_scale),
         vert(basket_x*-basket_scale, basket_y*- \
              basket_scale, basket_z*-basket_scale),
         vert(basket_x*-basket_scale, basket_y * \
              basket_scale, basket_z*-basket_scale),
         vert(basket_x*basket_scale, basket_y*basket_scale, basket_scale),
         vert(basket_x*basket_scale, basket_y*-basket_scale, basket_scale),
         vert(basket_x*-basket_scale, basket_y*-basket_scale, basket_scale),
         vert(basket_x*-basket_scale, basket_y*basket_scale, basket_scale),
         vert((basket_x*basket_scale)-wall_thickness, (basket_y*basket_scale) - \
              wall_thickness, (basket_z*-basket_scale)+wall_thickness),  # bottom square
         vert((basket_x*-basket_scale)+wall_thickness, (basket_y*basket_scale) - \
              wall_thickness, (basket_z*-basket_scale)+wall_thickness),
         vert((basket_x*-basket_scale)+wall_thickness, (basket_y*-basket_scale) + \
              wall_thickness, (basket_z*-basket_scale)+wall_thickness),
         vert((basket_x*basket_scale)-wall_thickness, (basket_y*-basket_scale) + \
              wall_thickness, (basket_z*-basket_scale)+wall_thickness),
         vert((basket_x*basket_scale)-wall_thickness, (basket_y * \
              basket_scale)-wall_thickness, basket_scale),  # top square
         vert((basket_x*-basket_scale)+wall_thickness,
              (basket_y*basket_scale)-wall_thickness, basket_scale),
         vert((basket_x*-basket_scale)+wall_thickness,
              (basket_y*-basket_scale)+wall_thickness, basket_scale),
         vert((basket_x*basket_scale)-wall_thickness, (basket_y*-basket_scale)+wall_thickness, basket_scale)]


faces = [(0, 1, 2, 3),  # bottom
         #         (4, 7, 6, 5), #top
         (4, 7, 13, 12),  # top insets
         (13, 7, 6, 14),
         (15, 14, 6, 5),
         (4, 12, 15, 5),
         (8, 9, 10, 11),  # bottom inner square
         (8, 9, 13, 12),  # inner sides
         (9, 10, 14, 13),
         (11, 10, 14, 15),
         (11, 8, 12, 15),
         (0, 4, 5, 1),  # outer sides
         (1, 5, 6, 2),
         (2, 6, 7, 3),
         (4, 0, 3, 7)]


# -----------------------------------------------------------------------------
# Add Object to Scene

mesh = bpy.data.meshes.new(name)
mesh.from_pydata(verts, [], faces)

obj = bpy.data.objects.new(name, mesh)
bpy.context.scene.collection.objects.link(obj)

bpy.context.view_layer.objects.active = obj
obj.select_set(True)

# -----------------------------------------------------------------------------
# Offset mesh to move origin point

obj.location = [(i * -1) + mesh_offset[j] for j, i in enumerate(origin_offset)]


# -----------------------------------------------------------------------------
# Matrix Magic

#translation_matrix = Matrix.Translation(translation)
#scale_matrix = Matrix.Scale(scale_factor, 4, scale_axis)
#rotation_mat = Matrix.Rotation(rotation_angle, 4, rotation_axis)

#obj.matrix_world @= translation_matrix @ rotation_mat @ scale_matrix


# -----------------------------------------------------------------------------
# Matrix Magic (in the mesh)

# Uncomment this to change the mesh
## obj.data.transform(translation_matrix @ scale_matrix)
