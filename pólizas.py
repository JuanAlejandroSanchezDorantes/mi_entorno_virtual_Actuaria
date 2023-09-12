import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Generar un DataFrame con 100,000 filas de datos aleatorios
np.random.seed(0)  # Para reproducibilidad
data = pd.DataFrame({
    'PROD': np.random.choice(['T', 'V', 'DM'], 100000),
    'ECON': np.random.randint(18, 65, 100000),  
    'SEXO': np.random.choice(['M', 'F'], 100000),
    'STATUS': np.random.choice(['F', 'NF'], 100000),
    'T_P': np.random.uniform(0.01, 0.20, 100000),  
    'SAF': np.random.randint(10000, 1000000, 100000),  
    'SAD': np.random.randint(10000, 1000000, 100000),  
    'COB': np.random.randint(1, 30, 100000),  
    'PAG': np.random.randint(1, 30, 100000)  
})

# Creando el DataFrame para la tabla de mortalidad
data_mortalidad = {
    'Edad': list(range(112)),
    'qx': [
        0.000433, 0.000433, 0.000434, 0.000434, 0.000435, 0.000436, 0.000438, 
        0.000440, 0.000443, 0.000446, 0.000449, 0.000453, 0.000457, 0.000463, 
        0.000468, 0.000475, 0.000482, 0.000489, 0.000498, 0.000507, 0.000517, 
        0.000528, 0.000540, 0.000553, 0.000567, 0.000582, 0.000598, 0.000616, 
        0.000635, 0.000656, 0.000678, 0.000703, 0.000729, 0.000757, 0.000788, 
        0.000821, 0.000857, 0.000896, 0.000938, 0.000983, 0.001033, 0.001087, 
        0.001145, 0.001208, 0.001278, 0.001353, 0.001435, 0.001525, 0.001623, 
        0.001730, 0.001848, 0.001977, 0.002119, 0.002274, 0.002446, 0.002635, 
        0.002844, 0.003074, 0.003329, 0.003612, 0.003926, 0.004275, 0.004664, 
        0.005096, 0.005579, 0.006119, 0.006723, 0.007400, 0.008160, 0.009015, 
        0.009977, 0.011061, 0.012285, 0.013668, 0.015235, 0.017009, 0.019024, 
        0.021312, 0.023915, 0.026879, 0.030257, 0.034110, 0.038509, 0.043533, 
        0.049274, 0.055833, 0.063329, 0.071889, 0.081660, 0.092798, 0.105476, 
        0.119875, 0.136184, 0.154594, 0.175291, 0.198441, 0.224184, 0.252613, 
        0.283760, 0.317576, 0.353919, 0.392540, 0.433078, 0.475068, 0.517949, 
        0.561099, 0.603861, 0.645589, 0.685682, 0.723620, 0.758991, 1.000000
    ],
    'px': [
        0.999567, 0.999567, 0.999566, 0.999566, 0.999565, 0.999564, 0.999562, 
        0.999560, 0.999557, 0.999554, 0.999551, 0.999547, 0.999543, 0.999537, 
        0.999532, 0.999525, 0.999518, 0.999511, 0.999502, 0.999493, 0.999483, 
        0.999472, 0.999460, 0.999447, 0.999433, 0.999418, 0.999402, 0.999384, 
        0.999365, 0.999344, 0.999322, 0.999297, 0.999271, 0.999243, 0.999212, 
        0.999179, 0.999143, 0.999104, 0.999062, 0.999017, 0.998967, 0.998913, 
        0.998855, 0.998792, 0.998722, 0.998647, 0.998565, 0.998475, 0.998377, 
        0.998270, 0.998152, 0.998023, 0.997881, 0.997726, 0.997554, 0.997365, 
        0.997156, 0.996926, 0.996671, 0.996388, 0.996074, 0.995725, 0.995336, 
        0.994904, 0.994421, 0.993881, 0.993277, 0.992600, 0.991840, 0.990985, 
        0.990023, 0.988939, 0.987715, 0.986332, 0.984765, 0.982991, 0.980976, 
        0.978688, 0.976085, 0.973121, 0.969743, 0.965890, 0.961491, 0.956467, 
        0.950726, 0.944167, 0.936671, 0.928111, 0.918340, 0.907202, 0.894524, 
        0.880125, 0.863816, 0.845406, 0.824709, 0.801559, 0.775816, 0.747387, 
        0.716240, 0.682424, 0.646081, 0.607460, 0.566922, 0.524932, 0.482051, 
        0.438901, 0.396139, 0.354411, 0.314318, 0.276380, 0.241009, 0.000000
    ]
}

tabla_mortalidad = pd.DataFrame(data_mortalidad)

def edad_asegurable(edad,sexo, status):
    if sexo == "F" and status == 'NF':
        edad -= 5
    elif sexo=="F":
        edad -= 3
    elif status == 'NF':
        edad -= 2
    return edad

def seguro_temporal(edad, sexo, status, tasa, SA_T, cobertura):
    edad = edad_asegurable(edad, sexo, status)
    k = list(range(cobertura))
    x_k = list(range(edad, edad + cobertura))
    q_x = np.array(tabla_mortalidad.loc[x_k[0]:x_k[-1], 'qx'])
    v_k1 = [(1+tasa)**(-1-x) for x in k]
    kp_x = [1]
    for i in range(cobertura-1):
        valor = kp_x[i] * (1-q_x[i])
        kp_x.append(valor)
    PNU = sum(q_x * v_k1 * kp_x) * SA_T
    return np.round(PNU,2)

def seguro_vitalicio(edad, sexo, status, tasa, SA_T):
    omega = 111
    edad = edad_asegurable(edad, sexo, status)
    cobertura = omega - edad
    k = list(range(cobertura))
    x_k = list(range(edad, edad + cobertura))
    q_x = np.array(tabla_mortalidad.loc[x_k[0]:x_k[-1], 'qx'])
    v_k1 = [(1 + tasa) ** (-1 - x) for x in k]
    kp_x = [1]
    for i in range(cobertura - 1):
        valor = kp_x[i] * (1 - q_x[i])
        kp_x.append(valor)
    PNU = sum(q_x * v_k1 * kp_x) * SA_T
    return np.round(PNU, 2)

def seguro_dotal(edad, sexo, status, tasa, SA, cobertura):
    edad = edad_asegurable(edad, sexo, status)
    k = list(range(cobertura))
    x_k = list(range(edad, edad + cobertura))
    q_x = np.array(tabla_mortalidad.loc[x_k[0]:x_k[-1], 'qx'])
    npx = np.prod([1 - q_x[i] for i in range(len(q_x))])
    v_k = (1 + tasa) ** (-cobertura)
    PNU = SA * v_k * npx
    return np.round(PNU, 2)


def seguro_dotal_mixto(edad, sexo, status, tasa, SA_T, SA_D, cobertura):
    s_temporal = seguro_temporal(edad, sexo, status, tasa, SA_T, cobertura)
    s_dotal = seguro_dotal(edad, sexo, status, tasa, SA_D, cobertura)
    PNU = s_temporal + s_dotal
    return np.round(PNU,2)

def calcular_PNU(tipo_seguro,edad, sexo, status, tasa, SA_T, SA_D, cobertura):
    if tipo_seguro == 'T':
        PNU = seguro_temporal(edad, sexo, status, tasa, SA_T, cobertura)
    elif tipo_seguro == 'V':
        PNU = seguro_vitalicio(edad, sexo, status, tasa, SA_T)
    elif tipo_seguro == 'DM':
        PNU = seguro_dotal_mixto(edad, sexo, status, tasa, SA_T, SA_D, cobertura)
    return np.round(PNU,2)

def anualidad(edad, sexo, status, tasa, pagos):
    edad = edad_asegurable(edad, sexo, status)
    k = list(range(pagos))
    x_k = list(range(edad, edad + pagos))
    q_x = np.array(tabla_mortalidad.loc[x_k[0]:x_k[-1], 'qx'])
    v_k1 = [(1+tasa)**(-x) for x in k]
    kp_x = [1]
    for i in range(pagos-1):
        valor = kp_x[i] * (1-q_x[i])
        kp_x.append(valor)
    anualidad = sum(np.array(v_k1) * np.array(kp_x))
    return anualidad

# Añadiendo una columna de ID de cliente con valores únicos
data.insert(0, 'Cliente_ID', range(1, 1 + len(data)))

data['PNU'] =  data.apply(lambda x: calcular_PNU(x.PROD, x.ECON, x.SEXO, x.STATUS, x.T_P, x.SAF, x.SAD, x.COB), axis = 1)
data['Anualidad'] = data.apply(lambda x: anualidad(x.ECON, x.SEXO, x.STATUS, x.T_P, x.PAG), axis = 1)


GA = 0.15
CA = 0.15
U = 0.20

data['PT'] = data['PNU'] / (1-GA-CA-U)
data['PT'] = data['PT'].map(lambda x: np.round(x,2))

data['PA'] = data['PT']/ data['Anualidad']
data['PA'] = data['PA'].map(lambda x: np.round(x,2))

data['Anualidad'] = data['Anualidad'].map(lambda x: np.round(x,3))

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/alejandrosanchez/Documents/my-project-1567109950451-222fb56cd2dc.json', scope)
client = gspread.authorize(creds)

spreadsheet_id = '1u_YUCcPcVeSAgV3sJJQxdwHXO1adoBRuYAjyn9M4tlw'  
sheet = client.open_by_key(spreadsheet_id)

worksheet = sheet.get_worksheet(0)
worksheet.update([data.columns.values.tolist()] + data.values.tolist())

# Mostrando las primeras filas del DataFrame 'data' para verificar
print(data.head())

