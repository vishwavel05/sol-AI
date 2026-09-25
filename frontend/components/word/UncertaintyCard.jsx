import { AlertTriangle, Info } from "lucide-react";

export default function UncertaintyCard({ uncertainties = [], conflicts = [] }) {
  if ((!uncertainties || uncertainties.length === 0) && (!conflicts || conflicts.length === 0)) {
    return null;
  }

  return (
    <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center space-x-2 border-b border-white/5 pb-3">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <AlertTriangle className="w-5 h-5 text-amber-500" />
          <span>Uncertainty & Analysis Notes</span>
        </h3>
      </div>

      <div className="space-y-3 text-sm leading-relaxed pt-1">
        {conflicts.map((conf, idx) => (
          <div key={`conf-${idx}`} className="flex items-start space-x-3 bg-amber-950/20 p-3.5 rounded-xl border border-amber-500/20 text-[#F7F3EA]">
            <Info className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />
            <div>
              <strong className="font-semibold text-amber-500">Candidate Conflict: </strong>
              <span className="text-slate-300">{conf.description}</span>
            </div>
          </div>
        ))}

        {uncertainties.map((u, idx) => (
          <div key={`unc-${idx}`} className="flex items-start space-x-3 text-slate-300 px-1">
            <span className="w-1.5 h-1.5 rounded-full bg-amber-500/50 shrink-0 mt-2"></span>
            <span>{u}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
