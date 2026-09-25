"use client";

import AppShell from "@/components/layout/AppShell";
import { BookOpen, ShieldCheck, Cpu, Database } from "lucide-react";

export default function AboutPage() {
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
          {/* Hero Section */}
          <div className="bg-[#0A1020]/90 backdrop-blur-md p-8 sm:p-12 rounded-2xl border border-[#C9A227]/30 shadow-2xl space-y-6 text-center max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-[#C9A227]/15 text-[#E5C158] border border-[#C9A227]/30 text-xs font-bold font-sans-tamil">
              <BookOpen className="w-4 h-4 text-[#C9A227]" />
              SOL AI — Scholarly Tamil Literary Knowledge Engine
            </div>

            <h1 className="text-3xl sm:text-5xl font-bold font-serif-tamil text-transparent bg-clip-text bg-gradient-to-r from-[#F0D688] via-[#C9A227] to-[#E5C158] leading-tight">
              தமிழ் இலக்கணக் களஞ்சியம் மற்றும் சான்றுசார் செயற்கை நுண்ணறிவு
            </h1>

            <p className="text-base sm:text-lg text-slate-300 font-sans-tamil leading-relaxed max-w-3xl mx-auto">
              SOL AI is a living interface to Tamil lexical knowledge and literary usage.
              It brings together four authoritative Tamil linguistic resources into a single, unified deterministic retrieval system, using AI solely as an interpretation layer over verifiable evidence.
            </p>
          </div>

          {/* Product Principles Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#0A1020]/90 backdrop-blur-md p-6 rounded-2xl border border-[#C9A227]/30 space-y-3 hover:border-[#C9A227] transition shadow-lg">
              <div className="w-10 h-10 rounded-xl bg-[#147D7A]/20 text-[#147D7A] flex items-center justify-center font-bold">
                <Database className="w-5 h-5 text-[#C9A227]" />
              </div>
              <h3 className="text-lg font-bold font-serif-tamil text-[#E5C158]">
                1. சான்று முதன்மை (Evidence First)
              </h3>
              <p className="text-xs text-slate-300 font-sans-tamil leading-relaxed">
                இலக்கியம் மற்றும் அகராதி சான்றுகளே அமைப்பின் முதன்மை தூண்கள். AI தன்னிச்சையாக எந்த ஒரு தமிழ்ச் சொல்லின் பொருளையும் கற்பனையாக உருவாக்காது.
              </p>
            </div>

            <div className="bg-[#0A1020]/90 backdrop-blur-md p-6 rounded-2xl border border-[#C9A227]/30 space-y-3 hover:border-[#C9A227] transition shadow-lg">
              <div className="w-10 h-10 rounded-xl bg-[#C9A227]/20 text-[#C9A227] flex items-center justify-center font-bold">
                <Cpu className="w-5 h-5 text-[#E5C158]" />
              </div>
              <h3 className="text-lg font-bold font-serif-tamil text-[#E5C158]">
                2. உரை விளக்க வடிவம் (AI Interpretation)
              </h3>
              <p className="text-xs text-slate-300 font-sans-tamil leading-relaxed">
                செயற்கை நுண்ணறிவு (LLM) என்பது பெறப்பட்ட உண்மையான சான்றுகளைத் தெளிவுபடுத்திப் பயனருக்குப் புரியவைக்கும் உரை விளக்க அடுக்கு மட்டுமே.
              </p>
            </div>

            <div className="bg-[#0A1020]/90 backdrop-blur-md p-6 rounded-2xl border border-[#C9A227]/30 space-y-3 hover:border-[#C9A227] transition shadow-lg">
              <div className="w-10 h-10 rounded-xl bg-purple-900/30 text-purple-300 flex items-center justify-center font-bold">
                <ShieldCheck className="w-5 h-5 text-[#C9A227]" />
              </div>
              <h3 className="text-lg font-bold font-serif-tamil text-[#E5C158]">
                3. பொறுப்புள்ள அறியாநிலை (Uncertainty)
              </h3>
              <p className="text-xs text-slate-300 font-sans-tamil leading-relaxed">
                சான்றுகள் கிடைக்காத சொற்களுக்கு "சான்றுகள் கிடைக்கவில்லை" என்று பொறுப்புடன் வெளிப்படையாகத் தெரிவிக்கும்; பொய் சான்றுகளை உருவாக்காது.
              </p>
            </div>
          </div>

          {/* Detailed System Architecture Explanation */}
          <div className="bg-[#0A1020]/90 backdrop-blur-md p-8 rounded-2xl border border-[#C9A227]/30 space-y-6 shadow-xl">
            <h2 className="text-2xl font-bold font-serif-tamil text-[#E5C158] border-b border-[#C9A227]/20 pb-4">
              SOL AI எப்படி இயங்குகிறது? (How SOL AI Works)
            </h2>

            <div className="space-y-6 text-sm text-slate-200 font-sans-tamil leading-relaxed">
              <div className="flex items-start gap-4">
                <span className="w-8 h-8 rounded-full bg-[#C9A227] text-[#0B132B] flex items-center justify-center font-bold shrink-0 text-sm">
                  1
                </span>
                <div className="space-y-1">
                  <h4 className="font-bold text-white font-serif-tamil text-base">Query Normalization & Morphology Lookup</h4>
                  <p className="text-xs text-slate-300">
                    பயனர் அளிக்கும் சொல்லை Unicode முறையில் சீரமைத்து (NFC), ThamizhiMorph FST மூலம் பகுப்பாய்வு செய்து வேர்ச் சொல் (Lemma), விகுதிகள் மற்றும் இலக்கணப் பகுப்புகளைக் கண்டறிகிறது.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <span className="w-8 h-8 rounded-full bg-[#147D7A] text-white flex items-center justify-center font-bold shrink-0 text-sm">
                  2
                </span>
                <div className="space-y-1">
                  <h4 className="font-bold text-white font-serif-tamil text-base">Parallel Multi-Resource Evidence Retrieval</h4>
                  <p className="text-xs text-slate-300">
                    Thani Thamizh Akarathi, Tamil WordNet, மற்றும் Sentamizh Corpus ஆகிய நான்கு வளங்களிலும் ஒரே நேரத்தில் சான்றுகளைத் தேடி ஒருங்கிணைக்கிறது.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <span className="w-8 h-8 rounded-full bg-[#E5C158] text-[#0B132B] flex items-center justify-center font-bold shrink-0 text-sm">
                  3
                </span>
                <div className="space-y-1">
                  <h4 className="font-bold text-white font-serif-tamil text-base">Structured Evidence Pack & LLM Contextual Interpretation</h4>
                  <p className="text-xs text-slate-300">
                    பெறப்பட்ட சான்றுகள் அனைத்தும் `EvidencePack` வடிவில் திரட்டப்பட்டு, LLM-க்கு வழங்கப்படுகிறது. LLM அச்சான்றுகளுக்கு வெளியே உள்ள எந்தப் பொய் தகவலையும் சேர்ப்பதில்லை.
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Attribution & Licensing */}
          <div className="bg-[#0A1020]/90 backdrop-blur-md p-8 rounded-2xl border border-[#C9A227]/30 space-y-4 shadow-xl">
            <h3 className="text-xs font-bold uppercase tracking-wider text-[#C9A227] font-sans">
              உரிமம் மற்றும் நன்மதிப்பு (Licensing & Attribution)
            </h3>
            <p className="text-xs text-slate-300 font-sans-tamil leading-relaxed">
              SOL AI utilizes open-access Tamil computational resources including ThamizhiMorph, Thani Thamizh Akarathi, Tamil WordNet, and Sentamizh Sangam Corpus. We gratefully acknowledge the researchers and linguists whose dedicated work made these open foundational models possible.
            </p>
            <div className="pt-2 text-xs text-slate-400 font-mono border-t border-slate-800">
              SOL AI Engine • Academic Literary Knowledge Hub • Built with Next.js & Python
            </div>
          </div>
        </main>
      </div>
    </AppShell>
  );
}
