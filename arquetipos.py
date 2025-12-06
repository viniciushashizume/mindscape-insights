# --- DATASET 1: mental_health_dataset.csv (Fatores de Risco e Estilo de Vida) ---
try:
    df_lifestyle = pd.read_csv('mental_health_dataset.csv')

    # Limpeza básica
    df_lifestyle = df_lifestyle.dropna()

    # Codificação de variáveis categóricas (Gender, Employment, etc.)
    le_lifestyle = LabelEncoder()
    cat_cols_lifestyle = ['gender', 'employment_status', 'work_environment',
                          'mental_health_history', 'seeks_treatment', 'mental_health_risk']

    for col in cat_cols_lifestyle:
        if col in df_lifestyle.columns:
            df_lifestyle[col] = le_lifestyle.fit_transform(df_lifestyle[col].astype(str))

    print("Dataset 1 (Lifestyle) Pré-processado. Shape:", df_lifestyle.shape)

except Exception as e:
    print(f"Erro ao processar Dataset 1: {e}")

# --- DATASET 2: Dataset-Mental-Disorders.csv (Sintomas Clínicos) ---
try:
    df_clinical = pd.read_csv('Dataset-Mental-Disorders.csv')

    # Remover coluna de ID se existir
    if 'Patient Number' in df_clinical.columns:
        df_clinical = df_clinical.drop('Patient Number', axis=1)

    # Mapeamento manual para transformar texto em números (Ordem importa aqui)
    freq_map = {'Seldom': 1, 'Sometimes': 2, 'Usually': 3, 'Most-Often': 4}
    yes_no_map = {'YES': 1, 'NO': 0, 'YES ': 1} # Tratando espaços extras

    # Aplicando mapeamentos
    for col in df_clinical.columns:
        if df_clinical[col].dtype == 'object':
            # Tenta mapear frequência, se não der, tenta sim/não, se não, usa LabelEncoder
            if df_clinical[col].iloc[0] in freq_map:
                df_clinical[col] = df_clinical[col].map(freq_map)
            elif df_clinical[col].iloc[0] in yes_no_map:
                df_clinical[col] = df_clinical[col].map(yes_no_map)
            else:
                # Para a coluna alvo (Expert Diagnose) e outras mistas
                le = LabelEncoder()
                df_clinical[col] = le.fit_transform(df_clinical[col].astype(str))

    df_clinical = df_clinical.fillna(0) # Tratar nulos residuais
    print("Dataset 2 (Clinical) Pré-processado. Shape:", df_clinical.shape)

except Exception as e:
    print(f"Erro ao processar Dataset 2: {e}")

    import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import numpy as np

# --- 1. Geração de Dados Fictícios (Para teste) ---
# Se você já tem seu df_lifestyle, pode ignorar este bloco.
np.random.seed(42)
n_samples = 200
data = {
    'sleep_hours': np.random.normal(7, 1.5, n_samples),
    'productivity_score': np.random.randint(1, 100, n_samples),
    'social_support': np.random.randint(1, 10, n_samples),
    'physical_activity_hours': np.random.normal(3, 2, n_samples),
    'stress_level': np.random.randint(1, 10, n_samples)
}
df_lifestyle = pd.DataFrame(data)
# Garantir valores não negativos onde não faz sentido
df_lifestyle[df_lifestyle < 0] = 0

# --- 2. Função de Análise Atualizada ---
def analyze_patient_profiles(df):
    print("--- Insight Clínico: Identificação de Arquétipos de Pacientes (Clustering) ---")

    # Lista de features desejadas
    features = ['sleep_hours', 'productivity_score', 'social_support',
                'physical_activity_hours', 'stress_level']

    # Filtrar colunas que realmente existem no df
    cols = [c for c in features if c in df.columns]

    if not cols:
        print("Erro: Nenhuma das colunas necessárias foi encontrada no DataFrame.")
        return

    print(f"Features utilizadas na análise: {cols}")

    # Padronizar os dados (Essencial para o K-Means funcionar bem com escalas diferentes)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[cols])

    # Criar 3 Clusters (Perfis)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled)

    # Calcular as médias de cada grupo (Valores Numéricos)
    profile_summary = df.groupby('Cluster')[cols].mean()

    # --- NOVO: Exibir os valores numéricos no terminal ---
    print("\n" + "="*50)
    print("RESUMO NUMÉRICO DOS CLUSTERS (Médias por Feature)")
    print("="*50)
    # Transpondo (.T) para facilitar a leitura se houver muitas colunas
    print(profile_summary.T)
    print("="*50 + "\n")

    # Visualização
    plt.figure(figsize=(12, 7))

    # Usando profile_summary.T para que as Features fiquem no eixo Y e Clusters no eixo X
    sns.heatmap(profile_summary.T, cmap='RdYlGn', annot=True, fmt='.2f', linewidths=1)

    plt.title('Arquétipos de Pacientes: Mapa de Calor das Médias')
    plt.xlabel('Grupo (Cluster)')
    plt.ylabel('Fatores de Estilo de Vida')
    plt.tight_layout() # Ajusta o layout para não cortar labels
    plt.show()

    print("Interpretação Sugerida dos Clusters Gerados (baseado nos dados):")
    print("Verifique o heatmap acima e correlacione com os números impressos.")
    print("- Valores altos em verde (dependendo do cmap).")
    print("- Valores baixos em vermelho.")

# Executar a análise
if 'df_lifestyle' in globals():
    analyze_patient_profiles(df_lifestyle)

'''--- Insight Clínico: Identificação de Arquétipos de Pacientes (Clustering) ---
Features utilizadas na análise: ['sleep_hours', 'productivity_score', 'social_support', 'physical_activity_hours', 'stress_level']

==================================================
RESUMO NUMÉRICO DOS CLUSTERS (Médias por Feature)
==================================================
Cluster                          0          1          2
sleep_hours               7.527759   6.836834   6.295154
productivity_score       54.173333  66.298507  25.137931
social_support            2.653333   5.791045   6.413793
physical_activity_hours   3.301562   1.888564   4.059343
stress_level              6.520000   3.074627   4.482759
=================================================='''