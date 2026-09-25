"use client";

import { useState } from "react";
import { Quote, ExternalLink, ArrowRight, ChevronDown, ChevronUp } from "lucide-react";

export default function LiteraryContextCard({ contexts = [], query = "", lemma = "" }) {
  const [selectedPeriod, setSelectedPeriod] = useState("All Periods");
  const [isExpanded, setIsExpanded] = useState(false);
  const [expandedItems, setExpandedItems] = useState({});

  const toggleExpandItem = (idx) => {
    setExpandedItems((prev) => ({ ...prev, [idx]: !prev[idx] }));
  };

  const getRelevantLine = (text, queryKeyword, lemmaKeyword) => {
    if (!text) return "";
    // Split by newline or standard sentence-ending punctuation
    const sentences = text.split(/(?<=[.!?\n|])\s+/);
    const keywords = [queryKeyword, lemmaKeyword].filter(k => k && k.trim());
    
    const match = sentences.find((sentence) => 
      keywords.some(k => sentence.toLowerCase().includes(k.toLowerCase()))
    );
    
    let result = match ? match.trim() : sentences[0].trim();
    
    // If the matched sentence is extremely long, truncate it around the keyword
    if (result.length > 120) {
       const keywordIndex = keywords.reduce((idx, k) => {
         const kIdx = result.toLowerCase().indexOf(k.toLowerCase());
         return kIdx !== -1 && (idx === -1 || kIdx < idx) ? kIdx : idx;
       }, -1);
       
       if (keywordIndex > -1) {
           const start = Math.max(0, keywordIndex - 40);
           const end = Math.min(result.length, keywordIndex + 80);
           result = (start > 0 ? "... " : "") + result.substring(start, end).trim() + (end < result.length ? " ..." : "");
       } else {
           result = result.substring(0, 120) + "...";
       }
    }
    
    return result;
  };

  const highlightText = (text, queryKeyword, lemmaKeyword) => {
    if (!text) return text;
    const keywords = [queryKeyword, lemmaKeyword].filter(k => k && k.trim());
    if (keywords.length === 0) return text;

    const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const pattern = keywords.map(escapeRegExp).join('|');
    const regex = new RegExp(`(${pattern})`, 'gi');
    
    const lines = text.split('\n');
    
    return lines.map((line, lineIdx) => {
      const parts = line.split(regex);
      return (
        <span key={lineIdx}>
          {parts.map((part, i) => {
            const isMatch = keywords.some(k => part.toLowerCase() === k.toLowerCase());
            return isMatch ? (
              <span key={i} className="bg-[#C9A227]/30 text-[#E5C158] font-bold rounded px-1">{part}</span>
            ) : (
              part
            );
          })}
          {lineIdx < lines.length - 1 && <br />}
        </span>
      );
    });
  };

  const evidenceList = contexts;

  const filteredList =
    selectedPeriod === "All Periods"
      ? evidenceList
      : evidenceList.filter((item) =>
          (item.period || "").toLowerCase().includes(selectedPeriod.toLowerCase())
        );

  const visibleList = isExpanded ? filteredList : filteredList.slice(0, 2);

  if (!evidenceList || evidenceList.length === 0) {
    return (
      <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-5 text-slate-300">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <Quote className="w-5 h-5 text-[#C9A227]" />
          <span>Literary Evidence</span>
        </h3>
        <p className="text-sm italic text-slate-400">No literary evidence found for this word.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-5">
      {/* Title Header with Filter Dropdown */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-white/5 pb-3">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <Quote className="w-5 h-5 text-[#C9A227]" />
          <span>Literary Evidence</span>
        </h3>
      </div>

      {/* Literary Quotes List */}
      <div className="space-y-4">
        {visibleList.map((item, idx) => {
          const isItemExpanded = expandedItems[idx];
          const textContent = item.quote || item.text_segment || item.passage || "";
          
          const relevantLine = getRelevantLine(textContent, query, lemma);
          const canExpand = textContent.length > relevantLine.length + 10 || textContent.includes('\n');

          return (
            <div
              key={idx}
              className="p-4 rounded-xl bg-[#121212]/60 border border-white/5 hover:border-white/10 hover:bg-[#18181B]/80 transition flex flex-col md:flex-row md:items-center justify-between gap-4"
            >
              {/* Left Side: Verse, Source & Translation */}
              <div className="flex-1 space-y-2">
                <div className="text-base sm:text-lg font-serif-tamil text-[#F7F3EA] leading-relaxed italic pl-3 border-l-2 border-[#C9A227]">
                  “{isItemExpanded 
                    ? highlightText(textContent, query, lemma) 
                    : highlightText(relevantLine, query, lemma)}”
                </div>
                
                <div className="flex flex-wrap items-center gap-2 pl-3">
                  <span className="text-xs text-slate-500 font-serif-tamil font-medium">
                    {item.work ? `${item.work} ${item.verse_number ? `(${item.verse_number})` : ''}` : (item.source || "Sentamizh Corpus")}
                  </span>
                  
                  {(item.translation || item.meaning) && (
                    <span className="text-xs italic text-slate-500 border-l border-slate-700 pl-2">
                      {item.translation || item.meaning}
                    </span>
                  )}
                  
                  {canExpand && (
                    <button
                      onClick={() => toggleExpandItem(idx)}
                      className="text-[#E5C158] hover:text-white text-xs font-medium underline decoration-[#C9A227]/50 underline-offset-2 transition cursor-pointer ml-2"
                    >
                      {isItemExpanded ? "Hide verse" : "Read full verse"}
                    </button>
                  )}
                </div>
              </div>

              {/* Right Side: Period Badge & View Source Button */}
              <div className="flex flex-row md:flex-col items-center md:items-end justify-between md:justify-center gap-3 md:gap-4 md:min-w-[150px] shrink-0 pt-2 md:pt-0 border-t md:border-t-0 border-white/5">
                <span className={`px-2.5 py-0.5 rounded-full border text-[11px] font-medium whitespace-nowrap ${
                  (item.period || "").toLowerCase().includes("sangam")
                    ? "bg-cyan-950/40 text-cyan-300 border-cyan-800/40"
                    : (item.period || "").toLowerCase().includes("modern")
                    ? "bg-amber-950/40 text-amber-300 border-amber-800/40"
                    : "bg-[#2A2A2A]/50 text-slate-300 border-slate-700"
                }`}>
                  {item.period || "Sangam (300 BCE – 300 CE)"}
                </span>

                <button
                  className="flex items-center space-x-1 text-xs text-cyan-400 hover:text-cyan-300 font-medium transition cursor-pointer whitespace-nowrap"
                  title="View original corpus record"
                >
                  <span>View Source</span>
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* View More / Less Toggle */}
      {filteredList.length > 2 && (
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="w-full py-2.5 mt-2 flex items-center justify-center space-x-2 text-xs font-semibold text-[#E5C158] bg-[#C9A227]/10 hover:bg-[#C9A227]/20 border border-[#C9A227]/20 rounded-xl transition cursor-pointer"
        >
          <span>{isExpanded ? "View less" : `View more (${filteredList.length - 2})`}</span>
          {isExpanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
        </button>
      )}
    </div>
  );
}
