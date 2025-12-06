import { useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Cell,
} from "recharts";
import { nlpData, diagnosisLabels } from "@/data/nlpData";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

const diagnosisColors: Record<string, string> = {
  Depressão: "hsl(187, 92%, 35%)",
  Ansiedade: "hsl(263, 70%, 58%)",
  Bipolar: "hsl(152, 69%, 40%)",
  Suicida: "hsl(0, 84%, 60%)",
};

export function LinguisticaTab() {
  const [selectedDiagnosis, setSelectedDiagnosis] = useState<string>("Ansiedade");
  const words = nlpData[selectedDiagnosis] || [];
  const color = diagnosisColors[selectedDiagnosis];

  return (
    <div className="animate-fade-in space-y-4 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <h2 className="text-sm font-medium text-muted-foreground">
            Top 30 Palavras por Diagnóstico
          </h2>
          <Select value={selectedDiagnosis} onValueChange={setSelectedDiagnosis}>
            <SelectTrigger className="w-full sm:w-40">
              <SelectValue placeholder="Selecione" />
            </SelectTrigger>
            <SelectContent>
              {diagnosisLabels.map((label) => (
                <SelectItem key={label} value={label}>
                  {label}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="h-[600px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={words}
              layout="vertical"
              margin={{ top: 5, right: 20, left: 60, bottom: 5 }}
            >
              <XAxis 
                type="number" 
                domain={[0, 100]}
                tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }}
                axisLine={{ stroke: "hsl(var(--border))" }}
              />
              <YAxis
                type="category"
                dataKey="word"
                tick={{ fill: "hsl(var(--foreground))", fontSize: 11 }}
                axisLine={{ stroke: "hsl(var(--border))" }}
                width={55}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "hsl(var(--card))",
                  border: "1px solid hsl(var(--border))",
                  borderRadius: "12px",
                  boxShadow: "var(--shadow-soft)",
                }}
                labelStyle={{ color: "hsl(var(--foreground))", fontWeight: 600 }}
                formatter={(value: number) => [`Score: ${value}`, ""]}
              />
              <Bar 
                dataKey="score" 
                radius={[0, 4, 4, 0]}
                maxBarSize={20}
              >
                {words.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={color}
                    fillOpacity={0.7 + (entry.score / 100) * 0.3}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Info Card */}
      <div className="rounded-xl bg-card p-4 shadow-card">
        <h3 className="mb-2 text-sm font-semibold text-foreground">
          Sobre a Análise NLP
        </h3>
        <p className="text-xs leading-relaxed text-muted-foreground">
          Este gráfico mostra as palavras mais frequentes em textos associados a cada diagnóstico.
          O score representa a relevância estatística da palavra para identificar o padrão linguístico.
          Palavras com maior score são indicadores mais fortes do diagnóstico selecionado.
        </p>
      </div>
    </div>
  );
}
