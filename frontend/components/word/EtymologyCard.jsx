import { Sparkles, ExternalLink } from "lucide-react";

export default function EtymologyCard({ etymology, query = "" }) {
  const etymologyText =
    etymology ||
    "Etymology not currently available for this word.";

  return (
    <div className="bg-[#0B132B]/90 border border-[#C9A227]/30 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-white/10 pb-3">
        <h3 className="text-sm font-bold uppercase tracking-wider text-[#E5C158] flex items-center space-x-2">
          <Sparkles className="w-4 h-4 text-[#C9A227]" />
          <span>Etymology</span>
        </h3>
      </div>

      <p className="text-xs text-slate-300 font-sans leading-relaxed">
        {etymologyText}
      </p>

      <div className="pt-2 border-t border-white/5 flex items-center justify-between text-xs">
        <span className="text-slate-400">Source:</span>
        <a
          href="https://github.com/cltk/thamizhimorph"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center space-x-1 text-[#E5C158] hover:underline font-semibold"
        >
          <span>ThamizhiMorph</span>
          <ExternalLink className="w-3 h-3" />
        </a>
      </div>
    </div>
  );
}
