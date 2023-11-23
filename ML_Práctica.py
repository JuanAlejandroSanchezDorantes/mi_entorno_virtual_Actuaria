import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Cargar el conjunto de datos
data = pd.read_csv('/Users/alejandrosanchez/Downloads/app_scoring 2/application_data.csv')

# Separa las características (X) y el objetivo (y)
X = data.drop('TARGET', axis=1)
y = data['TARGET']

# Dividir los datos en conjuntos de entrenamiento y validación
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Identificar columnas categóricas y numéricas
categorical_cols = X_train.select_dtypes(include=['object', 'category']).columns
numerical_cols = X_train.select_dtypes(exclude=['object', 'category']).columns

# Crear transformadores para datos numéricos y categóricos
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))])

# Preprocesamiento de paquetes de datos numéricos y categóricos
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)])

# Definir el modelo de regresión logística
logreg_model = LogisticRegression(max_iter=10000, random_state=42)

# Crear un pipeline que combine el preprocesador con el modelo
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', logreg_model)])

# Entrenar el modelo
pipeline.fit(X_train, y_train)

# Predecir probabilidades en el conjunto de validación
y_val_pred = pipeline.predict_proba(X_val)[:, 1]

# Calcular las puntuaciones ROC AUC para los conjuntos de entrenamiento y validación
train_auc = roc_auc_score(y_train, pipeline.predict_proba(X_train)[:, 1])
val_auc = roc_auc_score(y_val, y_val_pred)

# Imprimir las puntuaciones AUC
print(f'Entrenamiento AUC: {train_auc}')
print(f'Validación AUC: {val_auc}')

# Extraer importancias de características
# Obtenga los nombres de las características codificadas en un punto
ohe = (pipeline.named_steps['preprocessor']
       .named_transformers_['cat']
       .named_steps['onehot'])
feature_names = ohe.get_feature_names_out(input_features=categorical_cols)
feature_names = np.r_[numerical_cols, feature_names]

# Obtener los coeficientes del modelo de regresión logística
coefficients = pipeline.named_steps['model'].coef_[0]

# Asignar coeficientes a nombres de características
feature_importance = zip(feature_names, coefficients)

# Ordenar las características por valor absoluto del coeficiente
sorted_features = sorted(feature_importance, key=lambda x: abs(x[1]), reverse=True)

# Imprime las 10 características más importantes
print('Las 10 funciones más importantes:')
for feature, coef in sorted_features[:10]:
    print(f'{feature}: {coef}')

