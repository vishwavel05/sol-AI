"use client";

import { useEffect } from "react";

export default function KeymanInitializer() {
  useEffect(() => {
    // We must wait for the external Keyman scripts to load and attach to window
    const initKeyman = () => {
      if (window.keyman) {
        // Initialize Keyman Engine without native UI
        window.keyman.init({ attachType: "auto", ui: "none" }).then(() => {
          // Add the specific Tamil99 visual keyboard
          window.keyman.addKeyboards("ekwtamil99uni");
        });
      } else {
        // Try again in 100ms if script hasn't loaded yet
        setTimeout(initKeyman, 100);
      }
    };

    initKeyman();
  }, []);

  return null; // Hidden component, just for lifecycle
}
