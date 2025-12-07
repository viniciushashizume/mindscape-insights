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


import matplotlib.pyplot as plt
import seaborn as sns

def plot_symptom_overlap_with_labels(df):
    print("--- Insight Clínico: Assinatura Sintomática (Com Rótulos) ---")

    # 1. Definir sintomas
    potential_symptoms = ['Sadness', 'Euphoria', 'Exhausted', 'Sleep_dissorder',
                          'Mood_Swing', 'Suicidal_thoughts', 'Anorexia', 'Sexual_Activity']

    symptoms = [c for c in potential_symptoms if c in df.columns]
    target = 'Expert Diagnose'

    # 2. Definir os nomes das Classes (Baseado na ordem alfabética do LabelEncoder)
    # 0: Bipolar 1, 1: Bipolar 2, 2: Depression, 3: Normal
    class_labels = ['Bipolar Type-1', 'Bipolar Type-2', 'Depression', 'Normal']

    # Verifica se os sintomas existem no DF
    if not symptoms or target not in df.columns:
        print("Dados necessários não encontrados.")
        return

    # 3. Agrupar e Calcular a Média
    symptom_matrix = df.groupby(target)[symptoms].mean()

    # CORREÇÃO 1: Preencher valores vazios (NaN) com 0
    symptom_matrix = symptom_matrix.fillna(0)

    # CORREÇÃO 2: Verificar se a classe 'Normal' (índice 3 provavelmente) existe
    # Se ela não existir na matriz (porque não tinha dados), vamos criá-la com zeros
    # Nota: Isso assume que o LabelEncoder usou 0,1,2,3.
    # Se 'Normal' for o índice 3 e não estiver no índice, adicionamos:
    if 3 not in symptom_matrix.index:
         # Adiciona uma linha de zeros para a classe 3
         symptom_matrix.loc[3] = 0
         # Reordena para garantir 0, 1, 2, 3
         symptom_matrix = symptom_matrix.sort_index()

    # 4. Plotar (Adicionando vmin=0 para forçar a escala a começar do zero)
    plt.figure(figsize=(12, 6))

    sns.heatmap(symptom_matrix, cmap='magma_r', annot=True, fmt='.2f',
                yticklabels=class_labels,
                vmin=0)  # <--- Isso garante que o 0 tenha cor (provavelmente amar

    plt.title('Assinatura Sintomática: Intensidade dos Sintomas por Diagnóstico')
    plt.ylabel('Diagnóstico')
    plt.xlabel('Sintomas')
    plt.yticks(rotation=0) # Deixa os nomes na horizontal para facilitar leitura
    plt.show()

    print("Insight Atualizado:")
    print(f"- Observe a linha 'Normal': Ela deve ser a mais clara (valores baixos), indicando ausência de sintomas graves.")
    print(f"- Compare 'Normal' com 'Depression': A diferença na coluna 'Sadness' deve ser gritante.")

# Executar
if 'df_clinical' in globals():
    plot_symptom_overlap_with_labels(df_clinical)