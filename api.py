# api.py (Unificado e Corrigido)
import pandas as pd
import numpy as np
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from collections import Counter

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
# PARTE 2: LÓGICA DE SINTOMAS (HEATMAP) - CORRIGIDA (IDENTICA AO COLAB)
# ==========================================
# No arquivo: viniciushashizume/.../api.py

def processar_sintomas():
    try:
        filename = 'Dataset-Mental-Disorders.csv'
        if not os.path.exists(filename):
             print(f"[Sintomas] AVISO: '{filename}' não encontrado.")
             return None

        # 1. Carregar CSV
        df = pd.read_csv(filename)

        if 'Patient Number' in df.columns:
            df = df.drop('Patient Number', axis=1)

        # 2. Renomear colunas (IGUAL AO COLAB)
        # O Colab usa este mapa para corrigir os nomes. O API precisa dele também.
        col_rename_map = {
            'Euphoric': 'Euphoria',
            'Sleep dissorder': 'Sleep_dissorder',
            'Mood Swing': 'Mood_Swing',
            'Suicidal thoughts': 'Suicidal_thoughts',
            'Anorxia': 'Anorexia',
            'Sexual Activity': 'Sexual_Activity'
        }
        df = df.rename(columns=col_rename_map)

        # 3. Mapas de Valores
        freq_map = {'Seldom': 1, 'Sometimes': 2, 'Usually': 3, 'Most-Often': 4}
        yes_no_map = {'YES': 1, 'NO': 0, 'YES ': 1} # 'YES ' com espaço p/ garantir

        target = 'Expert Diagnose'
        potential_symptoms = [
            'Sadness', 'Euphoria', 'Exhausted', 'Sleep_dissorder',
            'Mood_Swing', 'Suicidal_thoughts', 'Anorexia', 'Sexual_Activity'
        ]
        
        # Agora que renomeamos, 'symptoms' deve encontrar todas as 8 colunas
        symptoms = [c for c in potential_symptoms if c in df.columns]

        if not symptoms:
            return None

        # 4. Conversão de Texto para Números
        for col in df.columns:
            if col == target:
                continue

            if df[col].dtype == 'object':
                # Pega o primeiro valor válido para decidir qual mapa usar
                try:
                    first_val = df[col].dropna().iloc[0]
                except IndexError:
                    continue

                if first_val in freq_map:
                    df[col] = df[col].map(freq_map)
                elif first_val in yes_no_map:
                    df[col] = df[col].map(yes_no_map)
                else:
                    # Fallback
                    le = LabelEncoder()
                    df[col] = le.fit_transform(df[col].astype(str))

        df = df.fillna(0)

        # 5. Agrupar e Calcular Média
        symptom_matrix = df.groupby(target)[symptoms].mean()

        # 6. Forçar a ordem das classes (Igual ao Colab)
        class_labels = ['Bipolar Type-1', 'Bipolar Type-2', 'Depression', 'Normal']
        symptom_matrix = symptom_matrix.reindex(class_labels, fill_value=0)

        return {
            "symptoms": list(symptom_matrix.columns),
            "diagnoses": list(symptom_matrix.index),
            "matrix": symptom_matrix.values.tolist(),
            "min_val": 0,
            "max_val": float(symptom_matrix.max().max())
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


# ==========================================
# PARTE 3: LÓGICA DE LINGUÍSTICA (NLP)
# ==========================================

def get_vocab_cleaned(texts, final_stops):
    all_text = ' '.join(texts).lower()
    raw_words = all_text.split()
    cleaned_words = []
    for w in raw_words:
        clean_w = w.strip(".,!?:;\"'()[]{}*-")
        if len(clean_w) > 2 and clean_w not in final_stops and clean_w.isalpha():
            cleaned_words.append(clean_w)
    return cleaned_words

def analyze_distinctive_words_logic(df, class_a_label, class_b_label):
    base_stops = set(ENGLISH_STOP_WORDS)
    custom_stops = {
        "me", "my", "myself", "i", "im", "i'm", "ive", "i've", "id", "i'd",
        "its", "it's", "dont", "don't", "cant", "can't", "wont", "won't",
        "didnt", "didn't", "doesnt", "doesn't", "isnt", "isn't", "arent", "aren't",
        "wasnt", "wasn't", "werent", "weren't", "hasnt", "hasn't", "havent", "haven't",
        "hadnt", "hadn't", "wouldnt", "wouldn't", "shouldnt", "shouldn't", "couldnt", "couldn't",
        "thats", "that's", "theres", "there's", "heres", "here's", "whats", "what's",
        "youre", "you're", "we're", "they're", "yall", "just", "really", "very", "like", 
        "actually", "literally", "basically", "want", "know", "think", "going", "got", 
        "get", "make", "time", "day", "people", "thing", "things", "said"
    }
    final_stops = base_stops.union(custom_stops)

    texts_a = df[df['status'] == class_a_label]['clean_statement'].astype(str)
    texts_b = df[df['status'] == class_b_label]['clean_statement'].astype(str)

    vocab_a = Counter(get_vocab_cleaned(texts_a, final_stops))
    vocab_b = Counter(get_vocab_cleaned(texts_b, final_stops))

    total_a = sum(vocab_a.values())
    total_b = sum(vocab_b.values())

    if total_a == 0 or total_b == 0:
        return []

    distinctive_score = {}
    all_keys = set(vocab_a.keys()).union(set(vocab_b.keys()))

    for word in all_keys:
        freq_a = vocab_a.get(word, 0) / total_a
        freq_b = vocab_b.get(word, 0) / total_b
        score = (freq_a - freq_b) * 1000
        distinctive_score[word] = score

    top_a = sorted(distinctive_score.items(), key=lambda x: x[1], reverse=True)[:20]
    result_data = [{"word": word, "score": round(score, 1)} for word, score in top_a if score > 0]
    return result_data[:15]

@app.get("/api/linguistica-data")
def get_linguistica_data():
    filename = 'Combined Data.csv'
    if not os.path.exists(filename):
        return {"error": f"Arquivo '{filename}' não encontrado."}
    
    try:
        df = pd.read_csv(filename)
        df.columns = [c.strip().lower().replace(' ', '_') for c in df.columns]
        
        if 'statement' in df.columns and 'clean_statement' not in df.columns:
            df['clean_statement'] = df['statement']
            
        if 'status' not in df.columns:
             return {"error": "Coluna 'status' não encontrada no CSV."}

        df['clean_statement'] = df['clean_statement'].fillna('')

        diagnosticos_alvo = ['Depression', 'Anxiety', 'Suicidal', 'Stress', 'Bipolar']
        base_normal = 'Normal'
        
        response_data = {}

        for diag in diagnosticos_alvo:
            unique_statuses = df['status'].unique()
            match = next((s for s in unique_statuses if str(s).lower() == diag.lower()), None)
            match_normal = next((s for s in unique_statuses if str(s).lower() == base_normal.lower()), None)
            
            if match and match_normal:
                words_data = analyze_distinctive_words_logic(df, match, match_normal)
                response_data[diag] = words_data
            else:
                response_data[diag] = []

        return response_data

    except Exception as e:
        print(f"Erro NLP: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)