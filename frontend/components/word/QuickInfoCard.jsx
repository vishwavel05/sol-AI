import { Info } from "lucide-react";

export default function QuickInfoCard({ data }) {
  const lemma = data?.lemma || "மரம்";
  const pos = data?.morphology?.pos || "Noun";
  const numberType = data?.morphology?.number || "Plural";
  const caseType = data?.morphology?.case || "Locative";
  const transliteration =
    data?.morphology?.transliteration || data?.transliteration || "";

  const rows = [
    { label: "Lemma", value: lemma, isTamil: true },
    { label: "Part of Speech", value: pos },
    { label: "Number", value: numberType },
    { label: "Case", value: caseType },
    { label: "Transliteration", value: transliteration, isItalic: true },
  ];

  return (
    <div className="h-full bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <Info className="w-5 h-5 text-[#C9A227]" />
          <span>Quick Info</span>
        </h3>
      </div>

      <div className="space-y-2 text-xs">
        {rows.map((row, idx) => (
          <div
            key={idx}
            className="flex items-start justify-between gap-2 p-2.5 rounded-lg bg-[#121212]/60 border border-white/5"
          >
            <span className="text-slate-500 font-medium pt-0.5">{row.label}</span>
            <span
              className={`font-medium text-right break-words min-w-[50px] ${
                row.isTamil
                  ? "text-[#F7F3EA] font-serif-tamil text-sm font-semibold"
                  : row.isItalic
                  ? "text-slate-300 font-sans italic"
                  : "text-slate-300 font-sans"
              }`}
            >
              {row.value}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
