"use client";

import { useState } from "react";
import { Layers, ChevronDown, ChevronUp, CheckCircle2, XCircle } from "lucide-react";

const ALL_RESOURCES = [
  { name: "ThamizhiMorph", description: "Finite-State Transducer (FST) Morphological Parser", role: "Morphology & POS" },
  { name: "Tamil WordNet", description: "Lexical-semantic synset network & morphtable mappings", role: "Lexical & Morph Root" },
  { name: "Thani Thamizh Akarathi", description: "Purist Tamil Lexicon Dictionary", role: "Pure Lexical Senses" },
  { name: "Sentamizh", description: "Sangam & Classical Tamil Literary Corpus (10,393 records)", role: "Literary Context" },
];

export default function EvidencePanel({ sources = [], summary = {} }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-1.5">
            <Layers className="w-5 h-5 text-[#C9A227]" />
            <span>Evidence Provenance</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Based on evidence from {sources.length} active primary resources.
          </p>
        </div>

        <button
          onClick={() => setExpanded(!expanded)}
          className="flex items-center space-x-1 text-xs font-medium text-[#C9A227] hover:text-[#E5C158] transition cursor-pointer"
        >
          <span>{expanded ? "Collapse" : "Details"}</span>
          {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      </div>

      {/* Active Contributing Source Chips */}
      <div className="flex flex-wrap gap-2 mb-2">
        {sources.map((src) => (
          <div
            key={src}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-[#C9A227]/10 text-[#E5C158] border border-[#C9A227]/30 font-medium text-xs"
          >
            <CheckCircle2 className="w-3.5 h-3.5 text-[#E5C158]" />
            <span>{src}</span>
          </div>
        ))}
      </div>

      {/* Expandable Provenance Drawer */}
      {expanded && (
        <div className="mt-4 pt-4 border-t border-white/10 space-y-3">
          <div className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Resource Adapter Hit Audit:
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {ALL_RESOURCES.map((res) => {
              const isFound = sources.includes(res.name);
              return (
                <div
                  key={res.name}
                  className={`p-3 rounded-lg border text-xs ${
                    isFound
                      ? "bg-[#121212]/80 border-emerald-500/30"
                      : "bg-[#0A0A0A] border-white/5 opacity-60"
                  }`}
                >
                  <div className="flex flex-wrap items-center justify-between gap-1 font-medium">
                    <span className="text-[#F7F3EA]">{res.name}</span>
                    {isFound ? (
                      <span className="text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.5 rounded text-[10px]">
                        FOUND
                      </span>
                    ) : (
                      <span className="text-slate-400 bg-white/5 border border-white/10 px-1.5 py-0.5 rounded text-[10px]">
                        NOT FOUND
                      </span>
                    )}
                  </div>
                  <div className="text-slate-400 text-[11px] mt-1">{res.description}</div>
                  <div className="text-[#C9A227] font-medium text-[10px] mt-1">Role: {res.role}</div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
