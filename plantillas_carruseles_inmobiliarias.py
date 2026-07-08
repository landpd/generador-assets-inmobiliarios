def disenio_landscape_5fotos(datos):
    """
    Arquetipo A: Arquitectónico Minimalista (Estilo "La Pradera")
    - 5 Slides panorámicos (5400 x 1350px).
    - Uso intensivo del espacio en blanco (Aire).
    - Tipografía masiva y elegante.
    - Regla de contraste: Textos blancos sobre fondos de acento/secundarios.
    """
    
    # Extracción de datos con valores por defecto
    img1 = datos.get("img1", "")
    img2 = datos.get("img2", "")
    img3 = datos.get("img3", "")
    img4 = datos.get("img4", "")
    img5 = datos.get("img5", "")
    logo = datos.get("logo", "")
    
    tipo_operacion = datos.get("tipo_operacion", "Propiedad en Venta").upper()
    precio = datos.get("precio", "Consultar precio")
    colonia_estado = datos.get("colonia_estado", "Ubicación Premium")
    calle = datos.get("calle", "Dirección Exclusiva")
    
    # Los atributos ya vienen como <div>Texto</div> desde main.py
    atributos_html = datos.get("atributos_html", "")

    # Colores corporativos (Reglas estrictas)
    bg_color = "#FAFAFA"
    text_color = "#212322"
    accent_color = "#F6BE00"
    secondary_color = "#009A9A"

    return f"""<!DOCTYPE html>
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
    
    /* Formato específico para los atributos inyectados */
    .atributos-lista div {{
        border-bottom: 1px solid rgba(33, 35, 34, 0.2);
        padding: 20px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 300;
        font-size: 32px;
        color: {text_color};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        justify-content: space-between;
    }}
  </style>
</head>
<body>
  <!-- CONTENEDOR MAESTRO PANORÁMICO (5 Slides = 5400px) -->
  <div class="w-[5400px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}] text-[{text_color}]">

    <!-- ========================= SLIDE 1: PORTADA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-center px-[100px] z-20">
      
      <!-- Etiqueta de Operación (Corchetes en acento, texto en color texto) -->
      <div class="mb-10 inline-block font-nunito font-bold text-[24px] tracking-[0.2em] uppercase">
        <span class="text-[{accent_color}]">[</span>
        <span class="text-[{text_color}]"> {tipo_operacion} </span>
        <span class="text-[{accent_color}]">]</span>
      </div>

      <!-- Título Principal (Nombre de la calle) -->
      <h1 class="font-garamond text-[140px] leading-[0.9] font-normal mb-8 max-w-[800px]">
        {calle}
      </h1>
      
      <!-- Ubicación Secundaria -->
      <p class="font-nunito text-[40px] font-light tracking-wide text-[{text_color}]/70 border-l-4 border-[{accent_color}] pl-6">
        {colonia_estado}
      </p>

      <!-- Logo Flotante Inferior -->
      <div class="absolute bottom-[100px] left-[100px]">
        <img src="{logo}" alt="Logo Inmobiliaria" class="max-h-[80px] max-w-[300px] object-contain opacity-80 filter grayscale brightness-0">
      </div>
    </div>

    <!-- ========================= SLIDE 2: HERO IMAGE ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex z-20 p-[80px]">
      <!-- Foto gigante que respira dentro del slide -->
      <div class="w-full h-full bg-cover bg-center shadow-2xl rounded-sm" style="background-image: url('{img1}');"></div>
      
      <!-- Texto GIGANTE que atraviesa el slide por detrás -->
      <span class="absolute top-[50%] -translate-y-1/2 -left-[200px] font-garamond text-[350px] text-[{text_color}]/5 whitespace-nowrap z-[-1] pointer-events-none">
        {calle}
      </span>
    </div>

    <!-- ========================= SLIDE 3: FICHA TÉCNICA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-center px-[120px] z-20">
      
      <div class="flex flex-row h-[900px] gap-10">
        
        <!-- Columna Izquierda: Datos (Atributos) -->
        <div class="w-[50%] flex flex-col justify-center">
            <h2 class="font-nunito font-bold text-[24px] tracking-[0.2em] text-[{accent_color}] uppercase mb-12">
              Características
            </h2>
            <div class="atributos-lista w-full">
                {atributos_html}
            </div>
        </div>

        <!-- Columna Derecha: Foto de detalle -->
        <div class="w-[50%] h-full bg-cover bg-center shadow-lg" style="background-image: url('{img2}');"></div>
      
      </div>

    </div>

    <!-- ========================= SLIDE 4: GALERÍA Y DETALLES ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-center px-[100px] z-20">
      <div class="grid grid-cols-2 grid-rows-2 gap-[40px] h-[1000px]">
         <!-- Foto Superior (Ocupa las 2 columnas) -->
         <div class="col-span-2 bg-cover bg-center shadow-md" style="background-image: url('{img3}');"></div>
         <!-- Fotos Inferiores -->
         <div class="bg-cover bg-center shadow-md" style="background-image: url('{img4}');"></div>
         <div class="bg-cover bg-center shadow-md" style="background-image: url('{img5}');"></div>
      </div>
    </div>

    <!-- ========================= SLIDE 5: CIERRE Y CTA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col items-center justify-center px-[100px] text-center z-20">
      
      <!-- Etiqueta de Precio -->
      <span class="font-nunito font-bold text-[28px] tracking-[0.1em] text-[{text_color}]/50 uppercase mb-4">
        Valor de esta propiedad
      </span>
      
      <!-- Precio Masivo -->
      <h2 class="font-garamond text-[160px] leading-none mb-16 text-[{text_color}]">
        {precio}
      </h2>

      <!-- CTA Botón (Texto sobre fondo claro) -->
      <div class="bg-[{text_color}] text-[#FAFAFA] px-[80px] py-[30px] font-nunito text-[32px] font-bold uppercase tracking-widest shadow-xl mb-24">
        Agenda tu visita
      </div>

      <!-- Logo Final -->
      <img src="{logo}" alt="Logo Inmobiliaria" class="max-h-[120px] max-w-[400px] object-contain filter grayscale brightness-0">

    </div>

  </div>
</body>
</html>"""


# =====================================================================
# ARQUETIPO B: ELEGANCIA EDITORIAL (Estilo Urbanismo / Premium)
# =====================================================================
def disenio_editorial_5fotos(datos):
    """
    Arquetipo B: Elegancia Editorial (Estilo Urbanismo / Premium)
    - 5 Slides panorámicos (5400 x 1350px).
    - Uso de columnas laterales (sidebars) sólidas de color #212322.
    - Acentos sutiles en #F6BE00.
    - Grids rígidas y líneas divisorias.
    NO usa uppercase en EB Garamond.
    """

    img1 = datos.get("img1", "")
    img2 = datos.get("img2", "")
    img3 = datos.get("img3", "")
    img4 = datos.get("img4", "")
    img5 = datos.get("img5", "")
    logo = datos.get("logo", "")

    tipo_operacion = datos.get("tipo_operacion", "Propiedad en Venta").upper()
    precio = datos.get("precio", "Consultar precio")
    colonia_estado = datos.get("colonia_estado", "Ubicación Premium")
    calle = datos.get("calle", "Dirección Exclusiva")
    atributos_html = datos.get("atributos_html", "")

    bg_color = "#FAFAFA"
    text_color = "#212322"
    accent_color = "#F6BE00"
    secondary_color = "#009A9A"

    return f"""<!DOCTYPE html>
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
    .atributos-lista div {{
        border-bottom: 1px solid rgba(33, 35, 34, 0.2);
        padding: 18px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 400;
        font-size: 28px;
        color: {text_color};
        text-transform: uppercase;
        letter-spacing: 0.06em;
        display: flex;
        justify-content: space-between;
    }}
  </style>
</head>
<body>
  <div class="w-[5400px] h-[1350px] flex flex-row relative overflow-hidden bg-[{bg_color}] text-[{text_color}]">

    <!-- SLIDE 1: PORTADA EDITORIAL -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row overflow-hidden">
      <!-- Sidebar sólida izquierda -->
      <div class="w-[320px] h-full bg-[{text_color}] flex flex-col justify-between px-[40px] py-[60px] z-20">
        <div>
          <span class="font-nunito font-bold text-[18px] tracking-[0.2em] text-[{accent_color}] uppercase">
            [ {tipo_operacion} ]
          </span>
        </div>
        <div>
          <img src="{logo}" alt="Logo" class="max-h-[60px] max-w-[200px] object-contain filter grayscale brightness-0 invert">
        </div>
      </div>
      <!-- Foto principal -->
      <div class="flex-1 h-full bg-cover bg-center" style="background-image: url('{img1}');"></div>
      <!-- Texto superpuesto abajo -->
      <div class="absolute bottom-[60px] left-[360px] right-[40px] z-20">
        <h1 class="font-garamond text-[100px] leading-[0.95] font-normal mb-4">
          {calle}
        </h1>
        <p class="font-nunito text-[32px] font-light text-[{text_color}]/70 border-l-4 border-[{accent_color}] pl-5">
          {colonia_estado}
        </p>
      </div>
    </div>

    <!-- SLIDE 2: GALERÍA EN CUADRÍCULA -->
    <div class="w-[1080px] h-full shrink-0 relative grid grid-cols-2 grid-rows-2 gap-[6px] p-[6px] bg-[{text_color}]">
      <div class="bg-cover bg-center" style="background-image: url('{img1}');"></div>
      <div class="bg-cover bg-center" style="background-image: url('{img2}');"></div>
      <div class="bg-cover bg-center" style="background-image: url('{img3}');"></div>
      <div class="bg-cover bg-center" style="background-image: url('{img4}');"></div>
    </div>

    <!-- SLIDE 3: FICHA TÉCNICA -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row overflow-hidden">
      <!-- Sidebar sólida izquierda -->
      <div class="w-[400px] h-full bg-[{text_color}] flex flex-col justify-center px-[50px] z-20">
        <h2 class="font-nunito font-bold text-[20px] tracking-[0.2em] text-[{accent_color}] uppercase mb-10">
          Características
        </h2>
        <div class="atributos-lista">
          {atributos_html}
        </div>
        <div class="mt-10 border-t border-[{accent_color}]/30 pt-6">
          <span class="font-garamond text-[42px]">{precio}</span>
        </div>
      </div>
      <!-- Foto de detalle -->
      <div class="flex-1 h-full bg-cover bg-center" style="background-image: url('{img2}');"></div>
    </div>

    <!-- SLIDE 4: FOTO INMERSIVA + TEXTO FANTASMA -->
    <div class="w-[1080px] h-full shrink-0 relative flex items-end overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('{img3}');"></div>
      <!-- Texto fantasma -->
      <span class="absolute top-[45%] -translate-y-1/2 -left-[150px] font-garamond text-[280px] text-[{text_color}]/5 whitespace-nowrap z-[-1] pointer-events-none">
        {calle}
      </span>
      <!-- Barra inferior -->
      <div class="w-full bg-[{text_color}]/80 backdrop-blur-sm px-[80px] py-[40px] z-20">
        <p class="font-nunito text-[28px] font-light text-[#FAFAFA] tracking-wide">
          {colonia_estado}
        </p>
      </div>
    </div>

    <!-- SLIDE 5: CIERRE Y CTA -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col items-center justify-center px-[100px] text-center bg-[{bg_color}]">
      <span class="font-nunito font-bold text-[24px] tracking-[0.1em] text-[{text_color}]/50 uppercase mb-4">
        Valor de esta propiedad
      </span>
      <h2 class="font-garamond text-[140px] leading-none mb-12 text-[{text_color}]">
        {precio}
      </h2>
      <div class="bg-[{text_color}] text-[#FAFAFA] px-[80px] py-[30px] font-nunito text-[32px] font-bold uppercase tracking-widest shadow-xl mb-20">
        Agenda tu visita
      </div>
      <img src="{logo}" alt="Logo" class="max-h-[100px] max-w-[350px] object-contain filter grayscale brightness-0">
    </div>

  </div>
</body>
</html>"""


# =====================================================================
# ARQUETIPO C: BLOQUE CORPORATIVO / INDUSTRIAL
# =====================================================================
def disenio_corporativo_5fotos(datos):
    """
    Arquetipo C: Bloque Corporativo / Industrial
    - 5 Slides panorámicos (5400 x 1350px).
    - Alto contraste (Color-Blocking): alterna fondos oscuros y claros.
    - Slide 1, 3, 5: fondo #212322, texto #FAFAFA.
    - Slide 2, 4: fondo #FAFAFA, texto #212322.
    - Slide 3: atributos ENORMES.
    - Slide 5: CTA bloque completo en #009A9A.
    NO usa uppercase en EB Garamond.
    """

    img1 = datos.get("img1", "")
    img2 = datos.get("img2", "")
    img3 = datos.get("img3", "")
    img4 = datos.get("img4", "")
    img5 = datos.get("img5", "")
    logo = datos.get("logo", "")

    tipo_operacion = datos.get("tipo_operacion", "Propiedad en Venta").upper()
    precio = datos.get("precio", "Consultar precio")
    colonia_estado = datos.get("colonia_estado", "Ubicación Premium")
    calle = datos.get("calle", "Dirección Exclusiva")
    atributos_html = datos.get("atributos_html", "")

    # Paleta
    dark_bg = "#212322"
    light_bg = "#FAFAFA"
    dark_text = "#212322"
    light_text = "#FAFAFA"
    accent_color = "#F6BE00"
    secondary_color = "#009A9A"

    return f"""<!DOCTYPE html>
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
    body {{ overflow: hidden; }}
    .attr-dark div {{
        border-bottom: 1px solid rgba(250, 250, 250, 0.15);
        padding: 22px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 700;
        font-size: 52px;
        color: {light_text};
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
    .attr-light div {{
        border-bottom: 1px solid rgba(33, 35, 34, 0.15);
        padding: 22px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 700;
        font-size: 52px;
        color: {dark_text};
        text-transform: uppercase;
        letter-spacing: 0.04em;
    }}
  </style>
</head>
<body>
  <div class="w-[5400px] h-[1350px] flex flex-row relative overflow-hidden">

    <!-- ========================= SLIDE 1: FONDO OSCURO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-center px-[100px] bg-[{dark_bg}] text-[{light_text}]">
      <div class="mb-10 inline-block font-nunito font-bold text-[22px] tracking-[0.2em] uppercase">
        <span class="text-[{accent_color}]">[</span>
        <span class="text-[{light_text}]"> {tipo_operacion} </span>
        <span class="text-[{accent_color}]">]</span>
      </div>
      <h1 class="font-garamond text-[120px] leading-[0.9] font-normal mb-8 max-w-[850px]">
        {calle}
      </h1>
      <p class="font-nunito text-[36px] font-light tracking-wide text-[{light_text}]/60 border-l-4 border-[{accent_color}] pl-6">
        {colonia_estado}
      </p>
      <div class="absolute bottom-[80px] left-[100px]">
        <img src="{logo}" alt="Logo" class="max-h-[70px] max-w-[280px] object-contain opacity-70 filter grayscale brightness-0 invert">
      </div>
    </div>

    <!-- ========================= SLIDE 2: FONDO CLARO — HERO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{light_bg}] flex items-center justify-center p-[60px]">
      <div class="w-full h-full bg-cover bg-center shadow-2xl" style="background-image: url('{img1}');"></div>
    </div>

    <!-- ========================= SLIDE 3: FONDO OSCURO — ATRIBUTOS ENORMES ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row bg-[{dark_bg}] text-[{light_text}] overflow-hidden">
      <!-- Atributos masivos -->
      <div class="w-[55%] h-full flex flex-col justify-center px-[80px]">
        <div class="attr-dark">
          {atributos_html}
        </div>
        <div class="mt-8">
          <span class="font-garamond text-[64px] text-[{accent_color}]">{precio}</span>
        </div>
      </div>
      <!-- Foto -->
      <div class="w-[45%] h-full bg-cover bg-center" style="background-image: url('{img2}');"></div>
    </div>

    <!-- ========================= SLIDE 4: FONDO CLARO — FOTO + TEXTO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row bg-[{light_bg}] overflow-hidden">
      <!-- Foto -->
      <div class="w-[55%] h-full bg-cover bg-center" style="background-image: url('{img3}');"></div>
      <!-- Texto lado derecho -->
      <div class="w-[45%] h-full flex flex-col justify-center px-[60px]">
        <h2 class="font-garamond text-[72px] leading-[1.0] font-normal text-[{dark_text}] mb-8">
          {calle}
        </h2>
        <p class="font-nunito text-[30px] font-light text-[{dark_text}]/60 mb-8">
          {colonia_estado}
        </p>
        <div class="w-16 h-[3px] bg-[{accent_color}] mb-8"></div>
        <p class="font-nunito text-[28px] font-light text-[{dark_text}]/80 leading-relaxed">
          Un espacio diseñado para quienes buscan calidad y ubicación sin compromisos.
        </p>
      </div>
    </div>

    <!-- ========================= SLIDE 5: FONDO OSCURO — CTA BLOQUE COMPLETO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-between bg-[{dark_bg}] text-[{light_text}]">
      <!-- Sección superior: galería miniaturas -->
      <div class="flex flex-row h-[600px]">
        <div class="w-[33.4%] h-full bg-cover bg-center" style="background-image: url('{img4}');"></div>
        <div class="w-[33.3%] h-full bg-cover bg-center" style="background-image: url('{img5}');"></div>
        <div class="w-[33.3%] h-full bg-cover bg-center" style="background-image: url('{img1}');"></div>
      </div>
      <!-- Sección inferior: precio + CTA -->
      <div class="flex-1 flex flex-col justify-center px-[80px]">
        <span class="font-nunito font-bold text-[22px] tracking-[0.1em] text-[{light_text}]/40 uppercase mb-2">
          Valor de esta propiedad
        </span>
        <h2 class="font-garamond text-[130px] leading-none mb-8 text-[{light_text}]">
          {precio}
        </h2>
      </div>
      <!-- CTA: Bloque completo -->
      <div class="w-full bg-[{secondary_color}] text-[{light_text}] py-[35px] text-center font-nunito text-[36px] font-bold uppercase tracking-widest">
        Agenda tu visita
      </div>
      <!-- Logo y despedida -->
      <div class="flex flex-row items-center justify-between px-[80px] py-[30px]">
        <img src="{logo}" alt="Logo" class="max-h-[60px] max-w-[250px] object-contain filter grayscale brightness-0 invert">
        <span class="font-nunito text-[20px] text-[{light_text}]/40 tracking-widest">PULPPO</span>
      </div>
    </div>

  </div>
</body>
</html>"""
