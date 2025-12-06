import { TrendingUp, TrendingDown } from "lucide-react";
import { ClusterData } from "@/data/clusterData";
import { cn } from "@/lib/utils";

interface ClusterCardProps {
  cluster: ClusterData;
  isActive: boolean;
  onClick: () => void;
}

export function ClusterCard({ cluster, isActive, onClick }: ClusterCardProps) {
  return (
    <button
      onClick={onClick}
      className={cn(
        "w-full rounded-2xl border-2 bg-card p-4 text-left transition-all duration-300 shadow-card",
        isActive 
          ? "border-primary scale-[1.02]" 
          : "border-transparent hover:border-border"
      )}
    >
      <div className="mb-3 flex items-center gap-2">
        <div 
          className="h-3 w-3 rounded-full" 
          style={{ backgroundColor: cluster.color }}
        />
        <h3 className="font-semibold text-foreground">{cluster.name}</h3>
      </div>
      
      <div className="space-y-2">
        <div className="flex items-start gap-2">
          <TrendingUp className="mt-0.5 h-4 w-4 shrink-0 text-accent" />
          <div className="flex flex-wrap gap-1">
            {cluster.strengths.map((strength, idx) => (
              <span 
                key={idx}
                className="rounded-md bg-accent/10 px-2 py-0.5 text-xs text-accent"
              >
                {strength}
              </span>
            ))}
          </div>
        </div>
        
        <div className="flex items-start gap-2">
          <TrendingDown className="mt-0.5 h-4 w-4 shrink-0 text-destructive" />
          <div className="flex flex-wrap gap-1">
            {cluster.weaknesses.map((weakness, idx) => (
              <span 
                key={idx}
                className="rounded-md bg-destructive/10 px-2 py-0.5 text-xs text-destructive"
              >
                {weakness}
              </span>
            ))}
          </div>
        </div>
      </div>
    </button>
  );
}
