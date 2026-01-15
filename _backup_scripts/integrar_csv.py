#!/usr/bin/env python3
"""
Script para integrar los CSV Nacional e Internacional en un formato unificado
compatible con el index.html del proyecto TCE-XXI.
"""

import pandas as pd
import uuid
import json
import re
from pathlib import Path

# Rutas
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / 'DATA'
CSV_NACIONAL = DATA_DIR / 'TCE SXXI - Nacional.csv'
CSV_INTERNACIONAL = DATA_DIR / 'TCE SXXI - Internacional.csv'
OUTPUT_CSV = DATA_DIR / 'data.csv'
OUTPUT_JSON = DATA_DIR / 'data.json'

def limpiar_texto(texto):
    """Limpia texto de saltos de línea, comillas extra y espacios"""
    if pd.isna(texto) or texto == '':
        return ''
    texto = str(texto)
    # Quitar saltos de línea
    texto = texto.replace('\n', ' ').replace('\r', ' ')
    # Normalizar espacios múltiples
    texto = re.sub(r'\s+', ' ', texto)
    # Quitar comillas extra
    texto = texto.replace('""', '"').strip()
    return texto

def procesar_nacional():
    """Lee y procesa el CSV Nacional"""
    print(f"📂 Leyendo {CSV_NACIONAL}...")
    df = pd.read_csv(CSV_NACIONAL, encoding='utf-8')
    
    print(f"   Registros encontrados: {len(df)}")
    
    # Mapeo de campos
    df_procesado = pd.DataFrame({
        'Autor/a': df['Autor/a (atribución tradicional)'].apply(limpiar_texto),
        'Obra': df['Obra'].apply(limpiar_texto),
        'Fecha de estreno': df['Fecha de estreno'].apply(limpiar_texto),
        'Dirección': df['Dirección'].apply(limpiar_texto),
        'Compañía': df['Compañía'].apply(limpiar_texto),
        'Festivales': df['Festivales'].apply(limpiar_texto),
        'Lugar de estreno': df['Lugar de estreno'].apply(limpiar_texto),
        'fechaFormat': '',  # Vacío por ahora
        'lat': '',  # Vacío por ahora
        'lon': '',  # Vacío por ahora
        'tipo': 'Nacional'
    })
    
    return df_procesado

def procesar_internacional():
    """Lee y procesa el CSV Internacional"""
    print(f"📂 Leyendo {CSV_INTERNACIONAL}...")
    df = pd.read_csv(CSV_INTERNACIONAL, encoding='utf-8')
    
    print(f"   Registros encontrados: {len(df)}")
    
    # Mapeo de campos
    # Para Internacional, primero intentamos "Obra en español", si no existe usamos "Obra"
    obra_columna = 'Obra en español' if 'Obra en español' in df.columns else 'Obra'
    
    df_procesado = pd.DataFrame({
        'Autor/a': df['Autor/a (atribución tradicional)'].apply(limpiar_texto),
        'Obra': df[obra_columna].apply(limpiar_texto),
        'Fecha de estreno': df['Fecha de estreno'].apply(limpiar_texto),
        'Dirección': df['Dirección'].apply(limpiar_texto),
        'Compañía': df['Compañía'].apply(limpiar_texto),
        'Festivales': df['Festivales'].apply(limpiar_texto),
        'Lugar de estreno': df['Lugar de estreno'].apply(limpiar_texto),
        'fechaFormat': '',  # Vacío por ahora
        'lat': '',  # Vacío por ahora
        'lon': '',  # Vacío por ahora
        'tipo': 'Internacional'
    })
    
    return df_procesado

def unificar_y_exportar():
    """Unifica ambos CSV y exporta en formato pipe-delimited"""
    print("🔄 Iniciando integración de CSV...")
    print()
    
    # Procesar ambos CSV
    df_nacional = procesar_nacional()
    df_internacional = procesar_internacional()
    
    # Combinar
    print()
    print("🔗 Combinando datasets...")
    df_unificado = pd.concat([df_nacional, df_internacional], ignore_index=True)
    
    # Generar IDs secuenciales
    df_unificado.insert(0, 'id', range(1, len(df_unificado) + 1))
    
    # Generar UUIDs
    df_unificado['uuid'] = [str(uuid.uuid4()) for _ in range(len(df_unificado))]
    
    # Reordenar columnas según el formato esperado
    columnas_orden = [
        'id', 'Autor/a', 'Obra', 'Fecha de estreno', 'Dirección', 
        'Compañía', 'Festivales', 'Lugar de estreno', 'fechaFormat', 
        'lat', 'lon', 'uuid', 'tipo'
    ]
    df_unificado = df_unificado[columnas_orden]
    
    # Estadísticas
    print(f"   Total de registros: {len(df_unificado)}")
    print(f"   - Nacional: {len(df_unificado[df_unificado['tipo'] == 'Nacional'])}")
    print(f"   - Internacional: {len(df_unificado[df_unificado['tipo'] == 'Internacional'])}")
    print()
    
    # Exportar CSV con delimitador pipe
    print(f"💾 Exportando a {OUTPUT_CSV}...")
    df_unificado.to_csv(OUTPUT_CSV, sep='|', index=False, encoding='utf-8')
    print(f"   ✅ CSV exportado correctamente")
    
    # Exportar JSON
    print(f"💾 Exportando a {OUTPUT_JSON}...")
    records = df_unificado.to_dict('records')
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    print(f"   ✅ JSON exportado correctamente")
    
    print()
    print("✨ Integración completada exitosamente!")
    print()
    print("📊 Resumen:")
    print(f"   - Archivo CSV: {OUTPUT_CSV}")
    print(f"   - Archivo JSON: {OUTPUT_JSON}")
    print(f"   - Total registros: {len(df_unificado)}")
    print(f"   - Campos por registro: {len(columnas_orden)}")
    print()
    
    # Mostrar muestra de datos
    print("📋 Muestra de registros (primeros 3):")
    print()
    for i, row in df_unificado.head(3).iterrows():
        print(f"   Registro {row['id']}:")
        print(f"      Autor: {row['Autor/a']}")
        print(f"      Obra: {row['Obra']}")
        print(f"      Tipo: {row['tipo']}")
        print(f"      Lugar: {row['Lugar de estreno']}")
        print()

if __name__ == '__main__':
    try:
        unificar_y_exportar()
    except Exception as e:
        print(f"❌ Error durante la integración: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
