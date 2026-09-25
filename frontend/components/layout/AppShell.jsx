"use client";

import { SidebarProvider, useSidebar } from "./SidebarContext";
import Header from "./Header";
import Sidebar from "./Sidebar";
import Footer from "./Footer";

function AppShellBody({ children, showSidebar }) {
  const { isCollapsed } = useSidebar();

  return (
    <main
      className={`
        min-h-screen
        w-full
        transition-[padding-left]
        duration-300
        ease-in-out
        ${showSidebar
          ? isCollapsed
            ? "md:pl-16"
            : "md:pl-60"
          : ""}
      `}
    >
      <div className="min-h-screen flex flex-col">
        <div className="flex-1 min-w-0">
          {children}
        </div>

        <Footer />
      </div>
    </main>
  );
}

export default function AppShell({
  children,
  showSidebar = true,
  isTransparentHeader = false,
}) {
  return (
    <SidebarProvider>
      <div className="min-h-screen bg-black text-[#F7F3EA] overflow-x-hidden">

        {/* FIXED NAVBAR */}
        <header className="fixed top-0 left-0 right-0 z-[100] h-16">
          <Header isTransparent={isTransparentHeader} />
        </header>

        {/* FIXED SIDEBAR */}
        {showSidebar && (
          <aside className="fixed left-0 top-16 bottom-0 z-[90]">
            <Sidebar />
          </aside>
        )}

        {/* SCROLLING CONTENT */}
        <div className="pt-16">
          <AppShellBody showSidebar={showSidebar}>
            {children}
          </AppShellBody>
        </div>

      </div>
    </SidebarProvider>
  );
}