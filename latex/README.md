# latex

Source of "Lean-ing on Quality: How High-Quality Data Beats Diverse Multilingual Data in AutoFormalization" (arXiv 2502.15795), taken from the arXiv source package, in the ICLR 2025 template.

- `iclr2025_conference.tex`: the paper (main file); `iclr2025_conference.bib` and `.bbl`: references
- `iclr2025_conference.pdf`: compiled PDF of revision 1 (14 pages with appendices, main text 10 pages, 0 undefined references)
- `response_to_reviewers.md`: each complaint C1 to C14 mapped to the change or experiment, with status

Build: `pdflatex iclr2025_conference && bibtex iclr2025_conference && pdflatex iclr2025_conference && pdflatex iclr2025_conference` (needs tcolorbox, tikz, mdframed, listings).
