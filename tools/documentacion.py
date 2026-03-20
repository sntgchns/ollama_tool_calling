import os
def consultar_documento(nombre_archivo: str):
    base_dir = 'conocimiento'
    if not nombre_archivo.endswith('.md'): nombre_archivo += '.md'
    safe_path = os.path.join(base_dir, os.path.basename(nombre_archivo))
    try:
        if not os.path.exists(safe_path): return 'Error: No encontrado.'
        with open(safe_path, 'r', encoding='utf-8') as f: return {'contenido': f.read()}
    except Exception as e: return f'Error: {str(e)}'