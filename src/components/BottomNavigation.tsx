import { Users, Activity, MessageSquare } from "lucide-react";
import { cn } from "@/lib/utils";

export type TabType = "arquetipos" | "sintomas" | "linguistica";

interface BottomNavigationProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

const tabs = [
  { id: "arquetipos" as TabType, label: "Arquétipos", icon: Users },
  { id: "sintomas" as TabType, label: "Sintomas", icon: Activity },
  { id: "linguistica" as TabType, label: "Linguística", icon: MessageSquare },
];

export function BottomNavigation({ activeTab, onTabChange }: BottomNavigationProps) {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 border-t border-border bg-card shadow-soft">
      <div className="mx-auto flex max-w-md items-center justify-around px-4 py-2">
        {tabs.map((tab) => {
          const isActive = activeTab === tab.id;
          const Icon = tab.icon;
          
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={cn(
                "flex flex-1 flex-col items-center gap-1 rounded-xl px-3 py-2 transition-all duration-200",
                isActive 
                  ? "bg-primary/10 text-primary" 
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              )}
            >
              <Icon 
                className={cn(
                  "h-5 w-5 transition-transform duration-200",
                  isActive && "scale-110"
                )} 
              />
              <span className={cn(
                "text-xs font-medium transition-all duration-200",
                isActive && "font-semibold"
              )}>
                {tab.label}
              </span>
              {isActive && (
                <div className="absolute -bottom-0.5 h-0.5 w-12 rounded-full bg-primary" />
              )}
            </button>
          );
        })}
      </div>
    </nav>
  );
}
