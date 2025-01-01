import bmesh

def rotar_poligonos():
    # Crear un bmesh del objeto
    bm = bmesh.from_edit_mesh(obj.data)

    # Seleccionar las caras
    caras_seleccionadas = [f for f in bm.faces if f.select]

    # Convertir 35 grados a radianes
    angulo = math.radians(35)

    # Rotar cada cara seleccionada
    for cara in caras_seleccionadas:
        # Calcular el centro de la cara
        centro = cara.calc_center_median()
        
        # Crear la matriz de rotación alrededor del eje Y local de la cara
        eje_y_local = cara.normal.cross(Vector((0, 0, 1)))
        eje_y_local.normalize()
        matriz_rotacion = Matrix.Rotation(angulo, 4, eje_y_local)
        
        # Aplicar la rotación a cada vértice de la cara
        for v in cara.verts:
            v.co = matriz_rotacion @ (v.co - centro) + centro
        
    # Asegúrate de actualizar la malla al final
    bmesh.update_edit_mesh(obj.data)
    
    # Vuelve al modo objeto
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Actualiza la malla y la vista
    obj.data.update()
    bpy.context.view_layer.update()