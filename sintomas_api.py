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