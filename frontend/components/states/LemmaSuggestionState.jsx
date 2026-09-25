"use client";

import { Sparkles, ArrowRight, X } from "lucide-react";
import { useRouter } from "next/navigation";

export default function LemmaSuggestionState({ query, lemma, onAccept }) {
  const router = useRouter();
  
  return (
    <div className="flex-1 flex items-center justify-center py-12 px-4 animate-fade-in">
      <div className="max-w-xl w-full bg-[#070D19]/90 border border-[#C9A227]/30 rounded-3xl p-8 sm:p-10 shadow-2xl backdrop-blur-md text-center space-y-8 relative overflow-hidden">
        
        {/* Decorative Background Elements */}
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#C9A227] to-transparent opacity-50" />
        <div className="absolute -top-24 -right-24 w-48 h-48 bg-[#C9A227]/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-24 -left-24 w-48 h-48 bg-[#C9A227]/10 rounded-full blur-3xl" />

        {/* Icon */}
        <div className="relative mx-auto w-16 h-16 flex items-center justify-center rounded-2xl bg-[#050A14] border border-[#C9A227]/20 shadow-inner">
          <Sparkles className="w-8 h-8 text-[#E5C158]" />
        </div>

        {/* Messaging */}
        <div className="space-y-4 relative z-10">
          <h2 className="text-2xl sm:text-3xl font-serif-tamil font-bold text-[#F7F3EA] tracking-wide">
            "{query}"
          </h2>
          <div className="space-y-3">
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              We couldn't find a direct dictionary definition for the exact word you typed. 
            </p>
            <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
              However, we successfully extracted its root word <span className="font-serif-tamil text-[#E5C158] font-bold px-1 py-0.5 bg-[#C9A227]/10 rounded">"{lemma}"</span> and found rich evidence for it.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 relative z-10 pt-4">
          <button
            onClick={() => router.push("/")}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl border border-slate-700 hover:bg-slate-800 text-slate-300 text-sm font-medium transition flex items-center justify-center space-x-2 cursor-pointer"
          >
            <X className="w-4 h-4" />
            <span>Cancel</span>
          </button>
          
          <button
            onClick={onAccept}
            className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#C9A227] hover:bg-[#E5C158] text-[#0B132B] text-sm font-bold transition flex items-center justify-center space-x-2 shadow-[0_0_15px_rgba(201,162,39,0.3)] cursor-pointer"
          >
            <span>Explore Root Word</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
