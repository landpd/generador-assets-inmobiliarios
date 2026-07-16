"""Funciones auxiliares compartidas entre módulos."""


def formatear_atributo(valor, sufijos):
    """Formatea un atributo numérico con su sufijo correspondiente.

    Args:
        valor: Valor numérico (str, int, float).
        sufijos: str (siempre el mismo sufijo) o tuple (singular, plural).

    Returns:
        str: texto formateado (ej. "3 HABITACIONES") o "" si el valor es vacío/NaN.
    """
    val_str = str(valor).strip()
    if val_str.lower() in ['nan', 'none', '', '0', '0.0']:
        return ""
    if val_str.endswith('.0'):
        val_str = val_str[:-2]

    if isinstance(sufijos, tuple):
        sufijo_final = sufijos[0] if val_str == "1" else sufijos[1]
    else:
        sufijo_final = sufijos

    return f"{val_str} {sufijo_final}"