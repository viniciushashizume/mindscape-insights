import { diagnoses, symptoms, symptomMatrix, getIntensityColor, getIntensityLabel } from "@/data/symptomData";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";

export function SintomasTab() {
  return (
    <div className="animate-fade-in space-y-4 pb-24">
      <div className="rounded-2xl bg-card p-4 shadow-card">
        <h2 className="mb-4 text-center text-sm font-medium text-muted-foreground">
          Assinatura Sintomática por Diagnóstico
        </h2>
        
        <div className="overflow-x-auto">
          <div className="min-w-[360px]">
            {/* Header row with symptom names */}
            <div className="mb-2 flex">
              <div className="w-24 shrink-0" />
              {symptoms.map((symptom) => (
                <div 
                  key={symptom}
                  className="flex-1 px-1 text-center"
                >
                  <span className="inline-block -rotate-45 origin-center text-[10px] font-medium text-muted-foreground whitespace-nowrap">
                    {symptom}
                  </span>
                </div>
              ))}
            </div>

            {/* Rows for each diagnosis */}
            {diagnoses.map((diagnosis) => (
              <div key={diagnosis} className="mb-2 flex items-center">
                <div className="w-24 shrink-0 pr-2 text-right">
                  <span className="text-xs font-medium text-foreground">
                    {diagnosis}
                  </span>
                </div>
                <div className="flex flex-1 gap-1">
                  {symptoms.map((symptom) => {
                    const intensity = symptomMatrix[diagnosis][symptom];
                    const size = 20 + intensity * 24; // 20-44px
                    
                    return (
                      <div 
                        key={`${diagnosis}-${symptom}`}
                        className="flex flex-1 items-center justify-center py-1"
                      >
                        <Tooltip>
                          <TooltipTrigger asChild>
                            <button
                              className="rounded-full transition-transform hover:scale-110 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
                              style={{
                                width: size,
                                height: size,
                                backgroundColor: getIntensityColor(intensity),
                              }}
                            />
                          </TooltipTrigger>
                          <TooltipContent 
                            side="top" 
                            className="bg-card border border-border shadow-soft"
                          >
                            <div className="text-center">
                              <p className="font-medium text-foreground">{symptom}</p>
                              <p className="text-xs text-muted-foreground">
                                {diagnosis}: {(intensity * 100).toFixed(0)}%
                              </p>
                              <p className="text-xs font-medium" style={{ color: getIntensityColor(intensity) }}>
                                {getIntensityLabel(intensity)}
                              </p>
                            </div>
                          </TooltipContent>
                        </Tooltip>
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Legend */}
        <div className="mt-6 flex items-center justify-center gap-4">
          <span className="text-xs text-muted-foreground">Intensidade:</span>
          <div className="flex items-center gap-3">
            {[
              { label: "Baixa", value: 0.1 },
              { label: "Moderada", value: 0.35 },
              { label: "Alta", value: 0.6 },
              { label: "Crítica", value: 0.9 },
            ].map(({ label, value }) => (
              <div key={label} className="flex items-center gap-1">
                <div 
                  className="h-3 w-3 rounded-full"
                  style={{ backgroundColor: getIntensityColor(value) }}
                />
                <span className="text-[10px] text-muted-foreground">{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Insights Cards */}
      <div className="grid gap-3">
        <div className="rounded-xl bg-card p-4 shadow-card">
          <h3 className="mb-2 text-sm font-semibold text-foreground">Depressão</h3>
          <p className="text-xs text-muted-foreground">
            Alta correlação com <span className="font-medium text-destructive">Tristeza</span>, 
            <span className="font-medium text-destructive"> Insônia</span> e 
            <span className="font-medium text-destructive"> Ideação Suicida</span>.
          </p>
        </div>
        <div className="rounded-xl bg-card p-4 shadow-card">
          <h3 className="mb-2 text-sm font-semibold text-foreground">Bipolar</h3>
          <p className="text-xs text-muted-foreground">
            Caracterizado por <span className="font-medium text-secondary">Euforia</span> e 
            <span className="font-medium text-secondary"> Mudança de Humor</span> intensas.
          </p>
        </div>
        <div className="rounded-xl bg-card p-4 shadow-card">
          <h3 className="mb-2 text-sm font-semibold text-foreground">Ansiedade</h3>
          <p className="text-xs text-muted-foreground">
            Predominância de <span className="font-medium text-primary">Inquietação</span> e 
            <span className="font-medium text-primary"> Insônia</span>.
          </p>
        </div>
      </div>
    </div>
  );
}
