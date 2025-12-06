import pandas as pd
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_clusters():
    try:
        try:
            df = pd.read_csv('mental_health_dataset.csv')
            print("CSV carregado com sucesso.")
            
            # Normaliza nomes das colunas
            df.columns = [c.strip().lower().replace(' ', '_').replace('-', '_') for c in df.columns]
            
            # Renomear colunas específicas para o padrão esperado
            rename_map = {
                'social_support_score': 'social_support',
                'physical_activity_days': 'physical_activity_hours', 
                # Se houver outras discrepâncias, adicione aqui
            }
            df = df.rename(columns=rename_map)
            
            df = df.dropna()
            
            # Codificação de categóricas
            le = LabelEncoder()
            cat_cols = ['gender', 'employment_status', 'work_environment',
                        'mental_health_history', 'seeks_treatment', 'mental_health_risk']
            
            for col in cat_cols:
                if col in df.columns:
                    df[col] = le.fit_transform(df[col].astype(str))
                    
        except FileNotFoundError:
            print("CSV não encontrado.")
            return None, None

        # Features esperadas
        features = ['sleep_hours', 'productivity_score', 'social_support', 
                   'physical_activity_hours', 'stress_level']
        
        # Validação
        cols = [c for c in features if c in df.columns]
        if len(cols) < 5:
            print(f"AVISO: Algumas colunas não foram encontradas. Usando apenas: {cols}")

        # Padronização e Clusterização
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df[cols])

        # Usar 3 clusters
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X_scaled)

        # Calcula médias
        summary = df.groupby('Cluster')[cols].mean()
        
        return summary, df

    except Exception as e:
        print(f"Erro no processamento: {e}")
        import traceback
        traceback.print_exc()
        return None, None

@app.get("/api/dashboard-data")
def get_dashboard_data():
    summary, _ = process_clusters()
    
    if summary is None:
        raise HTTPException(status_code=500, detail="Erro ao processar dados.")

    def get_val(row, col_name):
        return float(row[col_name]) if col_name in row else 0.0

    # Lógica de Classificação dos Perfis
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
        id_stressed: {
            "name": "Estressado Isolado",
            "color": "hsl(0, 84%, 60%)", 
            "desc": "Níveis críticos de estresse combinados com baixo suporte social."
        },
        id_balanced: {
            "name": "Produtivo Sedentário",
            "color": "hsl(152, 69%, 40%)", 
            "desc": "Alta performance profissional, mas baixa atividade física."
        },
        id_social: {
            "name": "Social Disperso",
            "color": "hsl(38, 92%, 50%)", 
            "desc": "Forte conexão social e física, mas produtividade reduzida."
        }
    }

    # Configuração do Gráfico (Escala Visual 0-10)
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
        
        # --- NORMALIZAÇÃO VISUAL ---
        # Sono (0-10): Mantém original
        radar_data[0][name] = round(get_val(row, 'sleep_hours'), 1)
        
        # Produtividade (0-100): Divide por 10
        radar_data[1][name] = round(get_val(row, 'productivity_score') / 10, 1)
        
        # Social (0-100): Divide por 10  <-- CORREÇÃO AQUI
        radar_data[2][name] = round(get_val(row, 'social_support') / 10, 1)
        
        # Físico (0-7 ou 0-10): Mantém original (se for dias da semana, max é 7)
        radar_data[3][name] = round(get_val(row, 'physical_activity_hours'), 1)
        
        # Estresse (0-10): Mantém original
        radar_data[4][name] = round(get_val(row, 'stress_level'), 1)

    # Dados para os Cards (Mantém valores originais para leitura correta)
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
        
        # Ajuste texto de social para refletir escala 0-100
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
                "Social": int(social_val), # Valor original inteiro
                "Physical": round(get_val(row, 'physical_activity_hours'), 1),
                "Stress": round(stress_val, 1),
            },
            "strengths": strengths,
            "weaknesses": weaknesses
        })

    return {
        "radarData": radar_data,
        "clusters": clusters_info
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)