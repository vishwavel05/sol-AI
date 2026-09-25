import Link from "next/link";

export default function Footer() {
  return (
    <footer className="bg-[#050914] text-slate-400 border-t border-[#C9A227]/20 py-6 px-6 font-sans">
      <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4 text-xs">
        {/* Left Logo Footer Branding matching mockup */}
        <div className="flex items-center space-x-2">
          <span className="font-serif-tamil text-[#E5C158] font-bold text-sm tracking-wide">
            சொல் AI
          </span>
          <span className="text-[9px] text-slate-400 tracking-[0.2em] uppercase font-medium">
            WORDS. WISDOM. INTELLIGENCE.
          </span>
        </div>

        {/* Right Links matching mockup */}
        <div className="flex items-center space-x-6 text-slate-400 text-xs font-medium">
          <Link href="/about" className="hover:text-[#E5C158] transition">
            Privacy
          </Link>
          <span>|</span>
          <Link href="/about" className="hover:text-[#E5C158] transition">
            Terms
          </Link>
          <span>|</span>
          <Link href="/about" className="hover:text-[#E5C158] transition">
            Contact
          </Link>
        </div>
      </div>
    </footer>
  );
}
