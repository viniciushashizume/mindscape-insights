import { useState, useEffect } from "react";
import {
  RadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";
import { ClusterCard } from "./ClusterCard";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert"; // Mantido caso queira usar depois
import { AlertCircle } from "lucide-react";

// =========================================================================
// ÁREA DE EDIÇÃO MANUAL DOS VALORES (DADOS ESTÁTICOS)
// =========================================================================
// Instruções:
// 1. Ajuste os valores numéricos abaixo conforme seu Heatmap/Análise.
// 2. A escala do gráfico é de 0 a 10.
//    - Se sua produtividade é 66 (0-100), coloque 6.6 aqui.
//    - Se seu estresse é 3 (0-10), coloque 3.0 aqui.
// =========================================================================

const MANUAL_CLUSTERS = [
  {
    id: 0,
    name: "Grupo 1", // Correspondente ao Cluster 0 do seu Python
    description: "Níveis críticos de estresse combinados com baixo suporte social.",
    color: "hsl(0, 84%, 60%)", // Vermelho
    metrics: {
      // Valores baseados no output do seu arquetipos.py
      Sleep: 7.5,        // sleep_hours
      Productivity: 5.4, // productivity_score (54 / 10)
      Social: 2.6,       // social_support
      Physical: 3.3,     // physical_activity_hours
      Stress: 6.5,       // stress_level
    },
    strengths: ["Sono Regular"],
    weaknesses: ["Alto Estresse (6.5/10)", "Isolamento Social", "Produtividade Média"],
  },
  {
    id: 1,
    name: "Grupo 2", // Correspondente ao Cluster 1 do seu Python
    description: "Alta performance profissional, mas baixa atividade física.",
    color: "hsl(152, 69%, 40%)", // Verde
    metrics: {
      Sleep: 6.8,
      Productivity: 6.6, // 66 / 10
      Social: 5.8,
      Physical: 1.9,
      Stress: 3.0,
    },
    strengths: ["Alta Produtividade", "Baixo Estresse"],
    weaknesses: ["Sedentarismo (1.9h)", "Sono Levemente Reduzido"],
  },
  {
    id: 2,
    name: "Grupo 3", // Correspondente ao Cluster 2 do seu Python (Baixa Produtividade)
    description: "Forte conexão social e física, mas produtividade reduzida.",
    color: "hsl(38, 92%, 50%)", // Amarelo/Laranja
    metrics: {
      Sleep: 6.3,
      Productivity: 2.5, // 25 / 10
      Social: 6.4,
      Physical: 4.0,
      Stress: 4.5,
    },
    strengths: ["Bom Suporte Social", "Atividade Física Regular"],
    weaknesses: ["Baixa Produtividade (2.5/10)", "Sono Irregular"],
  },
];

// =========================================================================

// Tipos
interface ClusterData {
  id: number;
  name: string;
  description: string;
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

export function ArquetiposTab() {
  const [activeCluster, setActiveCluster] = useState<number | null>(null);
  const [data, setData] = useState<{ radarData: any[]; clusters: ClusterData[] } | null>(null);

  useEffect(() => {
    // Transforma os dados manuais para o formato do Recharts
    const clusters = MANUAL_CLUSTERS;

    const radarData = [
      { metric: "Sono", fullMark: 10 },
      { metric: "Produtividade", fullMark: 10 },
      { metric: "Social", fullMark: 10 },
      { metric: "Físico", fullMark: 10 },
      { metric: "Estresse", fullMark: 10 },
    ];

    // Popula o radarData com os valores de cada cluster
    clusters.forEach((cluster) => {
      radarData[0][cluster.name] = cluster.metrics.Sleep;
      radarData[1][cluster.name] = cluster.metrics.Productivity;
      radarData[2][cluster.name] = cluster.metrics.Social;
      radarData[3][cluster.name] = cluster.metrics.Physical;
      radarData[4][cluster.name] = cluster.metrics.Stress;
    });

    setData({ radarData, clusters });
  }, []);

  if (!data) return null;

  const { radarData, clusters } = data;

  return (
    <div className="animate-fade-in space-y-6 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <h2 className="mb-4 text-center text-sm font-medium text-muted-foreground">
          Análise de Arquétipos (Valores Fixos - Heatmap)
        </h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
              <PolarGrid stroke="hsl(var(--border))" strokeDasharray="3 3" />
              <PolarAngleAxis 
                dataKey="metric" 
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
              />
              <PolarRadiusAxis 
                angle={30} 
                domain={[0, 10]} // Domínio fixo em 10 para consistência visual
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "12px",
                  boxShadow: "var(--shadow-soft)",
                }}
                labelStyle={{ color: "hsl(var(--foreground))" }}
              />
              {clusters.map((cluster) => (
                <Radar
                  key={cluster.id}
                  name={cluster.name}
                  dataKey={cluster.name}
                  stroke={cluster.color}
                  fill={cluster.color}
                  fillOpacity={activeCluster === null || activeCluster === cluster.id ? 0.3 : 0.05}
                  strokeWidth={activeCluster === cluster.id ? 3 : 1.5}
                />
              ))}
              <Legend wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }} />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="px-1 text-sm font-medium text-muted-foreground">
          Interpretação dos Grupos
        </h3>
        {clusters.map((cluster) => (
          <div key={cluster.id} className="relative">
             <ClusterCard
                cluster={cluster}
                isActive={activeCluster === cluster.id}
                onClick={() => setActiveCluster(
                  activeCluster === cluster.id ? null : cluster.id
                )}
              />
              <div className="mt-2 px-2 text-xs text-muted-foreground italic">
                "{cluster.description}"
              </div>
          </div>
        ))}
      </div>
    </div>
  );
}