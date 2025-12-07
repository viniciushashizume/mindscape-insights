# sintomas_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np

app = FastAPI()

# Configuração de CORS para permitir que o Frontend (localhost:5173 ou similar) acesse o Backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique a URL do seu site
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def processar_dataset():
    try:
        # Carregar o dataset
        df = pd.read_csv('Dataset-Mental-Disorders.csv')

        # Remover colunas desnecessárias
        if 'Patient Number' in df.columns:
            df = df.drop('Patient Number', axis=1)

        # Mapeamentos (Baseado no seu código original)
        freq_map = {'Seldom': 1, 'Sometimes': 2, 'Usually': 3, 'Most-Often': 4}
        yes_no_map = {'YES': 1, 'NO': 0, 'YES ': 1, 'NO ': 0}

        # Aplicar mapeamentos
        for col in df.columns:
            # Ignorar a coluna de diagnóstico por enquanto
            if col == 'Expert Diagnose':
                continue
                
            if df[col].dtype == 'object':
                # Tenta mapear frequência
                if df[col].iloc[0] in freq_map:
                    df[col] = df[col].map(freq_map)
                # Tenta mapear Sim/Não
                elif df[col].iloc[0] in yes_no_map:
                    df[col] = df[col].map(yes_no_map)
        
        # Preencher valores nulos com 0
        df = df.fillna(0)

        # Agrupar por Diagnóstico e calcular a média (intensidade) dos sintomas
        # Isso cria a matriz do Heatmap
        heatmap_data = df.groupby('Expert Diagnose').mean()

        # Garantir que as classes desejadas existam e estejam na ordem correta
        desired_order = ['Normal', 'Bipolar Type-1', 'Bipolar Type-2', 'Depression']
        
        # Filtrar apenas as colunas numéricas (sintomas)
        heatmap_data = heatmap_data.select_dtypes(include=[np.number])
        
        # Reordenar linhas se existirem no dataset
        heatmap_data = heatmap_data.reindex([d for d in desired_order if d in heatmap_data.index])

        # Formatar para JSON
        result = {
            "symptoms": list(heatmap_data.columns),
            "diagnoses": list(heatmap_data.index),
            "matrix": heatmap_data.values.tolist(),
            "min_val": float(heatmap_data.min().min()),
            "max_val": float(heatmap_data.max().max())
        }
        
        return result

    except Exception as e:
        print(f"Erro ao processar dataset: {e}")
        return None

@app.get("/api/sintomas-heatmap")
def get_sintomas_heatmap():
    data = processar_dataset()
    if data:
        return data
    return {"error": "Erro ao processar dados"}

# Para rodar: uvicorn sintomas_api:app --reload