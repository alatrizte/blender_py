# Creacion de tubos aleatorios

import bpy
import random, os, string
from mathutils import Vector

def generar_codigo_aleatorio(longitud=8):
    # Definir los caracteres que se utilizarán
    caracteres = string.ascii_letters + string.digits
    
    # Generar el código aleatorio
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    
    return codigo

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

def create_points():
    bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=True, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

    # Obtén el objeto activo y su malla
    obj = bpy.context.active_object
    mesh = obj.data

    bpy.ops.mesh.select_all(action='DESELECT')

    # Selecciona una cara aleatoria
    bpy.ops.object.mode_set(mode='OBJECT')
    cara_aleatoria = random.choice(mesh.polygons)
    cara_aleatoria.select = True
    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

    bpy.ops.mesh.delete(type='VERT')
    bpy.ops.mesh.select_all(action='SELECT')

    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    bpy.ops.mesh.subdivide(number_cuts=3)

    bpy.ops.mesh.select_all(action='DESELECT')
    # Selecciona una cara aleatoria
    bpy.ops.object.mode_set(mode='OBJECT')
    cara_aleatoria = random.choice(mesh.polygons)
    cara_aleatoria.select = True
    cara_normal = cara_aleatoria.normal
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

    bpy.ops.mesh.merge(type='CENTER')

    bpy.ops.mesh.extrude_region_move(
         TRANSFORM_OT_translate={
            "value":Vector(cara_normal)*0.25,
        }
    )
    bpy.ops.object.mode_set(mode='OBJECT')
    
create_points()
create_points()
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()

bpy.ops.object.mode_set(mode='EDIT')
obj = bpy.context.active_object

vs= [Vector(v.co) for v in obj.data.vertices if v.select]
vs_ini = vs[0]
vs_fin = vs[1]

bpy.ops.object.mode_set(mode='OBJECT')
obj.data.vertices[1].select = False
bpy.ops.object.mode_set(mode='EDIT')

for v in obj.data.vertices:
    if v.select:
        print(v.co)
        ref_vector = v.co

res = vs_ini - vs_fin
vectores_resultantes = []

for i in range(len(res)):
    nuevo_vector = [0.0, 0.0, 0.0]
    nuevo_vector[i] = res[i]
    vectores_resultantes.append(tuple(nuevo_vector))
        
def get_order_based_on_max_index(vector):
    max_index = max(range(3), key=lambda i: abs(vector[i]))
    if max_index == 2:
        return [0, 1, 2]
    elif max_index == 1:
        return [2, 0, 1]
    else:  # max_index == 0
        return [1, 2, 0]
    
# Obtener el orden basado en el índice del valor máximo absoluto
order = get_order_based_on_max_index(ref_vector)

# Ordenar los vectores según la lista de orden
sorted_vectors = []
for i in order:
    sorted_vectors.append(vectores_resultantes[i])
        
for vector in sorted_vectors:
    print(vector)
    bpy.ops.mesh.extrude_region_move(
     TRANSFORM_OT_translate={
        "value":Vector(vector),
    }
)

bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.bevel(offset=0.1, offset_pct=0, affect='VERTICES')

bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.convert(target='CURVE')

#### Crear los círculos de los tubos
bpy.ops.mesh.primitive_circle_add(radius=0.05, enter_editmode=True, align='WORLD', location=(0, 0, 0))

for i in range(0, 3):
    bpy.ops.mesh.duplicate_move(
        TRANSFORM_OT_translate={
            "value":(-0.12, 0.0, 0.0)
        }
    )
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.translate(value=(0.18, 0.0, 0.0))
bpy.ops.transform.rotate(value=-1.5708)
bpy.ops.object.mode_set(mode='OBJECT')
bpy.ops.object.convert(target='CURVE')

path_pipes = bpy.data.objects["Cube.001"]
bpy.ops.object.select_all(action='DESELECT')
path_pipes.select_set(True)
# Establecer el objeto como activo
bpy.context.view_layer.objects.active = path_pipes
bpy.context.object.data.bevel_mode = 'OBJECT'
bpy.context.object.data.bevel_object = bpy.data.objects["Circle"]
bpy.ops.object.convert(target='MESH')


ruta = os.getcwd()
# Generar y mostrar el código

codigo_aleatorio = generar_codigo_aleatorio()
bpy.ops.wm.save_as_mainfile(filepath=f"./pipes/P_{codigo_aleatorio}.blend")

