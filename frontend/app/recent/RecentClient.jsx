"use client";

import { useState, useEffect } from "react";
import AppShell from "@/components/layout/AppShell";
import Link from "next/link";
import { Clock, Trash2, ArrowRight } from "lucide-react";
import WordExplorer from "@/components/word/WordExplorer";

export default function RecentClient() {
  const [history, setHistory] = useState([]);
  const [mounted, setMounted] = useState(false);
  const [selectedWord, setSelectedWord] = useState(null);

  useEffect(() => {
    setMounted(true);
    try {
      const saved = JSON.parse(localStorage.getItem("sol_recent_words") || "[]");
      setHistory(saved);
    } catch (e) {
      console.warn("Failed to load history", e);
    }
  }, []);

  const clearHistory = () => {
    localStorage.removeItem("sol_recent_words");
    setHistory([]);
    setSelectedWord(null);
  };

  const formatDate = (ts) => {
    const d = new Date(ts);
    return d.toLocaleDateString(undefined, { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' });
  };

  return (
    <AppShell showSidebar={true}>
      <main className="relative flex-1 min-w-0 w-full bg-black text-[#F7F3EA] overflow-x-hidden min-h-screen pb-12">
        <style jsx global>{`
          .sol-explore-theme {
            --sol-bg: #000000;
            --sol-panel: rgba(10, 10, 10, 0.84);
            --sol-panel-2: rgba(18, 18, 18, 0.9);
            --sol-gold: #d7a92b;
            --sol-gold-bright: #edc95a;
            --sol-cream: #f7f3ea;
            --sol-muted: #9caac0;
            --sol-line: rgba(190, 164, 91, 0.28);
          }
          .sol-explore-theme .sol-panel {
            background: linear-gradient(145deg, rgba(7,13,25,.93), rgba(5,10,18,.82));
            border: 1px solid rgba(173,151,88,.28);
            box-shadow: 0 18px 55px rgba(0,0,0,.22);
            backdrop-filter: blur(12px);
          }
          .sol-explore-theme .sol-panel :is([class*="bg-white"], [class*="bg-gray-50"], [class*="bg-slate-50"]) {
            background-color: rgba(10,17,30,.86) !important;
            color: var(--sol-cream) !important;
          }
          .sol-explore-theme .sol-panel :is([class*="border-gray"], [class*="border-slate"]) {
            border-color: rgba(125,139,161,.26) !important;
          }
          .sol-explore-theme .sol-panel :is([class*="text-gray-900"], [class*="text-gray-800"]) {
            color: var(--sol-cream) !important;
          }
          .sol-explore-theme .sol-panel :is([class*="text-gray-600"], [class*="text-gray-500"]) {
            color: #aeb9cb !important;
          }
          .sol-tab-scroll::-webkit-scrollbar { height: 0; }
          .sol-tab-scroll { scrollbar-width: none; }
          .sol-tamil-word {
            font-family: var(--font-serif-tamil, Georgia, serif);
            letter-spacing: .01em;
          }
        `}</style>
        
        {/* Background Atmosphere */}
        {selectedWord ? (
          <div className="absolute inset-x-0 top-0 h-[520px] overflow-hidden pointer-events-none z-0 transition-opacity duration-500">
            <img src="/explore_bg.png" alt="" aria-hidden="true" className="absolute inset-0 h-full w-full object-cover object-top opacity-90" />
            <div className="absolute inset-0 bg-gradient-to-b from-[#050505]/10 via-[#050505]/30 to-[#050505]" />
            <div className="absolute inset-0 bg-gradient-to-r from-[#050505]/70 via-transparent to-[#050505]/70" />
          </div>
        ) : (
          <div className="absolute inset-x-0 top-0 h-[500px] overflow-hidden pointer-events-none z-0 transition-opacity duration-500">
            <img src="/list_bg.png" alt="" aria-hidden="true" className="absolute inset-0 h-full w-full object-cover object-top opacity-100" />
            <div className="absolute inset-0 bg-gradient-to-b from-[#000000]/10 via-[#000000]/50 to-[#000000]" />
          </div>
        )}

        <div className="relative z-10 w-full sol-explore-theme pt-4">
          {selectedWord ? (
            <WordExplorer 
              data={selectedWord} 
              onBack={() => setSelectedWord(null)} 
            />
          ) : (
            <div className="mx-auto w-full max-w-[1200px] px-4 sm:px-6 lg:px-8 xl:px-10 pt-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8 border-b border-[var(--sol-line)] pb-6">
                <div className="flex items-center gap-3">
                  <div className="p-3 bg-[#111] rounded-2xl border border-[var(--sol-line)] text-[var(--sol-gold-bright)]">
                    <Clock className="w-6 h-6" />
                  </div>
                  <div>
                    <h1 className="text-2xl font-bold font-serif-tamil text-[var(--sol-cream)] tracking-wide">
                      Recent Words
                    </h1>
                    <p className="text-sm text-[var(--sol-muted)] font-serif-english italic mt-0.5">
                      Your previously explored Tamil words
                    </p>
                  </div>
                </div>

                {history.length > 0 && (
                  <button
                    onClick={clearHistory}
                    className="flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-400 hover:text-red-300 hover:bg-red-400/10 rounded-xl transition border border-transparent hover:border-red-400/20"
                  >
                    <Trash2 className="w-4 h-4" />
                    Clear History
                  </button>
                )}
              </div>

              {!mounted ? (
                <div className="text-center py-20 text-[var(--sol-muted)]">Loading...</div>
              ) : history.length === 0 ? (
                <div className="text-center py-20 flex flex-col items-center">
                  <div className="w-20 h-20 bg-[#111] border border-[var(--sol-line)] rounded-full flex items-center justify-center mb-4 text-[var(--sol-gold)] opacity-50">
                    <Clock className="w-8 h-8" />
                  </div>
                  <h2 className="text-xl font-bold text-[var(--sol-cream)] mb-2 font-serif-tamil">No recent words</h2>
                  <p className="text-[var(--sol-muted)] mb-6 max-w-sm">
                    You haven't explored any words yet. Words you search for will appear here.
                  </p>
                  <Link
                    href="/"
                    className="px-6 py-2.5 bg-[#C9A227] hover:bg-[#E5C158] text-[#0B132B] font-bold rounded-xl transition shadow-sm"
                  >
                    Start Exploring
                  </Link>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                  {history.map((item, idx) => (
                    <button
                      key={item.query + idx}
                      onClick={() => setSelectedWord(item)}
                      className="group relative bg-[#070D19]/90 border border-[var(--sol-line)] p-5 rounded-2xl hover:border-[var(--sol-gold-bright)]/60 transition-all hover:-translate-y-1 hover:shadow-[0_10px_30px_rgba(201,162,39,0.1)] flex flex-col h-full text-left"
                    >
                      <div className="flex justify-between items-start mb-4 w-full">
                        <h3 className="text-2xl font-bold text-[var(--sol-cream)] font-serif-tamil group-hover:text-[var(--sol-gold-bright)] transition-colors">
                          {item.lemma || item.query}
                        </h3>
                        <div className="w-8 h-8 rounded-full bg-[#111] flex items-center justify-center text-[var(--sol-gold)] group-hover:bg-[#C9A227] group-hover:text-[#0B132B] transition-colors border border-[var(--sol-line)] shrink-0 ml-4">
                          <ArrowRight className="w-4 h-4" />
                        </div>
                      </div>
                      
                      <div className="flex-1 w-full">
                        {item.meaning ? (
                          <p className="text-sm text-[#D4C5A9]/90 line-clamp-2 leading-relaxed">
                            {item.meaning.split(';').slice(0, 2).join('; ')}
                          </p>
                        ) : (
                          <p className="text-sm text-[var(--sol-muted)] italic">
                            Meaning not established.
                          </p>
                        )}
                      </div>

                      <div className="mt-5 pt-3 border-t border-[var(--sol-line)]/50 text-xs text-[var(--sol-muted)] flex justify-between items-center w-full">
                        {item.query !== item.lemma && item.lemma ? (
                          <span className="text-[var(--sol-gold)]/80">Searched: {item.query}</span>
                        ) : (
                          <span>&nbsp;</span>
                        )}
                        <span>{formatDate(item.timestamp)}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </AppShell>
  );
}
