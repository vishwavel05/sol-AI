import { Sparkles, Shield } from "lucide-react";

export default function InterpretationCard({ interpretation }) {
  if (!interpretation) return null;

  return (
    <div className="sol-card p-6 bg-gradient-to-br from-white to-teal-50/30 border-teal-200">
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-xs font-bold uppercase tracking-wider text-[#147D7A] flex items-center space-x-1.5">
          <Sparkles className="w-4 h-4 text-[#C9A227]" />
          <span>சூழல் விளக்கம் (Contextual Interpretation)</span>
        </h3>
        <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-teal-100 text-teal-800 border border-teal-200">
          Grounded Analysis
        </span>
      </div>

      <p className="text-base text-[#0B132B] leading-relaxed font-sans-tamil font-medium">
        {interpretation}
      </p>

      <div className="mt-4 pt-3 border-t border-teal-100 flex items-center space-x-2 text-xs text-slate-500">
        <Shield className="w-3.5 h-3.5 text-[#147D7A]" />
        <span>Synthesized exclusively from retrieved resource evidence without external fabrication.</span>
      </div>
    </div>
  );
}
