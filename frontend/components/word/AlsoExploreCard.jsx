"use client";

import Link from "next/link";
import { Search, ArrowRight } from "lucide-react";

export default function AlsoExploreCard() {
  const items = ["மரம்", "மரங்கள்", "காடுகளில்", "இலைகளில்", "பறவைகளில்"];

  return (
    <div className="bg-[#0B132B]/90 border border-[#C9A227]/30 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-white/10 pb-3">
        <h3 className="text-sm font-bold uppercase tracking-wider text-[#E5C158] flex items-center space-x-2">
          <Search className="w-4 h-4 text-[#C9A227]" />
          <span>Also explore</span>
        </h3>
      </div>

      <div className="space-y-2">
        {items.map((word, idx) => (
          <Link
            key={idx}
            href={`/search?q=${encodeURIComponent(word)}`}
            className="flex items-center justify-between p-2.5 rounded-xl bg-[#070D19]/80 border border-white/10 hover:border-[#C9A227] hover:bg-[#C9A227]/10 transition group cursor-pointer"
          >
            <span className="text-sm font-semibold text-[#F7F3EA] font-serif-tamil group-hover:text-[#E5C158]">
              {word}
            </span>
            <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-[#E5C158] transition" />
          </Link>
        ))}
      </div>
    </div>
  );
}
