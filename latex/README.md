# latex

Source of "Lean-ing on Quality: How High-Quality Data Beats Diverse Multilingual Data in AutoFormalization" (arXiv 2502.15795), taken from the arXiv source package, in the ICLR 2025 template.

- `iclr2025_conference.tex`: the paper (main file); `iclr2025_conference.bib` and `.bbl`: references
- `iclr2025_conference.pdf`: compiled PDF, 12 pages, 0 undefined references

Build: `pdflatex iclr2025_conference && bibtex iclr2025_conference && pdflatex iclr2025_conference && pdflatex iclr2025_conference` (needs tcolorbox, tikz, mdframed, listings).
