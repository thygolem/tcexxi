# Análisis de Campos del Dataset TCE SXXI

## 📊 Resumen de Carga de Datos

### ✅ El CSV se carga desde el repositorio (archivo externo)

**Ubicación en el código:**

```javascript
// index.html - Función obtenerObras()
const response = await fetch('DATA/data.csv');
```

**NO está embebido en el HTML** - Los datos se cargan dinámicamente al abrir la página web mediante una petición HTTP al archivo CSV externo.

**Fuentes integradas:**
- CSV Nacional: 581 registros
- CSV Internacional: 132 registros
- **Total: 713 registros**

---

## 🔍 Campos Mostrados vs Campos Ocultos

### ✅ Campos que SE MUESTRAN en la Tabla (8 campos + 1 badge)

| # | Campo | Cómo se muestra |
|---|-------|-----------------|
| 1 | `id` | Texto simple en columna "ID" |
| 2 | `Autor/a` | Texto simple en columna "Autor/a" |
| 3 | `Obra` | Texto simple en columna "Obra" **+ Badge de tipo** |
| 4 | **`tipo`** | **Badge visual (verde=Nacional, amarillo=Internacional)** |
| 5 | `Fecha de estreno` | Texto simple (sin fechaFormat) |
| 6 | `Dirección` | Texto simple en columna "Dirección" |
| 7 | `Compañía` | Texto simple en columna "Compañía" |
| 8 | `Festivales` | Texto simple en columna "Festivales" |
| 9 | `Lugar de estreno` | **Enlace a Google Maps** |

#### Código de visualización de la tabla:

```javascript
// función llenarTabla() en index.html
row.insertCell().textContent = obra.id;
row.insertCell().textContent = obra['Autor/a'];

// Columna Obra con badge de tipo
const obraCell = row.insertCell();
const tipoBadge = obra.tipo ? 
    `<span class="tipo-badge tipo-${obra.tipo.toLowerCase()}">${obra.tipo}</span>` : 
    '';
obraCell.innerHTML = `${obra.Obra}${tipoBadge}`;

row.insertCell().textContent = `${obra['Fecha de estreno']}`;
row.insertCell().textContent = obra.Dirección;
row.insertCell().textContent = obra['Compañía'] || '';
row.insertCell().textContent = obra.Festivales;

// El lugar de estreno se convierte en enlace a Google Maps
const lugarCell = row.insertCell();
const lugar = obra['Lugar de estreno'] || '';
if (lugar) {
    lugarCell.innerHTML = `
        <a class="lugar-link"
           href="https://www.google.com/maps/search/${encodeURIComponent(lugar)}"
           target="_blank">
            ${lugar}
        </a>
    `;
}
```

#### Estilos CSS para los badges:

```css
.tipo-badge {
    display: inline-block;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 11px;
    font-weight: bold;
    margin-left: 5px;
}

.tipo-nacional {
    background-color: #90EE90;
    color: #006400;
}

.tipo-internacional {
    background-color: #FFD700;
    color: #8B4513;
}
```

---

### ❌ Campos que NO SE MUESTRAN en la Tabla (4 campos)

| # | Campo | Uso en la aplicación | Propósito |
|---|-------|---------------------|-----------|
| 1 | `lat` | **Sí se usa** - Para el mapa interactivo | Latitud GPS para posicionar marcadores en el mapa de Leaflet |
| 2 | `lon` | **Sí se usa** - Para el mapa interactivo | Longitud GPS para posicionar marcadores en el mapa de Leaflet |
| 3 | `uuid` | **No se usa** | Identificador único universal (posible uso futuro para APIs) |
| 4 | `fechaFormat` | **Parcialmente** - Se usa para ordenar | Fecha en formato ISO para ordenamiento (mayormente vacío) |

---

## 🗺️ Uso de las Coordenadas (lat, lon)

Aunque **no se muestran** en la tabla, las coordenadas `lat` y `lon` son **fundamentales** para el funcionamiento de la aplicación:

### 1. Mapa Interactivo con Leaflet

Las coordenadas se utilizan para crear marcadores en el mapa:

```javascript
// Las coordenadas se usan para posicionar los marcadores
const marker = L.marker([obra.lat, obra.lon], {
    icon: L.divIcon({
        html: '<i class="fas fa-theater-masks"></i>',
        className: 'custom-marker'
    })
});
```

### 2. Agrupación de Marcadores (Clusters)

Se usa `MarkerClusterGroup` para agrupar marcadores cercanos:

```javascript
markerClusterGroup = L.markerClusterGroup({
    chunkedLoading: true,
    spiderfyOnMaxZoom: true
});
```

### 3. Filtrado Geográfico

El mapa se actualiza dinámicamente cuando se filtran las obras:

```javascript
function actualizarMapa(obrasData) {
    markerClusterGroup.clearLayers();
    
    obrasData.forEach(obra => {
        if (obra.lat && obra.lon) {
            const marker = L.marker([obra.lat, obra.lon])
                .bindPopup(`
                    <b>${obra.Obra}</b><br>
                    ${obra['Autor/a']}<br>
                    ${obra['Lugar de estreno']}
                `);
            markerClusterGroup.addLayer(marker);
        }
    });
}
```

### 4. Centrado del Mapa

Al hacer clic en un teatro, el mapa se centra en sus coordenadas:

```javascript
if (obra.lat && obra.lon) {
    map.setView([obra.lat, obra.lon], 13);
}
```

---

## 🔑 El Campo UUID (No Utilizado)

El campo `uuid` existe en todos los registros pero **no se utiliza** en ninguna parte del código actual.

### Posibles Usos Futuros:

1. **API REST:** Identificador único para endpoints
   ```
   GET /api/obras/{uuid}
   ```

2. **URLs Amigables:** Para enlaces compartibles
   ```
   https://teatro.example.com/obra/abcda10d-e1ca-4c7b-bb04-36cb94e832bc
   ```

3. **Relaciones en Base de Datos:** Clave primaria en PostgreSQL/MySQL

4. **Sincronización:** Para evitar duplicados al actualizar datos

5. **Compartir en Redes Sociales:** URLs únicas para cada obra

### Ejemplo de Registro con UUID:

```json
{
  "id": "1",
  "Obra": "La viuda valenciana",
  "uuid": "abcda10d-e1ca-4c7b-bb04-36cb94e832bc"
}
```

---

## 📊 Estadísticas de Completitud

### Datos Visibles en la Tabla

| Campo | Completos | Vacíos | % Completitud |
|-------|-----------|--------|---------------|
| ID | 584 | 0 | 100% |
| Autor/a | 584 | 0 | 100% |
| Obra | 584 | 0 | 100% |
| Fecha de estreno | 432 | 152 | 74% |
| Dirección | 584 | 0 | 100% |
| Compañía | 584 | 0 | 100% |
| Festivales | ~300 | ~284 | 51% |
| Lugar de estreno | 405 | 179 | 69% |

### Datos Ocultos (No visibles)

| Campo | Completos | Vacíos | % Completitud | ¿Se usa? |
|-------|-----------|--------|---------------|----------|
| lat | 405 | 179 | 69% | ✅ Sí (mapa) |
| lon | 405 | 179 | 69% | ✅ Sí (mapa) |
| uuid | 584 | 0 | 100% | ❌ No |
| fechaFormat | ~30 | ~554 | 5% | ⚠️ Parcial (se muestra junto a fecha) |

---

## 🎯 Problemas Detectados

### 1. Campo `fechaFormat` Mayormente Vacío

**Problema:** El campo `fechaFormat` está vacío en ~95% de los registros.

**Impacto en la UI:** 
```javascript
// Línea 1220
row.insertCell().textContent = `${obra['Fecha de estreno']} (${obra.fechaFormat})`;
// Resultado: "30 de marzo de 2023 ()" <- Paréntesis vacío
```

**Solución recomendada:**
```javascript
// Mostrar solo si fechaFormat existe
const fechaTexto = obra.fechaFormat 
    ? `${obra['Fecha de estreno']} (${obra.fechaFormat})`
    : obra['Fecha de estreno'];
row.insertCell().textContent = fechaTexto;
```

### 2. Coordenadas Faltantes (30.7%)

**Problema:** 179 registros sin coordenadas `lat` y `lon`.

**Impacto:**
- No aparecen en el mapa interactivo
- Experiencia de usuario incompleta
- Posibles teatros importantes sin visualización geográfica

**Obras sin coordenadas:**
- Registros con `Lugar de estreno` vacío: 179
- Registros con coordenadas vacías: 179
- **Coincidencia perfecta:** Los registros sin lugar tampoco tienen coordenadas

### 3. Registro Completamente Vacío

**Registro #23:**
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

**Acción recomendada:** Eliminar o completar este registro antes de migrar a Azure.

---

## 🔄 Visualización de Datos en el HTML

### Flujo de Datos:

```
1. Carga del CSV
   ↓
   fetch('data_con_coordenadas.csv')
   ↓
2. Parseo del CSV
   ↓
   Split por líneas y por delimitador '|'
   ↓
3. Almacenamiento
   ↓
   Array 'obrasOriginales' (global)
   ↓
4. Renderizado
   ├─→ Tabla HTML (8 campos visibles)
   ├─→ Mapa Leaflet (usa lat/lon)
   ├─→ Gráfico de Red (relaciones autor-obra)
   └─→ Contadores (estadísticas)
```

### Componentes que Usan los Datos:

1. **Tabla Principal** → 8 campos visibles
2. **Mapa de Leaflet** → Usa `lat`, `lon`, `Obra`, `Autor/a`, `Lugar de estreno`
3. **Red de Relaciones** → Usa `Autor/a`, `Obra`, `id`
4. **Filtros de Búsqueda** → Todos los campos de texto
5. **Contadores** → Calcula estadísticas de `Autor/a`, `Obra`, `Festivales`

---

## 📋 Recomendaciones para Migración a Azure

### 1. Mantener la Estructura Actual
✅ El CSV externo funciona bien para datos estáticos
✅ No requiere base de datos por ahora
✅ Fácil de actualizar (solo reemplazar el CSV)

### 2. Mejorar la Calidad de Datos
- [ ] Completar las 179 coordenadas faltantes
- [ ] Normalizar el campo `fechaFormat` o eliminarlo
- [ ] Eliminar/completar el registro #23
- [ ] Normalizar nombres de festivales

### 3. Considerar para el Futuro (Django)
- [ ] Usar `uuid` como primary key en PostgreSQL
- [ ] Crear tabla normalizada para festivales (muchos a muchos)
- [ ] API REST con endpoints por UUID
- [ ] Caché de coordenadas con Redis

### 4. Optimizaciones
- [ ] Comprimir el CSV (gzip) para reducir tiempo de carga
- [ ] Considerar formato JSON en lugar de CSV (más rápido de parsear)
- [ ] Implementar paginación para grandes datasets

---

## 📝 Conclusión

| Aspecto | Estado |
|---------|--------|
| **Carga de Datos** | ✅ Externa desde CSV (no embebida) |
| **Campos Mostrados** | ✅ 8 de 12 campos se muestran en la tabla |
| **Campos Ocultos pero Usados** | ✅ `lat` y `lon` se usan para el mapa |
| **Campos Sin Usar** | ⚠️ `uuid` no se utiliza (potencial futuro) |
| **Campo Problemático** | ❌ `fechaFormat` mayormente vacío |
| **Completitud de Datos** | ⚠️ 30.7% sin coordenadas |

---

**Documento generado el 15/01/2026**
