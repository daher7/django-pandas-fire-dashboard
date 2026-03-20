from django.shortcuts import render

from analysis.figures import (
    generar_grafico_3d, 
    generar_lista_principal,
    generar_mapa_provincias,
    generar_grafico_causas, 
    generar_grafico_gravedad,
    generar_grafico_top_provincias,
    generar_grafico_mensual
)
import requests


def inicio(request):

    
    query_tabla = 'http://127.0.0.1:8000/query?q=SELECT%20%20%20%20%20%20anio%2C%20%20%20%20%20%20COUNT%28id%29%20AS%20total_incendios%2C%20%20%20%20%20%20SUM%28superficie%29%20AS%20superficie_total%20FROM%20incendios%20WHERE%20anio%20BETWEEN%202010%20AND%202020%20GROUP%20BY%20anio%20ORDER%20BY%20anio%20DESC%3B'
    
    
    query_grafico = "http://127.0.0.1:8000/query?q=SELECT%20%20%09mes%2C%20%09anio%2C%20%20%09sum%28superficie%29%20AS%20superficie_total%20FROM%20INCENDIOS%20I%20%20WHERE%20anio%20BETWEEN%202010%20AND%202020%20GROUP%20BY%20anio%2C%20mes%3B"


    response_tabla = requests.get(query_tabla)
    data_tabla = response_tabla.json()

    response_grafico = requests.get(query_grafico)
    data_grafico = response_grafico.json()

    # Llamamos a la función de figures.py pasando los datos de la API
    chart_div = generar_grafico_3d(data_grafico)

    # Añadimos el gráfico al contexto para que llegue al HTML
    contexto = {
        'data': data_tabla,
        'chart_superficie': chart_div,
    }

    return render(request, 'analysis/inicio.html', contexto)


def mostrar_mapa(request):

    api_url = "http://127.0.0.1:8000/query?q=SELECT%20%20%20%20%20%20p.IDPROVINCIA%20AS%20idprovincia%2C%20%20%20%20%20p.PROVINCIA%20AS%20provincia%2C%20%20%20%20%20SUM%28i.superficie%29%20AS%20superficie_total_quemada%20FROM%20incendios%20AS%20i%20INNER%20JOIN%20provincias%20AS%20p%20%20%20%20%20%20ON%20p.IDPROVINCIA%20%3D%20i.IDPROVINCIA%20GROUP%20BY%20%20%20%20%20%20p.IDPROVINCIA%2C%20%20%20%20%20%20p.PROVINCIA%20ORDER%20BY%20%20%20%20%20%20p.IDPROVINCIA%3B"
    data = requests.get(api_url).json()

    # Generación el mapa con la función de figures.py
    mapa_div = generar_mapa_provincias(data)

    return render(request, 'analysis/mapa.html', {'mapa': mapa_div})



def mostrar_estadisticas(request):
    base_url = "http://127.0.0.1:8000/query?" 

    # 1. Tiempo: Evolución anual
    q_tiempo = "q=SELECT%20%20%20%20%20%20anio%2C%20%20%20%20%20%20COUNT%28id%29%20AS%20total_incendios%2C%20%20%20%20%20%20SUM%28superficie%29%20AS%20superficie_total%20FROM%20incendios%20WHERE%20anio%20BETWEEN%201968%20AND%202020%20GROUP%20BY%20anio%20ORDER%20BY%20anio%20ASC%3B"
    data_tiempo = requests.get(base_url + q_tiempo).json() # Sin urllib.parse.quote
    chart_tiempo = generar_lista_principal(data_tiempo)

    # 2. Calendario: Estacionalidad mensual
    # OJO: Aquí tenías la query de provincias repetida, te pongo la de MESES:
    q_mes = "q=SELECT%20mes%2C%20count%28id%29%20AS%20total_incendios%2C%20sum%28superficie%29%20AS%20superficie_quemada%20FROM%20incendios%20WHERE%20anio%20BETWEEN%201968%20AND%202020%20GROUP%20BY%20mes%20ORDER%20BY%20mes%20ASC%3B"
    data_mes = requests.get(base_url + q_mes).json()
    chart_mes = generar_grafico_mensual(data_mes)

    # 3. Origen: Causas
    q_causas = "q=SELECT%20%20%09c.causa%2C%20%09count%28id%29%20AS%20incendios_totales%2C%20%09sum%28superficie%29%20FROM%20incendios%20AS%20i%20%20INNER%20JOIN%20causas%20AS%20c%20%20ON%20i.idcausa%20%3D%20c.idcausa%20WHERE%20anio%20BETWEEN%201968%20AND%202020%20GROUP%20BY%20c.causa%3B"
    data_causas = requests.get(base_url + q_causas).json()
    chart_causas = generar_grafico_causas(data_causas)

    # 4. Gravedad: GIF
    q_grav = "q=SELECT%20%20%09count%28id%29%20AS%20incendios_totales%2C%20%09sum%28superficie%29%20AS%20superficie_quemada%2C%20%09sum%28superficie%29%2Fcount%28id%29%20AS%20superficie_media%2C%20%09anio%20FROM%20%20incendios%20%20WHERE%20anio%20BETWEEN%201968%20AND%202020%20GROUP%20BY%20anio%3B"
    data_grav = requests.get(base_url + q_grav).json()
    chart_gravedad = generar_grafico_gravedad(data_grav)

    # 5. Espacio: Top 20 Provincias
    q_prov = "q=SELECT%20%09%20%09sum%28superficie%29%20AS%20superficie_total%2C%20%09p.provincia%20FROM%20incendios%20AS%20i%20%20INNER%20JOIN%20provincias%20AS%20p%20%20ON%20i.idprovincia%20%3D%20p.idprovincia%20%20WHERE%20i.anio%20BETWEEN%201968%20AND%202020%20GROUP%20BY%20p.provincia%20ORDER%20BY%20superficie_total%20DESC%20LIMIT%2020%3B"
    data_prov = requests.get(base_url + q_prov).json()
    chart_top_provincias = generar_grafico_top_provincias(data_prov)

    # 6. Tragedia: Víctimas
    q_vic = "q=SELECT%20%20%09i.anio%2C%20%09i.municipio%2C%20%09p.provincia%2C%20%09i.muertos%20FROM%20incendios%20i%20%20INNER%20JOIN%20provincias%20p%20%20%20ON%20i.idprovincia%20%3D%20p.idprovincia%20%20ORDER%20BY%20muertos%20DESC%20%20LIMIT%2010%3B"
    victimas = requests.get(base_url + q_vic).json()

    contexto = {
        'chart_tiempo': chart_tiempo,
        'chart_mes': chart_mes,
        'chart_causas': chart_causas,
        'chart_gravedad': chart_gravedad,
        'chart_top_provincias': chart_top_provincias,
        'victimas': victimas,
    }
    
    return render(request, 'analysis/estadisticas.html', contexto)


def mostrar_metodologia(request):
    return render(request, 'analysis/metodologia.html')