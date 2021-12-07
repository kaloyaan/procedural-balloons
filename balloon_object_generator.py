
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

import bpy, math, bmesh

from mathutils import Vector
from bpy.props import (
    FloatProperty,
    IntProperty,
    BoolProperty
)
import random

def generate_Balloon(radialScale, height, ringFaces, heightFaces):

    verts = []
    edges = []
    faces = []

    heightFElements= heightFaces
    radialFElements = ringFaces

    for j in range(heightFElements+1):
        for i in range(radialFElements):
            u = (2 * math.pi) * (i / (radialFElements))
            v = (math.pi) * (j / (heightFElements))
            x = ((radialScale * 0.92 ) + 0.2 * v) * math.cos(u) * math.sin(v) * height * 0.5
            y = ((radialScale * 0.92 ) + 0.2 * v) * math.sin(u) * math.sin(v) * height * 0.5
            z = height * 0.6 * math.cos(v)
            verts.append(Vector((x , y , z)))
    for j in range(heightFElements):
        for i in range( radialFElements):
            a = i % radialFElements
            b = (i + 1)  % radialFElements
            r1 = radialFElements*j
            r2 = radialFElements*(j+1)
            faces.append([r1 + a, r2 + a, r2 + b, r1 + b])
    return verts, edges, faces


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
        default=16,
        min=4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    heightFaces: IntProperty(
        name="HeightFaces ",
        description="HeightFaces of the Balloon",
        default=20,
        min = 4,
        soft_min=4,
        soft_max=300,
        step=1
    )

    height: FloatProperty(
        name = "Height ",
        description = "Height of the Balloon",
        default = 1.0,
        min = 0.01,
        soft_min = 0.01,
        step = 1
    )

    radialScale: FloatProperty(
        name = "RadialScale",
        description = "RadialScale of the Balloon",
        default = 1.0,
        min = 0.01,
        soft_min = 0.01,
        step = 1
    )

    shadeSmooth: BoolProperty(
        name="Shade Smooth",
        description="",
        default=True,
    )

    optimizePoles: BoolProperty(
        name="Optimize Poles",
        description="",
        default=True,
    )

    # hasThickness: BoolProperty(
    #     name="Thickness",
    #     description="",
    #     default=False,
    # )

    def draw(self, context):
        layout = self.layout

        faceBox = layout.box()
        faceBox.label(text = "Faces")
        faceBox.prop(self, "ringFaces")
        faceBox.prop(self, "heightFaces")
        faceBox.prop(self, "optimizePoles")
        faceBox.prop(self, "shadeSmooth")

        sizebox = layout.box()
        sizebox.label(text = "Size")
        sizebox.prop(self, "height")
        sizebox.prop(self, "radialScale")

    def execute(self, context):

        verts, edges, faces = generate_Balloon(
                radialScale=self.radialScale,
                height=self.height,
                ringFaces=self.ringFaces,
                heightFaces=self.heightFaces)

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

        return {'FINISHED'}

    def generate_UVs(self, mesh, ringFaces,heightFaces):

        uvlayer = mesh.uv_layers.new()
        mesh.uv_layers.active = uvlayer

        for face in mesh.polygons:
            for idx, (vert_idx, loop_idx) in enumerate(zip(face.vertices, face.loop_indices)):
                x = vert_idx % (ringFaces)
                y = vert_idx // (ringFaces)
                if (x==0) and (idx > 1):
                    x=ringFaces
                uvlayer.data[loop_idx].uv = (x / (ringFaces)  , 1.0 - (y /(heightFaces)))

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


