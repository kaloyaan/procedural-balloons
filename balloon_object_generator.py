import bmesh
import math
import bpy
import random
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty
)
from mathutils import Vector
bl_info = {
    "name": "Ballon Object",
    "description": "Creates a Balloon",
    "author": "Debuk",
    "version": (1, 2, 0),
    'license': 'GPL v3',
    "blender": (2, 80, 0),
    "support": "COMMUNITY",
    "category": "Object"
}

# Origin point transformation settings
mesh_offset = (0, 0, 0)
origin_offset = (0, 0, 0)


def generate_Balloon(radialScale, height, ringFaces, heightFaces, distance):

    verts = []
    edges = []
    faces = []

    heightFElements = heightFaces
    radialFElements = ringFaces

    for j in range(heightFElements+1):
        for i in range(radialFElements):
            u = (2 * math.pi) * (i / (radialFElements))
            v = (math.pi) * (j / (heightFElements))
            x = ((radialScale * 0.92) + 0.2 * v) * \
                math.cos(u) * math.sin(v) * height * 0.5
            y = ((radialScale * 0.92) + 0.2 * v) * \
                math.sin(u) * math.sin(v) * height * 0.5
            z = - (height * 0.6 * math.cos(v)) + distance
            verts.append(Vector((x, y, z)))
    for j in range(heightFElements):
        for i in range(radialFElements):
            a = i % radialFElements
            b = (i + 1) % radialFElements
            r1 = radialFElements*j
            r2 = radialFElements*(j+1)
            faces.append([r1 + a, r2 + a, r2 + b, r1 + b])
    return verts, edges, faces


def vert(x, y, z):
    """ Make a vertex """

    return (x + origin_offset[0], y + origin_offset[1], z + origin_offset[2])


def generate_Basket(basket_x, basket_y, basket_z, basket_scale, wall_thickness_factor):
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
    return verts, faces


class Add_Balloon_Menu(bpy.types.Menu):
    bl_label = "Essentials"
    bl_idname = "OBJECT_MT_Add_Balloon_Menu"

    def draw(self, context):
        layout = self.layout

        layout.operator("mesh.add_balloon")


class Add_Balloon(bpy.types.Operator):
    """Create Balloon"""
    bl_idname = "mesh.add_balloon"
    bl_label = "Balloon"
    bl_options = {'UNDO', 'REGISTER'}

    ringFaces: IntProperty(
        name="RingFaces",
        description="RingFaces of the Balloon",
        default=14,
        min=4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    heightFaces: IntProperty(
        name="HeightFaces ",
        description="HeightFaces of the Balloon",
        default=150,
        min=4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    height: FloatProperty(
        name="Height ",
        description="Height of the Balloon",
        default=1.0,
        min=0.01,
        soft_min=0.01,
        step=1
    )

    radialScale: FloatProperty(
        name="RadialScale",
        description="RadialScale of the Balloon",
        default=0.7,
        min=0.01,
        soft_min=0.01,
        step=1
    )

    distance: FloatProperty(
        name="Distance",
        description="Distance between basket and balloon",
        default=0.7,
        min=0.2,
        soft_min=0.01,
        step=0.5
    )

    shadeSmooth: BoolProperty(
        name="Shade Smooth",
        description="",
        default=False,
    )

    optimizePoles: BoolProperty(
        name="Optimize Poles",
        description="",
        default=True,
    )

    basket_x: FloatProperty(
        name="Basket Width",
        description="Width of the basket",
        default=1.0,
        min=0.01,
        soft_min=0.01,
        soft_max=30.0,
        step=1
    )

    basket_y: FloatProperty(
        name="Basket Length",
        description="Length of the basket",
        default=1.0,
        min=0.01,
        soft_min=0.01,
        soft_max=30.0,
        step=1
    )

    basket_scale: FloatProperty(
        name="Basket Scale",
        description="Scale of the basket",
        default=0.09,
        min=0.01,
        soft_min=0.01,
        soft_max=1.0,
        step=0.1
    )

    basket_z: FloatProperty(
        name="Basket Height",
        description="Height of the basket",
        default=0.6,
        min=0.01,
        soft_min=0.01,
        soft_max=30.0,
        step=1
    )

    wall_thickness_factor: FloatProperty(
        name="Basket Wall Thickness",
        description="Wall thickness of the basket",
        default=0.25,
        min=0.01,
        soft_min=0.01,
        soft_max=0.9,
        step=0.2
    )

    def draw(self, context):
        layout = self.layout

        faceBox = layout.box()
        faceBox.label(text="Faces")
        faceBox.prop(self, "ringFaces")
        faceBox.prop(self, "heightFaces")
        faceBox.prop(self, "optimizePoles")
        faceBox.prop(self, "shadeSmooth")

        sizebox = layout.box()
        sizebox.label(text="Size")
        sizebox.prop(self, "height")
        sizebox.prop(self, "radialScale")

        basketBox = layout.box()
        basketBox.label(text="Basket")
        basketBox.prop(self, "basket_x")
        basketBox.prop(self, "basket_y")
        basketBox.prop(self, "basket_z")
        basketBox.prop(self, "basket_scale")
        basketBox.prop(self, "wall_thickness_factor")

        distanceBox = layout.box()
        distanceBox.label(text="Distance")
        distanceBox.prop(self, "distance")

    def generate_mat_balloon():
        balloon_mat = bpy.data.materials.new("BalloonMat")
        balloon_mat.use_nodes = True
        bpy.context.object.active_material = balloon_mat
        principled_node = balloon_mat.node_tree.nodes.get('Principled BSDF')
        principled_node.inputs[0].default_value = (
            random.random(), random.random(), random.random(), 1)  # Change color to random one

    def generate_mat_basket():

        basket_mat = bpy.data.materials.new("BasketMat")
        basket_mat.use_nodes = True
        bpy.context.object.active_material = basket_mat
        principled_node_basket = basket_mat.node_tree.nodes.get(
            'Principled BSDF')
        principled_node_basket.inputs[0].default_value = (
            0.370625, 0.258177, 0.0869385, 1)  # Change color to brown
        # set roughness to 1
        principled_node_basket.inputs[7].default_value = 1
        # set specular to 0.2
        principled_node_basket.inputs[5].default_value = 0.2

    def execute(self, context):

        verts, edges, faces = generate_Balloon(
            radialScale=self.radialScale,
            height=self.height,
            ringFaces=self.ringFaces,
            heightFaces=self.heightFaces,
            distance=self.distance)

        mesh = bpy.data.meshes.new("Balloon")
        mesh.from_pydata(verts, edges, faces)
        if self.shadeSmooth:
            for f in mesh.polygons:
                f.use_smooth = True

        # Normal calculation
        self.calcNormals(mesh)
        # Uvs
        self.generate_UVs(
            mesh,
            ringFaces=self.ringFaces,
            heightFaces=self.heightFaces
        )

        mesh.update()

        balloonObj = bpy.data.objects.new(mesh.name, mesh)
        bpy.context.collection.objects.link(balloonObj)
        bpy.context.view_layer.objects.active = balloonObj

        bpy.ops.object.mode_set(mode='EDIT')
        if self.optimizePoles:
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT')

        Add_Balloon.generate_mat_balloon()  # generate materials

        # Generate basket
        verts_basket, edges_basket = generate_Basket(
            basket_x=self.basket_x,
            basket_y=self.basket_y,
            basket_z=self.basket_z,
            basket_scale=self.basket_scale,
            wall_thickness_factor=self.wall_thickness_factor)
        mesh1 = bpy.data.meshes.new("Basket")
        mesh1.from_pydata(verts_basket, [], edges_basket)
        basketObj = bpy.data.objects.new(mesh1.name, mesh1)
        bpy.context.collection.objects.link(basketObj)
        bpy.context.view_layer.objects.active = basketObj

        Add_Balloon.generate_mat_basket()  # generate materials

        # Parent basket to balloon
        basketObj.parent = balloonObj

        return {'FINISHED'}

    def generate_UVs(self, mesh, ringFaces, heightFaces):

        uvlayer = mesh.uv_layers.new()
        mesh.uv_layers.active = uvlayer

        for face in mesh.polygons:
            for idx, (vert_idx, loop_idx) in enumerate(zip(face.vertices, face.loop_indices)):
                x = vert_idx % (ringFaces)
                y = vert_idx // (ringFaces)
                if (x == 0) and (idx > 1):
                    x = ringFaces
                uvlayer.data[loop_idx].uv = (
                    x / (ringFaces), 1.0 - (y / (heightFaces)))

    def calcNormals(self, mesh):
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.clear()
        mesh.update()
        bm.free()


def balloon_menu(self, context):
    lay_out = self.layout
    lay_out.menu(Add_Balloon_Menu.bl_idname)


def register():
    bpy.types.VIEW3D_MT_mesh_add.append(balloon_menu)
    bpy.utils.register_class(Add_Balloon_Menu)
    bpy.utils.register_class(Add_Balloon)


def unregister():
    bpy.utils.unregister_class(Add_Balloon_Menu)
    bpy.utils.unregister_class(Add_Balloon)
    bpy.types.VIEW3D_MT_mesh_add.remove(balloon_menu)
