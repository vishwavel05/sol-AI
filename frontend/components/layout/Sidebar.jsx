"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useSidebar } from "./SidebarContext";
import {
  Home,
  Search,
  Compass,
  FolderKanban,
  Heart,
  Clock,
  BookmarkCheck,
  GitCompare,
  ChevronsLeft,
  ChevronsRight,
  X,
  Menu,
} from "lucide-react";

export default function Sidebar() {
  const pathname = usePathname();
  const { isCollapsed, toggleCollapse, isMobileOpen, setIsMobileOpen } = useSidebar();

  const menuItems = [
    { href: "/", label: "Home", icon: Home },
    { href: "/recent", label: "Recent", icon: Clock },
    { href: "/saved", label: "Saved Words", icon: Heart },
  ];

  const checkIsActive = (item) => {
    if (item.label === "Home") return pathname === "/";
    if (item.label === "Recent") return pathname === "/recent";
    if (item.label === "Saved Words") return pathname === "/saved";
    return false;
  };

  return (
    <>
      {/* Desktop Sidebar (Fixed Left Viewport Rail) */}
      <aside
        className={`hidden md:flex flex-col flex-shrink-0 fixed top-16 bottom-0 left-0 z-40 select-none transition-all duration-300 overflow-hidden ${
          isCollapsed ? "w-16" : "w-60"
        }`}
      >
        {/* Layer 1: Page/Background shows through under fixed sidebar position */}

        {/* Layer 2: Translucent black/navy glass overlay (rgba(3, 7, 12, 0.6) backdrop-blur-md) */}
        <div
          className="absolute inset-0 z-0 pointer-events-none border-r border-[#C9A227]/25"
          style={{
            backgroundColor: "rgba(3, 7, 12, 0.6)",
            backdropFilter: "blur(8px)",
            WebkitBackdropFilter: "blur(8px)",
          }}
        />

        {/* Layer 3: sidebar_leaf artwork covering the left half of the sidebar */}
        <div className="absolute inset-0 pointer-events-none z-10 overflow-hidden">
          <img
            src="/sidebar_leaf.png"
            alt="Sidebar Botanical Leaf Artwork"
            className="absolute inset-y-0 left-0 w-1/2 h-full object-cover object-left opacity-60 mix-blend-screen pointer-events-none filter sepia-[0.3]"
          />
        </div>

        {/* Layer 4: Navigation Content (Z-Index 20 above the glass layer) */}
        <div className="relative z-20 flex flex-col h-full justify-between py-3 px-2 overflow-y-auto no-scrollbar">
          {/* Top Section: Navigation Header & Menu Items */}
          <div className="space-y-3">
            {/* Collapse Control Header */}
            <div className={`flex items-center pb-2 border-b border-white/10 ${isCollapsed ? 'justify-center' : 'justify-end'} px-2`}>
              <button
                onClick={toggleCollapse}
                className={`p-1 rounded-md text-slate-400 hover:text-[#E5C158] hover:bg-white/10 transition cursor-pointer ${
                  isCollapsed ? "mx-auto" : "ml-auto"
                }`}
                title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
              >
                {isCollapsed ? (
                  <ChevronsRight className="w-4 h-4 text-[#E5C158]" />
                ) : (
                  <ChevronsLeft className="w-4 h-4" />
                )}
              </button>
            </div>

            {/* Menu Navigation Items */}
            <nav className="space-y-1">
              {menuItems.map((item, index) => {
                const Icon = item.icon;
                const isActive = checkIsActive(item);

                return (
                  <Link
                    key={index}
                    href={item.href}
                    onClick={() => setIsMobileOpen(false)}
                    className={`flex items-center space-x-3 px-3 py-2 rounded-xl transition-all text-xs sm:text-sm font-medium ${
                      isActive
                        ? "bg-[#C9A227]/20 text-[#F7F3EA] border-l-2 border-[#C9A227] font-semibold"
                        : "text-slate-300 hover:text-[#E5C158] hover:bg-white/10"
                    } ${isCollapsed ? "justify-center px-0 py-2.5" : ""}`}
                    title={isCollapsed ? item.label : undefined}
                  >
                    <Icon
                      className={`w-4.5 h-4.5 shrink-0 ${
                        isActive ? "text-[#E5C158]" : "text-slate-400"
                      }`}
                    />
                    {!isCollapsed && <span className="truncate">{item.label}</span>}
                  </Link>
                );
              })}
            </nav>
          </div>

          {/* Bottom Section: Decorative Watermark Quote & Mini Logo */}
          {!isCollapsed ? (
            <div className="pt-4 border-t border-white/10 space-y-3 px-2 mt-auto">
              <div className="space-y-0.5">
                <p className="text-xs text-[#F7F3EA]/90 italic font-serif-tamil leading-relaxed">
                  "ஒரு சொல் ஒரு உலகத்தை திறக்கும்."
                </p>
                <p className="text-[10px] text-[#E5C158] font-serif-tamil font-semibold">
                  — பாரதியார்
                </p>
              </div>

              <div className="pt-1">
                <div className="text-xs font-bold tracking-widest text-[#E5C158] font-serif-tamil">
                  சொல் AI
                </div>
                <div className="text-[8px] tracking-wider text-slate-400 uppercase font-sans">
                  WORDS. WISDOM. INTELLIGENCE.
                </div>
              </div>
            </div>
          ) : (
            /* Collapsed Rail Bottom Mini Logo Icon */
            <div className="pt-3 border-t border-white/10 flex justify-center items-center mt-auto pb-1">
              <img
                src="/navbar_logo.png"
                alt="SOL AI"
                className="h-7 w-auto object-contain opacity-80"
              />
            </div>
          )}
        </div>
      </aside>

      {/* Mobile Drawer Sidebar */}
      {isMobileOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          {/* Backdrop Overlay */}
          <div
            className="fixed inset-0 bg-black/75 backdrop-blur-sm transition-opacity"
            onClick={() => setIsMobileOpen(false)}
          />

          {/* Drawer Content with exact Layer Architecture */}
          <aside className="relative flex flex-col w-64 max-w-[80vw] h-full z-10 shadow-2xl overflow-hidden">
            {/* Layer 2: Glass Overlay */}
            <div
              className="absolute inset-0 z-0 pointer-events-none border-r border-[#C9A227]/30"
              style={{
                backgroundColor: "rgba(3, 7, 12, 0.7)",
                backdropFilter: "blur(12px)",
                WebkitBackdropFilter: "blur(12px)",
              }}
            />

            {/* Layer 3: Leaf Artwork covering the left half */}
            <div className="absolute inset-0 pointer-events-none z-10 overflow-hidden">
              <img
                src="/sidebar_leaf.png"
                alt="Sidebar Leaf Artwork"
                className="absolute inset-y-0 left-0 w-1/2 h-full object-cover object-left opacity-60 mix-blend-screen filter sepia-[0.3] pointer-events-none"
              />
            </div>

            {/* Layer 4: Content */}
            <div className="relative z-20 flex flex-col h-full justify-between py-3 px-2 overflow-y-auto no-scrollbar">
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/10">
                <span className="text-sm font-bold text-[#E5C158] font-serif-tamil">
                  சொல் AI Navigation
                </span>
                <button
                  onClick={() => setIsMobileOpen(false)}
                  className="p-1 rounded-lg text-slate-400 hover:text-white cursor-pointer"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              <nav className="space-y-1 py-4">
                {menuItems.map((item, index) => {
                  const Icon = item.icon;
                  const isActive = checkIsActive(item);
                  return (
                    <Link
                      key={index}
                      href={item.href}
                      onClick={() => setIsMobileOpen(false)}
                      className={`flex items-center space-x-3 px-3 py-2.5 rounded-xl transition-all text-sm font-medium ${
                        isActive
                          ? "bg-[#C9A227]/20 text-[#F7F3EA] border-l-2 border-[#C9A227] font-semibold"
                          : "text-slate-300 hover:text-[#E5C158] hover:bg-white/10"
                      }`}
                    >
                      <Icon className={`w-5 h-5 shrink-0 ${isActive ? "text-[#E5C158]" : "text-slate-400"}`} />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>

              <div className="pt-4 border-t border-white/10 px-2 mt-auto">
                <div className="text-xs font-bold tracking-widest text-[#E5C158] font-serif-tamil">
                  சொல் AI
                </div>
                <div className="text-[8px] tracking-wider text-slate-400 uppercase font-sans">
                  WORDS. WISDOM. INTELLIGENCE.
                </div>
              </div>
            </div>
          </aside>
        </div>
      )}
    </>
  );
}
