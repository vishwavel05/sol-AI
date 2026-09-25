"use client";

import { useState, useEffect, Suspense } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import AppShell from "@/components/layout/AppShell";
import { querySolApi } from "@/lib/api";
import { BookOpen, ArrowLeft, ExternalLink, Sparkles, Layers, History, FileText } from "lucide-react";
import Link from "next/link";

const SAMPLE_PASSAGES = [
  {
    source_text: "புறநானூறு (Purananuru)",
    verse_number: "182",
    period: "சங்க காலம் (Sangam Era, c. 300 BCE – 300 CE)",
    layer: "சங்க இலக்கியம் (Classical Sangam Literature)",
    classical_tamil: "உண்டால் அம்ம இவ்வுலகம் இந்திரர்\nஅமிழ்தம் இயைவதாயினும் இனிதெனத்\nதமயர் உண்டலும் இலரே;\nமுனிவிலர்; துஞ்சலும் இலர்; பிறர் அஞ்சுவது அஞ்சி,\nபுகழ் எனின் உயிரும் கொடுக்குவர்; பழி எனின்\nஉலகுடன் பெறினும் கொள்ளலர்...",
    modern_tamil: "இந்திரருக்குரிய அமிழ்தமே கிடைப்ப தாயினும், அது இனிமையானது என்று தாம் மட்டுமே உண்ணமாட்டார். பிறரோடு சினம் கொள்ளார். சோம்பலின்றி உழைப்பர். பிறர் அஞ்சும் பழிக்கு அஞ்சுவர். புகழ் வருவதாயின் உயிரையும் தருவர்...",
    highlight_word: "மரங்களில்",
    provenance: "Sentamizh Literary Database - Verse ID #PUR-182",
  },
  {
    source_text: "குறுந்தொகை (Kuruntokai)",
    verse_number: "42",
    period: "சங்க காலம் (Sangam Era)",
    layer: "எட்டுத்தொகை (Ettuthokai)",
    classical_tamil: "யாருமில்லைத் தானே கள்வன்\nதான்அது பொய்ப் பின் யானெவன் செய்கோ\nதினைத்தா ளன்ன சிறுபசுங் கால\nஒழுகுநீ ராரல் பார்க்கும்\nகுருகும் உண்டுதான் மணந்த ஞான்றே.",
    modern_tamil: "தலைவன் என்னை மணந்தபோது சாட்சி யாரும் இல்லை; அவனே கள்வன். அவன் தன் கூற்றைப் பொய்த்தால் நான் என் செய்வேன்? தினைத்தாள் போன்ற சிறிய குட்டையான கால்களையுடைய கொக்கு, ஓடும் நீரில் ஆரல் மீனை எதிர்பார்ப்பது போல...",
    highlight_word: "யாழ்",
    provenance: "Sentamizh Literary Database - Verse ID #KUR-042",
  },
  {
    source_text: "திருக்குறள் (Tirukkural)",
    verse_number: "அறத்துப்பால் - 1",
    period: "சங்க மருவிய காலம் (Post-Sangam Era)",
    layer: "பதினெண்கீழ்க்கணக்கு (Pathinenkilkanakku)",
    classical_tamil: "அகர முதல எழுத்தெல்லாம் ஆதி\nபகவன் முதற்றே உலகு.",
    modern_tamil: "எழுத்துக்கள் எல்லாம் 'அ' என்ற எழுத்தை முதலாகக் கொண்டுள்ளன; அதுபோல உலகம் ஆதிபகவனை முதலாகக் கொண்டுள்ளது.",
    highlight_word: "அகதி",
    provenance: "Sentamizh Literary Database - Verse ID #KURAL-001",
  }
];

function ReadContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const query = searchParams.get("q") || "மரங்களில்";

  const [loading, setLoading] = useState(false);
  const [contexts, setContexts] = useState([]);
  const [selectedPassage, setSelectedPassage] = useState(null);

  useEffect(() => {
    async function loadData() {
      if (query) {
        setLoading(true);
        const res = await querySolApi(query);
        if (res.data && res.data.literary_context && res.data.literary_context.length > 0) {
          setContexts(res.data.literary_context);
          setSelectedPassage(res.data.literary_context[0]);
        } else {
          const matched = SAMPLE_PASSAGES.find(p => p.highlight_word === query) || SAMPLE_PASSAGES[0];
          setContexts(SAMPLE_PASSAGES);
          setSelectedPassage(matched);
        }
        setLoading(false);
      }
    }
    loadData();
  }, [query]);

  const highlightText = (text, target) => {
    if (!text || !target) return text;
    const parts = text.split(new RegExp(`(${target})`, "gi"));
    return parts.map((part, i) =>
      part.toLowerCase() === target.toLowerCase() ? (
        <span key={i} className="bg-[#C9A227]/30 text-[#E5C158] font-bold px-1 rounded border-b-2 border-[#C9A227]">
          {part}
        </span>
      ) : (
        part
      )
    );
  };

  return (
    <div className="space-y-8 animate-fade-in p-6">
      {/* Top Header Controls */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 bg-[#070D19]/90 p-6 rounded-2xl border border-[#C9A227]/30 shadow-xl backdrop-blur-md">
        <div className="flex items-center gap-3">
          <button
            onClick={() => router.back()}
            className="p-2.5 rounded-xl border border-white/10 hover:bg-white/5 transition text-slate-300 flex items-center gap-2 text-sm font-medium cursor-pointer"
          >
            <ArrowLeft className="w-4 h-4" />
            திரும்பிச் செல் (Back)
          </button>
          <div>
            <span className="text-xs font-semibold text-[#E5C158] tracking-wider uppercase">
              Literary Context / Reading View
            </span>
            <h1 className="text-xl sm:text-2xl font-bold text-[#F7F3EA] font-sans-tamil">
              இலக்கியப் பயன்பாடு (Literary Usage)
            </h1>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-sans-tamil">ஆய்வுச் சொல்:</span>
          <Link
            href={`/search?q=${encodeURIComponent(query)}`}
            className="px-3 py-1.5 rounded-lg bg-[#C9A227]/20 border border-[#C9A227]/50 text-[#E5C158] text-sm font-bold font-sans-tamil hover:bg-[#C9A227]/30 transition flex items-center gap-1.5"
          >
            <span>{query}</span>
            <ExternalLink className="w-3.5 h-3.5 opacity-80" />
          </Link>
        </div>
      </div>

      {/* Main Reading View Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Passages List Selector Sidebar (4 Cols) */}
        <div className="lg:col-span-4 space-y-4">
          <div className="bg-[#070D19]/90 p-5 rounded-2xl border border-[#C9A227]/30 shadow-xl backdrop-blur-md">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#E5C158] mb-3 flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-[#C9A227]" />
              கிடைத்த இலக்கியச் செய்யுள்கள் ({contexts.length})
            </h3>
            <p className="text-xs text-slate-400 mb-4">
              Select a verse to inspect provenance and classical syntax:
            </p>

            <div className="space-y-3">
              {contexts.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => setSelectedPassage(item)}
                  className={`w-full text-left p-4 rounded-xl border transition flex flex-col justify-between cursor-pointer ${
                    selectedPassage === item
                      ? "bg-[#C9A227]/20 text-[#E5C158] border-[#C9A227] shadow-md"
                      : "bg-[#050A14]/80 hover:bg-white/5 text-slate-300 border-white/10"
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-sm font-sans-tamil">
                      {item.source_text || item.work || "சங்க பாடல்"}
                    </span>
                    <span className={`text-xs px-2 py-0.5 rounded font-mono ${
                      selectedPassage === item ? "bg-[#C9A227] text-[#0B132B] font-bold" : "bg-white/10 text-slate-300"
                    }`}>
                      #{item.verse_number || item.verse_id || idx + 1}
                    </span>
                  </div>
                  <p className={`text-xs line-clamp-2 font-serif-tamil italic ${
                    selectedPassage === item ? "text-slate-200" : "text-slate-400"
                  }`}>
                    "{item.classical_tamil || item.verse}"
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Primary Reader Showcase (8 Cols) */}
        <div className="lg:col-span-8 space-y-6">
          {selectedPassage ? (
            <div className="bg-[#070D19]/90 p-6 sm:p-8 rounded-2xl border border-[#C9A227]/30 shadow-xl backdrop-blur-md space-y-6">
              {/* Header Badges & Source Title */}
              <div className="border-b border-white/10 pb-5 space-y-3">
                <div className="flex flex-wrap items-center gap-2">
                  <span className="px-3 py-1 rounded-full text-xs font-sans-tamil font-bold bg-[#C9A227]/20 text-[#E5C158] border border-[#C9A227]/30">
                    <BookOpen className="w-3.5 h-3.5 inline mr-1" />
                    {selectedPassage.source_text || selectedPassage.work || "சங்க இலக்கியம்"}
                  </span>

                  {selectedPassage.period && (
                    <span className="px-3 py-1 rounded-full text-xs bg-white/5 text-slate-300 border border-white/10 font-sans-tamil">
                      <History className="w-3.5 h-3.5 inline mr-1 text-slate-400" />
                      {selectedPassage.period}
                    </span>
                  )}
                </div>

                <h2 className="text-2xl font-bold text-[#F7F3EA] font-sans-tamil flex items-center justify-between">
                  <span>{selectedPassage.source_text || selectedPassage.work}</span>
                  {selectedPassage.verse_number && (
                    <span className="text-sm font-normal text-[#E5C158] font-mono bg-[#050A14] border border-white/10 px-3 py-1 rounded-full">
                      பாடல் எண்: {selectedPassage.verse_number}
                    </span>
                  )}
                </h2>
              </div>

              {/* Classical Tamil Verse Display */}
              <div className="bg-[#050A14]/80 p-6 rounded-2xl border border-[#C9A227]/30 space-y-3 relative overflow-hidden">
                <h4 className="text-xs font-bold uppercase tracking-wider text-[#E5C158] font-sans-tamil flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-[#C9A227]" />
                  செம்மொழிச் செய்யுள் மூலப் உரை (Classical Tamil Text):
                </h4>
                <div className="text-lg sm:text-xl font-serif-tamil text-[#F7F3EA] leading-relaxed whitespace-pre-line tracking-wide font-medium">
                  {highlightText(selectedPassage.classical_tamil || selectedPassage.verse, query)}
                </div>
              </div>

              {/* Modern Tamil Translation */}
              {selectedPassage.modern_tamil && (
                <div className="bg-[#050A14]/60 p-6 rounded-2xl border border-white/10 space-y-3">
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 font-sans-tamil flex items-center gap-1.5">
                    <FileText className="w-3.5 h-3.5 text-[#C9A227]" />
                    தற்கால உரை / பொருள் (Modern Tamil Gloss):
                  </h4>
                  <p className="text-base text-slate-200 font-sans-tamil leading-relaxed">
                    {highlightText(selectedPassage.modern_tamil, query)}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="bg-[#070D19]/90 p-12 text-center rounded-2xl border border-white/10">
              <BookOpen className="w-12 h-12 text-slate-500 mx-auto mb-3" />
              <p className="text-slate-400 font-sans-tamil">
                தேர்ந்தெடுக்கப்பட்ட செய்யுள் உரை இல்லை.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ReadPage() {
  return (
    <AppShell showSidebar={true}>
      <main className="flex-1 py-4 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full">
        <Suspense fallback={
          <div className="text-center p-12 text-[#F7F3EA]">
            இலக்கியக் காட்சியகம் ஏற்றப்படுகிறது...
          </div>
        }>
          <ReadContent />
        </Suspense>
      </main>
    </AppShell>
  );
}
