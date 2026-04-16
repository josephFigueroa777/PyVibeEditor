def emmetFunction(text_content, cursor_index):
    """
    Analiza el texto antes del cursor y expande el atajo.
    Retorna (nuevo_contenido, nuevo_indice_cursor)
    """
    parte_izquierda = text_content[:cursor_index]
    parte_derecha = text_content[cursor_index:]

    # --- 1. html:5 = Emmet ---
    if parte_izquierda.endswith("html:5"):
        nueva_izquierda = parte_izquierda[:-6]
        boiler_plate = """<!DOCTYPE html>
<html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Document</title>
    </head>
    <body>

    </body>
</html>
"""
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + boiler_plate + parte_derecha
        nuevo_indice = len(nueva_izquierda) + len(boiler_plate) - 21
        return (nuevo_contenido, nuevo_indice)

    # --- 2. Etiqueta: Headings ---
    elif len(parte_izquierda) >= 2 and parte_izquierda[-2] == 'h' and parte_izquierda[-1] in "123456":
        nueva_izquierda = parte_izquierda[:-2]
        expansion = "<h" + str(parte_izquierda[-1]) + "></h" + str(parte_izquierda[-1]) + ">"
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 4
        return (nuevo_contenido, nuevo_indice)
    
    # --- 3. Etiqueta: italic ---
    elif parte_izquierda.endswith("i"):
        nueva_izquierda = parte_izquierda[:-1]
        expansion = "<i></i>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 3 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 4. Etiqueta: sup ---
    elif parte_izquierda.endswith("sup"):
        nueva_izquierda = parte_izquierda[:-3]
        expansion = "<sup></sup>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 5 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 5. Etiqueta: sub ---
    elif parte_izquierda.endswith("sub"):
        nueva_izquierda = parte_izquierda[:-3]
        expansion = "<sub></sub>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 5 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 6. Etiqueta: Paragraphs ---
    elif parte_izquierda.endswith("p"):
        nueva_izquierda = parte_izquierda[:-1]
        expansion = "<p></p>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 3 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 7. Etiqueta: Bold ---
    elif parte_izquierda.endswith("b"):
        nueva_izquierda = parte_izquierda[:-1]
        expansion = "<b></b>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 3 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 13. Etiqueta: Abbreviations ---
    elif parte_izquierda.endswith("abbr"):
        nueva_izquierda = parte_izquierda[:-4]
        expansion = '<abbr title=""></abbr>'
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 15 
        return (nuevo_contenido, nuevo_indice)
    
    # --- 8, 9. Etiqueta: br y hr ---
    elif parte_izquierda.endswith("r"):
        if len(parte_izquierda) >= 2 and parte_izquierda[-2] == 'h':
            nueva_izquierda = parte_izquierda[:-2]
            expansion = """<hr />"""
        else:
            nueva_izquierda = parte_izquierda[:-2]
            expansion = """<br />"""
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 6
        return (nuevo_contenido, nuevo_indice)
    
    # --- 7. Etiqueta: strong ---
    elif parte_izquierda.endswith("strong"):
        nueva_izquierda = parte_izquierda[:-6]
        expansion = "<strong></strong>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 8
        return (nuevo_contenido, nuevo_indice)
    
    # --- 10. Etiqueta: emphasis ---
    elif parte_izquierda.endswith("em"):
        nueva_izquierda = parte_izquierda[:-2]
        expansion = "<em></em>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 4
        return (nuevo_contenido, nuevo_indice)
    
    # --- 11. Etiqueta: quotation (blockquote) ---
    elif parte_izquierda.endswith("bq"):
        nueva_izquierda = parte_izquierda[:-2]
        expansion = '<blockquote cite=""></blockquote>'
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 20
        return (nuevo_contenido, nuevo_indice)
    
    # --- 12. Etiqueta: quotation (q) ---
    elif parte_izquierda.endswith("q"):
        nueva_izquierda = parte_izquierda[:-1]
        expansion = "<q></q>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 3
        return (nuevo_contenido, nuevo_indice)

    # --- 14. Etiqueta: cite ---
    elif parte_izquierda.endswith("cite"):
        nueva_izquierda = parte_izquierda[:-4]
        expansion = "<cite></cite>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 6
        return (nuevo_contenido, nuevo_indice) 
    
    # --- 15. Etiqueta: dfn ---
    elif parte_izquierda.endswith("dfn"):
        nueva_izquierda = parte_izquierda[:-3]
        expansion = "<dfn></dfn>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 5
        return (nuevo_contenido, nuevo_indice)
    
    # --- 16. Etiqueta: address ---
    elif parte_izquierda.endswith("address"):
        nueva_izquierda = parte_izquierda[:-7]
        expansion = "<address></address>"
        
        # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 9
        return (nuevo_contenido, nuevo_indice)
    
    # --- 17. Etiqueta: Lista ordenada ---
    elif len(parte_izquierda) >= 3 and parte_izquierda[cursor_index - 3 : cursor_index - 1] == 'ol' and parte_izquierda.endswith("+"):
        print(parte_izquierda[cursor_index - 3 : cursor_index - 1])
        nueva_izquierda = parte_izquierda[:-3]
        expansion = """<ol>
    <li></li>
</ol>
"""
    # Insertamos el código en el centro
        nuevo_contenido = nueva_izquierda + expansion + parte_derecha
        nuevo_indice = len(nueva_izquierda) + 9
        return (nuevo_contenido, nuevo_indice)
    
    # Si no hay match, devolvemos todo intacto
    return (text_content, cursor_index)