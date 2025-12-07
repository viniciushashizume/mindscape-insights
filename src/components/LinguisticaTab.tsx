import { useState, useEffect } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  ResponsiveContainer,
  Tooltip,
  Cell,
} from "recharts";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Skeleton } from "@/components/ui/skeleton";

const diagnosisColors: Record<string, string> = {
  Depression: "hsl(187, 92%, 35%)", // Ciano Escuro
  Anxiety: "hsl(263, 70%, 58%)",    // Roxo
  Bipolar: "hsl(152, 69%, 40%)",    // Verde
  Suicidal: "hsl(0, 84%, 60%)",     // Vermelho
  Stress: "hsl(38, 92%, 50%)",      // Laranja/Amarelo
};

// Interface para os dados vindos da API
interface WordScore {
  word: string;
  score: number;
}

interface NlpResponse {
  [key: string]: WordScore[];
}

export function LinguisticaTab() {
  const [selectedDiagnosis, setSelectedDiagnosis] = useState<string>("Depression");
  const [nlpData, setNlpData] = useState<NlpResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Busca dados da API ao carregar o componente
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/linguistica-data");
        if (!response.ok) {
          throw new Error("Falha ao carregar dados linguísticos");
        }
        const data = await response.json();
        
        // Verifica se a API retornou erro
        if (data.error) {
            throw new Error(data.error);
        }

        setNlpData(data);
        setLoading(false);
      } catch (err) {
        console.error(err);
        setError("Erro ao conectar com a API de análise linguística.");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  // Dados atuais baseados na seleção
  const words = nlpData ? (nlpData[selectedDiagnosis] || []) : [];
  const color = diagnosisColors[selectedDiagnosis] || "hsl(200, 50%, 50%)";

  // Lista de diagnósticos disponíveis baseada no retorno da API
  const diagnosisLabels = nlpData ? Object.keys(nlpData) : ["Carregando..."];

  if (loading) {
    return (
      <div className="space-y-4 p-4">
        <Skeleton className="h-10 w-[200px]" />
        <Skeleton className="h-[400px] w-full rounded-2xl" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-red-50 p-6 text-red-600 border border-red-200">
        <h3 className="font-semibold">Erro de Carregamento</h3>
        <p>{error}</p>
        <p className="text-sm mt-2 opacity-80">Verifique se o arquivo 'Combined Data.csv' está na pasta do backend e se a API está rodando.</p>
      </div>
    );
  }

  return (
    <div className="animate-fade-in space-y-4 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <div className="mb-4 flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-lg font-semibold text-foreground">
              Análise de Vocabulário Distintivo
            </h2>
            <p className="text-xs text-muted-foreground">
              Comparação: {selectedDiagnosis} vs. Normal
            </p>
          </div>
          
          <Select value={selectedDiagnosis} onValueChange={setSelectedDiagnosis}>
            <SelectTrigger className="w-full sm:w-48">
              <SelectValue placeholder="Selecione o Diagnóstico" />
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

        <div className="h-[600px] w-full">
          {words.length > 0 ? (
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={words}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 60, bottom: 5 }}
              >
                <XAxis 
                  type="number" 
                  tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }}
                  axisLine={{ stroke: "hsl(var(--border))" }}
                />
                <YAxis
                  type="category"
                  dataKey="word"
                  tick={{ fill: "hsl(var(--foreground))", fontSize: 11, fontWeight: 500 }}
                  axisLine={{ stroke: "hsl(var(--border))" }}
                  width={70}
                />
                <Tooltip
                  cursor={{ fill: "transparent" }}
                  contentStyle={{
                    backgroundColor: "hsl(var(--card))",
                    border: "1px solid hsl(var(--border))",
                    borderRadius: "8px",
                    boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                  }}
                  formatter={(value: number) => [`Relevância: ${value.toFixed(1)}`, "Score"]}
                />
                <Bar 
                  dataKey="score" 
                  radius={[0, 4, 4, 0]}
                  barSize={20}
                >
                  {words.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={color}
                      fillOpacity={0.6 + (index / words.length) * 0.4} // Gradiente suave
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Nenhum dado encontrado para este diagnóstico.
            </div>
          )}
        </div>
      </div>

      {/* Info Card */}
      <div className="rounded-xl bg-card p-5 shadow-card border border-border/50">
        <h3 className="mb-2 text-sm font-semibold text-foreground flex items-center gap-2">
          <span className="block w-2 h-2 rounded-full bg-primary"></span>
          Metodologia
        </h3>
        <p className="text-xs leading-relaxed text-muted-foreground text-justify">
          Este gráfico exibe palavras que aparecem com frequência significativamente maior 
          em relatos de <strong>{selectedDiagnosis}</strong> comparado a relatos de pacientes diagnosticados como "Normal". 
          A pontuação é baseada na diferença de frequência relativa (Proporção {selectedDiagnosis} - Proporção Normal), 
          ajustada para visualização. Palavras comuns da língua inglesa (stopwords) foram removidas.
        </p>
      </div>
    </div>
  );
}