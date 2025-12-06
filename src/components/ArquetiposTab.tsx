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
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { AlertCircle } from "lucide-react";

// Tipos adaptados para a resposta da API
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
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Buscar dados da API Python
    fetch("http://localhost:8000/api/dashboard-data")
      .then((res) => {
        if (!res.ok) throw new Error("Falha ao conectar com a API Python");
        return res.json();
      })
      .then((data) => {
        setData(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Não foi possível carregar os dados do dataset. Certifique-se que o 'api.py' está rodando.");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div className="space-y-6 p-4">
        <Skeleton className="h-72 w-full rounded-2xl" />
        <Skeleton className="h-32 w-full rounded-2xl" />
        <Skeleton className="h-32 w-full rounded-2xl" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="p-4">
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertTitle>Erro de Conexão</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      </div>
    );
  }

  const { radarData, clusters } = data;

  return (
    <div className="animate-fade-in space-y-6 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <h2 className="mb-4 text-center text-sm font-medium text-muted-foreground">
          Análise de Arquétipos (Baseado no Dataset)
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
                // Ajuste o domínio baseado na escala máxima dos seus dados (ex: Produtividade vai até 100)
                domain={[0, 'auto']} 
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
              {/* Adicionando a descrição analítica personalizada abaixo do card quando ativo ou sempre */}
              <div className="mt-2 px-2 text-xs text-muted-foreground italic">
                "{cluster.description}"
              </div>
          </div>
        ))}
      </div>
    </div>
  );
}