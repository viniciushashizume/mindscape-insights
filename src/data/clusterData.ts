export interface ClusterData {
  id: number;
  name: string;
  color: string;
  metrics: {
    Sleep: number;
    Productivity: number;
    Social: number;
    Physical: number;
    Stress: number;
  };
  strengths: string[];
  weaknesses: string[];
}

export const clusters: ClusterData[] = [
  {
    id: 0,
    name: "Perfil Estressado",
    color: "hsl(0, 84%, 60%)",
    metrics: {
      Sleep: 7.5,
      Productivity: 54,
      Social: 2.6,
      Physical: 3.3,
      Stress: 6.5,
    },
    strengths: ["Boa qualidade de sono (7.5h)", "Produtividade mediana"],
    weaknesses: ["Alto nível de estresse", "Baixa interação social", "Atividade física limitada"],
  },
  {
    id: 1,
    name: "Perfil Equilibrado",
    color: "hsl(152, 69%, 40%)",
    metrics: {
      Sleep: 6.8,
      Productivity: 66,
      Social: 5.8,
      Physical: 1.9,
      Stress: 3.0,
    },
    strengths: ["Baixo estresse", "Alta produtividade", "Boa vida social"],
    weaknesses: ["Atividade física muito baixa", "Sono levemente reduzido"],
  },
  {
    id: 2,
    name: "Perfil Risco Social",
    color: "hsl(38, 92%, 50%)",
    metrics: {
      Sleep: 6.3,
      Productivity: 25,
      Social: 6.4,
      Physical: 4.0,
      Stress: 4.5,
    },
    strengths: ["Excelente vida social", "Boa atividade física"],
    weaknesses: ["Produtividade muito baixa", "Sono insuficiente", "Estresse moderado"],
  },
];

export const radarData = [
  { metric: "Sono", "Perfil Estressado": 7.5, "Perfil Equilibrado": 6.8, "Perfil Risco Social": 6.3, fullMark: 10 },
  { metric: "Produtividade", "Perfil Estressado": 5.4, "Perfil Equilibrado": 6.6, "Perfil Risco Social": 2.5, fullMark: 10 },
  { metric: "Social", "Perfil Estressado": 2.6, "Perfil Equilibrado": 5.8, "Perfil Risco Social": 6.4, fullMark: 10 },
  { metric: "Físico", "Perfil Estressado": 3.3, "Perfil Equilibrado": 1.9, "Perfil Risco Social": 4.0, fullMark: 10 },
  { metric: "Estresse", "Perfil Estressado": 6.5, "Perfil Equilibrado": 3.0, "Perfil Risco Social": 4.5, fullMark: 10 },
];
