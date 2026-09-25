"use client";

import { useState, useEffect, useRef, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { Search, ArrowRight, X, Keyboard } from "lucide-react";
import KeymanInitializer from "./KeymanInitializer";

const HERO_EXAMPLE_QUERIES = [
  { term: "மரங்களில்" },
  { term: "யாழ்" },
  { term: "அகதி" },
  { term: "அன்பு" },
  { term: "தமிழ்" },
];

const STANDARD_EXAMPLE_QUERIES = [
  { term: "மரங்களில்", type: "core" },
  { term: "யாழ்", type: "sangam" },
  { term: "அகதி", type: "lexical" },
  { term: "வந்தார்கள்", type: "core" },
  { term: "மாணவர்களுக்கு", type: "core" },
  { term: "போலிசொல்வார்த்தை123", type: "unknown" },
];

function SearchBarForm({ initialQuery = "", theme = "standard" }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [query, setQuery] = useState(initialQuery);
  const inputRef = useRef(null);

  useEffect(() => {
    const q = searchParams.get("q");
    if (q) {
      setQuery(q);
    } else {
      setQuery(initialQuery);
    }
  }, [searchParams, initialQuery]);

  const handleSubmit = (e) => {
    if (e) {
      e.preventDefault();
    }
    // Read directly from the input DOM node because KeymanWeb can modify it without triggering React's onChange
    const currentVal = inputRef.current ? inputRef.current.value : query;
    const trimmed = currentVal.trim();
    if (trimmed) {
      setQuery(trimmed);
      router.push(`/?q=${encodeURIComponent(trimmed)}`);
    }
  };

  const handleChipClick = (term) => {
    setQuery(term);
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const handleKeyboardToggle = () => {
    if (window.keyman && window.keyman.osk) {
      // Toggle the OSK (show if hidden, hide if visible)
      const isVisible = window.keyman.osk.isEnabled();
      if (isVisible) {
        window.keyman.osk.hide();
      } else {
        window.keyman.osk.show(true);
      }
    }
  };

  const isDarkHero = theme === "hero" || theme === "dark";

  return (
    <div className="w-full max-w-xl mx-auto space-y-4">
      <KeymanInitializer />
      <form onSubmit={handleSubmit} action="/" method="GET" className="relative group">
        {isDarkHero ? (
          /* Luxury Dark Pill Search Container */
          <div className="relative flex items-center shadow-2xl rounded-full border border-[#C9A227]/40 focus-within:border-[#C9A227] bg-black/80 backdrop-blur-md px-4 py-1.5 transition-all">
            <div className="text-slate-300 pr-2">
              <Search className="w-5 h-5 text-slate-300" />
            </div>
            <input
              ref={inputRef}
              type="text"
              name="q"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="ஒரு சொல்லைத் தேடுங்கள்..."
              className="w-full py-2.5 px-2 text-sm md:text-base text-white placeholder:text-slate-400 bg-transparent focus:outline-none font-sans-tamil font-medium tracking-wide"
              dir="auto"
              autoComplete="off"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            <button
              type="button"
              onClick={handleKeyboardToggle}
              className="text-slate-400 hover:text-[#C9A227] p-1.5 mr-1 transition-colors cursor-pointer"
              title="Toggle Tamil Keyboard"
            >
              <Keyboard className="w-5 h-5" />
            </button>
            {query && (
              <button
                type="button"
                onClick={() => setQuery("")}
                className="text-slate-400 hover:text-white p-1 mr-2"
              >
                <X className="w-4 h-4" />
              </button>
            )}
            <button
              type="submit"
              className="w-9 h-9 rounded-full bg-[#C9A227] hover:bg-[#E5C158] flex items-center justify-center transition-all transform hover:scale-105 shadow-md shrink-0 cursor-pointer"
              title="Search"
            >
              <ArrowRight className="w-5 h-5 text-black stroke-[2.5]" />
            </button>
          </div>
        ) : (
          /* Standard White Card Search Container */
          <div className="relative flex items-center shadow-lg rounded-2xl overflow-hidden border-2 border-[#147D7A]/30 focus-within:border-[#147D7A] bg-white transition-all">
            <div className="pl-5 text-[#147D7A]">
              <Search className="w-6 h-6" />
            </div>
            <input
              ref={inputRef}
              type="text"
              name="q"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="தேடுக... (Search Tamil word e.g. மரங்களில், யாழ், அகதி)"
              className="w-full py-4 pl-4 pr-32 text-lg text-[#0B132B] placeholder:text-slate-400 bg-transparent focus:outline-none font-medium"
              dir="auto"
              autoComplete="off"
              onKeyDown={(e) => {
                if (e.key === 'Enter') {
                  e.preventDefault();
                  handleSubmit();
                }
              }}
            />
            <button
              type="button"
              onClick={handleKeyboardToggle}
              className="absolute right-36 text-slate-400 hover:text-[#147D7A] p-2 transition-colors cursor-pointer"
              title="Toggle Tamil Keyboard"
            >
              <Keyboard className="w-6 h-6" />
            </button>
            {query && (
              <button
                type="button"
                onClick={() => setQuery("")}
                className="absolute right-44 text-slate-400 hover:text-slate-600 p-1"
              >
                <X className="w-5 h-5" />
              </button>
            )}
            <button
              type="submit"
              className="absolute right-2 top-2 bottom-2 px-6 bg-[#0B132B] hover:bg-[#147D7A] text-white font-semibold rounded-xl flex items-center space-x-2 transition-colors shadow-sm cursor-pointer"
            >
              <span>ஆய்வு செய்</span>
              <ArrowRight className="w-4 h-4 text-[#C9A227]" />
            </button>
          </div>
        )}
      </form>

      {/* Example Query Chips */}
      {isDarkHero ? (
        <div className="flex flex-wrap items-center justify-center gap-2 pt-1 text-xs font-sans-tamil">
          <span className="text-slate-300 font-medium mr-1">
            உதாரணங்கள்:
          </span>
          {HERO_EXAMPLE_QUERIES.map((chip) => (
            <button
              key={chip.term}
              type="button"
              onClick={() => handleChipClick(chip.term)}
              className="px-3.5 py-1 rounded-full bg-[#121212]/80 hover:bg-[#18181B] text-[#F7F3EA] hover:text-[#E5C158] border border-[#C9A227]/40 hover:border-[#C9A227] transition-all text-xs font-medium backdrop-blur-sm cursor-pointer"
            >
              {chip.term}
            </button>
          ))}
        </div>
      ) : (
        <div className="flex flex-wrap items-center gap-2 pt-1">
          <span className="text-xs font-bold text-slate-500 uppercase tracking-wider flex items-center space-x-1 mr-1">
            <span>மாதிரிச் சொற்கள்:</span>
          </span>
          {STANDARD_EXAMPLE_QUERIES.map((chip) => (
            <button
              key={chip.term}
              type="button"
              onClick={() => handleChipClick(chip.term)}
              className="text-xs px-3 py-1.5 rounded-full font-medium transition-all border bg-slate-100 hover:bg-[#147D7A] text-slate-700 hover:text-white border-slate-200 cursor-pointer"
            >
              {chip.term}
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

export default function SearchBar(props) {
  return (
    <Suspense fallback={
      <div className="w-full max-w-xl mx-auto p-3 text-center text-slate-400 font-sans-tamil text-xs">
        தேடல் பெட்டி ஏற்றப்படுகிறது...
      </div>
    }>
      <SearchBarForm {...props} />
    </Suspense>
  );
}
