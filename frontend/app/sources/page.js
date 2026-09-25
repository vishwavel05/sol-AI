"use client";

import AppShell from "@/components/layout/AppShell";
import { ShieldCheck, CheckCircle2, ArrowRight } from "lucide-react";
import Link from "next/link";

const RESOURCES = [
  {
    id: "thanithamizh_akarathi",
    name: "தனித்தமிழ் அகராதி (Thani Thamizh Akarathi)",
    type: "அகராதி / சொற்பொருள் (Lexical & Dictionary Evidence)",
    description: "செவ்வியல் தமிழ் சொற்களின் பொருள், சுட்டு மற்றும் வரையறைகளை வழங்கும் முதன்மை அகராதித் தரவுத்தளம்.",
    stats: "11,540+ Lexical Entries",
    provenance: "Deterministic SQLite Lexical Store (`akarathi.db`)",
    status: "Active & Integrated",
    accent: "border-l-4 border-l-[#147D7A]"
  },
  {
    id: "tamil_wordnet",
    name: "தமிழ் வேர்ட்நெட் (Tamil WordNet)",
    type: "சொற்பொருள் வலைப்பின்னல் (Lexical-Semantic & Synsets)",
    description: "சொற்களின் தொடர்புகள், வேர் வடிவங்கள் (lemmas), இலக்கணப் பாகுபாடுகள் மற்றும் கருத்தாக்க வலைப்பின்னல்களை வழங்குகிறது.",
    stats: "50,497 Nodes • 41,013 Sense Records",
    provenance: "Mapped WordNet Graph Engine (`wordnet.sqlite`)",
    status: "Active & Integrated",
    accent: "border-l-4 border-l-[#C9A227]"
  },
  {
    id: "thamizhimorph",
    name: "தமிழி மார்ஃப் (ThamizhiMorph)",
    type: "இலக்கண ஆய்வு (Morphological Analyzer - Core & Guesser)",
    description: "தகுந்த உருபனியல் ஆய்வுக் கருவிகள் (Finite State Transducers - FST) மூலம் பகுதி, விகுதி, காலம், பால் மற்றும் வேற்றுமைகளை பிரிக்கிறது.",
    stats: "Core `noun.fst` & `verb.fst` + Guesser Fallback",
    provenance: "FST Transducer Lookup Engine (`flookup`)",
    status: "Active & Integrated",
    accent: "border-l-4 border-l-[#E5C158]"
  },
  {
    id: "sentamizh",
    name: "செந்தமிழ் இலக்கியத் திரட்டு (Sentamizh Corpus)",
    type: "சங்க இலக்கியச் சான்றுகள் (Literary Context & Provenance)",
    description: "சங்க இலக்கியம் மற்றும் செவ்வியல் தமிழ் நூல்களின் செய்யுள் சான்றுகள், வரிகள் மற்றும் தற்கால உரைகளை சான்றாக அளிக்கிறது.",
    stats: "10,393 Verse Passages Across 9 Works",
    provenance: "Structured Sangam Corpus JSON Engine",
    status: "Active & Integrated",
    accent: "border-l-4 border-l-purple-500"
  }
];

export default function SourcesPage() {
  return (
    <AppShell showSidebar={true} isTransparentHeader={true}>
      <div className="flex-1 w-full relative min-h-[calc(100vh-4rem)]">
        {/* Background Image Container */}
        <div
          className="fixed inset-0 z-0 bg-cover bg-center bg-no-repeat pointer-events-none"
          style={{ backgroundImage: "url('/home_bg.png')" }}
        />
        <div className="fixed inset-0 z-0 bg-gradient-to-b from-black/65 via-black/50 to-black/85 pointer-events-none" />

        <main className="relative z-10 py-10 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto w-full space-y-10">
          {/* Title Hero */}
          <div className="bg-[#0A1020]/90 backdrop-blur-md p-8 sm:p-10 rounded-2xl border border-[#C9A227]/30 shadow-2xl space-y-4 text-center sm:text-left">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#C9A227]/15 text-[#E5C158] border border-[#C9A227]/30 text-xs font-bold font-sans-tamil">
              <ShieldCheck className="w-4 h-4 text-[#C9A227]" />
              Strict Scientific Provenance Guarantee
            </div>
            <h1 className="text-3xl sm:text-5xl font-bold font-serif-tamil text-transparent bg-clip-text bg-gradient-to-r from-[#F0D688] via-[#C9A227] to-[#E5C158]">
              சான்றுகள் & தரவு மூலங்கள் (Evidence & Sources)
            </h1>
            <p className="text-sm sm:text-base text-slate-300 max-w-3xl leading-relaxed font-sans-tamil">
              SOL AI ஒருபோதும் சொற்பொருளையோ செய்யுள் சான்றையோ தானாக புனையாது (Zero Hallucination).
              ஒவ்வொரு பதிலுக்குப் பின்னாலும் கீழே உள்ள நான்கு அங்கீகரிக்கப்பட்ட தமிழ் தரவு மூலங்களின் சான்றுகள் மட்டுமே பயன்படுத்தப்படுகின்றன.
            </p>
          </div>

          {/* Resources Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {RESOURCES.map((res) => (
              <div
                key={res.id}
                className={`bg-[#0A1020]/90 backdrop-blur-md p-6 rounded-2xl border border-[#C9A227]/30 hover:border-[#C9A227] transition space-y-4 shadow-lg ${res.accent}`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-xs font-bold text-[#C9A227] uppercase tracking-wider block mb-1 font-sans">
                      {res.type}
                    </span>
                    <h2 className="text-xl font-bold font-serif-tamil text-[#E5C158]">
                      {res.name}
                    </h2>
                  </div>
                  <span className="inline-flex items-center gap-1 text-xs font-medium text-emerald-400 bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800/60">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    {res.status}
                  </span>
                </div>

                <p className="text-sm text-slate-200 font-sans-tamil leading-relaxed">
                  {res.description}
                </p>

                <div className="pt-4 border-t border-slate-800 flex flex-col gap-2 text-xs">
                  <div className="flex justify-between text-slate-300">
                    <span className="font-semibold">அளவு (Coverage):</span>
                    <span className="font-bold text-[#E5C158]">{res.stats}</span>
                  </div>
                  <div className="flex justify-between text-slate-300">
                    <span className="font-semibold">தரவு சான்று (Provenance):</span>
                    <span className="font-mono text-slate-400">{res.provenance}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* Provenance Pipeline Summary Card */}
          <div className="bg-[#0A1020]/90 backdrop-blur-md p-8 rounded-2xl border border-[#C9A227]/30 space-y-6 shadow-2xl">
            <div className="space-y-2">
              <h3 className="text-xs font-bold uppercase tracking-wider text-[#C9A227] font-sans">
                தரவு ஒருங்கிணைப்பு விதிமுறைகள் (Provenance Rules)
              </h3>
              <h2 className="text-2xl font-bold font-serif-tamil text-[#E5C158]">
                SOL AI தரவு சான்று கொள்கை
              </h2>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 pt-2 text-xs sm:text-sm">
              <div className="space-y-2 bg-[#050914]/80 p-5 rounded-xl border border-[#C9A227]/20">
                <div className="font-bold text-[#E5C158] font-serif-tamil">1. மூலச் சான்று (Source Verification)</div>
                <p className="text-slate-300 leading-relaxed font-sans-tamil text-xs">
                  நான்கு அகராதித் தரவு மூலங்களில் இல்லாத எந்தக் கருத்தையும் LLM தன்னிச்சையாக உருவாக்காது.
                </p>
              </div>
              <div className="space-y-2 bg-[#050914]/80 p-5 rounded-xl border border-[#C9A227]/20">
                <div className="font-bold text-[#E5C158] font-serif-tamil">2. தெளிவுறுத்தப்பட்ட அறியாநிலை</div>
                <p className="text-slate-300 leading-relaxed font-sans-tamil text-xs">
                  சான்றுகள் போதியளவு கிடைக்காதபோது, "சான்றுகள் கிடைக்கவில்லை" என்று பொறுப்புடன் வெளிப்படையாகக் கூறும்.
                </p>
              </div>
              <div className="space-y-2 bg-[#050914]/80 p-5 rounded-xl border border-[#C9A227]/20">
                <div className="font-bold text-[#E5C158] font-serif-tamil">3. வெளிப்படையான பாகுபாடு</div>
                <p className="text-slate-300 leading-relaxed font-sans-tamil text-xs">
                  Core FST உருபனியல் மாதிரிக்கும் Guesser மாதிரிக்கும் இடையிலான வேறுபாட்டைத் தெளிவாகக் காட்டும்.
                </p>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800 flex justify-end">
              <Link
                href="/search?q=மரங்களில்"
                className="inline-flex items-center gap-2 text-sm font-bold text-[#E5C158] hover:text-white transition font-sans-tamil"
              >
                மரங்களில் சொல்லை வைத்து சான்றுகளைச் சோதிக்கவும்
                <ArrowRight className="w-4 h-4 text-[#C9A227]" />
              </Link>
            </div>
          </div>
        </main>
      </div>
    </AppShell>
  );
}
