import re
from recursos_graficos import TEXTURAS, SVGS


def formatear_texto_html(texto, color_acento):
    """Convierte texto plano con saltos de línea y viñetas en HTML formateado."""
    if not texto:
        return ""
    lineas = texto.split('\n')
    html_resultado = '<div class="space-y-4">'
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        # Detectar si la línea empieza con viñeta (•, -, *)
        if re.match(r'^[•\-*]\s*', linea):
            texto_limpio = re.sub(r'^[•\-*]\s*', '', linea)
            html_resultado += f'''
            <div class="flex items-start gap-4">
                <span class="text-[{color_acento}] font-bold mt-1 flex-shrink-0">•</span>
                <span>{texto_limpio}</span>
            </div>'''
        else:
            html_resultado += f'<p>{linea}</p>'
    html_resultado += '</div>'
    return html_resultado


def plantilla_panoramica_educativa(datos_array, paleta):
    """
    Genera un carrusel panorámico educativo con fondo oscuro,
    textura pizarra_rayones y efecto seamless con SVG llave en cada unión.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("pizarra_rayones", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']
    tamano_titulo_normal = "text-[110px]"
    tamano_titulo_portada = "text-[140px]"

    # ---- Construir SVGs seamless en cada unión ----
    seamless_svgs = ""
    for i in range(total_slides - 1):
        left_px = (i + 1) * 1080 - 280
        seamless_svgs += (
            SVGS['llave'].format(
                clases=(
                    f'w-[700px] h-[700px] text-[{secundario_color}] '
                    f'opacity-10 absolute top-[300px] left-[{left_px}px] z-10'
                )
            )
            + "\n      "
        )

    # ---- Construir slides dinámicamente ----
    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1
        tamano_titulo = tamano_titulo_portada if es_portada else tamano_titulo_normal
        num_str = str(i + 1).zfill(2)

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative p-[80px] flex flex-col justify-center z-20">

      {SVGS['logo_pulppo_full'].format(clases=f'w-[250px] text-[{texto_color}] absolute top-[80px] left-[80px] z-30') if es_portada else ''}

      {f'''
      <div class="flex items-center gap-4 mb-12">
        <span class="text-[{accent_color}] font-nunito text-[28px] font-bold leading-none">{num_str}</span>
        <div class="w-[60px] h-[2px] bg-[{accent_color}]"></div>
        <span class="text-[{texto_color}] font-nunito text-[20px] font-light opacity-50">/ {str(total_slides).zfill(2)}</span>
      </div>
      ''' if not es_portada else ''}

      <!-- Título principal -->
      <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold mb-10">
        {titulo}
      </h1>

      <!-- Texto del cuerpo (Formateado) -->
      <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.3] max-w-[800px] opacity-85">
        {formatear_texto_html(texto, accent_color)}
      </div>

      {f'''
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{"Guarda este post" if es_cta else "Desliza"}</span>
        <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
        </svg>
      </div>
      ''' if not es_portada else ''}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== TEXTURA GLOBAL: Pizarra Rayones ===== -->
    <div class="absolute inset-0 z-0 opacity-20 mix-blend-screen"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    <!-- ===== ELEMENTOS SEAMLESS ===== -->
    {seamless_svgs}

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_indiv_collage(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo collage/polaroid con marco central.
    Cada slide es una tarjeta polaroid centrada con textura y mix-blend-multiply.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("marco_polaroid", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        es_portada = i == 0
        es_cta = i == total_slides - 1
        indicador_texto = "Guarda este post" if es_cta else "Desliza"
        tamano_titulo = "text-[140px]" if es_portada else "text-[100px]"

        # Logo según tipo de slide
        if es_portada:
            logo = SVGS['logo_pulppo_full'].format(clases=f'w-[180px] text-[{texto_color}] absolute top-[80px] left-1/2 -translate-x-1/2 z-30')
        else:
            logo = SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}] absolute top-[80px] left-1/2 -translate-x-1/2 z-30')

        # Bloques condicionales
        bloque_estrellas = ''
        if es_cta:
            bloque_estrellas = '<div class="mb-10">' + SVGS['decoracion_estrellas'].format(clases=f'w-[80px] h-[80px] text-[{secundario_color}]') + '</div>'

        bloque_indicador = ''
        if not es_portada:
            bloque_indicador = f'''
    <!-- ===== INDICADOR DE SWIPE ===== -->
    <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
      <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{indicador_texto}</span>
      <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
      </svg>
    </div>'''

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden flex items-center justify-center z-20">

      <!-- ===== LOGO PULPPO ===== -->
      {logo}

      <!-- ===== TARJETA POLAROID CENTRAL ===== -->
      <div class="w-[864px] h-[1080px] relative overflow-hidden flex flex-col items-center justify-center p-[80px]"
           style="background-image: url('{textura}'); background-size: cover; background-position: center; mix-blend-mode: multiply;">

        {bloque_estrellas}

        <!-- Título principal -->
        <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold text-center mb-12">
          {slide['titulo']}
        </h1>

        <!-- Texto del cuerpo (Formateado) -->
        <div class="font-nunito text-[{texto_color}] text-[36px] font-light leading-[1.4] text-center max-w-[700px] opacity-80">
          {formatear_texto_html(slide['texto'], accent_color)}
        </div>

      </div>

      {bloque_indicador}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_indiv_tecnica(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo técnico/check-list con fondo oscuro.
    Textura de papel oscuro, check grande y composición alineada a la izquierda.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("papel_oscuro", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        es_portada = i == 0
        es_cta = i == total_slides - 1
        indicador_texto = "Guarda este post" if es_cta else "Desliza"
        tamano_titulo = "text-[140px]" if es_portada else "text-[110px]"

        # Logo según tipo de slide
        if es_portada:
            logo = SVGS['logo_pulppo_full'].format(clases=f'w-[180px] text-[{texto_color}] absolute top-[80px] left-[80px] z-30')
        else:
            logo = SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}] absolute top-[80px] left-[80px] z-30')

        # Bloques condicionales
        bloque_icono = ''
        if es_cta:
            bloque_icono = '<div class="mb-10">' + SVGS['decoracion_estrellas'].format(clases=f'w-[150px] h-[150px] text-[{accent_color}]') + '</div>'
        elif not es_portada:
            bloque_icono = '<div class="mb-10">' + SVGS['check_circulo'].format(clases=f'w-[150px] h-[150px] text-[{accent_color}]') + '</div>'

        bloque_indicador = ''
        if not es_portada:
            bloque_indicador = f'''
      <!-- Indicador de swipe -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{indicador_texto}</span>
        <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
        </svg>
      </div>'''

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative p-[80px] flex flex-col justify-center z-20">

      <!-- ===== LOGO PULPPO ===== -->
      {logo}

      <!-- ===== CONTENIDO ===== -->
      <div class="relative z-10 w-full h-full flex flex-col justify-center">

        {bloque_icono}

        <!-- Título principal -->
        <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold mb-10 max-w-[900px]">
          {slide['titulo']}
        </h1>

        <!-- Texto del cuerpo (Formateado) -->
        <div class="font-nunito text-[{texto_color}] text-[36px] font-light leading-[1.4] max-w-[800px] opacity-85">
          {formatear_texto_html(slide['texto'], accent_color)}
        </div>

      </div>

      {bloque_indicador}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== TEXTURA GLOBAL: Papel Oscuro ===== -->
    <div class="absolute inset-0 z-0 mix-blend-overlay opacity-60"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_individual_editorial(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo editorial / collage.
    Composición asimétrica con franja vertical, textura ruido_plata
    y decoración de flecha larga.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("ruido_plata", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        es_portada = i == 0
        es_cta = i == total_slides - 1
        indicador_texto = "Guarda este post" if es_cta else "Desliza"
        tamano_titulo = "text-[140px]" if es_portada else "text-[110px]"

        # Logo según tipo de slide
        if es_portada:
            logo = SVGS['logo_pulppo_full'].format(clases=f'w-[180px] text-[{texto_color}] absolute top-[80px] left-[360px] z-30')
        else:
            logo = SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}] absolute top-[80px] right-[80px] z-30')

        # Bloques condicionales
        bloque_numero_slide = ''
        if not es_portada:
            numero_slide_str = str(i + 1).zfill(2)
            bloque_numero_slide = f'''
    <!-- ===== MARCO INFERIOR CON NÚMERO GIGANTE ===== -->
    <div class="absolute bottom-0 left-[40px] w-[200px] h-[250px] border-l-[4px] border-b-[4px] border-[{texto_color}] z-20 flex items-end pb-[20px] pl-[20px]">
      <span class="font-garamond text-[{texto_color}] text-[180px] font-bold leading-none opacity-30">{numero_slide_str}</span>
    </div>'''

        bloque_etiqueta = ''
        if not es_portada:
            bloque_etiqueta = f'''
      <!-- Etiqueta / Categoría -->
      <span class="font-nunito text-[28px] font-bold uppercase tracking-wider text-[{accent_color}] mb-6 border-b-[1px] border-[{accent_color}] pb-4 inline-block">
        {slide['etiqueta']}
      </span>'''

        bloque_estrellas = ''
        if es_cta:
            bloque_estrellas = '<div class="mb-10">' + SVGS['decoracion_estrellas'].format(clases=f'w-[80px] h-[80px] text-[{secundario_color}]') + '</div>'

        bloque_indicador = ''
        if not es_portada:
            bloque_indicador = f'''
    <!-- ===== INDICADOR DE SWIPE ===== -->
    <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-20">
      <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{indicador_texto}</span>
      <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
      </svg>
    </div>'''

        bloque_flecha = ''
        if not es_portada:
            bloque_flecha = '\n    ' + SVGS['flecha_larga'].format(clases=f'w-[100px] text-[{accent_color}] absolute bottom-[80px] right-[150px] z-20')

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- ===== LOGO PULPPO ===== -->
      {logo}

      <!-- ===== BANNER LATERAL IZQUIERDO ===== -->
      <div class="absolute left-0 top-0 w-[324px] h-full bg-[{secundario_color}] z-10"></div>

      {bloque_numero_slide}

      <!-- ===== CONTENIDO PRINCIPAL (derecha) ===== -->
      <div class="absolute left-[360px] top-[80px] right-[80px] bottom-[320px] flex flex-col justify-center z-20">

        {bloque_etiqueta}

        {bloque_estrellas}

        <!-- Título principal -->
        <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold mb-12">
          {slide['titulo']}
        </h1>

        <!-- Texto del cuerpo (Formateado) -->
        <div class="font-nunito text-[{texto_color}] text-[38px] font-light leading-[1.4] max-w-[700px]">
          {formatear_texto_html(slide['texto'], accent_color)}
        </div>

      </div>

      {bloque_indicador}

      {bloque_flecha}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== TEXTURA GLOBAL: Ruido Plata (look revista impresa) ===== -->
    <div class="absolute inset-0 z-0 opacity-30 mix-blend-multiply"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_pano_cinematografica(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo cinematográfico/cultural con textura de polvo
    y efecto seamless de comillas en cada unión entre slides.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("polvo_blanco", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']
    tamano_titulo_normal = "text-[110px]"
    tamano_titulo_portada = "text-[140px]"

    # ---- Construir SVGs seamless en cada unión ----
    seamless_svgs = ""
    for i in range(total_slides - 1):
        left_px = (i + 1) * 1080 - 180
        seamless_svgs += (
            SVGS['comillas'].format(
                clases=(
                    f'w-[600px] h-[600px] text-[{secundario_color}] '
                    f'opacity-20 absolute top-[100px] left-[{left_px}px] z-10'
                )
            )
            + "\n      "
        )

    # ---- Construir slides dinámicamente ----
    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1
        tamano_titulo = tamano_titulo_portada if es_portada else tamano_titulo_normal
        num_str = str(i + 1).zfill(2)

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative p-[80px] flex flex-col justify-center z-20">

      {SVGS['logo_pulppo_full'].format(clases=f'w-[250px] text-[{texto_color}] absolute top-[80px] left-[80px] z-30') if es_portada else ''}

      {f'''
      <div class="flex items-center gap-4 mb-12">
        <span class="text-[{accent_color}] font-nunito text-[28px] font-bold leading-none">{num_str}</span>
        <div class="w-[60px] h-[2px] bg-[{accent_color}]"></div>
        <span class="text-[{texto_color}] font-nunito text-[20px] font-light opacity-50">/ {str(total_slides).zfill(2)}</span>
      </div>
      ''' if not es_portada else ''}

      <!-- Título principal -->
      <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold mb-10">
        {titulo}
      </h1>

      <!-- Texto del cuerpo (Formateado) -->
      <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.3] max-w-[800px] opacity-85">
        {formatear_texto_html(texto, accent_color)}
      </div>

      {f'''
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{"Guarda este post" if es_cta else "Desliza"}</span>
        <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
        </svg>
      </div>
      ''' if not es_portada else ''}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== TEXTURA GLOBAL: Polvo Blanco ===== -->
    <div class="absolute inset-0 z-0 mix-blend-screen opacity-40"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    <!-- ===== ELEMENTOS SEAMLESS ===== -->
    {seamless_svgs}

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_pano_halftone(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo promocional/pop con textura de halftone amarillo.
    Incluye flechas seamless que cruzan cada unión entre slides.

    datos_array: lista de dicts con llaves 'titulo', 'texto' (y opcional 'etiqueta').
    paleta: dict con claves 'fondo', 'texto', 'acento', 'secundario'.
    """
    textura = TEXTURAS.get("halftone_amarillo", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']
    tamano_titulo_normal = "text-[110px]"
    tamano_titulo_portada = "text-[140px]"

    # ---- Construir SVGs seamless en cada unión ----
    seamless_svgs = ""
    for i in range(total_slides - 1):
        left_px = (i + 1) * 1080 - 100
        seamless_svgs += (
            SVGS['flecha_larga'].format(
                clases=(
                    f'w-[800px] text-[{accent_color}] '
                    f'absolute bottom-[200px] left-[{left_px}px] z-10'
                )
            )
            + "\n      "
        )

    # ---- Construir slides dinámicamente ----
    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1
        tamano_titulo = tamano_titulo_portada if es_portada else tamano_titulo_normal
        num_str = str(i + 1).zfill(2)

        slides_html += f"""
    <!-- ========================= SLIDE {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative p-[80px] flex flex-col justify-center z-20">

      {SVGS['logo_pulppo_full'].format(clases=f'w-[250px] text-[{texto_color}] absolute top-[80px] left-[80px] z-30') if es_portada else ''}

      {f'''
      <div class="flex items-center gap-4 mb-12">
        <span class="text-[{accent_color}] font-nunito text-[28px] font-bold leading-none">{num_str}</span>
        <div class="w-[60px] h-[2px] bg-[{accent_color}]"></div>
        <span class="text-[{texto_color}] font-nunito text-[20px] font-light opacity-50">/ {str(total_slides).zfill(2)}</span>
      </div>
      ''' if not es_portada else ''}

      <!-- Título principal -->
      <h1 class="font-garamond text-[{texto_color}] {tamano_titulo} leading-[0.95] font-bold mb-10">
        {titulo}
      </h1>

      <!-- Texto del cuerpo (Formateado) -->
      <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.3] max-w-[800px] opacity-85">
        {formatear_texto_html(texto, accent_color)}
      </div>

      {f'''
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">{"Guarda este post" if es_cta else "Desliza"}</span>
        <svg width="40" height="16" viewBox="0 0 40 16" fill="none" xmlns="http://www.w3.org/2000/svg">
          <path d="M39.7071 8.70711C40.0976 8.31658 40.0976 7.68342 39.7071 7.29289L33.3431 0.928932C32.9526 0.538408 32.3195 0.538408 31.9289 0.928932C31.5384 1.31946 31.5384 1.95262 31.9289 2.34315L37.5858 8L31.9289 13.6569C31.5384 14.0474 31.5384 14.6805 31.9289 15.0711C32.3195 15.4616 32.9526 15.4616 33.3431 15.0711L39.7071 8.70711ZM0 9H39V7H0V9Z" fill="{accent_color}"/>
        </svg>
      </div>
      ''' if not es_portada else ''}

    </div>
"""

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Nunito+Sans:ital,opsz,wght@0,6..12,200..1000;1,6..12,200..1000&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {{
      theme: {{
        extend: {{
          fontFamily: {{
            garamond: ['"EB Garamond"', 'serif'],
            nunito: ['"Nunito Sans"', 'sans-serif'],
          }}
        }}
      }}
    }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== TEXTURA GLOBAL: Halftone Amarillo ===== -->
    <div class="absolute inset-0 z-0 mix-blend-multiply opacity-20"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    <!-- ===== ELEMENTOS SEAMLESS ===== -->
    {seamless_svgs}

    {slides_html}

  </div>
</body>
</html>'''