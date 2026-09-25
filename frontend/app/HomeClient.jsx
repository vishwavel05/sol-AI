"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import AppShell from "@/components/layout/AppShell";
import SearchBar from "@/components/search/SearchBar";
import WordHeader from "@/components/word/WordHeader";
import WordExplorer from "@/components/word/WordExplorer";
import UnknownWordState from "@/components/states/UnknownWordState";
import ErrorState from "@/components/states/ErrorState";
import { querySolApi } from "@/lib/api";
import { Loader2 } from "lucide-react";

function HomeContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q");

  const [loading, setLoading] = useState(false);
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [hasAcceptedLemma, setHasAcceptedLemma] = useState(false);

  useEffect(() => {
    if (!query) {
      setData(null);
      setError(null);
      setLoading(false);
      setHasAcceptedLemma(false);
      return;
    }

    const fetchResult = async (word) => {
      setLoading(true);
      setError(null);
      
      try {
        // 1. Check Cache First (Recent or Saved)
        let cachedData = null;
        try {
          const saved = JSON.parse(localStorage.getItem("sol_saved_words") || "[]");
          const recent = JSON.parse(localStorage.getItem("sol_recent_words") || "[]");
          const found = saved.find(item => item.query === word) || recent.find(item => item.query === word);
          
          if (found && found.morphology) {
            cachedData = found;
          }
        } catch(e) {}
        
        if (cachedData) {
          setData(cachedData);
          setLoading(false);
          return;
        }

        // 2. Fetch from API if not cached
        const result = await querySolApi(word, "mock");
        if (result.isError || result.isOffline || result.isTimeout) {
          setError(result.error || "An error occurred while fetching data.");
          setData(null);
        } else {
          setData(result.data);
          setError(null);
          
          // Save FULL object to recent history if valid
          const isUnknown = (!result.data.evidence_summary || result.data.evidence_summary.total_found === 0) && !result.data.lemma && !result.data.meaning;
          if (!isUnknown) {
            try {
              const history = JSON.parse(localStorage.getItem("sol_recent_words") || "[]");
              const newEntry = {
                ...result.data, // Save entire data object
                timestamp: Date.now()
              };
              const filtered = history.filter(item => item.query !== result.data.query);
              const updated = [newEntry, ...filtered].slice(0, 50);
              localStorage.setItem("sol_recent_words", JSON.stringify(updated));
            } catch (e) {
              console.warn("Could not save history", e);
            }
          }
        }
      } catch (err) {
        setError("An unexpected error occurred: " + (err.message || String(err)));
        setData(null);
      } finally {
        setLoading(false);
      }
    };

    fetchResult(query);
  }, [query]);

  const [isKeyboardVisible, setIsKeyboardVisible] = useState(false);

  useEffect(() => {
    let interval;
    if (!query) {
      interval = setInterval(() => {
        const osk = document.getElementById('KeymanWeb_OSK') || document.querySelector('.kmw-osk-desktop');
        const visible = osk && osk.style.display !== 'none' && osk.style.visibility !== 'hidden' && osk.style.opacity !== '0' && osk.offsetHeight > 0;
        
        setIsKeyboardVisible((prev) => {
          if (visible && !prev) {
            // Keyboard just opened, scroll down to ensure it's visible
            setTimeout(() => {
              window.scrollBy({ top: 250, behavior: 'smooth' });
            }, 100);
          }
          return !!visible;
        });
      }, 200);
    }
    return () => clearInterval(interval);
  }, [query]);

  // If there's NO search query, show the Idle/Hero Home state
  if (!query) {
    return (
      <AppShell showSidebar={true} isTransparentHeader={true}>
        <div className="flex-1 w-full flex flex-col justify-between relative text-[#F7F3EA] select-none min-h-[calc(100vh-4rem)]">
          {/* Background Image Container with Overlay */}
          <div
            className="absolute -top-16 inset-x-0 bottom-0 z-0 bg-cover bg-center bg-no-repeat pointer-events-none"
            style={{ backgroundImage: "url('/home_bg.png')" }}
          />
          <div className="absolute -top-16 inset-x-0 bottom-0 z-0 bg-gradient-to-b from-black/50 via-black/30 to-black/70 pointer-events-none" />

          {/* Top Right Thirukkural Epigraph Quote */}
          <div className={`absolute top-8 right-6 sm:right-12 lg:right-16 z-20 hidden sm:block text-right max-w-sm space-y-1.5 font-serif-tamil tracking-wide drop-shadow-lg transition-opacity duration-500 ${isKeyboardVisible ? "opacity-0 pointer-events-none" : "opacity-100"}`}>
            <p className="text-sm sm:text-base md:text-[17px] font-medium text-[#FFF8E7] leading-relaxed italic tracking-wide">
              "கற்றதனால் ஆய பயனென்கொல் வாலறிவன்<br />
              நற்றாள் தொழாஅர் எனின்."
            </p>
            <p className="text-xs sm:text-sm text-[#E5C158] font-serif-tamil font-semibold tracking-wider pt-0.5">
              — திருக்குறள் 2
            </p>
          </div>

          {/* Main Centered Hero Section */}
          <main className="relative z-20 flex-1 flex flex-col items-center justify-center text-center px-4 max-w-4xl mx-auto py-12 space-y-6 transition-all duration-700 ease-in-out my-auto">
            {/* Official SOL AI Logo Asset */}
            <div className="flex justify-center items-center py-2">
              <img
                src="/logo.png"
                alt="சொல் AI Logo"
                className="h-36 sm:h-44 md:h-52 w-auto max-w-full object-contain drop-shadow-2xl hover:scale-105 transition-transform"
              />
            </div>

            {/* Mission Statement & English Subtitle */}
            <div className="space-y-2 max-w-xl mx-auto">
              <p className="text-base sm:text-lg md:text-xl font-serif-tamil font-normal text-[#F5EBD7] leading-relaxed tracking-wider drop-shadow-sm">
                சொல்லின் பொருளையும், சூழலையும், இலக்கியப் பயணத்தையும் அறிக.
              </p>
              <p className="text-xs sm:text-sm md:text-base font-serif-english text-[#D4C5A9]/90 tracking-wide font-normal italic">
                Explore Tamil words through language, literature, and contextual evidence.
              </p>
            </div>

            {/* Search Bar */}
            <div className="w-full pt-1">
              <style dangerouslySetInnerHTML={{__html: `
                /* GENTLE KEYMAN OVERRIDES */
                html body div#KeymanWeb_OSK, html body div.kmw-osk-desktop {
                  background-color: #050505 !important;
                  border: 1px solid #C9A227 !important;
                  border-radius: 8px !important;
                  box-shadow: 0 10px 30px -5px rgba(0,0,0,0.9), 0 0 20px rgba(201, 162, 39, 0.15) !important;
                  margin-top: 50px !important;
                }
                
                /* HIDE HEADER/FOOTER MINIMALLY */
                html body div#keymanweb_title_bar,
                html body div.kmw-title-bar,
                html body div.kmw-footer {
                  display: none !important;
                }

                /* SIMPLE KEY COLORS */
                html body div[id^="KeymanWeb_OSK"] div[class*="kmw-key"],
                html body div[class*="kmw-osk-inner-frame"] div[class*="kmw-key"] {
                  background-color: #0D0D0D !important;
                  border: 1px solid rgba(201, 162, 39, 0.4) !important;
                  border-radius: 4px !important;
                }
                
                /* KEY HOVERS */
                html body div[id^="KeymanWeb_OSK"] div[class*="kmw-key"]:hover,
                html body div[class*="kmw-osk-inner-frame"] div[class*="kmw-key"]:hover {
                  background-color: #151515 !important;
                  border-color: rgba(201, 162, 39, 0.8) !important;
                }

                html body div[id^="KeymanWeb_OSK"] div[class*="kmw-key-down"],
                html body div[class*="kmw-osk-inner-frame"] div[class*="kmw-key-down"] {
                  background-color: rgba(201, 162, 39, 0.15) !important;
                  border-color: #C9A227 !important;
                }

                /* TEXT COLOR AND POINTER EVENTS FIX */
                html body div[id^="KeymanWeb_OSK"] span[class*="kmw-key-text"],
                html body div[class*="kmw-osk-inner-frame"] span[class*="kmw-key-text"] {
                  color: #F7F3EA !important;
                  font-family: var(--font-sans-tamil, sans-serif) !important;
                  pointer-events: none !important;
                }
              `}} />
              <SearchBar theme="hero" />
            </div>
          </main>


        </div>
      </AppShell>
    );
  }

  // Active Search State
  const isUnknown =
    data &&
    (!data.evidence_summary || data.evidence_summary.total_found === 0) &&
    !data.lemma &&
    !data.meaning;

  return (
    <AppShell showSidebar={true}>
      <main className="relative flex-1 min-w-0 w-full bg-black text-[#F7F3EA] overflow-x-hidden">
        <div className="sol-explore-theme relative z-10 min-h-screen w-full">
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
              color: var(--sol-cream);
            }

            .sol-explore-theme .sol-panel {
              background: linear-gradient(145deg, rgba(7,13,25,.93), rgba(5,10,18,.82));
              border: 1px solid rgba(173,151,88,.28);
              box-shadow: 0 18px 55px rgba(0,0,0,.22);
              backdrop-filter: blur(12px);
            }

            .sol-explore-theme .sol-panel :is(
              [class*="bg-white"],
              [class*="bg-gray-50"],
              [class*="bg-slate-50"]
            ) {
              background-color: rgba(10,17,30,.86) !important;
              color: var(--sol-cream) !important;
            }

            .sol-explore-theme .sol-panel :is(
              [class*="bg-gray-100"],
              [class*="bg-slate-100"],
              [class*="bg-zinc-100"]
            ) {
              background-color: rgba(15,24,40,.9) !important;
            }

            .sol-explore-theme .sol-panel :is(
              [class*="border-gray"],
              [class*="border-slate"],
              [class*="border-zinc"]
            ) {
              border-color: rgba(125,139,161,.26) !important;
            }

            .sol-explore-theme .sol-panel :is(
              [class*="text-gray-900"],
              [class*="text-gray-800"],
              [class*="text-slate-900"],
              [class*="text-slate-800"]
            ) {
              color: var(--sol-cream) !important;
            }

            .sol-explore-theme .sol-panel :is(
              [class*="text-gray-600"],
              [class*="text-gray-500"],
              [class*="text-slate-600"],
              [class*="text-slate-500"]
            ) {
              color: #aeb9cb !important;
            }

            .sol-tab-scroll::-webkit-scrollbar { height: 0; }
            .sol-tab-scroll { scrollbar-width: none; }

            .sol-tamil-word {
              font-family: var(--font-serif-tamil, Georgia, serif);
              letter-spacing: .01em;
            }
          `}</style>

          {/* Atmospheric background (ONLY for valid results) */}
          {!loading && !error && data && !isUnknown && (
            <div className="absolute inset-x-0 top-0 h-[520px] overflow-hidden pointer-events-none z-0">
              <img
                src="/explore_bg.png"
                alt=""
                aria-hidden="true"
                className="absolute inset-0 h-full w-full object-cover object-top opacity-90"
              />
              <div className="absolute inset-0 bg-gradient-to-b from-[#050505]/10 via-[#050505]/30 to-[#050505]" />
              <div className="absolute inset-0 bg-gradient-to-r from-[#050505]/70 via-transparent to-[#050505]/70" />
            </div>
          )}

          {/* Top Prominent Search Bar */}
          <div className="w-full relative z-10 pt-4">
            <SearchBar initialQuery={query} theme="hero" />
          </div>

          {/* Loading State */}
          {loading && (
            <div className="relative z-10 bg-[#0A0A0A]/90 p-12 text-center my-8 max-w-2xl mx-auto border border-white/5 rounded-2xl shadow-xl backdrop-blur-md space-y-4">
              <Loader2 className="w-10 h-10 text-[#C9A227] animate-spin mx-auto" />
              <div className="text-xl font-bold text-[#F7F3EA] font-serif-tamil">
                "{query}" சொல்லை ஆய்வு செய்கிறது...
              </div>
              <p className="text-xs text-slate-400">
                Retrieving morphology from ThamizhiMorph, definitions from Akarathi & WordNet, and Sangam literary evidence from Sentamizh.
              </p>
            </div>
          )}

          {/* Error / Backend Offline State */}
          {!loading && error && (
            <div className="relative z-10">
              <ErrorState error={error} onRetry={() => { window.location.reload() }} />
            </div>
          )}

          {/* Unknown Word State */}
          {!loading && !error && isUnknown && (
            <div className="relative z-10">
              <UnknownWordState query={query} />
            </div>
          )}

          {/* Valid Result Word Explorer Screen */}
          {!loading && !error && data && !isUnknown && (
            <WordExplorer data={data} />
          )}
        </div>
      </main>
    </AppShell>
  );
}

export default function HomeClient() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-black flex items-center justify-center font-serif-tamil text-slate-300">
          சொல் AI ஏற்றப்படுகிறது...
        </div>
      }
    >
      <HomeContent />
    </Suspense>
  );
}
