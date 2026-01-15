# Scripts de Procesamiento

## Scripts Útiles

### `integrar_csv.py`
Integra los CSV de Nacional e Internacional en un solo `data.csv` unificado.

**Uso:**
```bash
cd _backup_scripts
python3 integrar_csv.py
```

Genera:
- `DATA/data.csv` - Base de datos unificada
- `DATA/data.json` - Versión JSON

---

### `extraer_mejorado.py`
Extrae coordenadas GPS de Google Maps para los lugares sin coordenadas.

**Uso:**
```bash
cd _backup_scripts
python3 extraer_mejorado.py
```

Características:
- Procesa solo obras sin coordenadas
- Guarda cada 10 obras automáticamente
- Se puede interrumpir con Ctrl+C y reanudar
- Usa múltiples métodos de extracción

---

### `requirements.txt`
Dependencias de Python necesarias.

**Instalar:**
```bash
pip install -r requirements.txt
```

---

## Notas

- Estos scripts son para **procesamiento de datos**, no para el sitio web
- El sitio web solo necesita `index.html` y `DATA/data.csv`
- Guardar estos scripts por si necesitas reprocesar datos en el futuro
