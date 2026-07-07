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
      
      <!-- Etiqueta de Operación (Amarillo) -->
      <div class="mb-10 inline-block">
        <span class="font-nunito font-bold text-[24px] tracking-[0.2em] text-[{accent_color}] uppercase">
          [ {tipo_operacion} ]
        </span>
      </div>

      <!-- Título Principal (Nombre de la calle) -->
      <h1 class="font-garamond text-[140px] leading-[0.9] font-normal mb-8 max-w-[800px] uppercase">
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
      <span class="absolute top-[50%] -translate-y-1/2 -left-[200px] font-garamond text-[350px] text-[{text_color}]/5 whitespace-nowrap z-[-1] pointer-events-none uppercase">
        {calle}
      </span>
    </div>

    <!-- ========================= SLIDE 3: FICHA TÉCNICA ========================= -->
    <div class="w-[1080px] h-full shrink-0 relative flex flex-col justify-center px-[120px] z-20">
      
      <div class="flex flex-row h-[900px] gap-16">
        
        <!-- Columna Izquierda: Datos (Atributos) -->
        <div class="w-[45%] flex flex-col justify-center">
            <h2 class="font-nunito font-bold text-[24px] tracking-[0.2em] text-[{accent_color}] uppercase mb-12">
              Características
            </h2>
            <div class="atributos-lista w-full">
                {atributos_html}
            </div>
        </div>

        <!-- Columna Derecha: Foto de detalle -->
        <div class="w-[55%] h-full bg-cover bg-center shadow-lg" style="background-image: url('{img2}');"></div>
      
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
        Valor de Inversión
      </span>
      
      <!-- Precio Masivo -->
      <h2 class="font-garamond text-[160px] leading-none mb-16 text-[{text_color}]">
        {precio}
      </h2>

      <!-- CTA Botón (Cumpliendo regla estricta: Fondo Acento -> Texto Blanco) -->
      <div class="bg-[{accent_color}] text-[#FAFAFA] px-[80px] py-[30px] font-nunito text-[32px] font-bold uppercase tracking-widest shadow-xl mb-24">
        Agenda tu visita
      </div>

      <!-- Logo Final y Despedida -->
      <img src="{logo}" alt="Logo Inmobiliaria" class="max-h-[120px] max-w-[400px] object-contain mb-8 filter grayscale brightness-0">
      <p class="font-nunito text-[24px] font-light text-[{text_color}]/60 tracking-widest">
        WWW.PULPPO.COM
      </p>

    </div>

  </div>
</body>
</html>"""