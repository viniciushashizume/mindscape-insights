import { useState } from "react";
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
import { clusters, radarData } from "@/data/clusterData";
import { ClusterCard } from "./ClusterCard";

export function ArquetiposTab() {
  const [activeCluster, setActiveCluster] = useState<number | null>(null);

  return (
    <div className="animate-fade-in space-y-6 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <h2 className="mb-4 text-center text-sm font-medium text-muted-foreground">
          Comparação de Clusters
        </h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart data={radarData} margin={{ top: 20, right: 30, bottom: 20, left: 30 }}>
              <PolarGrid 
                stroke="hsl(var(--border))" 
                strokeDasharray="3 3"
              />
              <PolarAngleAxis 
                dataKey="metric" 
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
              />
              <PolarRadiusAxis 
                angle={30} 
                domain={[0, 10]} 
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
              <Radar
                name="Perfil Estressado"
                dataKey="Perfil Estressado"
                stroke="hsl(0, 84%, 60%)"
                fill="hsl(0, 84%, 60%)"
                fillOpacity={activeCluster === null || activeCluster === 0 ? 0.3 : 0.05}
                strokeWidth={activeCluster === 0 ? 3 : 1.5}
              />
              <Radar
                name="Perfil Equilibrado"
                dataKey="Perfil Equilibrado"
                stroke="hsl(152, 69%, 40%)"
                fill="hsl(152, 69%, 40%)"
                fillOpacity={activeCluster === null || activeCluster === 1 ? 0.3 : 0.05}
                strokeWidth={activeCluster === 1 ? 3 : 1.5}
              />
              <Radar
                name="Perfil Risco Social"
                dataKey="Perfil Risco Social"
                stroke="hsl(38, 92%, 50%)"
                fill="hsl(38, 92%, 50%)"
                fillOpacity={activeCluster === null || activeCluster === 2 ? 0.3 : 0.05}
                strokeWidth={activeCluster === 2 ? 3 : 1.5}
              />
              <Legend 
                wrapperStyle={{ fontSize: "11px", paddingTop: "10px" }}
              />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="space-y-3">
        <h3 className="px-1 text-sm font-medium text-muted-foreground">
          Detalhes dos Perfis
        </h3>
        {clusters.map((cluster) => (
          <ClusterCard
            key={cluster.id}
            cluster={cluster}
            isActive={activeCluster === cluster.id}
            onClick={() => setActiveCluster(
              activeCluster === cluster.id ? null : cluster.id
            )}
          />
        ))}
      </div>
    </div>
  );
}
