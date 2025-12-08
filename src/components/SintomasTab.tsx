// src/components/SintomasTab.tsx
import { useEffect, useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { Info, AlertCircle } from "lucide-react";

interface HeatmapData {
  symptoms: string[];
  diagnoses: string[];
  matrix: number[][];
  min_val: number;
  max_val: number;
}

const SintomasTab = () => {
  const [data, setData] = useState<HeatmapData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/sintomas-heatmap');
        
        if (!response.ok) {
           throw new Error(`Erro HTTP: ${response.status}`);
        }

        const jsonData = await response.json();

        // VALIDAÇÃO DE SEGURANÇA (AQUI ESTAVA O PROBLEMA)
        // Se a API retornou { "error": "..." } ou não tem diagnoses, lançamos erro
        if (jsonData.error) {
            throw new Error(jsonData.error);
        }
        if (!jsonData.diagnoses || !Array.isArray(jsonData.diagnoses)) {
            throw new Error("Formato de dados inválido recebido da API.");
        }

        setData(jsonData);
      } catch (err: any) {
        console.error("Erro no fetch:", err);
        setError(err.message || "Erro desconhecido ao carregar dados.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getColor = (value: number, min: number, max: number) => {
    // Evita divisão por zero se max e min forem iguais
    const denominator = max - min || 1;
    const ratio = (value - min) / denominator;
    
    // Simulação do 'magma_r' (Invertido: 0 = Claro/Amarelo, 1 = Escuro/Roxo)
    // Low value (0) -> Hue ~60 (Amarelo), Lightness ~95%
    // High value (max) -> Hue ~260 (Roxo), Lightness ~20%
    
    const hue = 60 + (200 * ratio); 
    const lightness = 95 - (75 * ratio); 
    
    return `hsl(${hue}, 70%, ${lightness}%)`;
  };

  if (loading) {
    return <div className="p-4 space-y-4">
      <Skeleton className="h-8 w-1/3" />
      <Skeleton className="h-64 w-full" />
    </div>;
  }

  if (error || !data) {
    return (
      <Alert variant="destructive" className="my-4">
        <AlertCircle className="h-4 w-4" />
        <AlertTitle>Erro ao carregar gráfico</AlertTitle>
        <AlertDescription>
          {error}. <br/>
          <strong>Dica:</strong> Verifique no terminal onde o Python está rodando se o arquivo <em>Dataset-Mental-Disorders.csv</em> foi encontrado e lido corretamente.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Diagnósticos</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.diagnoses.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">Sintomas</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{data.symptoms.length}</div>
          </CardContent>
        </Card>
      </div>

      <Card className="overflow-hidden border-none shadow-md bg-white/50">
        <CardHeader>
          <CardTitle>Mapa de Calor de Sintomas</CardTitle>
          <CardDescription>Intensidade média por diagnóstico</CardDescription>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          <div 
            className="grid min-w-[800px] p-6 gap-1"
            style={{ gridTemplateColumns: `180px repeat(${data.symptoms.length}, 1fr)` }}
          >
            <div></div>
            {data.symptoms.map((symptom, i) => (
              <div key={i} className="h-32 flex items-end justify-center pb-2">
                 <span className="-rotate-45 text-xs font-medium text-muted-foreground whitespace-nowrap origin-bottom-left translate-x-4">
                  {symptom}
                 </span>
              </div>
            ))}
            {data.diagnoses.map((diagnose, rowIdx) => (
              <>
                <div className="flex items-center justify-end pr-4 text-sm font-bold text-slate-700 border-r border-slate-200">
                  {diagnose}
                </div>
                {data.matrix[rowIdx].map((value, colIdx) => (
                  <div 
                    key={`${rowIdx}-${colIdx}`}
                    className="h-10 w-full flex items-center justify-center text-[10px] font-medium transition-all hover:scale-110 cursor-pointer rounded-sm"
                    style={{ 
                      backgroundColor: getColor(value, data.min_val, data.max_val),
                      color: value > (data.max_val / 2) ? 'white' : 'black'
                    }}
                    title={`${diagnose}: ${data.symptoms[colIdx]} (${value.toFixed(2)})`}
                  >
                   {value.toFixed(1)}
                  </div>
                ))}
              </>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export { SintomasTab };
export default SintomasTab;