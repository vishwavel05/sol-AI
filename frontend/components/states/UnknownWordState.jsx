"use client";

import Link from "next/link";
import { HelpCircle, Sparkles, RefreshCw, Search } from "lucide-react";

export default function UnknownWordState({ query }) {
  return (
    <div className="sol-card p-8 md:p-12 text-center max-w-3xl mx-auto bg-white border-amber-200 my-8 shadow-sm">
      <div className="w-16 h-16 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center mx-auto mb-4">
        <HelpCircle className="w-8 h-8" />
      </div>

      <h2 className="text-2xl md:text-3xl font-extrabold text-[#0B132B] font-sans-tamil mb-2">
        போதுமான சான்றுகள் கிடைக்கவில்லை
      </h2>

      <p className="text-base text-slate-600 mb-6 max-w-xl mx-auto">
        SOL AI could not find sufficient evidence for query <strong>"{query}"</strong> in the available resources.
      </p>

      <div className="bg-amber-50 border border-amber-200 text-amber-900 p-4 rounded-xl text-xs text-left max-w-lg mx-auto mb-8 space-y-1">
        <div className="font-bold flex items-center space-x-1">
          <Sparkles className="w-3.5 h-3.5 text-amber-600" />
          <span>Responsible Non-Hallucination Policy:</span>
        </div>
        <p>
          SOL AI does not fabricate etymologies or definitions when primary resources (ThamizhiMorph, WordNet, Akarathi, Sentamizh) return no matches.
        </p>
      </div>

      <div className="space-y-4">
        <div className="text-xs font-bold uppercase tracking-wider text-slate-400">
          Suggested Actions:
        </div>
        <div className="flex flex-wrap items-center justify-center gap-2">
          <Link
            href="/?q=மரம்"
            className="px-4 py-2 bg-slate-100 hover:bg-[#147D7A] text-slate-700 hover:text-white rounded-lg text-xs font-semibold transition-colors"
          >
            Try Base Form (e.g. மரம்)
          </Link>
          <Link
            href="/?q=யாழ்"
            className="px-4 py-2 bg-slate-100 hover:bg-[#147D7A] text-slate-700 hover:text-white rounded-lg text-xs font-semibold transition-colors"
          >
            Try Literary Word (யாழ்)
          </Link>
          <Link
            href="/?q=அகதி"
            className="px-4 py-2 bg-slate-100 hover:bg-[#147D7A] text-slate-700 hover:text-white rounded-lg text-xs font-semibold transition-colors"
          >
            Try Dictionary Word (அகதி)
          </Link>
        </div>
      </div>
    </div>
  );
}
