import bpy
import os

def borrar_coleccion_seleccionada(name_collection):
    # Obtener la colección activa
    coleccion_activa = bpy.data.collections.get(name_collection)
    
    # Verificar si hay una colección seleccionada
    if coleccion_activa:
        # Desenlazar la colección de su padre
        bpy.context.scene.collection.children.unlink(coleccion_activa)
        
        # Borrar la colección
        bpy.data.collections.remove(coleccion_activa)
        
        print(f"La colección ha sido eliminada.")
    else:
        print("No hay ninguna colección seleccionada.")

def encontrar_blend_sin_png():

    def listar_archivos(directorio, extension):
        return [f for f in os.listdir(directorio) if f.endswith(extension)]
    
    directorio_blend = './objects'
    directorio_png = './renders'

    # Obtener listas de archivos
    archivos_blend = listar_archivos(directorio_blend, '.blend')
    archivos_png = listar_archivos(directorio_png, '.png')

    # Convertir nombres de archivos .png a set para búsqueda eficiente
    nombres_png = set(os.path.splitext(f)[0] for f in archivos_png)

    # Encontrar archivos .blend sin correspondiente .png
    blend_sin_png = [os.path.splitext(f)[0] for f in archivos_blend if os.path.splitext(f)[0] not in nombres_png]

    return blend_sin_png

lst_to_render = encontrar_blend_sin_png()

print(lst_to_render)

for f in lst_to_render:
    print(f)
    # Ruta al archivo .blend que contiene la colección
    ruta_archivo = f"./objects/{f}.blend"

    # Vincular la colección
    with bpy.data.libraries.load(ruta_archivo, link=True) as (data_from, data_to):
        data_to.collections = [f]

    # Agregar la colección vinculada a la escena actual
    for coleccion in data_to.collections:
        if coleccion is not None:
            bpy.context.scene.collection.children.link(coleccion)

    # Configurar el formato de salida
    bpy.context.scene.render.image_settings.file_format = 'PNG'

    # Establecer la ruta de salida del render
    bpy.context.scene.render.filepath = f"./renders/{f}.png"

    # Ejecutar el render
    bpy.ops.render.render(write_still=True)
    print(f"Render: {f}.png")

    # Borra el objeto
    borrar_coleccion_seleccionada(f)

bpy.ops.wm.quit_blender()