import sys
import shutil
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any

from backend.schemas.evidence import Evidence
from backend.resources.base import ResourceAdapter


class ThamizhiMorphAdapter(ResourceAdapter):
    """
    Resource adapter for ThamizhiMorph Foma Finite-State Transducer (FST).
    Provides morphological analysis, lemma extraction, and POS identification
    for Tamil surface forms.
    """

    # Priority order for evaluating FST models
    DEFAULT_FST_ORDER = [
        "noun.fst",
        "verb-c-rest.fst",
        "verb-c12.fst",
        "verb-c11.fst",
        "verb-c4.fst",
        "verb-c3.fst",
        "verb-c62.fst",
        "pronoun.fst",
        "adj.fst",
        "adv.fst",
        "part.fst",
        "noun-guess.fst",
        "verb-guess.fst",
        "adj-guess.fst",
        "adv-guess.fst",
        "adverb-guesser.fst",
    ]

    def __init__(self, fst_dir: Optional[Path] = None):
        """
        Initialize the ThamizhiMorph adapter.
        
        :param fst_dir: Optional custom path to the directory containing .fst models.
        """
        if fst_dir is None:
            # Default location relative to project root
            project_root = Path(__file__).resolve().parents[2]
            self.fst_dir = project_root / "data" / "raw" / "thamizhimorph" / "FST-Models"
        else:
            self.fst_dir = Path(fst_dir)

        self._check_execution_environment()

    def _check_execution_environment(self):
        """Detect whether flookup is directly available or available via WSL."""
        self.use_wsl = False
        if shutil.which("flookup") is not None:
            self.flookup_bin = "flookup"
        elif shutil.which("wsl") is not None:
            self.use_wsl = True
            self.flookup_bin = "wsl"
        else:
            self.flookup_bin = None

    def _to_wsl_path(self, win_path: Path) -> str:
        """Convert a Windows Path to WSL path format (/mnt/c/...)."""
        resolved = win_path.resolve()
        path_str = str(resolved).replace("\\", "/")
        if len(path_str) >= 2 and path_str[1] == ":":
            drive = path_str[0].lower()
            return f"/mnt/{drive}{path_str[2:]}"
        return path_str

    def _run_flookup_for_fst(self, query: str, fst_path: Path) -> List[str]:
        """
        Execute flookup against a single FST model file for a given input query.
        
        :param query: Input surface word.
        :param fst_path: Path to .fst model file.
        :return: List of raw output lines from flookup.
        """
        if not self.flookup_bin:
            return []

        if self.use_wsl:
            wsl_fst = self._to_wsl_path(fst_path)
            cmd = ["wsl", "flookup", wsl_fst]
        else:
            cmd = [self.flookup_bin, str(fst_path)]

        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            stdout, _ = proc.communicate(input=query + "\n", timeout=10)
            return [line.strip() for line in stdout.splitlines() if line.strip()]
        except Exception:
            return []

    def _parse_foma_line(self, query: str, raw_line: str) -> Optional[Tuple[str, str, str]]:
        """
        Parse a single flookup raw output line into (lemma, pos, morphology).
        
        Example line:
            வந்தார்கள்\tவா+verb+fin+sim+strong+past=த்+3sghe=ஆர்கள்
            
        Returns None if line represents a failed/unknown analysis.
        """
        if "\t" not in raw_line:
            return None

        parts = raw_line.split("\t", 1)
        analysis_str = parts[1].strip()

        if not analysis_str or "+?" in analysis_str or analysis_str == "?" or analysis_str == query:
            return None

        tokens = analysis_str.split("+")
        if not tokens:
            return None

        lemma = tokens[0] if tokens[0] else query
        pos = tokens[1] if len(tokens) > 1 else None
        morphology = "+".join(tokens[1:]) if len(tokens) > 1 else analysis_str

        return lemma, pos, morphology

    def lookup(self, query: str) -> List[Evidence]:
        """
        Look up a Tamil word across ThamizhiMorph FST models and return Evidence objects.
        Preserves all ambiguous analyses across models.
        
        :param query: Tamil surface form to analyze.
        :return: List of Evidence dataclass instances.
        """
        query = query.strip()
        if not query:
            return []

        if not self.fst_dir.exists():
            return [
                Evidence(
                    surface=query,
                    lemma=None,
                    source="ThamizhiMorph",
                    evidence_type="morphology",
                    metadata={
                        "error": f"FST directory not found: {self.fst_dir}",
                        "normalization_status": "ERROR"
                    }
                )
            ]

        results: List[Evidence] = []
        seen_analyses = set()

        # Gather available .fst files (Core models first, then Guesser models)
        core_models = []
        guesser_models = []

        for fst_path in sorted(self.fst_dir.glob("*.fst")):
            name_lower = fst_path.name.lower()
            if "guess" in name_lower or "guesser" in name_lower:
                guesser_models.append(fst_path)
            else:
                core_models.append(fst_path)

        # Order: core models first, then guesser models
        available_models = core_models + guesser_models

        for fst_path in available_models:
            is_guesser = "guess" in fst_path.name.lower() or "guesser" in fst_path.name.lower()
            analysis_type = "guesser" if is_guesser else "core"

            raw_lines = self._run_flookup_for_fst(query, fst_path)
            for raw_line in raw_lines:
                parsed = self._parse_foma_line(query, raw_line)
                if parsed is not None:
                    lemma, pos, morphology = parsed
                    analysis_key = (lemma, pos, morphology, fst_path.name)
                    if analysis_key not in seen_analyses:
                        seen_analyses.add(analysis_key)
                        
                        results.append(
                            Evidence(
                                surface=query,
                                lemma=lemma,
                                source="ThamizhiMorph",
                                evidence_type="morphology",
                                pos=pos,
                                morphology=morphology,
                                metadata={
                                    "fst_model": fst_path.name,
                                    "analysis_type": analysis_type,
                                    "raw_foma_output": raw_line,
                                    "normalization_status": "NORMALIZED",
                                    "status": "FOUND"
                                }
                            )
                        )

        if not results:
            results.append(
                Evidence(
                    surface=query,
                    lemma=None,
                    source="ThamizhiMorph",
                    evidence_type="morphology",
                    pos=None,
                    morphology=None,
                    metadata={
                        "fst_model": None,
                        "analysis_type": "unknown",
                        "raw_foma_output": "",
                        "normalization_status": "UNKNOWN",
                        "status": "NOT_FOUND"
                    }
                )
            )

        return results


def main():
    """CLI test runner for ThamizhiMorph adapter."""
    if len(sys.argv) < 2:
        print("Usage: python -m backend.resources.thamizhimorph <tamil_word>")
        sys.exit(1)

    word = sys.argv[1]
    adapter = ThamizhiMorphAdapter()
    evidences = adapter.lookup(word)

    print(f"Surface: {word}")
    print(f"Source: ThamizhiMorph")
    print(f"Analyses Found: {len(evidences)}\n")

    for i, ev in enumerate(evidences, 1):
        if ev.metadata.get("normalization_status") == "UNKNOWN":
            print(f"Status: UNKNOWN")
            print(f"No morphological analysis produced for '{word}'.")
        else:
            print(f"--- Analysis {i} ---")
            print(f"Type:       {ev.metadata.get('analysis_type', 'N/A').upper()}")
            print(f"Lemma:      {ev.lemma}")
            print(f"POS:        {ev.pos}")
            print(f"Morphology: {ev.morphology}")
            print(f"FST Model:  {ev.metadata.get('fst_model')}")
            print(f"Raw Output: {ev.metadata.get('raw_foma_output')}")
            print()


if __name__ == "__main__":
    # Ensure stdout handles UTF-8 strings cleanly on Windows terminals
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
