import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import pandas as pd

def generar_grafico_principal(data):
    df = pd.DataFrame(data)
    
    # Gráfico de líneas para ver la tendencia de superficie quemada
    fig = px.line(
        df, x='anio', y='superficie_total',
        title='Evolución de la Superficie Quemada (ha)',
        markers=True # Para que se vean los puntos de cada año
    )
    
    # Aplicamos tu estilo de colores y fondo transparente
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8')
    )
    
    return opy.plot(fig, auto_open=False, output_type='div', config={'responsive': True})


def generar_mapa_provincias(data):
    # 1. Creamos el DataFrame desde los datos de tu API
    df = pd.DataFrame(data)
    
    # Si la API está vacía, evitamos que el código explote
    if df.empty:
        return "<p>No hay datos disponibles para el mapa</p>"

    # 2. LIMPIEZA ABSOLUTA (Basada en tu SELECT)
    if 'provincia' in df.columns:
        df['provincia'] = df['provincia'].astype(str).str.strip()
        
        # Corrección manual para que coincidan con el GeoJSON de Click That Hood
        mapping = {
            "Vizcaya": "Bizkaia",
            "Guipúzcoa": "Gipuzkoa",
            "Guipuzcoa": "Gipuzkoa",
            "Álava": "Araba/Álava"
        }
        df['provincia'] = df['provincia'].replace(mapping)

    # 3. GeoJSON oficial
    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson"

    # 4. Creación del mapa
    fig = px.choropleth(
        df,
        geojson=geojson_url,
        locations='provincia',        # Columna de tu SQL
        featureidkey="properties.name", 
        color='superficie_total_quemada', # Columna de tu SQL (el SUM)
        color_continuous_scale="OrRd", 
        hover_name="provincia",
        labels={'superficie_total_quemada': 'Hectáreas Quemadas'}
    )

    # 5. Configuración Geográfica (Para que no salga el mapa mundial)
    fig.update_geos(
        fitbounds="locations", 
        visible=False,
        bgcolor='rgba(0,0,0,0)',
        showcoastlines=True,
        coastlinecolor="#334155"
    )

    # 6. Ajuste de Layout
    fig.update_layout(
        height=600, # Ajustado para que quepa bien en la card
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin={"r":10, "t":50, "l":10, "b":10}, # Márgenes más finos
        font=dict(color='#f8fafc', size=12),
        coloraxis_colorbar=dict(
            title="Ha",
            thickness=15,
            len=0.7,
            yanchor="middle", y=0.5,
            xanchor="left", x=0.02,
            tickfont=dict(color='#94a3b8')
        )
    )

    fig.update_traces(marker_line_width=0.5, marker_line_color="#0f172a")

    return opy.plot(fig, auto_open=False, output_type='div', config={'responsive': True, 'displayModeBar': False})


def generar_grafico_mensual(data):
    df = pd.DataFrame(data)
    if df.empty: return ""
    
    # Mapeo para que el eje X sea legible
    meses_map = {1: 'Ene', 2: 'Feb', 3: 'Mar', 4: 'Abr', 5: 'May', 6: 'Jun', 
                 7: 'Jul', 8: 'Ago', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dic'}
    df['mes_label'] = df['mes'].map(meses_map)
    
    fig = px.bar(df, x='mes_label', y='total_incendios',
                 title="Frecuencia por Mes",
                 color_discrete_sequence=['#fb923c'])
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font=dict(color='#94a3b8'), margin=dict(t=30, b=20, l=20, r=20))
    return opy.plot(fig, auto_open=False, output_type='div', config={'responsive': True})


def generar_grafico_intensidad(data):
    df = pd.DataFrame(data)
    fig = go.Figure()
    
    # Barras para el total de incendios
    fig.add_trace(go.Bar(x=df['anio'], y=df['incendios_totales'], name='Nº Incendios', marker_color='#94a3b8'))
    
    # Línea para la superficie media (Eje secundario)
    fig.add_trace(go.Scatter(x=df['anio'], y=df['superficie_media'], name='Ha Medias', yaxis='y2', 
                             line=dict(color='#f97316', width=3)))

    fig.update_layout(
        yaxis2=dict(overlaying='y', side='right'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(orientation="h", y=-0.2)
    )
    return opy.plot(fig, auto_open=False, output_type='div')


def generar_grafico_causas(data):
    df = pd.DataFrame(data)
    if df.empty: return ""
    
    fig = px.pie(df, names='causa', values=df.columns[2], # La 3ª columna es el SUM
                 hole=0.4,
                 color_discrete_sequence=px.colors.sequential.Oranges_r)
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#94a3b8'),
                      showlegend=True, margin=dict(t=0, b=0, l=0, r=0))
    return opy.plot(fig, auto_open=False, output_type='div')


def generar_grafico_gravedad(data):
    df = pd.DataFrame(data)
    if df.empty: return ""
    
    # Creamos un gráfico de doble eje 
    fig = go.Figure()
    
    fig.add_trace(go.Bar(x=df['anio'], y=df['incendios_totales'], 
                         name='Nº Incendios', marker_color='#475569'))
    
    fig.add_trace(go.Scatter(x=df['anio'], y=df['superficie_media'], 
                             name='Superficie Media (ha)', yaxis='y2',
                             line=dict(color='#f97316', width=3)))

    fig.update_layout(
        title="Intensidad: Cantidad vs Tamaño Medio",
        yaxis2=dict(overlaying='y', side='right'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        legend=dict(orientation="h", y=-0.2),
        margin=dict(t=40, b=20, l=20, r=20)
    )
    return opy.plot(fig, auto_open=False, output_type='div')


def generar_grafico_top_provincias(data):
    df = pd.DataFrame(data)
    if df.empty: return ""
    
    # Ordenamos para que la más grande salga arriba en el gráfico horizontal
    df = df.sort_values('superficie_total', ascending=True)
    
    fig = px.bar(df, x='superficie_total', y='provincia', 
                 orientation='h',
                 title="Top 20 Provincias más Afectadas (ha)",
                 color='superficie_total',
                 color_continuous_scale='OrRd')
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      font=dict(color='#94a3b8'), showlegend=False)
    return opy.plot(fig, auto_open=False, output_type='div')