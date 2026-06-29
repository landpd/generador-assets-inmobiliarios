def disenio_vertical_3fotos(datos):
    """ Plantilla Clásica: 1080 x 1350 con 3 fotos """
    return f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@500&family=Nunito+Sans:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; width: 1080px; height: 1350px; background: #000; overflow: hidden; }}
        /* Agregado position: relative para poder anclar el logo al fondo del contenedor */
        .container {{ position: relative; display: flex; flex-direction: column; width: 1080px; height: 1350px; }}

        .img-box {{ width: 1080px; height: 450px; position: relative; overflow: hidden; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}

        .overlay {{
            position: absolute; top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(33, 35, 34, 0.3);
            display: flex; flex-direction: column; justify-content: space-between;
            padding: 40px 60px; box-sizing: border-box;
        }}

        .block-top {{ text-align: right; width: 100%; }}
        .block-middle {{ text-align: left; width: 100%; }}
        .block-bottom {{ text-align: right; width: 100%; }}

        .colonia {{ font-family: 'Nunito Sans', sans-serif; font-weight: 400; font-size: 18pt; text-transform: uppercase; color: #FAFAFA; margin-bottom: 5px; }}
        .calle {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 42pt; text-transform: none; color: #FAFAFA; margin: 0; line-height: 1.1; }}

        .tipo {{ font-family: 'Nunito Sans', sans-serif; font-weight: 900; font-size: 16pt; text-transform: none; color: #FAFAFA; margin-bottom: 5px; }}
        .precio {{ font-family: 'Nunito Sans', sans-serif; font-weight: 900; font-size: 16pt; text-transform: none; color: #FAFAFA; margin-bottom: 0; }}

        /* --- CORCHETES Y DIAGONALES AMARILLAS --- */
        .bracket {{ color: #F6BE00; font-weight: 600; margin: 0 5px; }}

        .atributos {{ font-family: 'Nunito Sans', sans-serif; font-weight: 400; font-size: 16pt; text-transform: none; color: #FAFAFA; line-height: 1.3; }}
        .atributos div::before {{ content: '/ '; color: #F6BE00; font-weight: 400; padding-right: 5px; }}

        .text-shadow {{ text-shadow: 1px 1px 4px rgba(0,0,0,0.4); }}

        /* --- LOGO INFERIOR CENTRADO --- */
        .logo-bottom {{
            position: absolute; 
            bottom: 50px; 
            left: 50%; 
            transform: translateX(-50%); /* Lo centra perfectamente en la horizontal */
            width: 280px; 
            height: 100px;
            display: flex; 
            justify-content: center; 
            align-items: center;
            z-index: 20;
        }}
        .logo-bottom img {{
            max-width: 100%; 
            max-height: 100%; 
            object-fit: contain;
            filter: brightness(0) invert(1); /* Pasa el logo a color blanco */
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <div class="img-box"><img src="{datos['img1']}"></div>
            <div class="img-box">
                <img src="{datos['img2']}">
                <div class="overlay">
                    <div class="block-top text-shadow">
                        <div class="tipo"><span class="bracket">[</span> {datos['tipo_operacion']} <span class="bracket">]</span></div>
                        <div class="precio">{datos['precio']}</div>
                    </div>
                    <div class="block-middle text-shadow">
                        <div class="colonia">{datos['colonia_estado']}</div>
                        <h1 class="calle">{datos['calle']}</h1>
                    </div>
                    <div class="block-bottom text-shadow">
                        <div class="atributos">
                            {datos['atributos_html']}
                        </div>
                    </div>
                </div>
            </div>
            <div class="img-box"><img src="{datos['img3']}"></div>

            <!-- Cajón del logotipo (Superpuesto hasta abajo del diseño) -->
            <div class="logo-bottom">
                <img src="{datos.get('logo', '')}">
            </div>
        </div>
    </body>
    </html>
    """

def disenio_landscape_5fotos(datos):
    """ Nueva Plantilla Landscape: 1920 x 1080 con 5 fotos """
    return f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Nunito+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; padding: 0; width: 1920px; height: 1080px; background: #FAFAFA; overflow: hidden; }}
        .container {{ position: relative; width: 1920px; height: 1080px; }}

        /* --- LOGO INMOBILIARIA (Cuadro oscuro superior izquierdo) --- */
        .logo-box {{
            position: absolute; left: 0px; top: 0px;
            width: 333px; height: 188px;
            background: #212322;
            display: flex; justify-content: center; align-items: center;
            z-index: 20; /* Asegura que esté por encima de la foto 1 */
        }}
        .logo-box img {{
            max-width: 277px; max-height: 94px; 
            object-fit: contain;
            /* Esta propiedad invierte los colores: de Negro a Blanco puro */
            filter: brightness(0) invert(1);
        }}

        /* --- FOTOS --- */
        .img-box {{ position: absolute; overflow: hidden; background: #eaeaea; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}

        /* Coordenadas exactas extraídas del diseño */
        .img1 {{ left: 0px; top: 0px; width: 1111px; height: 740px; z-index: 1; }}
        .img2 {{ left: 1180px; top: 124px; width: 740px; height: 616px; z-index: 1; }}
        .img3 {{ left: 1344px; top: 628px; width: 224px; height: 168px; z-index: 10; }}
        .img4 {{ left: 1624px; top: 628px; width: 224px; height: 168px; z-index: 10; }}
        .img5 {{ left: 1624px; top: 852px; width: 224px; height: 168px; z-index: 10; }}

        /* --- ETIQUETA SUPERIOR DERECHA --- */
        .tipo-etiqueta {{
            position: absolute; right: 47px; top: 40px;
            font-family: 'Nunito Sans', sans-serif; font-weight: 600; font-size: 32px;
            text-transform: none; color: #212322;
            text-align: right;
            z-index: 10;
        }}
        .bracket {{ color: #F6BE00; font-weight: 600; margin: 0 5px; }}

        /* --- ZONA DE DIRECCIÓN --- */
        .text-container {{
            position: absolute; left: 151px; top: 788px;
            width: 1400px;
            z-index: 10;
        }}
        .calle {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 57px; margin: 0; line-height: 1.1; color: #212322; }}
        .colonia {{ font-family: 'EB Garamond', serif; font-weight: 500; font-size: 57px; margin: 0; line-height: 1.2; padding-top: 10px; color: #212322; }}

        /* --- LÍNEA DIVISORIA GRIS --- */
        .divider {{
            position: absolute; left: 0px; top: 946px; 
            width: 735px; height: 1px;
            background-color: #B3B3B3;
        }}

        /* --- ATRIBUTOS CON GUIONES AMARILLOS --- */
        .atributos {{
            position: absolute; left: 792px; top: 935px;
            display: grid;
            grid-template-columns: auto auto; /* Mantiene 2 columnas */
            column-gap: 60px; row-gap: 15px;
            z-index: 10;
        }}
        .atributos div {{
            font-family: 'Nunito Sans', sans-serif; font-weight: 600; font-size: 31px;
            text-transform: none; color: #212322;
            white-space: nowrap;
        }}
        /* Inserta la diagonal amarilla automáticamente antes de cada atributo */
        .atributos div::before {{
            content: '/ '; 
            color: #F6BE00; 
            font-weight: 600;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <!-- CAJA OSCURA LOGO -->
            <div class="logo-box">
                <img src="{datos.get('logo', '')}">
            </div>

            <!-- ETIQUETA: TIPO DE PROPIEDAD -->
            <div class="tipo-etiqueta">
                <span class="bracket">[</span> {datos['tipo_operacion']} <span class="bracket">]</span>
            </div>

            <!-- GALERÍA DE FOTOS -->
            <div class="img-box img1"><img src="{datos['img1']}"></div>
            <div class="img-box img2"><img src="{datos['img2']}"></div>
            <div class="img-box img3"><img src="{datos['img3']}"></div>
            <div class="img-box img4"><img src="{datos['img4']}"></div>
            <div class="img-box img5"><img src="{datos['img5']}"></div>

            <!-- TEXTOS: CALLE Y COLONIA -->
            <div class="text-container">
                <h1 class="calle">{datos['calle']}</h1>
                <h2 class="colonia">{datos['colonia_estado']}</h2>
            </div>

            <!-- LÍNEA SEPARADORA -->
            <div class="divider"></div>

            <!-- ATRIBUTOS -->
            <div class="atributos">
                {datos['atributos_html']}
            </div>
        </div>
    </body>
    </html>
    """

def disenio_story_figma(datos):
    """ Nueva Plantilla Story 1080x1920 importada desde Figma """
    return f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500&family=Nunito+Sans:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ margin: 0; padding: 0; width: 1080px; height: 1920px; background: #FAFAFA; overflow: hidden; }}
        .container {{ position: relative; width: 1080px; height: 1920px; }}

        /* --- LOGO INMOBILIARIA --- */
        .logo-box {{
            position: absolute; left: 373px; top: 0px;
            width: 333px; height: 188px; background: #212322;
            display: flex; justify-content: center; align-items: center;
            z-index: 20; /* Asegura que esté por encima de la foto */
        }}
        .logo-box img {{
            max-width: 277px; max-height: 94px;
            object-fit: contain;
            filter: brightness(0) invert(1); /* Pasa el logo png a color blanco */
        }}

        /* --- FOTOS GRANDES --- */
        .img-box {{ position: absolute; overflow: hidden; background: #D9D9D9; z-index: 1; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}

        .img-top {{ top: 0px; left: 0px; width: 1080px; height: 354px; }}
        .img-mid {{ top: 413px; left: 0px; width: 1080px; height: 730px; }}
        .img-bot {{ top: 1560px; left: 0px; width: 1080px; height: 360px; }}

        /* --- FOTOS CHICAS --- */
        .img-mini-1 {{ top: 633px; left: 705px; width: 330px; height: 240px; z-index: 10; }}
        .img-mini-2 {{ top: 931px; left: 705px; width: 330px; height: 240px; z-index: 10; }}
        .img-mini-3 {{ top: 1358px; left: 705px; width: 330px; height: 240px; z-index: 10; }}

        /* --- TEXTOS PRINCIPALES --- */
        .text-zone {{
            position: absolute;
            top: 1171px;
            left: 99px;
            width: 800px;
            z-index: 10;
        }}
        .calle {{
            font-family: 'EB Garamond', serif; font-weight: 400; font-size: 40px;
            color: #212322; margin: 0; line-height: 1.1;
            /* Blindaje automático para textos largos */
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }}
        .colonia {{
            font-family: 'EB Garamond', serif; font-weight: 400; font-size: 40px;
            color: #212322; margin: 0; padding-top: 5px;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }}
        .operacion {{
            font-family: 'Nunito Sans', sans-serif; font-weight: 600; font-size: 25px;
            text-transform: none; color: #212322; margin-top: 15px;
        }}
        .bracket {{ 
            color: #F6BE00; font-weight: 600; margin: 0 5px; 
        }}

        /* --- LÍNEA DIVISORIA Y ATRIBUTOS --- */
        .divider {{
            position: absolute; top: 1363px; left: 0px;
            width: 312px; height: 2px; background-color: #D9D9D9;
        }}

        .atributos {{
            position: absolute; top: 1355px; left: 374px;
            display: flex; flex-direction: column; gap: 10px;
        }}
        .atributos div {{
            font-family: 'Nunito Sans', sans-serif; font-weight: 400; font-size: 22px;
            text-transform: none; color: #212322;
        }}
        .atributos div::before {{
            content: '/ '; color: #F6BE00; font-weight: 400; padding-right: 5px;
        }}
    </style>
    </head>
    <body>
        <div class="container">
            <!-- CAJA OSCURA LOGO -->
            <div class="logo-box">
                <img src="{datos.get('logo', '')}">
            </div>

            <!-- Fotos -->
            <div class="img-box img-top"><img src="{datos['img1']}"></div>
            <div class="img-box img-mid"><img src="{datos['img2']}"></div>
            <div class="img-box img-bot"><img src="{datos['img3']}"></div>

            <div class="img-box img-mini-1"><img src="{datos['img4']}"></div>
            <div class="img-box img-mini-2"><img src="{datos['img5']}"></div>
            <div class="img-box img-mini-3"><img src="{datos['img6']}"></div>

            <!-- Textos -->
            <div class="text-zone">
                <h1 class="calle">{datos['calle']}</h1>
                <h2 class="colonia">{datos['colonia_estado']}</h2>
                <div class="operacion"><span class="bracket">[</span> {datos['tipo_operacion']} <span class="bracket">]</span></div>
            </div>

            <!-- Detalles Inferiores -->
            <div class="divider"></div>
            <div class="atributos">
                {datos['atributos_html']}
            </div>

        </div>
    </body>
    </html>
    """

def disenio_carrusel_6fotos(datos):
    """ Plantilla Carrusel Panorámico: 6480 x 1350 (Se dividirá en 6 slides) """
    return f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Nunito+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ width: 6480px; height: 1350px; background: #FAFAFA; overflow: hidden; }}
        .container {{ position: relative; width: 6480px; height: 1350px; }}

        /* --- FOTOS (8 Fotografías) --- */
        .img-box {{ position: absolute; overflow: hidden; background: #D9D9D9; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}

        /* Coordenadas corregidas para flujo perfecto sin huecos */
        .img1 {{ left: 0px; top: 0px; width: 1080px; height: 1350px; z-index: 1; }}
        .img2 {{ left: 1181px; top: 170px; width: 1958px; height: 1010px; z-index: 1; }} /* Cruza Slide 2 y 3 */
        .img3 {{ left: 3300px; top: 0px; width: 476px; height: 645px; z-index: 1; }}
        .img4 {{ left: 3300px; top: 707px; width: 951px; height: 643px; z-index: 1; }}
        .img5 {{ left: 3836px; top: 0px; width: 967px; height: 645px; z-index: 1; }} /* Cruza Slide 4 y 5 */
        .img6 {{ left: 4388px; top: 707px; width: 951px; height: 643px; z-index: 1; }}
        .img7 {{ left: 5475px; top: 2px; width: 951px; height: 643px; z-index: 1; }}
        .img8 {{ left: 5475px; top: 705px; width: 415px; height: 645px; z-index: 1; }}

        /* --- OVERLAY OSCURO (Solo en la Foto 1) --- */
        .overlay {{
            position: absolute; left: 0px; top: 0px; width: 1080px; height: 1350px;
            background: rgba(33, 36, 34, 0.3); z-index: 2; pointer-events: none;
        }}

        /* --- LOGO INMOBILIARIA --- */
        .logo-box {{
            position: absolute; left: 518px; top: 0px;
            width: 428px; height: 255px; background: #212322;
            display: flex; justify-content: center; align-items: center; z-index: 10;
        }}
        .logo-box img {{
            max-width: 316px; max-height: 106px; object-fit: contain;
            filter: brightness(0) invert(1);
        }}

        /* --- TEXTOS PRINCIPALES --- */
        .calle {{
            position: absolute; left: 67px; top: 1134px; width: 900px;
            font-family: 'EB Garamond', serif; font-size: 40px; font-weight: 500; color: #FAFAFA; z-index: 10;
        }}
        .operacion {{
            position: absolute; left: 1181px; top: 61px;
            font-family: 'Nunito Sans', sans-serif; font-size: 28px; font-weight: 600; color: #212322; z-index: 10;
            text-transform: none;
        }}
        .bracket {{ color: #F6BE00; font-weight: 700; margin: 0 5px; }}

        .colonia {{
            position: absolute; left: 2324px; top: 1236px; width: 815px;
            font-family: 'EB Garamond', serif; font-size: 40px; font-weight: 400; color: #212322; text-align: right; z-index: 10;
        }}
        .linea {{
            position: absolute; left: 2488px; top: 1288px; width: 651px; height: 2px;
            background-color: #F6BE00; z-index: 10;
        }}

        /* --- ATRIBUTOS (Slide 5) --- */
        .atributos {{
            position: absolute; 
            left: 4863px; 
            bottom: 705px; /* Anclado al fondo para que crezca hacia arriba */
            height: 300px; /* Cajón invisible para contener los textos */
            display: flex;
            flex-direction: column;
            justify-content: flex-end; /* Alinea los textos al piso del cajón */
            gap: 15px;
            z-index: 10;
            /* writing-mode: vertical-rl; <-- Descomenta esto si quieres que las letras giren 90 grados */
        }}
        .atributos div {{
            font-family: 'Nunito Sans', sans-serif; font-size: 28px; font-weight: 500; color: #212322; text-transform: none;
        }}
        .atributos div::before {{
            content: '/ '; color: #F6BE00; font-weight: 600; padding-right: 5px;
        }}
        
        /* --- CTA FINAL: AGENDA TU VISITA (SLIDE 6) --- */
        .cta-box {{
            position: absolute; 
            left: 5890px; 
            top: 705px;   
            width: 590px; 
            height: 645px;
            display: flex;
            flex-direction: column;
            justify-content: center; /* Centra perfectamente en vertical */
            align-items: center;     /* Centra perfectamente en horizontal */
            gap: 35px; /* Separación entre el logo y los textos */
            z-index: 10;
        }}
        .cta-logo {{
            width: 214px;
            height: 72px;
            object-fit: contain;
        }}
        .cta-text-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 5px; /* Separación suave entre las líneas de texto */
        }}
        .cta-text-container div {{
            font-family: 'Nunito Sans', sans-serif; 
            font-size: 26px; 
            font-weight: 400; 
            color: #212322; 
        }}
        .cta-highlight {{
            font-weight: 600 !important;
        }}
        .cta-dash {{
            color: #F6BE00;
            font-weight: 600;
        }}

    </style>
    </head>
    <body>
        <div class="container">
            <!-- Capa oscura de Slide 1 -->
            <div class="overlay"></div>

            <!-- Logo Superior (Blanco) -->
            <div class="logo-box"><img src="{datos.get('logo', '')}"></div>

            <!-- Textos Principales -->
            <h1 class="calle">{datos['calle']}</h1>
            <div class="operacion"><span class="bracket">[</span> {datos['tipo_operacion']} <span class="bracket">]</span></div>
            <h2 class="colonia">{datos['colonia_estado']}</h2>
            <div class="linea"></div>
            
            <div class="atributos">
                {datos['atributos_html']}
            </div>

            <!-- CTA Final -->
            <div class="cta-box">
                <img class="cta-logo" src="{datos.get('logo', '')}">
                <div class="cta-text-container">
                    <div class="cta-highlight"><span class="cta-dash">—</span> Agenda tu visita <span class="cta-dash">—</span></div>
                    <div>para conocer</div>
                    <div>esta propiedad</div>
                    <div>en persona</div>
                </div>
            </div>

            <!-- 8 Fotografías (Img 9 removida) -->
            <div class="img-box img1"><img src="{datos.get('img1', '')}"></div>
            <div class="img-box img2"><img src="{datos.get('img2', '')}"></div>
            <div class="img-box img3"><img src="{datos.get('img3', '')}"></div>
            <div class="img-box img4"><img src="{datos.get('img4', '')}"></div>
            <div class="img-box img5"><img src="{datos.get('img5', '')}"></div>
            <div class="img-box img6"><img src="{datos.get('img6', '')}"></div>
            <div class="img-box img7"><img src="{datos.get('img7', '')}"></div>
            <div class="img-box img8"><img src="{datos.get('img8', '')}"></div>

        </div>
    </body>
    </html>
    """

def disenio_oferta_baja_precio(datos):
    """ Nueva Plantilla Story para Bajas de Precio: 1080 x 1920 con 1 foto """
    return f"""
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Nunito+Sans:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ width: 1080px; height: 1920px; background: #FFFFFF; overflow: hidden; }}
        .container {{ position: relative; width: 1080px; height: 1920px; }}

        /* --- LÍNEA VERTICAL DE FONDO --- */
        /* Cruza todo el diseño por detrás de la fotografía */
        .linea-eje {{
            position: absolute; left: 110px; top: 0px; 
            width: 3px; height: 1920px; background: #212322;
            z-index: 1;
        }}

        /* --- CAJÓN DEL LOGO (SUPERIOR DERECHA) --- */
        .logo-box {{
            position: absolute; top: 92px; left: 561px;
            width: 519px; height: 166px; background: #212322;
            display: flex; justify-content: center; align-items: center;
            z-index: 20;
        }}
        .logo-box img {{
            max-width: 335px; max-height: 114px; object-fit: contain;
            filter: brightness(0) invert(1); /* Lo pasa a color blanco */
        }}

        /* --- FOTOGRAFÍA PRINCIPAL --- */
        .img-box {{ 
            position: absolute; top: 346px; left: 0px; 
            width: 1080px; height: 804px; background: #D9D9D9; 
            overflow: hidden; z-index: 10; 
        }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}

        /* ========================================================= */
        /* --- STICKER DECORATIVO: "BAJA DE PRECIO" --- */
        /* ========================================================= */
        .sticker-wrapper {{ position: absolute; top: 0px; left: 0px; width: 1080px; height: 346px; z-index: 20; }}
        
        /* Cajas Negras con Texto */
        .box-baja {{
            position: absolute; top: 124px; left: 73px; width: 230px; height: 55px;
            background: #212322; transform: rotate(-4deg);
            display: flex; justify-content: center; align-items: center;
        }}
        .box-precio {{
            position: absolute; top: 191px; left: 112px; width: 204px; height: 59px;
            background: #212322; transform: rotate(-4deg);
            display: flex; justify-content: center; align-items: center;
        }}
        .box-text {{
            font-family: 'Nunito Sans', sans-serif; font-weight: 800; font-size: 47px; color: #FFFFFF; text-transform: uppercase;
        }}

        /* Líneas decorativas (Reconstruidas en CSS) */
        .dec-line {{ position: absolute; height: 3px; border-radius: 2px; }}
        .line-grey-1 {{ top: 113px; left: 64px; width: 37px; background: #D9D9D9; transform: rotate(-6deg); }}
        .line-grey-2 {{ top: 154px; left: 315px; width: 46px; background: #D9D9D9; transform: rotate(-4deg); }}
        .line-yellow-1 {{ top: 212px; left: 43px; width: 60px; background: #F6BE00; transform: rotate(-5deg); }}
        .line-yellow-2 {{ top: 253px; left: 227px; width: 107px; background: #F6BE00; transform: rotate(-4deg); }}
        .line-black-1 {{ top: 239px; left: 90px; width: 61px; background: #212322; transform: rotate(-4deg); }}
        .line-black-2 {{ top: 116px; left: 265px; width: 61px; background: #212322; transform: rotate(-4deg); }}
        
        /* Puntos decorativos */
        .dec-dot {{ position: absolute; border-radius: 50%; }}
        .dot-grey {{ top: 255px; left: 98px; width: 5px; height: 5px; background: #D9D9D9; }}
        .dot-black {{ top: 140px; left: 54px; width: 6px; height: 6px; background: #212322; }}
        .dot-yellow {{ top: 135px; left: 313px; width: 6px; height: 6px; background: #F6BE00; }}

        /* ========================================================= */
        /* --- TEXTOS INFERIORES PROTEGIDOS CON FLEXBOX --- */
        /* ========================================================= */
        .bottom-zone {{
            position: absolute; top: 1220px; left: 191px; width: 800px;
            display: flex; flex-direction: column; gap: 15px; z-index: 20;
        }}

        .operacion {{
            font-family: 'Nunito Sans', sans-serif; font-size: 25px; font-weight: 800; color: #212322; text-transform: uppercase;
        }}
        .bracket {{ color: #F6BE00; font-weight: 800; margin: 0 5px; }}

        .calle {{
            font-family: 'EB Garamond', serif; font-size: 40px; font-weight: 400; color: #212322; margin: 0; line-height: 1.1;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }}
        .colonia {{
            font-family: 'EB Garamond', serif; font-size: 40px; font-weight: 400; color: #212322; margin: 0; line-height: 1.1;
            display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
        }}

        /* Atributos en Grid 2x2 */
        .atributos {{
            display: grid; grid-template-columns: auto auto; column-gap: 50px; row-gap: 10px; margin-top: 10px;
        }}
        .atributos div {{
            font-family: 'Nunito Sans', sans-serif; font-size: 22px; font-weight: 600; color: #212322; text-transform: uppercase;
        }}
        .atributos div::before {{
            content: '/ '; color: #F6BE00; font-weight: 700; padding-right: 5px;
        }}

        .precio {{
            font-family: 'Nunito Sans', sans-serif; font-size: 48px; font-weight: 800; color: #212322; margin-top: 25px; text-transform: uppercase;
        }}

    </style>
    </head>
    <body>
        <div class="container">
            
            <!-- Eje vertical de fondo -->
            <div class="linea-eje"></div>

            <!-- Logo -->
            <div class="logo-box"><img src="{datos.get('logo', '')}"></div>

            <!-- Sticker Baja de Precio -->
            <div class="sticker-wrapper">
                <div class="dec-line line-grey-1"></div>
                <div class="dec-line line-black-2"></div>
                <div class="dec-line line-grey-2"></div>
                <div class="dec-dot dot-black"></div>
                <div class="dec-dot dot-yellow"></div>
                
                <div class="box-baja"><span class="box-text">BAJA DE</span></div>
                <div class="box-precio"><span class="box-text">PRECIO</span></div>
                
                <div class="dec-line line-yellow-1"></div>
                <div class="dec-line line-black-1"></div>
                <div class="dec-line line-yellow-2"></div>
                <div class="dec-dot dot-grey"></div>
            </div>

            <!-- Fotografía -->
            <div class="img-box"><img src="{datos.get('img1', '')}"></div>

            <!-- Textos Informativos -->
            <div class="bottom-zone">
                <div class="operacion"><span class="bracket">[</span> {datos['tipo_operacion']} <span class="bracket">]</span></div>
                <h1 class="calle">{datos['calle']}</h1>
                <h2 class="colonia">{datos['colonia_estado']}</h2>
                
                <div class="atributos">
                    {datos['atributos_html']}
                </div>
                
                <div class="precio">{datos['precio']}</div>
            </div>

        </div>
    </body>
    </html>
    """