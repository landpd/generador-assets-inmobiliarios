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
# ARQUETIPO C: BLOQUE CORPORATIVO / INDUSTRIAL
# =====================================================================
def disenio_corporativo_5fotos(datos):
    """
    Arquetipo C: Bloque Corporativo / Industrial
    - 5 Slides panorámicos (5400 x 1350px).
    - Alto contraste (Color-Blocking): alterna fondos oscuros y claros.
    - Slide 1, 3, 5: fondo #212322, texto #FAFAFA.
    - Slide 2, 4: fondo #FAFAFA, texto #212322.
    - Slide 1: Portada con doble foto (img1 a sangre + img6 flotante).
    - Slide 3: atributos compactos sin precio duplicado.
    - Slide 5: precio único + CTA bloque completo en #009A9A.
    NO usa uppercase en EB Garamond.
    """

    img1 = datos.get("img1", "")
    img2 = datos.get("img2", "")
    img3 = datos.get("img3", "")
    img4 = datos.get("img4", "")
    img5 = datos.get("img5", "")
    img6 = datos.get("img6", "")
    logo = datos.get("logo", "")

    tipo_operacion = datos.get("tipo_operacion", "Propiedad en Venta").upper()
    precio = datos.get("precio", "Consultar precio")
    colonia_estado = datos.get("colonia_estado", "Ubicación Premium")
    calle = datos.get("calle", "Dirección Exclusiva")
    atributos_html = datos.get("atributos_html", "")

    # Texturas dinámicas de Pexels
    textura_oscura = datos.get("textura_oscura", "")

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
        padding: 10px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 700;
        font-size: 28px;
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

    <!-- ========================= SLIDE 1: FONDO OSCURO — PORTADA DOBLE FOTO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{dark_bg}] text-[{light_text}] overflow-hidden">
      <!-- Textura polvo_blanco sobre fondo oscuro -->
      <div class="absolute inset-0 bg-cover bg-center mix-blend-screen opacity-15 pointer-events-none z-[1]" style="background-image: url('{textura_oscura}');"></div>

      <!-- Foto principal img1: mitad derecha a sangre -->
      <div class="absolute top-0 right-0 w-[540px] h-full bg-cover bg-center z-[2]" style="background-image: url('{img1}');"></div>

      <!-- Columna izquierda: contenido editorial sobre fondo oscuro -->
      <div class="relative z-[3] flex flex-col justify-center h-full px-[70px] w-[540px]">
        <div class="mb-10 inline-block font-nunito font-bold text-[22px] tracking-[0.2em] uppercase">
          <span class="text-[{accent_color}]">[</span>
          <span class="text-[{light_text}]"> {tipo_operacion} </span>
          <span class="text-[{accent_color}]">]</span>
        </div>
        <h1 class="font-garamond text-[110px] leading-[1.1] font-normal mb-8 max-w-[460px]">
          {calle}
        </h1>
        <p class="font-nunito text-[34px] font-light tracking-wide text-[{light_text}]/60 border-l-4 border-[{accent_color}] pl-6">
          {colonia_estado}
        </p>
      </div>

      <!-- Logo -->
      <div class="absolute bottom-[80px] left-[70px] z-[4]">
        <img src="{logo}" alt="Logo" class="max-h-[70px] max-w-[280px] object-contain opacity-70 filter grayscale brightness-0 invert">
      </div>
    </div>

    <!-- ========================= SLIDE 2: FONDO CLARO — HERO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{light_bg}] flex items-center justify-center p-[60px]">
      <div class="w-full h-full bg-cover bg-center shadow-2xl" style="background-image: url('{img2}');"></div>
    </div>

    <!-- ========================= SLIDE 3: FONDO OSCURO — ATRIBUTOS COMPACTOS ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row bg-[{dark_bg}] text-[{light_text}] overflow-hidden">
      <!-- Textura polvo_blanco -->
      <div class="absolute inset-0 bg-cover bg-center mix-blend-screen opacity-15 pointer-events-none z-[1]" style="background-image: url('{textura_oscura}');"></div>

      <!-- Atributos compactos (sin precio — precio solo en Slide 5) -->
      <div class="relative z-[2] w-[55%] h-full flex flex-col justify-center px-[80px]">
        <h2 class="font-nunito font-bold text-[24px] tracking-[0.2em] text-[{accent_color}] uppercase mb-10">
          Características
        </h2>
        <div class="attr-dark">
          {atributos_html}
        </div>
      </div>
      <!-- Foto -->
      <div class="relative z-[2] w-[45%] h-full bg-cover bg-center" style="background-image: url('{img3}');"></div>
    </div>

    <!-- ========================= SLIDE 4: FONDO CLARO — FOTO + TEXTO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-row bg-[{light_bg}] overflow-hidden">
      <!-- Foto -->
      <div class="w-[55%] h-full bg-cover bg-center" style="background-image: url('{img4}');"></div>
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
      <!-- Textura polvo_blanco -->
      <div class="absolute inset-0 bg-cover bg-center mix-blend-screen opacity-15 pointer-events-none z-[1]" style="background-image: url('{textura_oscura}');"></div>

      <!-- Sección superior: galería miniaturas -->
      <div class="relative z-[2] flex flex-row h-[600px]">
        <div class="w-[33.4%] h-full bg-cover bg-center" style="background-image: url('{img5}');"></div>
        <div class="w-[33.3%] h-full bg-cover bg-center" style="background-image: url('{img1}');"></div>
        <div class="w-[33.3%] h-full bg-cover bg-center" style="background-image: url('{img6}');"></div>
      </div>
      <!-- Sección inferior: precio + CTA -->
      <div class="relative z-[2] flex-1 flex flex-col justify-center px-[80px]">
        <span class="font-nunito font-bold text-[22px] tracking-[0.1em] text-[{light_text}]/40 uppercase mb-2">
          Valor de esta propiedad
        </span>
        <h2 class="font-garamond text-[130px] leading-none mb-8 text-[{light_text}]">
          {precio}
        </h2>
      </div>
      <!-- CTA: Bloque completo -->
      <div class="relative z-[2] w-full bg-[{secondary_color}] text-[{light_text}] py-[35px] text-center font-nunito text-[36px] font-bold uppercase tracking-widest">
        Agenda tu visita
      </div>
      <!-- Logo y despedida -->
      <div class="relative z-[2] flex flex-row items-center justify-between px-[80px] py-[30px]">
        <img src="{logo}" alt="Logo" class="max-h-[60px] max-w-[250px] object-contain filter grayscale brightness-0 invert">
        <span class="font-nunito text-[20px] text-[{light_text}]/40 tracking-widest">PULPPO</span>
      </div>
    </div>

  </div>
</body>
</html>"""


# =====================================================================
# ARQUETIPO C: BLOQUE CORPORATIVO — MODO CLARO
# =====================================================================
def disenio_corporativo_claro_5fotos(datos):
    """
    Arquetipo C: Bloque Corporativo / Industrial — Modo Claro
    - 5 Slides panorámicos (5400 x 1350px).
    - Fondo claro #FAFAFA, textos #212322.
    - Slide 1: Portada corporativa clara con foto bloque.
    - Slides 2-3 (2160px): Centro panorámico con img2 GIGANTE que
      cruza ambos slides, atributos ENORMES estilo corporativo.
    - Slide 4: Cuadrícula estructurada con img3, img4, img5.
    - Slide 5: CTA masivo con botón bg-[#009A9A] ancho completo.
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

    # Texturas dinámicas de Pexels
    textura_clara = datos.get("textura_clara", "")

    light_bg = "#FAFAFA"
    dark_text = "#212322"
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
    body {{ overflow: hidden; background: {light_bg}; }}
    .attr-corp-light div {{
        border-bottom: 2px solid rgba(33, 35, 34, 0.12);
        padding: 20px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 700;
        font-size: 40px;
        color: {dark_text};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        display: flex;
        justify-content: space-between;
    }}
    .attr-corp-light div:last-child {{
        border-bottom: none;
    }}
  </style>
</head>
<body>
  <!-- CONTENEDOR MAESTRO PANORÁMICO (5 Slides = 5400px) -->
  <div class="w-[5400px] h-[1350px] flex flex-row relative overflow-hidden bg-[{light_bg}] text-[{dark_text}]">

    <!-- Textura de fondo global -->
    <div class="absolute inset-0 z-0 opacity-10 mix-blend-multiply bg-cover bg-center" style="background-image: url('{textura_clara}'); pointer-events: none;"></div>

    <!-- ========================= SLIDE 1: PORTADA CORPORATIVA CLARA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col bg-[{light_bg}] z-20">

      <!-- Barra superior: logo + etiqueta -->
      <div class="flex items-center justify-between px-[80px] pt-[60px]">
        <img src="{logo}" alt="Logo" class="max-h-[60px] max-w-[220px] object-contain filter grayscale brightness-0">
        <div class="font-nunito font-bold text-[20px] tracking-[0.25em] uppercase">
          <span class="text-[{accent_color}]">[</span>
          <span> {tipo_operacion} </span>
          <span class="text-[{accent_color}]">]</span>
        </div>
      </div>

      <!-- Cuerpo: título + ubicación -->
      <div class="flex-1 flex flex-col justify-center px-[80px]">
        <h1 class="font-garamond text-[120px] leading-[0.9] font-normal mb-6 max-w-[850px]">
          {calle}
        </h1>
        <div class="flex items-center gap-5">
          <div class="w-[50px] h-[3px] bg-[{accent_color}]"></div>
          <p class="font-nunito text-[32px] font-light tracking-wide text-[{dark_text}]/60">
            {colonia_estado}
          </p>
        </div>
      </div>

      <!-- Bloque de foto corporativo (img1) -->
      <div class="absolute bottom-0 left-0 right-0 h-[380px] bg-cover bg-center" style="background-image: url('{img1}');"></div>

      <!-- Número de slide -->
      <span class="absolute bottom-[400px] right-[60px] font-nunito font-bold text-[16px] tracking-[0.3em] text-[{dark_text}]/15 uppercase z-10">01 — 05</span>
    </div>

    <!-- ========================= SLIDES 2-3: PANORÁMICO CENTRAL (2160px) ========================= -->
    <div class="w-[2160px] h-full shrink-0 relative flex flex-col bg-[{light_bg}] z-20">

      <!-- Sección superior: foto gigante centrada -->
      <div class="flex-1 flex items-center justify-center px-[60px] pt-[60px]">
        <div class="w-[1600px] h-[800px] bg-cover bg-center shadow-xl" style="background-image: url('{img2}');"></div>
      </div>

      <!-- Sección inferior: atributos ENORMES estilo corporativo -->
      <div class="px-[100px] pb-[50px] pt-[30px]">
        <div class="attr-corp-light">
          {atributos_html}
        </div>
      </div>

      <!-- Líneas divisorias verticales que marcan los cortes de slide -->
      <div class="absolute top-0 left-0 w-[1px] h-full bg-[{dark_text}]/5 z-30"></div>
      <div class="absolute top-0 right-0 w-[1px] h-full bg-[{dark_text}]/5 z-30"></div>
    </div>

    <!-- ========================= SLIDE 4: CUADRÍCULA ESTRUCTURADA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col bg-[{light_bg}] z-20 p-[60px] gap-[30px]">

      <!-- Fila superior: img3 ancha -->
      <div class="flex-1 bg-cover bg-center shadow-md" style="background-image: url('{img3}');"></div>

      <!-- Fila inferior: img4 + img5 lado a lado -->
      <div class="flex-1 flex flex-row gap-[30px]">
        <div class="flex-1 bg-cover bg-center shadow-md" style="background-image: url('{img4}');"></div>
        <div class="flex-1 bg-cover bg-center shadow-md" style="background-image: url('{img5}');"></div>
      </div>

      <!-- Overlay de galería -->
      <div class="absolute bottom-[80px] left-[80px] z-10">
        <span class="font-nunito font-bold text-[16px] tracking-[0.3em] text-[{dark_text}]/30 uppercase bg-[{light_bg}]/80 px-[24px] py-[12px]">
          Galería · {colonia_estado}
        </span>
      </div>
    </div>

    <!-- ========================= SLIDE 5: CTA MASIVO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col bg-[{light_bg}] z-20">

      <!-- Logo y operación arriba -->
      <div class="flex items-center justify-between px-[80px] pt-[60px]">
        <img src="{logo}" alt="Logo" class="max-h-[50px] max-w-[200px] object-contain filter grayscale brightness-0">
        <div class="font-nunito font-bold text-[16px] tracking-[0.25em] text-[{dark_text}]/30 uppercase">
          <span class="text-[{accent_color}]">[</span>
          <span> {tipo_operacion} </span>
          <span class="text-[{accent_color}]">]</span>
        </div>
      </div>

      <!-- Centro: precio masivo + label -->
      <div class="flex-1 flex flex-col items-center justify-center px-[80px] text-center">
        <span class="font-nunito font-bold text-[24px] tracking-[0.15em] text-[{dark_text}]/30 uppercase mb-4">
          Valor de esta propiedad
        </span>
        <h2 class="font-garamond text-[110px] leading-none mb-10 text-[{dark_text}]">
          {precio}
        </h2>
        <div class="w-[100px] h-[2px] bg-[{accent_color}] mb-10"></div>
      </div>

      <!-- CTA GIGANTE de ancho completo -->
      <div class="bg-[{secondary_color}] text-[{light_bg}] w-full py-[35px] text-center font-nunito text-[36px] font-bold uppercase tracking-widest shadow-xl">
        Agenda tu visita
      </div>

      <!-- Footer -->
      <div class="flex items-center justify-center px-[80px] py-[25px]">
        <span class="font-nunito text-[16px] tracking-[0.3em] text-[{dark_text}]/15 uppercase">Pulppo</span>
      </div>
    </div>

  </div>
</body>
</html>"""


# =====================================================================
# ARQUETIPO D: DINÁMICO ALTERNADO (8 FOTOS)
# =====================================================================
def disenio_dinamico_alternado_5fotos(datos):
    """
    Arquetipo D: Dinámico Alternado (5 Slides / 8 Fotos)
    - 5 Slides panorámicos (5400 x 1350px).
    - Alternancia estricta de fondos:
      Slides 1,3 → fondo #212322 (oscuro), texto #FAFAFA.
      Slides 2,4 → fondo #FAFAFA (claro), texto #212322.
      Slide 5   → fondo #FAFAFA (claro), texto #212322.
    - Numeración estricta: la portada NO cuenta. Slide 2 = '01', etc.
    - EB Garamond NUNCA uppercase, SIEMPRE leading-[1.1].
    - CTA final con botón bg-[#009A9A] y texto blanco.
    """

    img1 = datos.get("img1", "")
    img2 = datos.get("img2", "")
    img3 = datos.get("img3", "")
    img4 = datos.get("img4", "")
    img5 = datos.get("img5", "")
    img6 = datos.get("img6", "")
    img7 = datos.get("img7", "")
    img8 = datos.get("img8", "")
    logo = datos.get("logo", "")

    tipo_operacion = datos.get("tipo_operacion", "Propiedad en Venta").upper()
    precio = datos.get("precio", "Consultar precio")
    colonia_estado = datos.get("colonia_estado", "Ubicación Premium")
    calle = datos.get("calle", "Dirección Exclusiva")
    atributos_html = datos.get("atributos_html", "")

    # Texturas dinámicas de Pexels
    textura_oscura = datos.get("textura_oscura", "")

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
    .attr-light div {{
        border-bottom: 1px solid rgba(33, 35, 34, 0.12);
        padding: 12px 0;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 700;
        font-size: 28px;
        color: {dark_text};
        text-transform: uppercase;
        letter-spacing: 0.04em;
        display: flex;
        justify-content: space-between;
    }}
    .num-bg {{
        position: absolute;
        font-family: 'Nunito Sans', sans-serif;
        font-weight: 900;
        font-size: 360px;
        line-height: 1;
        opacity: 0.04;
        pointer-events: none;
        user-select: none;
        z-index: 0;
    }}
  </style>
</head>
<body>
  <div class="w-[5400px] h-[1350px] flex flex-row relative overflow-hidden">

    <!-- ========================= SLIDE 1: PORTADA — OSCURO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{dark_bg}] text-[{light_text}] overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-center mix-blend-screen opacity-15 pointer-events-none z-[1]" style="background-image: url('{textura_oscura}');"></div>
      <div class="absolute inset-0 bg-cover bg-center z-[2]" style="background-image: url('{img1}');"></div>
      <div class="absolute inset-0 bg-[{dark_bg}]/60 z-[3]"></div>
      <div class="relative z-[4] flex flex-col justify-between h-full px-[70px] py-[80px]">
        <div class="inline-block font-nunito font-bold text-[22px] tracking-[0.2em] uppercase">
          <span class="text-[{accent_color}]">[</span>
          <span> {tipo_operacion} </span>
          <span class="text-[{accent_color}]">]</span>
        </div>
        <div class="flex-1 flex flex-col justify-center">
          <h1 class="font-garamond text-[110px] leading-[1.1] font-normal max-w-[800px] mb-8">
            {calle}
          </h1>
          <div class="flex items-center gap-5">
            <div class="w-[50px] h-[3px] bg-[{accent_color}]"></div>
            <p class="font-nunito text-[30px] font-light tracking-wide text-[{light_text}]/60">
              {colonia_estado}
            </p>
          </div>
        </div>
        <div>
          <img src="{logo}" alt="Logo" class="max-h-[60px] max-w-[250px] object-contain opacity-70 filter grayscale brightness-0 invert">
        </div>
      </div>
    </div>

    <!-- ========================= SLIDE 2: ATRIBUTOS — CLARO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{light_bg}] text-[{dark_text}] overflow-hidden">
      <span class="num-bg text-[{dark_text}] top-[50%] -translate-y-1/2 -left-[60px]">01</span>
      <div class="relative z-[2] flex flex-row h-full">
        <div class="w-[50%] h-full flex flex-col justify-center px-[60px]">
          <h2 class="font-nunito font-bold text-[22px] tracking-[0.2em] text-[{accent_color}] uppercase mb-8">
            Características
          </h2>
          <div class="attr-light">
            {atributos_html}
          </div>
        </div>
        <div class="w-[50%] h-full flex flex-col">
          <div class="flex-1 bg-cover bg-center" style="background-image: url('{img2}');"></div>
          <div class="flex-1 bg-cover bg-center border-t border-[{dark_text}]/10" style="background-image: url('{img3}');"></div>
        </div>
      </div>
    </div>

    <!-- ========================= SLIDE 3: GALERÍA 1 — OSCURO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{dark_bg}] text-[{light_text}] overflow-hidden">
      <div class="absolute inset-0 bg-cover bg-center mix-blend-screen opacity-15 pointer-events-none z-[1]" style="background-image: url('{textura_oscura}');"></div>
      <span class="num-bg text-[{light_text}] bottom-[60px] left-[60px]">02</span>
      <div class="relative z-[2] flex flex-col p-[40px] gap-[20px] h-full">
        <div class="flex-[3] bg-cover bg-center shadow-lg" style="background-image: url('{img4}');"></div>
        <div class="flex-[2] flex flex-row gap-[20px]">
          <div class="flex-1 bg-cover bg-center shadow-lg" style="background-image: url('{img5}');"></div>
          <div class="flex-1 bg-cover bg-center shadow-lg" style="background-image: url('{img6}');"></div>
        </div>
      </div>
    </div>

    <!-- ========================= SLIDE 4: GALERÍA 2 — CLARO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{light_bg}] text-[{dark_text}] overflow-hidden">
      <span class="num-bg text-[{dark_text}] top-[50%] -translate-y-1/2 -right-[60px]">03</span>
      <div class="relative z-[2] flex flex-row gap-[20px] p-[50px] h-full">
        <div class="flex-1 bg-cover bg-center shadow-md" style="background-image: url('{img7}');"></div>
        <div class="flex-1 bg-cover bg-center shadow-md" style="background-image: url('{img8}');"></div>
      </div>
    </div>

    <!-- ========================= SLIDE 5: CTA — CLARO ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative bg-[{light_bg}] text-[{dark_text}] flex flex-col overflow-hidden z-20">
      <div class="flex-1 flex flex-col items-center justify-center px-[80px] text-center">
        <span class="font-nunito font-bold text-[22px] tracking-[0.15em] text-[{dark_text}]/30 uppercase mb-4">
          Valor de esta propiedad
        </span>
        <h2 class="font-garamond text-[110px] leading-[1.1] mb-10 text-[{dark_text}]">
          {precio}
        </h2>
        <img src="{logo}" alt="Logo" class="max-h-[80px] max-w-[300px] object-contain filter grayscale brightness-0 mb-4">
      </div>
      <div class="w-full bg-[{secondary_color}] text-[#FAFAFA] py-[40px] text-center font-nunito text-[38px] font-bold uppercase tracking-widest shadow-xl">
        Agenda tu visita
      </div>
      <div class="flex items-center justify-center px-[80px] py-[25px]">
        <span class="font-nunito text-[16px] tracking-[0.3em] text-[{dark_text}]/15 uppercase">Pulppo</span>
      </div>
    </div>

  </div>
</body>
</html>"""


# =====================================================================
# DICCIONARIO DE REGISTRO (Exportaciones)
# =====================================================================
# Las funciones se registran en PLANTILLAS_DISPONIBLES dentro de pages/2_Automatizacion_Metricool.py
