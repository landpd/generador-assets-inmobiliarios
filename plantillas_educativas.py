import re
from recursos_graficos import TEXTURAS, SVGS, obtener_foto_random_b64


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

        # Reemplazar negritas **texto** por un span con el color de acento
        linea = re.sub(r'\*\*(.*?)\*\*', f'<span class="text-[{color_acento}] font-bold">\\1</span>', linea)

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


def plantilla_geometria_limpia(datos_array, paleta):
    """
    Genera un carrusel panorámico estilo Geometría Corporativa Limpia (Arquetipo B).
    Uso de formas geométricas puras cortadas por los bordes, aire y limpieza extrema.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Foto de fondo + overlay =====
            foto_fondo = obtener_foto_random_b64()
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Fondo fotográfico -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_fondo}');"></div>

      <!-- Overlay de color -->
      <div class="absolute inset-0 bg-[{bg_color}]/80 z-10"></div>

      <!-- Forma geométrica cortada (esquina inferior derecha) -->
      <div class="absolute rounded-full bg-[{secundario_color}] w-[800px] h-[800px] -bottom-[400px] -right-[400px] opacity-15 z-0"></div>

      <!-- Logo full -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_full'].format(clases=f'w-[250px] text-[{texto_color}]')}
      </div>

      <!-- Contenido centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Etiqueta -->
        <div class="bg-[{accent_color}] text-[{bg_color}] px-6 py-2 inline-block font-nunito font-bold text-[24px] tracking-widest uppercase mb-8">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </div>

        <!-- Título gigante -->
        <h1 class="font-garamond text-[{texto_color}] text-[130px] leading-[0.9] font-normal max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Limpio, centrado, con bookmark =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden flex flex-col items-center justify-center text-center px-[120px] z-20">

      <!-- Forma geométrica cortada (esquina superior izquierda) -->
      <div class="absolute rounded-full bg-[{secundario_color}] w-[600px] h-[600px] -top-[300px] -left-[300px] opacity-10 z-0"></div>

      <!-- Logo isotipo -->
      <div class="mb-16 z-10">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[100px] h-[100px] text-[{texto_color}]')}
      </div>

      <!-- Título -->
      <h1 class="font-garamond text-[{texto_color}] text-[120px] leading-[0.95] font-normal mb-12 z-10">
        {titulo}
      </h1>

      <!-- Texto formateado -->
      <div class="font-nunito text-[{texto_color}] text-[36px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-16 z-10">
        {formatear_texto_html(texto, accent_color)}
      </div>

      <!-- Indicador: Guarda este post + bookmark -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
        {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Asimetría alternada =====
            es_impar = i % 2 == 1
            clase_forma_1 = '-top-[300px] -right-[300px]' if es_impar else '-bottom-[300px] -left-[300px]'
            clase_forma_2 = '-bottom-[200px] -left-[200px]' if es_impar else '-top-[200px] -right-[200px]'
            align_flex = 'items-end text-right' if es_impar else 'items-start text-left'
            justify_num = 'justify-end' if es_impar else 'justify-start'

            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Forma geométrica 1 (grande, cortada) -->
      <div class="absolute rounded-full bg-[{secundario_color}] w-[600px] h-[600px] opacity-10 {clase_forma_1} z-0"></div>

      <!-- Forma geométrica 2 (pequeña, decorativa) -->
      <div class="absolute rounded-full bg-[{accent_color}] w-[200px] h-[200px] opacity-15 {clase_forma_2} z-0"></div>

      <!-- Logo isotipo -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}]')}
      </div>

      <!-- Contenido alineado asimétricamente -->
      <div class="absolute inset-0 z-10 flex flex-col justify-center h-full px-[100px] {align_flex}">

        <!-- Numeración -->
        <div class="flex items-center gap-4 mb-8 w-full {justify_num}">
          <span class="text-[{accent_color}] font-nunito text-[28px] font-bold leading-none">{str(i + 1).zfill(2)}</span>
          <div class="w-[60px] h-[2px] bg-[{accent_color}]"></div>
          <span class="text-[{texto_color}] font-nunito text-[20px] font-light opacity-50">/ {str(total_slides).zfill(2)}</span>
        </div>

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[0.95] font-normal mb-10 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[700px]">
          {formatear_texto_html(texto, accent_color)}
        </div>

      </div>

      <!-- Indicador: Desliza + flecha -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Desliza</span>
        {SVGS['flecha_larga'].format(clases=f'w-[80px] text-[{accent_color}]')}
      </div>

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


def plantilla_editorial_grunge(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo Editorial Grunge (Arquetipo A).
    Uso de texturas de papel, cajas de color rotadas, contraste agresivo.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    textura = TEXTURAS.get("pizarra_rayones", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Mitad izquierda (texto) + Mitad derecha (foto) =====
            foto_fondo = obtener_foto_random_b64()
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Logo full -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_full'].format(clases=f'w-[200px] text-[{texto_color}]')}
      </div>

      <!-- Mitad derecha: Foto de stock -->
      <div class="absolute top-0 right-0 w-[540px] h-full bg-cover bg-center z-0"
           style="background-image: url('{foto_fondo}');"></div>

      <!-- Mitad izquierda: Contenido -->
      <div class="absolute top-0 left-0 w-[540px] h-full flex flex-col justify-center px-[80px] z-20">

        <!-- Etiqueta -->
        <span class="font-nunito text-[24px] font-bold uppercase tracking-widest text-[{accent_color}] mb-6">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Título en caja rotada -->
        <div class="bg-[{accent_color}] text-[{bg_color}] p-8 -rotate-2 inline-block z-20">
          <h1 class="font-garamond font-normal text-[110px] leading-none">
            {titulo}
          </h1>
        </div>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Centrado, limpio con textura =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden flex flex-col items-center justify-center text-center px-[120px] z-20">

      <!-- Logo isotipo -->
      <div class="mb-16 z-10">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[100px] h-[100px] text-[{texto_color}]')}
      </div>

      <!-- Título -->
      <h1 class="font-garamond text-[{texto_color}] text-[120px] leading-[0.95] font-normal mb-12 z-10">
        {titulo}
      </h1>

      <!-- Texto formateado -->
      <div class="font-nunito text-[{texto_color}] text-[36px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-16 z-10">
        {formatear_texto_html(texto, accent_color)}
      </div>

      <!-- Indicador: Guarda este post + bookmark -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
        {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Asimetría rústica =====
            es_impar = i % 2 == 1
            align_flex = 'items-start text-left pr-[200px]' if es_impar else 'items-end text-right pl-[200px]'

            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Logo isotipo -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}]')}
      </div>

      <!-- Contenido asimétrico -->
      <div class="absolute inset-0 z-10 flex flex-col justify-center h-full px-[100px] {align_flex}">

        <!-- Título en caja rotada con fondo secundario -->
        <div class="bg-[{secundario_color}] text-[{bg_color}] p-6 -rotate-1 inline-block mb-8 z-20 {'self-start' if es_impar else 'self-end'}">
          <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[0.95] font-normal">
            {titulo}
          </h1>
        </div>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[700px]">
          {formatear_texto_html(texto, accent_color)}
        </div>

      </div>

      <!-- Indicador: Desliza + flecha -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Desliza</span>
        {SVGS['flecha_larga'].format(clases=f'w-[80px] text-[{accent_color}]')}
      </div>

    </div>
"""

    # Determinar blend según tema de color (claro vs oscuro)
    blend_mode = "mix-blend-screen" if bg_color.upper() in ["#FAFAFA", "#FFFFFF", "#F5F5F5"] else "mix-blend-multiply"

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

    <!-- ===== TEXTURA GLOBAL: Pizarra Rayones (efecto grunge) ===== -->
    <div class="absolute inset-0 z-0 opacity-30 {blend_mode}"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_cinematografica(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo Cinematográfico/Full Bleed (Arquetipo E).
    Fotografías a pantalla completa con viñetas, textos centrados como créditos de cine.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    textura = TEXTURAS.get("polvo_blanco", "") or ""
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        # Cada slide obtiene su propia foto para efecto de escena independiente
        foto_fondo = obtener_foto_random_b64()

        if es_portada:
            # ===== PORTADA: Textos centrados tipo apertura de película =====
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_fondo}');"></div>

      <!-- Gradiente viñeta -->
      <div class="absolute inset-0 bg-gradient-to-t from-[{bg_color}] via-[{bg_color}]/70 to-[{bg_color}]/40 z-10"></div>

      <!-- Logo full centrado arriba -->
      <div class="absolute top-[80px] left-1/2 -translate-x-1/2 z-30">
        {SVGS['logo_pulppo_full'].format(clases=f'w-[250px] text-[{texto_color}]')}
      </div>

      <!-- Contenido centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Etiqueta -->
        <span class="font-nunito text-[24px] font-bold uppercase tracking-widest text-[{accent_color}] mb-8">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Título gigante -->
        <h1 class="font-garamond text-[{texto_color}] text-[120px] leading-[0.9] font-normal max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Modo créditos de película =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_fondo}');"></div>

      <!-- Gradiente viñeta más oscuro para CTA -->
      <div class="absolute inset-0 bg-gradient-to-t from-[{bg_color}] via-[{bg_color}]/80 to-[{bg_color}]/60 z-10"></div>

      <!-- Contenido centrado tipo créditos -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Logo isotipo -->
        <div class="mb-12">
          {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[100px] h-[100px] text-[{texto_color}]')}
        </div>

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[0.95] font-normal mb-10">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-12">
          {formatear_texto_html(texto, accent_color)}
        </div>

        <!-- Indicador: Guarda este post + bookmark -->
        <div class="flex items-center gap-3">
          <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
          {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
        </div>

      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Subtítulos de cine (parte inferior) =====
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_fondo}');"></div>

      <!-- Gradiente viñeta -->
      <div class="absolute inset-0 bg-gradient-to-t from-[{bg_color}] via-[{bg_color}]/70 to-[{bg_color}]/40 z-10"></div>

      <!-- Textos centrados en la parte inferior (como subtítulos) -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-end text-center px-[120px] pb-[150px]">

        <!-- Línea decorativa -->
        <div class="w-[100px] h-[1px] bg-[{accent_color}] mb-8"></div>

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[90px] leading-[0.95] font-normal mb-8 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-85">
          {formatear_texto_html(texto, accent_color)}
        </div>

      </div>

      <!-- Logo isotipo (esquina superior izquierda) -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}]')}
      </div>

      <!-- Indicador: Desliza -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Desliza</span>
        {SVGS['flecha_larga'].format(clases=f'w-[80px] text-[{accent_color}]')}
      </div>

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

    <!-- ===== TEXTURA GLOBAL: Polvo Blanco (look de película) ===== -->
    <div class="absolute inset-0 z-0 opacity-30 mix-blend-screen"
         style="background-image: url('{textura}'); background-size: cover; background-repeat: repeat;"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_impacto_brutalista(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo Impacto Brutalista (Arquetipo C).
    Tipografía colosal, contraste agresivo, líneas de cuadrícula, números héroe de fondo.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Minimalismo extremo =====
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Logo full -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_full'].format(clases=f'w-[200px] text-[{texto_color}]')}
      </div>

      <!-- Contenido -->
      <div class="absolute inset-0 z-20 flex flex-col justify-center px-[80px]">

        <!-- Etiqueta sobre la línea -->
        <span class="font-nunito text-[18px] font-bold uppercase tracking-[0.3em] text-[{accent_color}] mb-4">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Línea horizontal -->
        <div class="w-full h-[2px] bg-[{texto_color}]/20 mb-8"></div>

        <!-- Título colosal -->
        <h1 class="font-garamond font-normal text-[150px] leading-[0.85] text-[{texto_color}] uppercase tracking-tighter max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Texto colosal alineado a la izquierda =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Logo isotipo -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}]')}
      </div>

      <!-- Contenido -->
      <div class="absolute inset-0 z-20 flex flex-col justify-center px-[80px]">

        <!-- Título colosal -->
        <h1 class="font-garamond font-normal text-[130px] leading-[0.85] text-[{texto_color}] uppercase tracking-tighter mb-10">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-12">
          {formatear_texto_html(texto, accent_color)}
        </div>

        <!-- CTA directo -->
        <div class="flex items-center gap-4">
          <span class="font-nunito text-[{accent_color}] text-[24px] font-bold uppercase tracking-widest">Guarda este post</span>
          {SVGS['bookmark'].format(clases=f'w-[32px] h-[32px] text-[{accent_color}]')}
        </div>

      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Número héroe + texto a la derecha =====
            num_str = str(i + 1).zfill(2)
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Número héroe colosal de fondo -->
      <span class="font-garamond text-[600px] text-[{texto_color}] opacity-5 absolute -left-[100px] -bottom-[100px] z-0 leading-none">
        {num_str}
      </span>

      <!-- Logo isotipo -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[60px] h-[60px] text-[{texto_color}]')}
      </div>

      <!-- Contenido centrado verticalmente a la derecha -->
      <div class="absolute inset-0 z-10 flex flex-col items-end justify-center text-right pl-[150px] pr-[80px]">

        <!-- Línea vertical divisoria -->
        <div class="border-r-4 border-[{accent_color}] pr-8">

          <!-- Título -->
          <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[0.95] font-normal uppercase mb-8">
            {titulo}
          </h1>

          <!-- Texto formateado -->
          <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[600px]">
            {formatear_texto_html(texto, accent_color)}
          </div>

        </div>

      </div>

      <!-- Indicador: Desliza -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Desliza</span>
        {SVGS['flecha_larga'].format(clases=f'w-[80px] text-[{accent_color}]')}
      </div>

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

    <!-- ===== LÍNEA DE CUADRÍCULA GLOBAL ===== -->
    <div class="absolute top-[200px] left-0 w-full h-[2px] bg-[{texto_color}]/10 z-0"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_corporativo_listas(datos_array, paleta):
    """
    Genera un carrusel panorámico en estilo Corporativo de Listas (Arquetipo D).
    Tarjetas flotantes (Cards) con sombras pesadas sobre fondo fotográfico.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    foto_fondo = obtener_foto_random_b64()
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Tarjeta con borde superior =====
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Logo isotipo (fuera de la tarjeta) -->
      <div class="absolute top-[80px] left-[80px] z-30">
        {SVGS['logo_pulppo_full'].format(clases=f'w-[180px] text-[{texto_color}]')}
      </div>

      <!-- Tarjeta flotante centrada -->
      <div class="w-[850px] bg-[{bg_color}] shadow-2xl p-[80px] border-t-8 border-[{accent_color}] relative z-20 mx-auto mt-[180px]">

        <!-- Etiqueta -->
        <span class="font-nunito text-[20px] font-bold uppercase tracking-widest text-[{accent_color}] mb-6 block">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[0.95] font-normal">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Tarjeta centrada + bookmark =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Tarjeta flotante centrada -->
      <div class="w-[850px] bg-[{bg_color}] shadow-2xl p-[80px] border-t-8 border-[{accent_color}] relative z-20 mx-auto mt-[180px] flex flex-col items-center text-center">

        <!-- Logo isotipo -->
        <div class="mb-10">
          {SVGS['logo_pulppo_isotipo'].format(clases=f'w-[80px] h-[80px] text-[{texto_color}]')}
        </div>

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[90px] leading-[0.95] font-normal mb-8">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[30px] font-light leading-[1.4] max-w-[600px] opacity-80 mb-10">
          {formatear_texto_html(texto, accent_color)}
        </div>

        <!-- Bookmark + CTA -->
        <div class="flex items-center gap-3">
          <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
          {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
        </div>

      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Número gigante de fondo + tarjeta =====
            num_str = str(i + 1).zfill(2)
            es_impar = i % 2 == 1
            cargo_numero = '-right-[250px] -top-[200px]' if es_impar else '-left-[250px] -bottom-[200px]'
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Número gigante de fondo -->
      <span class="font-garamond text-[500px] text-[{texto_color}] opacity-5 absolute leading-none {cargo_numero} z-0">
        {num_str}
      </span>

      <!-- Tarjeta flotante centrada -->
      <div class="w-[850px] bg-[{bg_color}] shadow-2xl p-[80px] border-l-8 border-[{secundario_color}] z-20 mx-auto mt-[200px]">

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[90px] leading-[0.95] font-normal mb-8">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85">
          {formatear_texto_html(texto, accent_color)}
        </div>

      </div>

      <!-- Indicador: Desliza -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-10">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Desliza</span>
        {SVGS['flecha_larga'].format(clases=f'w-[80px] text-[{accent_color}]')}
      </div>

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

    <!-- ===== FONDO FOTOGRÁFICO CORPORATIVO ===== -->
    <div class="absolute inset-0 bg-cover bg-center z-0"
         style="background-image: url('{foto_fondo}');"></div>

    <!-- ===== OVERLAY PESADO ===== -->
    <div class="absolute inset-0 bg-[{bg_color}]/95 z-0"></div>

    {slides_html}

  </div>
</body>
</html>'''
