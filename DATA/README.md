# Dataset: Teatro Contemporáneo Español del Siglo XXI (TCE SXXI)

## 📊 Información General

Este dataset contiene información sobre **713 registros** de obras del Teatro Contemporáneo Español del Siglo XXI, incluyendo adaptaciones de clásicos del Siglo de Oro español, tanto nacionales como internacionales.

**Fuentes originales:**
- Nacional: `TCE SXXI - Nacional.csv` (581 registros)
- Internacional: `TCE SXXI - Internacional.csv` (132 registros)
- Web anterior: https://seahorse-app-kg7ca.ondigitalocean.app/

**Formato de datos:** El dataset se encuentra disponible en dos formatos:
- `data.csv` - Archivo CSV unificado con delimitador `|` (pipe)
- `data.json` - Archivo JSON estructurado

**Método de carga:** Los datos se cargan desde un archivo externo (`DATA/data.csv`) mediante `fetch()` en JavaScript, **NO están embebidos en el HTML**.

---

## 📋 Estructura de Datos

Cada registro contiene los siguientes campos:

| Campo | Tipo | Descripción | Completitud |
|-------|------|-------------|-------------|
| `id` | string | Identificador único numérico secuencial | 100% |
| `Autor/a` | string | Nombre del autor/a de la obra original | ~100% |
| `Obra` | string | Título de la obra teatral | ~100% |
| `Fecha de estreno` | string | Fecha de estreno (formato texto español) | ~74% |
| `Dirección` | string | Director/a de la puesta en escena | ~100% |
| `Compañía` | string | Compañía teatral que representa la obra | ~100% |
| `Festivales` | string | Festival(es) donde se presentó (separados por comas) | ~50% |
| `Lugar de estreno` | string | Teatro o lugar donde se estrenó | ~69% |
| `fechaFormat` | string | Fecha en formato ISO (mayormente vacío) | ~5% |
| `lat` | string | Latitud GPS del lugar de estreno | ~0% (inicialmente) |
| `lon` | string | Longitud GPS del lugar de estreno | ~0% (inicialmente) |
| `uuid` | string | Identificador único universal (UUID v4) | 100% |
| **`tipo`** | **string** | **"Nacional" o "Internacional"** | **100%** |

---

## 🗺️ Coordenadas Geográficas

Las coordenadas GPS (`lat`, `lon`) fueron obtenidas mediante **Google Maps**:
- Se buscó el nombre del teatro en Google Maps
- Se centraron las coordenadas en el teatro
- Se extrajeron de la URL generada por Google Maps

**Estado actual:**
- ❌ **713 registros** sin coordenadas inicialmente (100%)
- ℹ️ Use el script `scripts/extraer_coordenadas.py` para obtener coordenadas automáticamente de Google Maps

---

## 📈 Estadísticas del Dataset

### Datos Generales
- **Total de registros:** 713
  - **Nacional:** 581 registros (81.5%)
  - **Internacional:** 132 registros (18.5%)
- **Autores únicos:** ~30+
- **Obras únicas:** ~500+
- **Directores únicos:** ~500+
- **Compañías únicas:** ~550+
- **Lugares únicos:** ~400+
- **Festivales únicos:** ~80+

### Datos Faltantes
- **Sin coordenadas:** 713 registros inicialmente (100%) - usar script de extracción
- **Sin lugar de estreno:** Variable por tipo
- **Sin fecha de estreno:** Variable por tipo

---

## 👥 Top 10 Autores

| # | Autor/a | Nº de Obras |
|---|---------|-------------|
| 1 | Pedro Calderón de la Barca | 165 |
| 2 | Miguel de Cervantes | 155 |
| 3 | Lope de Vega | 131 |
| 4 | Tirso de Molina | 41 |
| 5 | Francisco de Rojas Zorrilla | 25 |
| 6 | Agustín Moreto | 13 |
| 7 | María de Zayas y Sotomayor | 12 |
| 8 | Lope de Rueda | 9 |
| 9 | Juan Ruiz de Alarcón | 7 |
| 10 | Vélez de Guevara | 5 |

> **Nota:** Los tres principales autores (Calderón, Cervantes y Lope de Vega) representan el **77% del total** de las obras registradas.

---

## 🎭 Top 10 Directores

| # | Director/a | Nº de Obras |
|---|------------|-------------|
| 1 | No disponible | 13 |
| 2 | Eduardo Vasco | 10 |
| 3 | Helena Pimenta | 7 |
| 4 | Eva del Palacio | 5 |
| 5 | Manuel Canseco | 4 |
| 6 | Laila Ripoll | 4 |
| 7 | Gabriel Garbisu | 4 |
| 8 | Mariano de Paco Serrano | 3 |
| 9 | Juan Polanco | 3 |
| 10 | César Barló | 3 |

---

## 🎪 Top 10 Festivales

| # | Festival | Apariciones |
|---|----------|-------------|
| 1 | Festival de Teatro Clásico de Almagro | 49 |
| 2 | Festival Internacional de Teatro Clásico de Almagro | 20 |
| 3 | No disponible | 13 |
| 4 | Festival Clásicos en Alcalá | 12 |
| 5 | Festival de Teatro Clásico de Cáceres | 9 |
| 6 | Festival internacional de Teatro Clásico de Almagro | 7 |
| 7 | Festival de Teatro Clásico de Olmedo | 7 |
| 8 | Festival Internacional de Teatro Clásico | 5 |
| 9 | Festival Clásicos de Alcalá | 4 |
| 10 | Festival de Otoño | 4 |

> **Nota:** El Festival de Teatro Clásico de Almagro (en sus variantes de nomenclatura) es el evento más importante, con más de **76 apariciones** combinadas.

---

## 🏛️ Top 10 Lugares de Estreno

Los lugares más frecuentes incluyen:
- Teatro de la Comedia de Madrid
- Corral de Comedias de Almagro
- Teatro Municipal de Almagro
- Corral de Comedias de Alcalá de Henares
- Teatro Español de Madrid

---

## 📝 Ejemplos de Registros

### Ejemplo 1: Registro Completo
```json
{
  "id": "1",
  "Autor/a": "Lope de Vega",
  "Obra": "La viuda valenciana",
  "Fecha de estreno": "30 de marzo de 2023",
  "Dirección": "Adrián Novella",
  "Compañía": "La Valenciana",
  "Festivales": "",
  "Lugar de estreno": "Teatro Rialto de Valencia",
  "fechaFormat": "",
  "lat": "39.4710227",
  "lon": "-0.3763002",
  "uuid": "abcda10d-e1ca-4c7b-bb04-36cb94e832bc"
}
```

### Ejemplo 2: Registro con Festival
```json
{
  "id": "3",
  "Autor/a": "Lope de Vega",
  "Obra": "Lo fingido verdadero. Historia de San Ginés, mártir y comediante; La finzione veritiera",
  "Fecha de estreno": "22 de julio de 2022",
  "Dirección": "Luca Vonella",
  "Compañía": "Teatro a Canone",
  "Festivales": "Festival internacional de Teatro Clásico de Almagro",
  "Lugar de estreno": "Teatro Municipal de Almagro, Ciudad Real",
  "fechaFormat": "",
  "lat": "38.8903455",
  "lon": "-3.7117528",
  "uuid": "154e33a4-dcf9-4b4d-8028-ffa7122b0348"
}
```

### Ejemplo 3: Registro con Datos Incompletos
```json
{
  "id": "23",
  "Autor/a": "",
  "Obra": "",
  "Fecha de estreno": "",
  "Dirección": "",
  "Compañía": "",
  "Festivales": "",
  "Lugar de estreno": "",
  "fechaFormat": "",
  "lat": "",
  "lon": "",
  "uuid": "2c0bf0f6-7068-4b18-ab53-8827aa597f9f"
}
```

---

## 🔧 Uso Técnico

### Lectura en JavaScript (método actual)

```javascript
// Cargar desde archivo CSV externo
const response = await fetch('data_con_coordenadas.csv');
const csvText = await response.text();

// Procesar CSV manualmente
const lines = csvText.split('\n');
const headers = lines[0].split('|');

const obras = lines.slice(1).map(line => {
    const values = line.split('|');
    const obra = {};
    headers.forEach((header, index) => {
        obra[header] = values[index];
    });
    return obra;
});
```

### Lectura en Python

```python
import csv

# Leer CSV
with open('data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f, delimiter='|')
    obras = list(reader)

# Acceder a los datos
for obra in obras:
    print(f"{obra['Autor/a']} - {obra['Obra']}")
```

### Lectura del JSON

```javascript
// JavaScript
const obras = await fetch('data.json').then(r => r.json());
```

```python
# Python
import json

with open('data.json', 'r', encoding='utf-8') as f:
    obras = json.load(f)
```

---

## 🚀 Próximos Pasos (Migración a Azure)

Según el plan de migración:

1. **Repositorio GitHub:** Crear nuevo repositorio con estos datos
2. **Azure App Services:** Desplegar aplicación estática
3. **Lectura de datos:** Mantener carga desde CSV/JSON (sin base de datos externa por ahora)
4. **Futuro:** Migración a Django con base de datos relacional

### Tareas pendientes para mejorar el dataset:
- [ ] Completar las 179 coordenadas faltantes
- [ ] Normalizar formatos de fecha (convertir a ISO 8601)
- [ ] Completar los 152 registros sin fecha de estreno
- [ ] Normalizar nombres de festivales (hay variaciones del mismo festival)
- [ ] Eliminar o completar el registro #23 (completamente vacío)

---

## 📊 Archivos Relacionados

- `data.csv` - Dataset completo en formato CSV (118 KB)
- `data.json` - Dataset completo en formato JSON (252 KB)
- `estadisticas.json` - Análisis estadístico detallado
- `../OLD/index.html` - Aplicación web original desplegada en DigitalOcean

---

## 📅 Información de Versión

- **Última actualización:** 15 de enero de 2026
- **Fuente:** https://seahorse-app-kg7ca.ondigitalocean.app/
- **Formato:** CSV con delimitador `|`
- **Encoding:** UTF-8
- **Total de registros:** 584

---

## 📄 Licencia y Uso

Este dataset documenta obras del Teatro Contemporáneo Español del Siglo XXI. Los datos son recopilados con fines académicos y de investigación teatral.

---

**Generado automáticamente el 15/01/2026**
