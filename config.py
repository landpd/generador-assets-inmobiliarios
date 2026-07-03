from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()

DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"
FOTOS_DIR = ASSETS_DIR / "fotos"
LOGOS_DIR = ASSETS_DIR / "logos"
GRAFICOS_DIR = ASSETS_DIR / "graficos"
OUTPUT_DIR = BASE_DIR / "output"
STOCK_DIR = ASSETS_DIR / "stock"

# Asegurar que las carpetas existan al importar este módulo
for directory in [DATA_DIR, ASSETS_DIR, FOTOS_DIR, LOGOS_DIR, GRAFICOS_DIR, OUTPUT_DIR]:
    directory.mkdir(parents=True, exist_ok=True)