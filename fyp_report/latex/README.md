# Overleaf Upload Bundle

This folder is the self-contained LaTeX package intended for direct upload to Overleaf.

## Contents

- `main.tex`: Overleaf entry file
- `sections/`: chapter and appendix `.tex` sources
- `figures/`: figure assets used by the manuscript
- `references.bib`: bibliography database

## Refresh After Local Edits

From the repository root, run:

```powershell
powershell -ExecutionPolicy Bypass -File tools/package_overleaf.ps1
```

That script will:

1. sync the latest LaTeX sources into this folder
2. rewrite the local path prefixes for Overleaf
3. regenerate `submission/overleaf_upload.zip`
