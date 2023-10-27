from sqlalchemy import create_engine
import pandas as pd

# Función para muestrear datos
def sample_data(ruta):
    data = pd.read_csv(ruta, dtype={'ARREST_KEY': int})
    sample_size = min(len(data), 100000)
    sampled_data = data.sample(sample_size).reset_index(drop=True)
    return sampled_data

# Función para dividir columnas con valores separados por comas
def split_comma_separated_values(df, column_name):
    df_split = df[column_name].str.split(',', expand=True)
    df_split.columns = [f"{column_name}_{i+1}" for i in range(df_split.shape[1])]
    return df_split

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:BAJXQ829112002@localhost/Actuaria_2")

# Rutas de los archivos CSV
ruta1 = '/Users/alejandrosanchez/Downloads/nyc_arrests/NYPD_Arrest_Data__Year_to_Date_.csv'
ruta2 = '/Users/alejandrosanchez/Downloads/nyc_arrests/NYPD_Arrests_Data__Historic_.csv'

# Carga de datos y preparación
data1_sampled = sample_data(ruta1)
data2_sampled = sample_data(ruta2)
combined_data = pd.concat([data1_sampled, data2_sampled]).reset_index(drop=True)
combined_data_cleaned = combined_data.dropna().reset_index(drop=True)

# Creación de entidades y exportación
df_arrest = combined_data_cleaned[['ARREST_KEY', 'ARREST_DATE', 'ARREST_BORO', 'ARREST_PRECINCT']].copy()
df_offense = combined_data_cleaned[['ARREST_KEY', 'PD_CD', 'PD_DESC', 'KY_CD', 'OFNS_DESC']].copy()
df_location = combined_data_cleaned[['ARREST_KEY', 'X_COORD_CD', 'Y_COORD_CD', 'Latitude', 'Longitude']].copy()
df_perpetrator = combined_data_cleaned[['ARREST_KEY', 'AGE_GROUP', 'PERP_SEX', 'PERP_RACE']].copy()

# Añadir columnas de ID para OFFENSE y PERPETRATOR
df_offense['ID'] = range(1, len(df_offense) + 1)
df_perpetrator['ID'] = range(1, len(df_perpetrator) + 1)

# Transformaciones adicionales en df_offense
df_pd_desc_split = split_comma_separated_values(df_offense, 'PD_DESC')
df_ofns_desc_split = split_comma_separated_values(df_offense, 'OFNS_DESC')
df_offense_transformed = df_offense.drop(columns=['PD_DESC', 'OFNS_DESC'])
df_offense_transformed = pd.concat([df_offense_transformed, df_pd_desc_split, df_ofns_desc_split], axis=1)

# Exportación a la base de datos
df_arrest.to_sql('ARREST', engine, if_exists='replace', index=False)
df_offense_transformed.to_sql('OFFENSE', engine, if_exists='replace', index=False)
df_location.to_sql('LOCATION', engine, if_exists='replace', index=False)
df_perpetrator.to_sql('PERPETRATOR', engine, if_exists='replace', index=False)



