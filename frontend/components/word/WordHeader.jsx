"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Volume2, Copy, Share2, Heart, Check, ChevronRight } from "lucide-react";

export default function WordHeader({ data, activeTab, setActiveTab }) {
  const query = data?.query || "";
  const lemma = data?.lemma || "";
  const meaning = data?.meaning || "Meaning not available for this word.";
  const morphology = data?.morphology || {};
  const evidenceSummary = data?.evidence_summary || {};
  const totalEvidence = evidenceSummary.total_found || 0;

  const [copied, setCopied] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);
  
  useEffect(() => {
    try {
      const saved = JSON.parse(localStorage.getItem("sol_saved_words") || "[]");
      if (saved.some(item => item.query === query)) {
        setIsSaved(true);
      } else {
        setIsSaved(false);
      }
    } catch(e) {}
  }, [query]);

  const toggleSave = () => {
    try {
      const saved = JSON.parse(localStorage.getItem("sol_saved_words") || "[]");
      if (isSaved) {
        const newSaved = saved.filter(item => item.query !== query);
        localStorage.setItem("sol_saved_words", JSON.stringify(newSaved));
        setIsSaved(false);
      } else {
        const newEntry = {
          ...data,
          timestamp: Date.now()
        };
        const newSaved = [newEntry, ...saved];
        localStorage.setItem("sol_saved_words", JSON.stringify(newSaved));
        setIsSaved(true);
      }
    } catch(e) {}
  };

  const transliteration =
    morphology.transliteration || data?.transliteration || "";

  const literaryContext = data?.literary_context || [];
  
  let headerQuote = null;
  let headerQuoteSource = null;

  if (literaryContext.length > 0) {
    const kuralMatch = literaryContext.find(item => (item.work || "").toLowerCase().includes("thirukkural") || (item.work || "").includes("திருக்குறள்"));
    const selectedItem = kuralMatch || literaryContext[0];
    
    const textContent = selectedItem.quote || selectedItem.text_segment || selectedItem.passage || "";
    if (textContent) {
      const lines = textContent.split('\n');
      const relevantLine = lines.find(line => line.includes(query) || (lemma && line.includes(lemma))) || lines[0];
      
      headerQuote = relevantLine.trim();
      if (headerQuote.length > 80) {
        headerQuote = headerQuote.substring(0, 80) + "...";
      }
      
      headerQuoteSource = selectedItem.work ? `${selectedItem.work} ${selectedItem.verse_number || ''}`.trim() : (selectedItem.source || "Sentamizh");
    }
  }

  if (!headerQuote) {
    headerQuote = "எண்ணென்ப ஏனை எழுத்தென்ப இவ்விரண்டும்\nகண்ணென்ப வாழும் உயிர்க்கு.";
    headerQuoteSource = "திருக்குறள் 392";
  }

  const handleCopy = () => {
    try {
      navigator.clipboard.writeText(meaning);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (e) {}
  };

  const handlePlayAudio = () => {
    setIsPlayingAudio(true);
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(query);
      utterance.lang = "ta-IN";
      utterance.onend = () => setIsPlayingAudio(false);
      utterance.onerror = () => setIsPlayingAudio(false);
      window.speechSynthesis.speak(utterance);
    } else {
      setTimeout(() => setIsPlayingAudio(false), 1000);
    }
  };

  const tabs = [
    { id: "overview", label: "Overview" },
    { id: "meanings", label: "Meanings" },
    { id: "morphology", label: "Morphology" },
    { id: "evidence", label: "Literary Evidence" },
    { id: "related", label: "Related Words" },
  ];

  return (
    <section className="relative w-full">
      <div className="relative py-4 sm:py-6">
        <div className="flex flex-wrap items-start justify-between gap-5">
          <div className="min-w-0">
            <div className="mb-4 flex items-center gap-2 text-[13px] text-[#b8c1cf]">
              <Link href="/" className="hover:text-[#e5c158]">Home</Link>
              <ChevronRight className="h-3.5 w-3.5 text-[#647087]" />
              <span>Search</span>
              <ChevronRight className="h-3.5 w-3.5 text-[#647087]" />
              <span className="font-serif-tamil text-[#e5c158]">{query}</span>
            </div>

            <div className="flex items-center gap-4">
              <h1 className="sol-tamil-word text-[42px] font-medium leading-none tracking-tight text-[#f8f5ed] sm:text-[54px] lg:text-[60px]">
                {query}
              </h1>
              <button
                type="button"
                aria-label="Pronounce word"
                onClick={handlePlayAudio}
                className={`mt-2 flex h-10 w-10 shrink-0 items-center justify-center rounded-full border transition cursor-pointer ${
                  isPlayingAudio
                    ? "border-[#e2b93f] bg-[#d7a92b]/30 text-[#e2b93f] animate-pulse"
                    : "border-[#b28c2a]/70 text-[#e2b93f] hover:bg-[#d7a92b]/10"
                }`}
              >
                <Volume2 className="h-5 w-5" />
              </button>
            </div>

            <p className="mt-2 text-[18px] italic tracking-wide text-[#c1c9d5]">
              {transliteration}
            </p>

            <div className="mt-4 flex flex-wrap gap-2">
              <span className="rounded-full border border-[#60708a]/70 bg-[#0a1220]/75 px-3.5 py-1.5 text-xs font-semibold text-[#e7edf5]">
                Tamil Word
              </span>
              <span className="rounded-full border border-[#60708a]/70 bg-[#0a1220]/75 px-3.5 py-1.5 text-xs font-semibold text-[#e7edf5]">
                Inflected Form
              </span>
              {lemma && (
                <span className="rounded-full border border-[#c9a227]/75 bg-[#c9a227]/10 px-3.5 py-1.5 text-xs font-semibold text-[#e5c158] font-serif-tamil">
                  வேர்: {lemma}
                </span>
              )}
            </div>

            {/* Display a short snippet of the meaning if it's too long, full meaning goes to MeaningCard */}
            <p className="mt-5 text-[18px] font-medium text-[#f3f0e9] sm:text-[20px] line-clamp-2">
              {meaning.split('\n')[0].length > 150 ? meaning.substring(0, 150) + "..." : meaning.split('\n')[0]}
            </p>
          </div>

          <div className="flex shrink-0 items-center gap-2">
            <button
              onClick={handleCopy}
              type="button"
              className="flex items-center gap-2 rounded-xl border border-[#65728a]/60 bg-[#09111f]/70 px-4 py-2.5 text-sm font-medium text-[#e5e8ed] transition hover:border-[#c9a227] hover:text-[#f0c85a] cursor-pointer"
            >
              {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
              {copied ? "Copied" : "Copy"}
            </button>
            <button
              onClick={toggleSave}
              type="button"
              className={`flex items-center gap-2 rounded-xl border px-4 py-2.5 text-sm font-semibold transition cursor-pointer ${
                isSaved
                  ? "border-[#e4c46a] bg-[#e5bd52] text-[#111827] shadow-lg hover:bg-[#f1cf73]"
                  : "border-[#65728a]/60 bg-[#09111f]/70 text-[#e5e8ed] hover:border-[#c9a227] hover:text-[#f0c85a]"
              }`}
            >
              <Heart className={`h-4 w-4 ${isSaved ? "fill-[#111827]" : ""}`} />
              {isSaved ? "Saved" : "Save"}
            </button>
          </div>
        </div>

        {/* Dynamic Quote inside the hero */}
        <div className="mt-7 flex justify-end">
          <div className="max-w-[390px] rounded-2xl border border-[#5d6880]/35 bg-[#070d19]/45 px-6 py-5 text-right backdrop-blur-sm">
            <p className="font-serif-tamil text-[15px] leading-8 text-[#f3efe5] whitespace-pre-line">
              "{headerQuote}"
            </p>
            <p className="mt-1 font-serif-tamil text-sm font-semibold text-[#e3b93e]">
              — {headerQuoteSource}
            </p>
          </div>
        </div>

        {/* Tabs exactly as a single horizontal navigation strip. */}
        <div className="sol-tab-scroll mt-7 overflow-x-auto border-t border-[#667086]/25">
          <div className="flex min-w-max items-center gap-2 pt-4">
            {tabs.map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  type="button"
                  onClick={() => setActiveTab(tab.id)}
                  className={`rounded-xl border px-4 py-2.5 text-sm transition cursor-pointer ${
                    isActive
                      ? "border-[#c9a227]/80 bg-[#c9a227]/12 font-semibold text-[#e9c553] shadow-[inset_0_-2px_0_#d7a92b]"
                      : "border-transparent font-medium text-[#aab6c8] hover:border-[#4e5c72] hover:text-[#f4efe4]"
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
}
