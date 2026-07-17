import re
from recursos_graficos import SVGS


def formatear_texto_html(texto, color_acento):
    """Convierte texto plano con saltos de línea en HTML formateado.
    Negritas **texto** -> span con color de acento. Viñetas -> bullet con color.
    Todo texto queda alineado a la izquierda (text-left).
    """
    if not texto:
        return ""
    lineas = texto.split('\n')
    html_resultado = '<div class="space-y-4 text-left">'
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue

        # Reemplazar negritas **texto** por un span con el color de acento
        linea = re.sub(r'\*\*(.*?)\*\*', f'<span class="text-[{color_acento}] font-bold">\\1</span>', linea)

        # Detectar si la línea empieza con viñeta
        if re.match(r'^[•\-*]\s*', linea):
            texto_limpio = re.sub(r'^[•\-*]\s*', '', linea)
            html_resultado += f'''
            <div class="flex items-start gap-4 text-left">
                <span class="text-[{color_acento}] font-bold mt-1 flex-shrink-0">·</span>
                <span>{texto_limpio}</span>
            </div>'''
        else:
            html_resultado += f'<p class="text-left">{linea}</p>'
    html_resultado += '</div>'
    return html_resultado


# ── Helper de cobranding (logo Pulppo + logo inmobiliaria) ─────────────────
def _logo_header(texto_color, logo_inmo, es_portada=False):
    """Genera el bloque de cobranding con logo Pulppo + logo inmobiliaria.
    Posición inamovible: top-[80px] right-[80px].
    """
    svg_key = 'logo_pulppo_full' if es_portada else 'logo_pulppo_isotipo'
    svg_size = 'w-[250px]' if es_portada else 'w-[80px] h-[80px]'
    svg_html = SVGS[svg_key].format(clases=f'{svg_size} text-[{texto_color}]')

    if logo_inmo:
        return f'''<div class="absolute top-[80px] right-[80px] z-30 flex items-center gap-4">
          {svg_html}
          <div class="w-[1px] h-[40px] bg-[{texto_color}]/20"></div>
          <img src="{logo_inmo}" class="h-[40px] object-contain">
        </div>'''
    else:
        return f'''<div class="absolute top-[80px] right-[80px] z-30">
          {svg_html}
        </div>'''


def plantilla_geometria_limpia(datos_array, paleta, imagenes_b64=None):
    """
    Genera un carrusel panorámico estilo Geometría Corporativa Limpia (Arquetipo B).
    Fotos solo en portada y CTA. Slides intermedios con fondo liso y formas
    geométricas asimétricas (cuartos de círculo). Etiqueta Flowbite Badge.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    secundario_color = paleta['secundario']
    fotos = imagenes_b64.get('fotos', []) if imagenes_b64 else []
    logo_inmo = imagenes_b64.get('logo_inmobiliaria') if imagenes_b64 else None

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1
        foto_actual = fotos[i % len(fotos)] if fotos else ''

        if es_portada:
            # ===== PORTADA: Foto full-bleed + overlay + Badge Flowbite =====
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo full-bleed -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay -->
      <div class="absolute inset-0 bg-[{bg_color}]/85 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=True)}

      <!-- Contenido centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Badge Flowbite adaptado a Pulppo (sin rounded) -->
        <span class="bg-[{accent_color}] text-[#FAFAFA] font-bold uppercase tracking-widest px-[30px] py-[12px] inline-block font-nunito text-[24px] mb-8">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Título -->
        <h1 class="font-garamond font-normal text-[130px] leading-[1.1] text-[{texto_color}] max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Foto + overlay + bookmark centrado =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden flex flex-col items-center justify-center px-[120px] z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay fuerte -->
      <div class="absolute inset-0 bg-[{bg_color}]/90 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Título -->
      <h1 class="font-garamond font-normal text-[100px] leading-[1.1] text-[{texto_color}] mb-10 z-20">
        {titulo}
      </h1>

      <!-- Texto formateado -->
      <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-16 z-20 text-left">
        {formatear_texto_html(texto, accent_color)}
      </div>

      <!-- Bookmark + CTA -->
      <div class="flex items-center gap-3 z-20">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
        {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Fondo liso + patrón isométrico =====
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <div class="absolute inset-0 z-0 patron-isometrico opacity-5"></div>

      <!-- Logo isotipo -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Contenido centrado verticalmente -->
      <div class="absolute inset-0 z-10 flex flex-col justify-center px-[100px] text-left">

        <!-- Numeración limpia (0-indexada) -->
        <div class="flex items-center gap-4 mb-8">
          <span class="text-[{accent_color}] font-nunito text-[24px] font-bold leading-none">{str(i).zfill(2)}</span>
          <div class="w-[60px] h-[2px] bg-[{accent_color}]"></div>
          <span class="text-[{texto_color}] font-nunito text-[20px] font-light opacity-50">/ {str(total_slides - 2).zfill(2)}</span>
        </div>

        <!-- Título -->
        <h1 class="font-garamond font-normal text-[100px] leading-[1.1] text-[{texto_color}] mb-10 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[700px]">
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
    * {{ box-shadow: none !important; text-shadow: none !important; margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
    .patron-isometrico {{
      background-image:
        linear-gradient(30deg, {texto_color} 12%, transparent 12.5%, transparent 87%, {texto_color} 87.5%, {texto_color}),
        linear-gradient(150deg, {texto_color} 12%, transparent 12.5%, transparent 87%, {texto_color} 87.5%, {texto_color}),
        linear-gradient(30deg, {texto_color} 12%, transparent 12.5%, transparent 87%, {texto_color} 87.5%, {texto_color}),
        linear-gradient(150deg, {texto_color} 12%, transparent 12.5%, transparent 87%, {texto_color} 87.5%, {texto_color}),
        linear-gradient(60deg, {texto_color}77 25%, transparent 25.5%, transparent 75%, {texto_color}77 75%, {texto_color}77),
        linear-gradient(60deg, {texto_color}77 25%, transparent 25.5%, transparent 75%, {texto_color}77 75%, {texto_color}77);
      background-size: 42px 74px;
      background-position: 0 0, 0 0, 21px 37px, 21px 37px, 0 0, 21px 37px;
    }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_impacto_brutalista(datos_array, paleta, imagenes_b64=None):
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
    fotos = imagenes_b64.get('fotos', []) if imagenes_b64 else []
    logo_inmo = imagenes_b64.get('logo_inmobiliaria') if imagenes_b64 else None

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Foto de fondo + overlay + minimalismo extremo =====
            foto_actual = fotos[i % len(fotos)] if fotos else ''
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay de color -->
      <div class="absolute inset-0 bg-[{bg_color}]/90 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=True)}

      <!-- Contenido -->
      <div class="absolute inset-0 z-20 flex flex-col justify-center px-[80px]">

        <!-- Etiqueta sobre la línea -->
        <span class="font-nunito text-[18px] font-bold uppercase tracking-[0.3em] text-[{accent_color}] mb-4">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Línea horizontal -->
        <div class="w-full h-[2px] bg-[{texto_color}]/20 mb-8"></div>

        <!-- Título colosal -->
        <h1 class="font-garamond font-normal text-[150px] leading-[1.1] text-[{texto_color}] tracking-tighter max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Foto de fondo + overlay + texto colosal =====
            foto_actual = fotos[i % len(fotos)] if fotos else ''
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay fuerte -->
      <div class="absolute inset-0 bg-[{bg_color}]/90 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Contenido -->
      <div class="absolute inset-0 z-20 flex flex-col justify-center px-[80px]">

        <!-- Título colosal -->
        <h1 class="font-garamond font-normal text-[130px] leading-[1.1] text-[{texto_color}] tracking-tighter mb-10">
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
            # ===== CONTENIDO: Número héroe + texto alineado alternadamente =====
            num_str = str(i).zfill(2)
            es_impar = i % 2 == 1
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Número héroe colosal de fondo -->
      <span class="font-garamond font-normal text-[600px] text-[{texto_color}] opacity-5 absolute -left-[100px] -bottom-[100px] z-0 leading-none">
        {num_str}
      </span>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Contenedor único con alineación alternada -->
      <div class="relative z-10 flex flex-col justify-center h-full px-[120px] {'text-right items-end' if es_impar else 'text-left items-start'}">

        <!-- Título -->
        <h1 class="font-garamond text-[{texto_color}] text-[100px] leading-[1.1] font-normal mb-8 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[600px]">
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
    * {{ box-shadow: none !important; text-shadow: none !important; margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
    .halftone {{
      --dotSize: 0.20rem;
      --bgSize: 1.35rem;
      --bgPosition: calc(var(--bgSize) / 2);
      background-image: radial-gradient(circle at center, {texto_color} var(--dotSize), transparent 0),
                        radial-gradient(circle at center, {texto_color} var(--dotSize), transparent 0);
      background-size: var(--bgSize) var(--bgSize);
      background-position: 0 0, var(--bgPosition) var(--bgPosition);
      opacity: 0.05;
    }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- ===== LÍNEA DE CUADRÍCULA GLOBAL ===== -->
    <div class="absolute top-[200px] left-0 w-full h-[2px] bg-[{texto_color}]/10 z-0"></div>

    <div class="halftone absolute inset-0 z-0"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_data_driven(datos_array, paleta, imagenes_b64=None):
    """
    Genera un carrusel panorámico en estilo Data-Driven Analítico (Arquetipo D).
    Fondo de color sólido sin fotos de fondo. Tipografía minimalista.
    Número héroe colosal de fondo en slides de contenido.
    Etiqueta estilo Flowbite Badge adaptado a Pulppo.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    logo_inmo = imagenes_b64.get('logo_inmobiliaria') if imagenes_b64 else None
    fotos = imagenes_b64.get('fotos', []) if imagenes_b64 else []
    textura = imagenes_b64.get('textura', '') if imagenes_b64 else ''

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1

        if es_portada:
            # ===== PORTADA: Foto fondo + overlay + badge Flowbite + título =====
            foto_actual = fotos[i % len(fotos)] if fotos else ''
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0 grayscale contrast-125"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay -->
      <div class="absolute inset-0 bg-[{bg_color}]/90 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=True)}

      <!-- Contenido -->
      <div class="absolute inset-0 z-20 flex flex-col justify-center px-[100px]">

        <!-- Badge Flowbite adaptado a Pulppo -->
        <span class="bg-[{accent_color}] text-[#FAFAFA] font-bold uppercase tracking-widest px-[30px] py-[12px] inline-block font-nunito text-[24px] mb-10">
          {etiqueta or 'DATA INSIGHT'}
        </span>

        <!-- Título gigante alineado a la izquierda -->
        <h1 class="font-garamond font-normal text-[130px] leading-[0.9] text-[{texto_color}] max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Foto fondo + overlay + bookmark =====
            foto_actual = fotos[i % len(fotos)] if fotos else ''
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden flex flex-col items-center justify-center px-[120px] z-20">

      <!-- Foto de fondo -->
      <div class="absolute inset-0 bg-cover bg-center z-0 grayscale contrast-125"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay -->
      <div class="absolute inset-0 bg-[{bg_color}]/90 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Título -->
      <h1 class="font-garamond font-normal text-[100px] leading-[0.95] text-[{texto_color}] mb-10 z-20">
        {titulo}
      </h1>

      <!-- Texto formateado -->
      <div class="font-nunito text-[{texto_color}] text-[34px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-16 z-20">
        {formatear_texto_html(texto, accent_color)}
      </div>

      <!-- Bookmark + CTA -->
      <div class="flex items-center gap-3 z-20">
        <span class="font-nunito text-[{accent_color}] text-[20px] font-light tracking-widest uppercase">Guarda este post</span>
        {SVGS['bookmark'].format(clases=f'w-[36px] h-[36px] text-[{accent_color}]')}
      </div>

    </div>
"""
        else:
            # ===== CONTENIDO: Número héroe + texto alineado a la izquierda =====
            num_str = str(i).zfill(2)
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Número héroe colosal de fondo -->
      <span class="font-garamond font-normal text-[600px] text-[{texto_color}] opacity-5 absolute -left-[50px] bottom-[100px] z-0 leading-none">
        {num_str}
      </span>

      <!-- Contenido alineado a la izquierda -->
      <div class="absolute inset-0 z-10 flex flex-col justify-center px-[100px]">

        <!-- Línea superior amarilla de 2px -->
        <div class="w-[80px] h-[2px] bg-[{accent_color}] mb-8"></div>

        <!-- Título -->
        <h1 class="font-garamond font-normal text-[100px] leading-[0.95] text-[{texto_color}] mb-8 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] opacity-85 max-w-[700px]">
          {formatear_texto_html(texto, accent_color)}
        </div>

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
    * {{ box-shadow: none !important; text-shadow: none !important; margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    <!-- Textura blanca global con blend -->
    <div class="absolute inset-0 z-0 mix-blend-multiply opacity-40 grayscale contrast-125"
         style="background-image: url('{textura}'); background-size: cover;"></div>

    {slides_html}

  </div>
</body>
</html>'''


def plantilla_hero_minimalista(datos_array, paleta, imagenes_b64=None):
    """
    Genera un carrusel panorámico en estilo Hero Minimalista (Arquetipo E).
    Fotos full-bleed con overlay oscuro pesado en todos los slides.
    Contenido estrictamente centrado. Inspirado en Blockquote de Flowbite.
    Estructura de 3 Actos: PORTADA → CONTENIDO → CTA.
    """
    fotos = imagenes_b64.get('fotos', []) if imagenes_b64 else []
    total_slides = len(datos_array)
    ancho_total = total_slides * 1080
    bg_color = paleta['fondo']
    texto_color = paleta['texto']
    accent_color = paleta['acento']
    logo_inmo = imagenes_b64.get('logo_inmobiliaria') if imagenes_b64 else None

    slides_html = ""
    for i, slide in enumerate(datos_array):
        titulo = slide.get('titulo', '')
        texto = slide.get('texto', '')
        etiqueta = slide.get('etiqueta', '')
        es_portada = i == 0
        es_cta = i == total_slides - 1
        foto_actual = fotos[i % len(fotos)] if fotos else ''

        if es_portada:
            # ===== PORTADA: Foto full-bleed, overlay pesado, título centrado =====
            slides_html += f"""
    <!-- ========================= PORTADA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo full-bleed -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay pesado -->
      <div class="absolute inset-0 bg-[{bg_color}]/85 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=True)}

      <!-- Contenido estrictamente centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Etiqueta -->
        <span class="font-nunito text-[22px] font-bold uppercase tracking-widest text-[{accent_color}] mb-8">
          {etiqueta or 'GUÍA INMOBILIARIA'}
        </span>

        <!-- Título masivo centrado -->
        <h1 class="font-garamond font-normal text-[130px] leading-[1.15] text-[{texto_color}] max-w-[900px]">
          {titulo}
        </h1>

      </div>

    </div>
"""
        elif es_cta:
            # ===== CTA: Foto full-bleed, overlay pesado, centrado =====
            slides_html += f"""
    <!-- ========================= CTA {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo full-bleed -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay pesado -->
      <div class="absolute inset-0 bg-[{bg_color}]/85 z-10"></div>

      <!-- Logo cobranding -->
      {_logo_header(texto_color, logo_inmo, es_portada=False)}

      <!-- Contenido estrictamente centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Título -->
        <h1 class="font-garamond font-normal text-[100px] leading-[1.15] text-[{texto_color}] mb-10">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-80 mb-16">
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
            # ===== CONTENIDO: Foto full-bleed, overlay pesado, centrado =====
            slides_html += f"""
    <!-- ========================= CONTENIDO {i+1} ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative overflow-hidden z-20">

      <!-- Foto de fondo full-bleed -->
      <div class="absolute inset-0 bg-cover bg-center z-0"
           style="background-image: url('{foto_actual}');"></div>

      <!-- Overlay pesado -->
      <div class="absolute inset-0 bg-[{bg_color}]/85 z-10"></div>

      <!-- Contenido estrictamente centrado -->
      <div class="absolute inset-0 z-20 flex flex-col items-center justify-center text-center px-[120px]">

        <!-- Línea separadora centrada -->
        <div class="w-[80px] h-[2px] bg-[{accent_color}] mx-auto mb-8"></div>

        <!-- Título -->
        <h1 class="font-garamond font-normal text-[100px] leading-[1.15] text-[{texto_color}] mb-8 max-w-[800px]">
          {titulo}
        </h1>

        <!-- Texto formateado -->
        <div class="font-nunito text-[{texto_color}] text-[32px] font-light leading-[1.4] max-w-[700px] opacity-85">
          {formatear_texto_html(texto, accent_color)}
        </div>

      </div>

      <!-- Indicador: Desliza -->
      <div class="absolute bottom-[80px] right-[80px] flex items-center gap-3 z-30">
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
    * {{ box-shadow: none !important; text-shadow: none !important; margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ overflow: hidden; background: {bg_color}; }}
  </style>
</head>
<body>
  <div class="w-[{ancho_total}px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}]">

    {slides_html}

  </div>
</body>
</html>'''