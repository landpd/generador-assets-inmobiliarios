(function () {
    // 1. Preguntar las rutas
    var csvFilePath = prompt("Ingresa la ruta absoluta de tu archivo CSV (ej. C:\\ruta\\datos.csv):");
    if (!csvFilePath) return;

    var photoFolderName = prompt("Nombre de la carpeta principal de Medios en el proyecto (Fotos/Videos):", "Medios");
    var audioFolderName = prompt("Nombre de la carpeta principal de Audios en el proyecto:", "Audios");

    var comp = app.project.activeItem;
    if (!comp || !(comp instanceof CompItem)) {
        alert("Por favor selecciona/abre tu composición plantilla.");
        return;
    }

    // Funciones de ayuda
    function findFolder(name) {
        for (var i = 1; i <= app.project.numItems; i++) {
            var item = app.project.item(i);
            if (item instanceof FolderItem && item.name === name) return item;
        }
        return null;
    }

    function findFootageRecursive(folder, name) {
        if (!name || name === "") return null;
        for (var i = 1; i <= folder.numItems; i++) {
            var item = folder.item(i);
            if (item instanceof FootageItem && item.name === name) {
                return item;
            } else if (item instanceof FolderItem) {
                var foundInside = findFootageRecursive(item, name);
                if (foundInside) return foundInside;
            }
        }
        return null; 
    }

    function getLayerByName(composition, name) {
        for (var i = 1; i <= composition.layers.length; i++) {
            if (composition.layers[i].name === name) return composition.layers[i];
        }
        return null;
    }

    // Lector inteligente de CSV compatible con ExtendScript
    function parseCSV(str) {
        var arr = [];
        var quote = false;
        var cell = '';
        for (var c = 0; c < str.length; c++) {
            var letra = str[c]; // <-- CORREGIDO: "char" era una palabra reservada en After Effects
            if (letra === '"' && str[c+1] === '"') {
                cell += '"'; 
                c++; 
            } else if (letra === '"') {
                quote = !quote;
            } else if (letra === ',' && !quote) {
                arr.push(cell);
                cell = '';
            } else {
                cell += letra;
            }
        }
        arr.push(cell);
        return arr;
    }

    var mediaFolder = findFolder(photoFolderName);
    var audioFolder = findFolder(audioFolderName);

    if (!mediaFolder) {
        alert("Error: Asegúrate de tener la carpeta '" + photoFolderName + "' creada en el panel de proyecto.");
        return;
    }

    var audioList = [];
    function gatherAudios(folder) {
        for (var a = 1; a <= folder.numItems; a++) {
            var item = folder.item(a);
            if (item instanceof FootageItem) {
                audioList.push(item);
            } else if (item instanceof FolderItem) {
                gatherAudios(item); 
            }
        }
    }
    
    if (audioFolder) {
        gatherAudios(audioFolder);
    }

    // 2. Leer el CSV
    var csvFile = new File(csvFilePath);
    if(!csvFile.open("r")) {
        alert("No se pudo abrir el archivo CSV.");
        return;
    }
    var csvData = csvFile.read();
    csvFile.close();

    var lines = csvData.split("\n");
    
    // USAMOS EL LECTOR INTELIGENTE PARA LOS ENCABEZADOS
    var headers = parseCSV(lines[0].replace(/\r/g, "")); 
    var columnIndexes = {};

    for (var j = 0; j < headers.length; j++) {
        columnIndexes[headers[j]] = j;
    }

    app.beginUndoGroup("Generar Videos Bulk");

    // 3. Iterar por cada fila del CSV
    for (var k = 1; k < lines.length; k++) {
        var cleanLine = lines[k].replace(/\r/g, "");
        if (cleanLine === "") continue; 

        // USAMOS EL LECTOR INTELIGENTE PARA LA FILA DE DATOS
        var cells = parseCSV(cleanLine);
        var name = cells[columnIndexes["Name"]];
        var rowData = {};

        for (var l = 0; l < headers.length; l++) {
            rowData[headers[l]] = cells[l];
        }

        // Duplicar la comp principal
        var newComp = comp.duplicate();
        newComp.name = name ? name : "Propiedad_" + k;

        // ==========================================
        //  REEMPLAZO DE TEXTOS NORMALES
        // ==========================================
        function setTextLayer(layerName, csvColumn) {
            var layer = getLayerByName(newComp, layerName);
            if (layer) {
                var value = rowData[csvColumn];
                var valClean = (value !== undefined && value !== null) ? value.toString() : " ";
                if(valClean === "" || valClean.toLowerCase() === "nan") valClean = " ";
                layer.property("Source Text").setValue(valClean);
            }
        }

        setTextLayer("Calle", "Calle");
        setTextLayer("Colonia, Estado", "Colonia, Estado");
        setTextLayer("[ inmueble en operacion ]", "inmueble en operacion");
        // setTextLayer("Precio", "Precio"); // Descomentar si usas la capa Precio

        // ==========================================
        //  SINCRONIZACIÓN DE ATRIBUTOS Y GUIONES ( / )
        // ==========================================
        function processAttribute(csvColumn, textLayerName, slashLayerName) {
            var textLayer = getLayerByName(newComp, textLayerName);
            var slashLayer = getLayerByName(newComp, slashLayerName);
            
            var value = rowData[csvColumn];
            var valClean = (value !== undefined && value !== null) ? value.toString().replace(/^\s+|\s+$/g, '') : "";
            var valLower = valClean.toLowerCase();

            if (valClean === "" || valLower === "0" || valLower === "0.0" || valLower === "nan") {
                if (textLayer) textLayer.property("Source Text").setValue(" ");
                if (slashLayer) slashLayer.property("Source Text").setValue(" ");
            } else {
                if (textLayer) textLayer.property("Source Text").setValue(valClean);
                if (slashLayer) slashLayer.property("Source Text").setValue("/ ");
            }
        }

        processAttribute("habitaciones", "1 habitaciones", "/ 1");
        processAttribute("baños", "2 baños", "/ 2");
        processAttribute("estacionamientos", "3 estacionamientos", "/ 3");
        processAttribute("metros totales", "4 metros totales", "/ 4");

        // ==========================================
        //  REEMPLAZAR HASTA 10 MEDIOS (FOTOS/VIDEOS)
        // ==========================================
        for (var m = 1; m <= 10; m++) {
            var numStr = (m < 10) ? "0" + m : m.toString(); 
            var columnName = "Media_" + numStr;
            var layerName = "placeholder_" + numStr;
            
            var targetLayer = getLayerByName(newComp, layerName);
            var mediaFileName = rowData[columnName];

            if (targetLayer) {
                if (mediaFileName && mediaFileName !== "") {
                    var newMedia = findFootageRecursive(mediaFolder, mediaFileName);
                    
                    if (newMedia) {
                        targetLayer.replaceSource(newMedia, false);
                        targetLayer.enabled = true;
                    } else {
                        targetLayer.enabled = false;
                    }
                } else {
                    targetLayer.enabled = false;
                }
            }
        }

        // ==========================================
        //  AUDIO ALEATORIO
        // ==========================================
        if (audioList.length > 0) {
            var audioLayer = getLayerByName(newComp, "placeholder_audio");
            if (audioLayer) {
                var randomAudio = audioList[Math.floor(Math.random() * audioList.length)];
                audioLayer.replaceSource(randomAudio, false);
            }
        }
    }

    app.endUndoGroup();
    alert("¡Proceso completado con éxito! Se generaron todas las precomposiciones.");

})();