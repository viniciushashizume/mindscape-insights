import { useState } from "react";
import { Header } from "@/components/Header";
import { BottomNavigation, TabType } from "@/components/BottomNavigation";
import { ArquetiposTab } from "@/components/ArquetiposTab";
import { SintomasTab } from "@/components/SintomasTab";
import { LinguisticaTab } from "@/components/LinguisticaTab";

const Index = () => {
  const [activeTab, setActiveTab] = useState<TabType>("arquetipos");

  return (
    <div className="min-h-screen bg-background">
      <Header />
      
      <main className="mx-auto max-w-md px-4 py-6">
        {activeTab === "arquetipos" && <ArquetiposTab />}
        {activeTab === "sintomas" && <SintomasTab />}
        {activeTab === "linguistica" && <LinguisticaTab />}
      </main>

      <BottomNavigation activeTab={activeTab} onTabChange={setActiveTab} />
    </div>
  );
};

export default Index;
