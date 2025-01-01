import bpy
import random
import string
import bmesh
from mathutils import Vector

import os

PALETA = {
        "0A": (0.2667, 0.2667, 0.2667, 1),
        "0B": (0.9882, 0.9686, 0.8196, 1),
        "0C": (0.6627, 0.6627, 0.4784, 1),
        "0D": (0.7098, 0.1725, 0, 1),
        "0E": (0.549, 0, 0.0196, 1),
    }

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)


def create_rand_text(color_aleatorio):
    
    rmm = bpy.data.materials.new(name="random_metal_material")
    rmm.use_nodes = True

    nodes = rmm.node_tree.nodes
    links = rmm.node_tree.links

    for node in nodes:
        nodes.remove(node)
        
    # Crear nodos principales
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    output_node.location = (300, 0)

    principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    principled_node.inputs[2].default_value = 0.1
    principled_node.location = (0, 0)

    node_bump = nodes.new(type="ShaderNodeBump")
    node_bump.invert = True
    node_bump.location = (-200, -200)

    color_ramp_node_01 = nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node_01.color_ramp.interpolation = 'CONSTANT'
    elementos_01 = color_ramp_node_01.color_ramp.elements

    # Generar un color aleatorio
    # color_aleatorio = (
    #     random.random(),  # Rojo
    #     random.random(),  # Verde
    #     random.random(),  # Azul
    #     1.0               # Alpha (opacidad completa)
    # )

    elementos_01[0].color = color_aleatorio
    elementos_01[1].position = 0.4
    color_ramp_node_01.location = (-500, 200)

    color_ramp_node_02 = nodes.new(type="ShaderNodeValToRGB")
    color_ramp_node_02.color_ramp.interpolation = 'CONSTANT'
    elementos_02 = color_ramp_node_02.color_ramp.elements
    elementos_02[1].position = 0.4
    color_ramp_node_02.location = (-800, 0)

    converter_sep_color = nodes.new(type="ShaderNodeSeparateColor")
    converter_sep_color.mode = 'HSV'
    converter_sep_color.location = (-1000, 0)

    color_mix_diff = nodes.new( type="ShaderNodeMixRGB")
    color_mix_diff.blend_type = 'DIFFERENCE'
    color_mix_diff.inputs[0].default_value = 1
    color_mix_diff.location = (-1200, 0)


    input_bevel_01 = nodes.new(type="ShaderNodeBevel")
    input_bevel_01.location = (-1400, 0)

    input_bevel_02 = nodes.new(type="ShaderNodeBevel")
    input_bevel_02.samples = 2
    input_bevel_02.inputs[0].default_value = 0.01
    input_bevel_02.location = (-1400, -200)

    input_map_range = nodes.new(type="ShaderNodeMapRange")
    input_map_range.location = (-1600, 0)

    input_image_texture = nodes.new(type="ShaderNodeTexImage")
    # Cargar la imagen
    imagen = bpy.data.images.load("/home/alatrizte/Documentos/python/blender_py/smudges_basecolor.png")
    input_image_texture.image = imagen
    input_image_texture.location = (-2000, 0)

    input_image_bump = nodes.new(type="ShaderNodeTexImage")
    # Imagen de Bump
    imagen_bump = bpy.data.images.load("/home/alatrizte/Documentos/python/blender_py/bump.jpg")
    input_image_bump.image = imagen_bump
    input_image_bump.location = (-2000, -400)

    bright_contrast = nodes.new(type="ShaderNodeBrightContrast")
    bright_contrast.inputs[1].default_value = -0.67
    bright_contrast.inputs[2].default_value = -1.63
    bright_contrast.location = (-1500, -400)

    input_mapping = nodes.new(type="ShaderNodeMapping")
    input_mapping.inputs["Scale"].default_value = (6,8.4,6)
    input_mapping.location = (-2200, 0)

    input_texture_coordinate = nodes.new(type="ShaderNodeTexCoord")
    input_texture_coordinate.location = (-2400, 0)


    # Conectar los nodos
    links.new(principled_node.outputs['BSDF'], output_node.inputs['Surface'])
    #links.new(node_gamma.outputs['Color'], principled_node.inputs['Base Color'])
    links.new(color_ramp_node_01.outputs['Color'],principled_node.inputs['Base Color'])
    links.new(color_ramp_node_02.outputs['Color'], principled_node.inputs['Metallic'])
    links.new(color_ramp_node_02.outputs['Color'], color_ramp_node_01.inputs['Fac'])
    #links.new(color_ramp_node_02.outputs['Color'], node_bump.inputs['Height'])
    #    links.new(node_bump.outputs['Normal'], principled_node.inputs['Normal'])
    links.new(converter_sep_color.outputs[2], color_ramp_node_02.inputs['Fac'])
    links.new(color_mix_diff.outputs['Color'], converter_sep_color.inputs['Color'])
    links.new(input_bevel_01.outputs['Normal'], color_mix_diff.inputs[1])
    links.new(input_bevel_02.outputs['Normal'], color_mix_diff.inputs[2])
    links.new(input_map_range.outputs['Result'], input_bevel_01.inputs[0])
    links.new(input_image_texture.outputs['Color'], input_map_range.inputs[0])
    links.new(input_mapping.outputs['Vector'], input_image_texture.inputs[0])
    links.new(input_texture_coordinate.outputs['UV'], input_mapping.inputs[0])
    links.new(input_mapping.outputs['Vector'], input_image_bump.inputs[0])
    links.new(input_image_bump.outputs['Color'], bright_contrast.inputs[0])
    links.new(bright_contrast.outputs['Color'], node_bump.inputs['Height'])  
    links.new(node_bump.outputs['Normal'], principled_node.inputs['Normal'])    
    
    return rmm


def extrude(value):
    bpy.ops.mesh.extrude_region_shrink_fatten(
        MESH_OT_extrude_region={"use_normal_flip":False, "use_dissolve_ortho_edges":False, "mirror":False}, 
        TRANSFORM_OT_shrink_fatten={
            "value":value, 
            "use_even_offset":False, 
            "mirror":False,
            "use_proportional_edit":False, 
            "proportional_edit_falloff":'SMOOTH', 
            "proportional_size":0.85, 
            "use_proportional_connected":False, 
            "use_proportional_projected":False, 
            "snap":False, 
            "release_confirm":False, 
            "use_accurate":False
        }
    )

def select_pols(obj, size, margin=0.02):
    mesh = obj.data
    for cara in mesh.polygons:
        if cara.area < size + margin and cara.area > size - margin:
            
            print(f"Índice de la cara: {cara.index}")
            print(f"Vértices: {cara.vertices}")
            print(f"Normal: {cara.normal}")
            print(f"Área: {cara.area}")
            print(f"Centro: {cara.center}")
            print("---")
            
            mesh.polygons[cara.index].select = True
    return [f for f in mesh.polygons if f.select]

def duplicate_by_face(to_duplicate, target):
    # Obtén los objetos específicos por nombre
    obj_to_duplicate = bpy.data.objects[to_duplicate]
    target_obj = bpy.data.objects[target]

    # Deselecciona todos los objetos y selecciona solo el objeto destino
    bpy.ops.object.select_all(action='DESELECT')
    target_obj.select_set(True)
    bpy.context.view_layer.objects.active = target_obj

    # Guarda el modo actual y cambia al modo edición si no está ya en él
    current_mode = bpy.context.object.mode
    bpy.ops.object.mode_set(mode='EDIT')

    # Crea un bmesh del objeto destino
    bm = bmesh.from_edit_mesh(target_obj.data)
    bm.faces.ensure_lookup_table()

    # Itera solo sobre las caras seleccionadas
    for face in [f for f in bm.faces if f.select]:
        # Crea una copia del objeto
        new_obj = obj_to_duplicate.copy()
        new_obj.data = obj_to_duplicate.data.copy()
        bpy.context.collection.objects.link(new_obj)
        
        # Calcula la posición y rotación para la nueva copia
        new_obj.location = target_obj.matrix_world @ face.calc_center_median()
        new_obj.rotation_euler = face.normal.to_track_quat('Z', 'Y').to_euler()

    # Actualiza la malla
    bmesh.update_edit_mesh(target_obj.data)

    # Vuelve al modo original
    bpy.ops.object.mode_set(mode=current_mode)

bpy.ops.mesh.primitive_cube_add(size=2, enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))

# Asegúrate de estar en modo edición
bpy.ops.object.mode_set(mode='EDIT')

# Obtén el objeto activo y su malla
obj = bpy.context.active_object
mesh = obj.data

bpy.ops.mesh.subdivide(number_cuts=3)
bpy.ops.mesh.select_all(action='DESELECT')

# Selecciona una cara aleatoria
bpy.ops.object.mode_set(mode='OBJECT')
cara_aleatoria = random.choice(mesh.polygons)
cara_aleatoria.select = True
bpy.ops.object.mode_set(mode='EDIT')

# Almacena el índice de la cara seleccionada
indice_cara_seleccionada = cara_aleatoria.index

bpy.ops.mesh.select_all(action='DESELECT')

bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
rand_num = random.randint(1,100)

bpy.ops.mesh.select_random(seed=rand_num)

#mesh.polygons[indice_cara_seleccionada].select = False

for i in range(1, 3):
    extrude_rand = random.uniform(0.05, 0.2)
    extrude(extrude_rand)
    rand_num = random.randint(1,100)
    bpy.ops.mesh.select_random(seed=rand_num, action='DESELECT')

for i in range(1, 3):
    thickness_rand = random.uniform(0.5, 0.75)
    bpy.ops.mesh.inset(thickness=0.115147, depth=0, use_individual=True)
    extrude_rand = random.uniform(0.5, 1)
    extrude(extrude_rand)
    rand_num = random.randint(1,100)
    bpy.ops.mesh.select_random(seed=rand_num, action='DESELECT')
    
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.editmode_toggle()

"""
bpy.ops.object.modifier_add(type='BEVEL')
bpy.context.object.modifiers["Bevel"].offset_type = 'ABSOLUTE'
bpy.context.object.modifiers["Bevel"].width = 0.01
"""

# Obtén el objeto activo y su malla
obj = bpy.context.active_object
select_pols(obj, 0.25)

        
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.inset(thickness=0.0385833, depth=0, use_individual=True)

for i in range(1,4):
    extrude_rand = random.uniform(0.05, 0.2)
    extrude(extrude_rand)
    rand_num = random.randint(1,100)
    bpy.ops.mesh.select_random(seed=rand_num, action='DESELECT')
    bpy.ops.mesh.inset(thickness=0.0385833, depth=0, use_individual=True)
    
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')


bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.uv.smart_project()
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.editmode_toggle()
obj = bpy.context.active_object
mesh = obj.data
sf = select_pols(obj, 0.16)

def is_square(face):
    data = obj.data
    distances = []
    for edge in face.edge_keys:
        v1 = Vector(data.vertices[edge[0]].co)
        v2 = Vector(data.vertices[edge[1]].co)
        distancia = (v2 - v1).length
        distances.append(distancia)
    return len(set(distances)) == 1

for face in sf:
    if face.select and len(face.vertices) == 4:
        if not is_square(face):
            face.select = False
            
bpy.ops.object.mode_set(mode='EDIT')
            
rand_num = random.randint(1,100)
bpy.ops.mesh.select_random(seed=rand_num, action='DESELECT')
  
#bpy.ops.object.editmode_toggle()
#bpy.ops.mesh.inset(thickness=0.02, depth=0, use_individual=True)

clave, color_aleatorio = random.choice(list(PALETA.items()))
# Crear un nuevo material
ramdom_material = create_rand_text(color_aleatorio)
obj.data.materials.append(ramdom_material)
bpy.context.scene.render.engine = 'CYCLES'

def generar_codigo_aleatorio(longitud=8):
    # Definir los caracteres que se utilizarán
    caracteres = string.ascii_letters + string.digits
    
    # Generar el código aleatorio
    codigo = ''.join(random.choice(caracteres) for _ in range(longitud))
    
    return codigo

def add_obj_to_scene(path, name):
    bpy.ops.object.mode_set(mode='OBJECT')   

    # Realizar el append
    with bpy.data.libraries.load(path) as (data_from, data_to):
        data_to.objects = [name]

    # Enlazar el objeto a la escena actual
    for obj in data_to.objects:
        if obj is not None:
            bpy.context.collection.objects.link(obj)

########## Añadir tuberias aleatorias 
ruta = os.getcwd()
path_to_pipes = f"{ruta}/pipes"
archivos_blend = [f for f in os.listdir(path_to_pipes) if f.endswith('.blend')]
archivo_seleccionado = random.choice(archivos_blend)
pipes = f"{path_to_pipes}/{archivo_seleccionado}"
name_pipes = "Cube.001"

add_obj_to_scene(pipes, name_pipes)

path_pipes = bpy.data.objects["Cube.001"]
bpy.ops.object.select_all(action='DESELECT')

# Selecciona y activa el objeto
path_pipes.select_set(True)
bpy.context.view_layer.objects.active = path_pipes
path_pipes.data.materials.append(ramdom_material)

# Duplica el objeto
bpy.ops.object.duplicate()

# Lista de ejes posibles
axes = ['X', 'Y', 'Z']
grados = [3.14159, 1.5708]

for i in range (0, 2):
    # Selecciona un eje aleatorio
    random_axis = random.choice(axes)
    random_grads = random.choice(grados)

    # Rota el objeto duplicado en el eje aleatorio
    bpy.ops.transform.rotate(value=random_grads, orient_axis=random_axis)


path_to_staffs = f"{ruta}/staffs"
# Listar archivos .blend en la carpeta
archivos_blend = [f for f in os.listdir(path_to_staffs) if f.endswith('.blend')]
archivo_seleccionado = random.choice(archivos_blend)

path_staffs = f"{path_to_staffs}/{archivo_seleccionado}"
name_staffs = "grid"

add_obj_to_scene(path_staffs, name_staffs)
grid = path_pipes = bpy.data.objects["grid"]
grid.data.materials.append(ramdom_material)

duplicate_by_face("grid", "Cube")

# Generar y mostrar el código
codigo_aleatorio = generar_codigo_aleatorio()
codigo_aleatorio = clave + codigo_aleatorio
print(f"Código aleatorio: {codigo_aleatorio}")

# Nombre actual de la colección
nombre_actual = "Collection"

# Obtener la colección por su nombre actual
coleccion = bpy.data.collections.get(nombre_actual)

# Verificar si la colección existe
if coleccion:
    # Renombrar la colección
    coleccion.name = codigo_aleatorio
    print(f"La colección '{nombre_actual}' ha sido renombrada a '{codigo_aleatorio}'.")
else:
    print(f"No se encontró la colección '{nombre_actual}'.")

bpy.ops.wm.save_as_mainfile(filepath=f"{ruta}/objects/{codigo_aleatorio}.blend")



