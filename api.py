# api.py (Unificado)
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# PARTE 1: LÓGICA DE ARQUÉTIPOS (DASHBOARD)
# ==========================================
def process_clusters():
    try:
        try:
            # Tenta carregar o dataset de arquétipos
            df = pd.read_csv('mental_health_dataset.csv')
            print("[Arquétipos] CSV carregado com sucesso.")
            
            df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
            
            rename_map = {
                'social_support_score': 'social_support',
                'physical_activity_days': 'physical_activity_hours', 
            }
            df = df.rename(columns=rename_map)
            df = df.dropna()
            
            le = LabelEncoder()
            cat_cols = ['gender', 'employment_status', 'work_environment',
                        'mental_health_history', 'seeks_treatment', 'mental_health_risk']
            
            for col in cat_cols:
                if col in df.columns:
                    df[col] = le.fit_transform(df[col].astype(str))
                    
        except FileNotFoundError:
            print("[Arquétipos] ERRO: 'mental_health_dataset.csv' não encontrado.")
            return None, None

        features = ['sleep_hours', 'productivity_score', 'social_support', 
                   'physical_activity_hours', 'stress_level']
        
        cols = [c for c in features if c in df.columns]
        if len(cols) < 5:
            print(f"[Arquétipos] AVISO: Colunas insuficientes. Usando: {cols}")

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[cols])

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X_scaled)

        summary = df.groupby('Cluster')[cols].mean()
        
        return summary, df

    except Exception as e:
        print(f"[Arquétipos] Erro no processamento: {e}")
        return None, None

@app.get("/api/dashboard-data")
def get_dashboard_data():
    summary, _ = process_clusters()
    
    if summary is None:
        raise HTTPException(status_code=500, detail="Erro ao processar dados de arquétipos.")

    def get_val(row, col_name):
        return float(row[col_name]) if col_name in row else 0.0

    try:
        id_stressed = summary['stress_level'].idxmax()
        remaining = [i for i in range(3) if i != id_stressed]
        id_balanced = summary.loc[remaining, 'productivity_score'].idxmax() if remaining else 0
        remaining_social = [i for i in remaining if i != id_balanced]
        id_social = remaining_social[0] if remaining_social else (0 if id_stressed != 0 and id_balanced != 0 else 1)
    except Exception as e:
        print(f"Erro na classificação: {e}")
        id_stressed, id_balanced, id_social = 0, 1, 2

    cluster_map = {
        id_stressed: {"name": "Estressado Isolado", "color": "hsl(0, 84%, 60%)", "desc": "Níveis críticos de estresse combinados com baixo suporte social."},
        id_balanced: {"name": "Produtivo Sedentário", "color": "hsl(152, 69%, 40%)", "desc": "Alta performance profissional, mas baixa atividade física."},
        id_social: {"name": "Social Disperso", "color": "hsl(38, 92%, 50%)", "desc": "Forte conexão social e física, mas produtividade reduzida."}
    }

    radar_data = [
        {"metric": "Sono", "fullMark": 10},
        {"metric": "Produtividade", "fullMark": 10}, 
        {"metric": "Social", "fullMark": 10},
        {"metric": "Físico", "fullMark": 10},
        {"metric": "Estresse", "fullMark": 10},
    ]

    for idx, row in summary.iterrows():
        if idx not in cluster_map: continue
        name = cluster_map[idx]["name"]
        radar_data[0][name] = round(get_val(row, 'sleep_hours'), 1)
        radar_data[1][name] = round(get_val(row, 'productivity_score') / 10, 1)
        radar_data[2][name] = round(get_val(row, 'social_support') / 10, 1)
        radar_data[3][name] = round(get_val(row, 'physical_activity_hours'), 1)
        radar_data[4][name] = round(get_val(row, 'stress_level'), 1)

    clusters_info = []
    for idx, info in cluster_map.items():
        if idx not in summary.index: continue
        row = summary.loc[idx]
        
        prod_val = get_val(row, 'productivity_score')
        stress_val = get_val(row, 'stress_level')
        social_val = get_val(row, 'social_support')
        
        strengths = []
        weaknesses = []
        
        if prod_val > 50: strengths.append(f"Alta Produtividade ({int(prod_val)})")
        else: weaknesses.append(f"Baixa Produtividade ({int(prod_val)})")
        
        if stress_val < 5: strengths.append("Estresse Controlado")
        else: weaknesses.append(f"Alto Estresse ({int(stress_val)}/10)")
        
        if social_val > 50: strengths.append("Bom Suporte Social")
        else: weaknesses.append("Isolamento Social")

        clusters_info.append({
            "id": int(idx),
            "name": info["name"],
            "description": info["desc"],
            "color": info["color"],
            "metrics": {
                "Sleep": round(get_val(row, 'sleep_hours'), 1),
                "Productivity": int(prod_val),
                "Social": int(social_val),
                "Physical": round(get_val(row, 'physical_activity_hours'), 1),
                "Stress": round(stress_val, 1),
            },
            "strengths": strengths,
            "weaknesses": weaknesses
        })

    return {"radarData": radar_data, "clusters": clusters_info}


# ==========================================
# PARTE 2: LÓGICA DE SINTOMAS (HEATMAP)
# ==========================================
def processar_sintomas():
    try:
        # Tenta encontrar o arquivo correto
        filename = 'Dataset-Mental-Disorders.csv'
        if not os.path.exists(filename):
             # Fallback caso o nome esteja diferente ou não exista
             print(f"[Sintomas] AVISO: '{filename}' não encontrado.")
             return None

        print(f"[Sintomas] Lendo arquivo: {filename}")
        df = pd.read_csv(filename)

        if 'Patient Number' in df.columns:
            df = df.drop('Patient Number', axis=1)

        freq_map = {'Seldom': 1, 'Sometimes': 2, 'Usually': 3, 'Most-Often': 4}
        yes_no_map = {'YES': 1, 'NO': 0, 'YES ': 1, 'NO ': 0}

        for col in df.columns:
            if col == 'Expert Diagnose':
                continue
            if df[col].dtype == 'object':
                first_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else ""
                if first_val in freq_map:
                    df[col] = df[col].map(freq_map)
                elif first_val in yes_no_map:
                    df[col] = df[col].map(yes_no_map)
        
        df = df.fillna(0)

        # Validação da coluna Expert Diagnose
        if 'Expert Diagnose' not in df.columns:
             # Tenta achar coluna parecida
             possiveis = [c for c in df.columns if 'Diagnos' in c]
             if possiveis:
                 df = df.rename(columns={possiveis[0]: 'Expert Diagnose'})
             else:
                 return None

        heatmap_data = df.groupby('Expert Diagnose').mean(numeric_only=True)
        heatmap_data = heatmap_data.select_dtypes(include=[np.number])

        # Ordenação Específica
        desired_order = ['Normal', 'Bipolar Type-1', 'Bipolar Type-2', 'Depression']
        heatmap_data = heatmap_data.reindex([d for d in desired_order if d in heatmap_data.index])

        return {
            "symptoms": list(heatmap_data.columns),
            "diagnoses": list(heatmap_data.index),
            "matrix": heatmap_data.values.tolist(),
            "min_val": float(heatmap_data.min().min()),
            "max_val": float(heatmap_data.max().max())
        }

    except Exception as e:
        print(f"[Sintomas] Erro ao processar dataset: {e}")
        return None

@app.get("/api/sintomas-heatmap")
def get_sintomas_heatmap():
    data = processar_sintomas()
    if data:
        return data
    return {"error": "Erro ao processar dados de sintomas. Verifique se 'Dataset-Mental-Disorders.csv' existe."}


if __name__ == "__main__":
    import uvicorn
    # Roda tudo na porta 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)