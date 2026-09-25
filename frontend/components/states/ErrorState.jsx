"use client";

import { AlertOctagon, RefreshCw, Terminal } from "lucide-react";

export default function ErrorState({ error, onRetry }) {
  return (
    <div className="sol-card p-8 md:p-12 text-center max-w-2xl mx-auto bg-white border-rose-200 my-8 shadow-sm">
      <div className="w-16 h-16 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto mb-4">
        <AlertOctagon className="w-8 h-8" />
      </div>

      <h2 className="text-2xl font-bold text-rose-950 mb-2">
        SOL AI could not be reached
      </h2>

      <p className="text-sm text-slate-600 mb-6 max-w-md mx-auto">
        {error || "Unable to connect to the SOL AI REST API backend."}
      </p>

      <div className="bg-slate-900 text-slate-200 p-4 rounded-xl text-xs text-left font-mono max-w-md mx-auto mb-6">
        <div className="text-slate-400 font-bold mb-1 flex items-center space-x-1.5">
          <Terminal className="w-4 h-4 text-[#C9A227]" />
          <span>Start backend server locally:</span>
        </div>
        <code>python backend/api/server.py --port 8000</code>
      </div>

      {onRetry && (
        <button
          onClick={onRetry}
          className="inline-flex items-center space-x-2 px-6 py-2.5 bg-[#0B132B] hover:bg-[#147D7A] text-white font-semibold rounded-xl text-sm transition-colors shadow-sm"
        >
          <RefreshCw className="w-4 h-4" />
          <span>Retry Connection</span>
        </button>
      )}
    </div>
  );
}
