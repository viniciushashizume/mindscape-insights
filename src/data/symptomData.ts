export interface SymptomIntensity {
  diagnosis: string;
  symptoms: {
    name: string;
    intensity: number;
  }[];
}

export const diagnoses = ["Normal", "Depressão", "Bipolar", "Ansiedade"];
export const symptoms = ["Tristeza", "Euforia", "Insônia", "Anorexia", "Suicídio", "Inquietação", "Mudança Humor"];

export const symptomMatrix: Record<string, Record<string, number>> = {
  Normal: {
    Tristeza: 0.1,
    Euforia: 0.2,
    Insônia: 0.15,
    Anorexia: 0.1,
    Suicídio: 0.05,
    Inquietação: 0.1,
    "Mudança Humor": 0.15,
  },
  Depressão: {
    Tristeza: 0.92,
    Euforia: 0.1,
    Insônia: 0.85,
    Anorexia: 0.65,
    Suicídio: 0.78,
    Inquietação: 0.35,
    "Mudança Humor": 0.45,
  },
  Bipolar: {
    Tristeza: 0.55,
    Euforia: 0.88,
    Insônia: 0.72,
    Anorexia: 0.3,
    Suicídio: 0.45,
    Inquietação: 0.6,
    "Mudança Humor": 0.95,
  },
  Ansiedade: {
    Tristeza: 0.4,
    Euforia: 0.15,
    Insônia: 0.82,
    Anorexia: 0.35,
    Suicídio: 0.25,
    Inquietação: 0.9,
    "Mudança Humor": 0.5,
  },
};

export const getIntensityColor = (intensity: number): string => {
  if (intensity < 0.25) return "hsl(187, 92%, 85%)";
  if (intensity < 0.5) return "hsl(187, 92%, 65%)";
  if (intensity < 0.75) return "hsl(187, 92%, 45%)";
  return "hsl(263, 70%, 50%)";
};

export const getIntensityLabel = (intensity: number): string => {
  if (intensity < 0.25) return "Baixa";
  if (intensity < 0.5) return "Moderada";
  if (intensity < 0.75) return "Alta";
  return "Crítica";
};
