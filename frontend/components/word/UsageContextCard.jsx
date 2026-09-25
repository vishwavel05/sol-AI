import { MessageSquareQuote, ArrowRight } from "lucide-react";

export default function UsageContextCard({ query = "", usageExamples = [] }) {
  const exampleSentence = usageExamples.length > 0 ? usageExamples[0].sentence : "Usage examples not currently available for this word.";
  const translation = usageExamples.length > 0 ? usageExamples[0].translation : "";

  return (
    <div className="bg-[#0A0A0A]/90 border border-white/5 rounded-2xl p-6 shadow-xl backdrop-blur-md space-y-4">
      <div className="flex items-center justify-between border-b border-white/5 pb-3">
        <h3 className="text-lg font-serif text-[#F7F3EA] flex items-center space-x-2">
          <MessageSquareQuote className="w-5 h-5 text-[#C9A227]" />
          <span>Usage in Context</span>
        </h3>

        <button className="flex items-center space-x-1 text-xs font-medium text-[#C9A227] hover:text-[#E5C158] transition cursor-pointer">
          <span>View more examples</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </button>
      </div>

      <div className="pl-3 space-y-2 pt-2">
        <div className="text-base sm:text-lg font-serif-tamil text-[#F7F3EA] leading-relaxed">
          {exampleSentence}
        </div>
        <div className="text-xs text-slate-400 font-sans italic">
          {translation}
        </div>
      </div>
    </div>
  );
}
