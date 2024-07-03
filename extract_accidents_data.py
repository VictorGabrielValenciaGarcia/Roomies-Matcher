import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select
import re

DATABASE_URL = "mysql+mysqlconnector://root:@localhost/temperaturas_bd"
engine = create_engine(DATABASE_URL)
    
def get_accidents_data():
    try:
        # Basic Data for Connection
        metadata = MetaData()
        analisis_accidentes = Table('analisis_accidentes', metadata, autoload_with=engine)
        
        # Basic Queries
        consulta_segementadora = select(analisis_accidentes).order_by(analisis_accidentes.c.REF_AREA).group_by(analisis_accidentes.c.REF_AREA)
        consulta_general = select(analisis_accidentes).order_by(analisis_accidentes.c.REF_AREA)
        with engine.connect() as conn:
            df = conn.execute(consulta_segementadora).fetchall()
            data = conn.execute(consulta_general).fetchall()
            
        # Format & Group Data
        new_list = []

        for row in df:
            new_list.append({"REF_AREA":row[0], "2022-Q4":0, "2023-Q1":0, "2023-Q2":0, "2023-Q3":0, "2023-Q4":0,})
            
        for row in data:
            for i, obj in enumerate(new_list):
                if new_list[i]['REF_AREA'] == row[0]:
                    new_list[i][row[1]] = row[2]
                    
        return new_list
    except Exception as err:
        print(f"Error al consultar Accidentes: {err}")
        return []
            
def get_form_data():
    try:
        # Basic Data for Connection
        metadata = MetaData()
        analisis_accidentes = Table('analisis_accidentes', metadata, autoload_with=engine)
        
        # Basic Queries
        region_query = select(analisis_accidentes).order_by(analisis_accidentes.c.REF_AREA).group_by(analisis_accidentes.c.REF_AREA)
        periods_query = select(analisis_accidentes).order_by(analisis_accidentes.c.TIME_PERIOD).group_by(analisis_accidentes.c.TIME_PERIOD)
        with engine.connect() as conn:
            regions = conn.execute(region_query).fetchall()
            periods = conn.execute(periods_query).fetchall()
            
        # Format & Group Data
        data_form = []
        region_names = []
        period_ids = []
        available_years = []
        
        year_regex = r"(\d{4})" #Regex para obtener los primeros 4 carcateres del texto

        for region in regions:
            region_names.append(region[0])
            
        for period in periods:
            period_ids.append(period[1])
            
        for period in period_ids:
            year = re.findall(year_regex, period)[0]
            if year not in available_years:
                available_years.append(year)

        
        data_form.append(region_names)
        data_form.append(period_ids)
        data_form.append(available_years)
        
        return data_form
    except Exception as err:
        print(f"Error al consultar Accidentes: {err}")
        return []
        
    
def get_graph_data(region_selected : str, period_selected : str):
    
    data = get_accidents_data()
    
    valores_filtrados = {}
    for item in data:
        if item['REF_AREA'] == region_selected:
            # valores_filtrados['REF_AREA'] = region_selected
            for key, value in item.items():                    
                if key.startswith(f"{period_selected}-"):
                    valores_filtrados[key] = value
    return valores_filtrados
    
# Accident Data
# data = get_accidents_data()
# data =  pd.DataFrame(data)
# print(data)

# Form Data
# data = get_form_data()
# print(data)

# Graph Data
data = get_graph_data('USA', '2023')
print(data)

