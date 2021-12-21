import bpy
import random

for balloon in bpy.data.objects:
    print(balloon.name)
    if "Balloon" in balloon.name:
        try:
            # Add path
            bpy.ops.curve.primitive_nurbs_path_add(radius=(
                2*random.random()), rotation=(random.random(), random.random(), random.random()))
            curve_ob = bpy.context.object

            frame_start = 1
            length = 500

            con = balloon.constraints.new('FOLLOW_PATH')
            con.target = curve_ob

            # Limit rotation Constraint
            lr_constraint = balloon.constraints.new('LIMIT_ROTATION')
            lr_constraint.use_limit_x = True
            lr_constraint.use_limit_y = True
            lr_constraint.use_limit_z = True

            curve_ob.data.use_path = True
            anim = curve_ob.data.animation_data_create()
            anim.action = bpy.data.actions.new("%sAction" % curve_ob.data.name)

            fcu = anim.action.fcurves.new("eval_time")
            mod = fcu.modifiers.new('GENERATOR')
            mod.coefficients = (-frame_start / length * 100,
                                frame_start / length / frame_start * 100)

        except:
            print(ob.name + "could not animate")
