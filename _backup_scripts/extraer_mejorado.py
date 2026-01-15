#!/usr/bin/env python3
"""Script mejorado para extraer coordenadas incluso cuando hay múltiples resultados"""

import pandas as pd
import time
import re
import urllib.parse
import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Configuración
CSV_FILE = Path('../DATA/data.csv')
JSON_FILE = Path('../DATA/data.json')
GUARDAR_CADA = 10
ESPERA = 5

def setup_driver():
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1920,1080')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=opts)
    
    # Ir a Google Maps y aceptar cookies
    try:
        driver.get("https://www.google.com/maps")
        time.sleep(2)
        try:
            btns = driver.find_elements(By.TAG_NAME, "button")
            for btn in btns:
                try:
                    if any(word in btn.text.lower() for word in ['accept', 'aceptar', 'agree', 'rechazar', 'reject']):
                        btn.click()
                        time.sleep(1)
                        break
                except:
                    pass
        except:
            pass
    except:
        pass
    
    return driver

def extraer_coords_url(url):
    """Extrae coordenadas de la URL"""
    m = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
    if m:
        return m.group(1), m.group(2)
    
    m2 = re.search(r'!3d(-?\d+\.\d+)!4d(-?\d+\.\d+)', url)
    if m2:
        return m2.group(1), m2.group(2)
    
    return None, None

def extraer_coords_pagina(driver):
    """Intenta extraer coordenadas del primer resultado o del mapa visible"""
    try:
        # Esperar un momento para que cargue
        time.sleep(2)
        
        # Método 1: Buscar en los atributos data de los elementos
        try:
            elementos = driver.find_elements(By.CSS_SELECTOR, "[data-latitude][data-longitude]")
            if elementos:
                lat = elementos[0].get_attribute("data-latitude")
                lon = elementos[0].get_attribute("data-longitude")
                if lat and lon:
                    return lat, lon
        except:
            pass
        
        # Método 2: Hacer clic en el primer resultado si existe
        try:
            # Buscar el primer resultado de lugar
            wait = WebDriverWait(driver, 3)
            primer_resultado = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/maps/place/']"))
            )
            
            # Obtener el href que puede contener coordenadas
            href = primer_resultado.get_attribute('href')
            lat, lon = extraer_coords_url(href)
            if lat and lon:
                return lat, lon
            
            # Si no hay coordenadas en el href, hacer clic
            primer_resultado.click()
            time.sleep(2)
            
            # Ahora la URL debe tener coordenadas
            current_url = driver.current_url
            lat, lon = extraer_coords_url(current_url)
            if lat and lon:
                return lat, lon
        except:
            pass
        
        # Método 3: Buscar en el HTML de la página
        try:
            page_source = driver.page_source
            # Buscar patrones de coordenadas en el HTML
            matches = re.findall(r'"(-?\d+\.\d{4,})",\s*"(-?\d+\.\d{4,})"', page_source)
            if matches:
                # Filtrar coordenadas válidas (aproximadamente entre -90,90 y -180,180)
                for lat, lon in matches:
                    lat_f, lon_f = float(lat), float(lon)
                    if -90 <= lat_f <= 90 and -180 <= lon_f <= 180:
                        return str(lat_f), str(lon_f)
        except:
            pass
        
    except:
        pass
    
    return None, None

def buscar(driver, lugar):
    """Busca un lugar y extrae coordenadas con múltiples métodos"""
    try:
        url = f"https://www.google.com/maps/search/{urllib.parse.quote(lugar)}"
        driver.get(url)
        time.sleep(ESPERA)
        
        # Método 1: Coordenadas en la URL
        lat, lon = extraer_coords_url(driver.current_url)
        if lat and lon:
            return lat, lon, 'url'
        
        # Método 2: Extraer de la página
        lat, lon = extraer_coords_pagina(driver)
        if lat and lon:
            return lat, lon, 'page'
        
        return None, None, 'no'
        
    except Exception as e:
        return None, None, 'err'

def guardar(df):
    df.to_csv(CSV_FILE, sep='|', index=False, encoding='utf-8')
    df.to_json(JSON_FILE, orient='records', indent=2, force_ascii=False)

def main():
    print("\n" + "="*70)
    print("🗺️  EXTRACCIÓN MEJORADA DE COORDENADAS")
    print("="*70)
    
    df = pd.read_csv(CSV_FILE, sep='|', encoding='utf-8')
    
    # Solo procesar las que NO tienen coordenadas
    sin_coords = df[
        ((df['lat'].isna()) | (df['lat'] == '')) & 
        (df['Lugar de estreno'].notna()) & 
        (df['Lugar de estreno'] != '')
    ]
    
    total = len(sin_coords)
    print(f"\n📊 Total a procesar: {total} obras")
    print(f"⏱️  Estimado: ~{total * ESPERA // 60} minutos")
    print(f"🔧 Método mejorado: múltiples estrategias de extracción\n")
    print("="*70 + "\n")
    
    driver = setup_driver()
    stats = {'url': 0, 'page': 0, 'no': 0, 'err': 0}
    contador = 0
    inicio = time.time()
    
    try:
        for idx, (i, row) in enumerate(sin_coords.iterrows(), 1):
            lugar = row['Lugar de estreno']
            tipo = row.get('tipo', '?')[:3]
            
            # Progreso
            porc = (idx / total) * 100
            transcurrido = time.time() - inicio
            if idx > 1:
                restante = ((transcurrido / (idx-1)) * (total - idx + 1)) / 60
                eta = f"{int(restante)}m"
            else:
                eta = "..."
            
            sys.stdout.write(f"\r[{idx}/{total}] {porc:5.1f}% | {tipo} | {lugar[:40]:40} | ETA: {eta:6}")
            sys.stdout.flush()
            
            lat, lon, status = buscar(driver, lugar)
            
            if status in ['url', 'page']:
                df.at[i, 'lat'] = str(lat)
                df.at[i, 'lon'] = str(lon)
                stats[status] += 1
                icon = '🎯' if status == 'url' else '📍'
                sys.stdout.write(f" {icon}\n")
            elif status == 'no':
                stats['no'] += 1
                sys.stdout.write(" ⚠️\n")
            else:
                stats['err'] += 1
                sys.stdout.write(" ❌\n")
            
            sys.stdout.flush()
            contador += 1
            
            # Guardar progreso
            if contador >= GUARDAR_CADA:
                sys.stdout.write("💾 Guardando...")
                sys.stdout.flush()
                guardar(df)
                contador = 0
                total_encontrado = stats['url'] + stats['page']
                sys.stdout.write(f" ✅ ({total_encontrado} coords)\n")
                sys.stdout.flush()
        
        # Guardar final
        print("\n\n💾 Guardando resultados finales...")
        guardar(df)
        
        # Estadísticas
        total_min = int((time.time() - inicio) / 60)
        total_encontrado = stats['url'] + stats['page']
        
        print(f"\n{'='*70}")
        print("📊 RESULTADOS DETALLADOS")
        print("="*70)
        print(f"🎯 Desde URL:        {stats['url']:4} ({stats['url']/total*100:5.1f}%)")
        print(f"📍 Desde página:     {stats['page']:4} ({stats['page']/total*100:5.1f}%)")
        print(f"{'─'*70}")
        print(f"✅ TOTAL EXITOSOS:   {total_encontrado:4} ({total_encontrado/total*100:5.1f}%)")
        print(f"⚠️  No encontrados:   {stats['no']:4} ({stats['no']/total*100:5.1f}%)")
        print(f"❌ Errores:          {stats['err']:4} ({stats['err']/total*100:5.1f}%)")
        print(f"⏱️  Tiempo total:     {total_min} minutos")
        print("="*70)
        print("\n✨ ¡Completado!\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido - Guardando progreso...")
        guardar(df)
        total_encontrado = stats['url'] + stats['page']
        print(f"✅ Guardado: {total_encontrado} nuevas coordenadas\n")
    
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
