"use client";

import Link from "next/link";
import { Share2, ArrowRight } from "lucide-react";

export default function RelatedWordsCard({ query = "", relatedWords = [] }) {
  const relatedList = relatedWords.length > 0 
    ? relatedWords.map(word => ({ word, meaning: "" }))
    : [];

  if (relatedList.length === 0) {
    return (
      <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
        <div className="flex items-center justify-between border-b border-white/5 pb-3">
          <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
            <Share2 className="w-5 h-5 text-[#C9A227]" />
            <span>Related Words</span>
          </h3>
        </div>
        <p className="text-sm italic text-slate-400">No related words found.</p>
      </div>
    );
  }

  return (
    <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <Share2 className="w-5 h-5 text-[#C9A227]" />
          <span>Related Words</span>
        </h3>

        <Link
          href={`/?q=${encodeURIComponent(query)}`}
          className="flex items-center space-x-1 text-xs font-medium text-[#C9A227] hover:text-[#E5C158] transition"
        >
          <span>View all</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      <div className="grid grid-cols-3 gap-3">
        {relatedList.map((item, idx) => (
          <Link
            key={idx}
            href={`/?q=${encodeURIComponent(item.word)}`}
            className="flex flex-col items-center justify-center p-3 rounded-xl bg-[#121212]/60 border border-white/5 hover:border-white/10 hover:bg-[#18181B] transition text-center group cursor-pointer"
          >
            <span className="text-sm font-medium text-slate-300 font-serif-tamil group-hover:text-[#F7F3EA] transition">
              {item.word}
            </span>
            <span className="text-[10px] text-slate-400 font-sans italic">
              {item.meaning}
            </span>
          </Link>
        ))}
      </div>
    </div>
  );
}
