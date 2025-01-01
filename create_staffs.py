import bpy
import os
import string, random

def generar_codigo_aleatorio(longitud=8):
    # Definir los caracteres que se utilizarán
    caracteres = string.ascii_letters + string.digits
    
    # Generar el código aleatorio
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    
    return codigo

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(0.07, 0.15, 0.01))
bpy.ops.transform.rotate(value=0.668092, orient_axis='Y')

translate = 0.07
duplicates = 5
for i in range(0, duplicates):
    bpy.ops.mesh.duplicate_move(
        MESH_OT_duplicate={"mode":1}, 
        TRANSFORM_OT_translate={
            "value":(translate, 0.0, 0.0)
        }
    )
bpy.ops.mesh.select_all(action='SELECT')


bpy.ops.transform.translate(
    value=(-(translate * duplicates / 2), 0, 0.01)
)


bpy.ops.object.mode_set(mode='OBJECT')
bpy.context.object.name = "grid"

ruta = os.getcwd()
# Generar y mostrar el código
codigo_aleatorio = generar_codigo_aleatorio()
bpy.ops.wm.save_as_mainfile(filepath=f"{ruta}/staffs/S_{codigo_aleatorio}.blend")




