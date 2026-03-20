import plotly.express as px
import plotly.offline as opy
import plotly.graph_objects as go
import pandas as pd


def generar_grafico_3d(data):
    df = pd.DataFrame(data).sort_values(['anio', 'mes'])
    if df.empty: return "<p>Sin datos</p>"

    df_pivot = df.pivot(index='anio', columns='mes', values='superficie_total').fillna(0)

    fig = go.Figure(go.Surface(
        z=df_pivot.values, x=df_pivot.columns, y=df_pivot.index,
        colorscale='YlOrRd',
        colorbar=dict(title='HECTÁREAS', ticksuffix=" ha", thickness=20)
    ))

    fig.update_layout(
        title='Análisis Topográfico: Impacto Estacional por Año',
        # Configuramos la fuente UNA SOLA VEZ para todo el gráfico
        font=dict(family="Verdana", color="#f8fafc"),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, b=0, t=50),
        scene=dict(
            xaxis_title='Mes',
            yaxis_title='Año',
            zaxis_title='Superficie (ha)',
            aspectratio=dict(x=1, y=1, z=0.5),
            bgcolor='rgba(15, 23, 42, 0.5)'
        )
    )

    return opy.plot(fig, auto_open=False, output_type='div', config={'responsive': True})



def generar_lista_principal(data):
    df = pd.DataFrame(data)
    if df.empty: return ""
    
    fig = px.line(df, x='anio', y='superficie_total', 
                  markers=True, 
                  line_shape='spline',
                  color_discrete_sequence=['#f97316'])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor='#334155'),
        margin=dict(t=20, b=20, l=20, r=20)
    )
    return opy.plot(fig, auto_open=False, output_type='div')


def generar_mapa_provincias(data):
    df = pd.DataFrame(data)
    if df.empty: return "<p>Sin datos</p>"

    # Limpieza y mapeo rápido
    df['provincia'] = df['provincia'].astype(str).str.strip().replace({
        "Vizcaya": "Bizkaia", "Guipúzcoa": "Gipuzkoa", 
        "Guipuzcoa": "Gipuzkoa", "Álava": "Araba/Álava"
    })

    fig = px.choropleth(
        df, locations='provincia', color='superficie_total_quemada',
        geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/spain-provinces.geojson",
        featureidkey="properties.name", color_continuous_scale="OrRd",
        hover_name="provincia"
    )

    # El truco está aquí: bgcolor='rgba(0,0,0,0)' dentro de geos
    fig.update_geos(
        fitbounds="locations", visible=False, 
        bgcolor='rgba(0,0,0,0)', showcoastlines=True, coastlinecolor="#334155"
    )

    fig.update_layout(
        height=500, margin={"r":0, "t":0, "l":0, "b":0},
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#f8fafc'),
        coloraxis_colorbar=dict(title="Ha", thickness=15, len=0.6, x=0.02)
    )

    fig.update_traces(marker_line_width=0.5, marker_line_color="#0f172a")

    return opy.plot(fig, auto_open=False, output_type='div', config={'displayModeBar': False})


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