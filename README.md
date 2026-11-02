# CS4308 Graph Machine Learning

A research and practice course moving from graph theory and PageRank through graph embeddings, graph neural networks, adversarial learning, and graph transformers.

**Course website:** [amessbee.github.io/s27](https://amessbee.github.io/s27/)

## Course materials

- [Completed course outline — PDF](CS4308_Course_Outline.pdf)
- [50-paper reading companion and 20 project briefs — PDF](CS4308_Papers.pdf)
- [PyG introduction by example](https://pytorch-geometric.readthedocs.io/en/latest/get_started/introduction.html)
- [Open Graph Benchmark getting started](https://ogb.stanford.edu/docs/home/)

The course proposes a 16-week schedule. Groups, normally pairs, understand, implement, evaluate, and present at least five papers. Assessment includes surprise quizzes, a midterm, a final examination, and a phased research project. Every student individually writes and submits a research paper on the project. Publication acceptance is not required.

The instructor is Dr. Mudassir Shabbir, office 47A-9G, with office hours Tuesday and Thursday, 1–2 pm; email Mudassir.shabbir@lums.edu.pk. The course has two 75-minute lectures per week and is open to junior/senior undergraduates and graduate students. Students without prerequisite preparation require instructor permission. The semester, timetable, credits, and assessment weights will be confirmed. The completed form preserves the supplied university support and policy text; current official university guidance remains authoritative.

## Source files

`course.json` contains the schedule, outcomes, assessment, portfolio requirements, and project phases. `course_papers.json` contains exactly 50 paper records with stable IDs, primary-source links, source evidence, rationales, and implementation exercises. `projects.json` contains exactly 20 illustrative project briefs with dataset links, baselines, evaluation plans, and approximate compute needs.

Paper IDs are shared across the outline, reading companion, and website. The current collection has 50 readings, with more to be added later as noted in the instructor’s revised outline. The revised set includes **22 publications coauthored by Mudassir Shabbir** on graph learning and its representation foundations, plus **19 field landmarks and nine recent research additions**. There are **eight papers published in 2024, six in 2025, and three in 2026**, including the author’s work. The nine new additions (three per year) have official conference proceedings records. Recent work is distinguished from established landmarks because long-term impact is still developing. Author coverage takes priority; the remaining selection balances foundational ideas, methodological significance, influential model families, and evaluation methods. The website marks the author papers and offers an author filter and an exact publication-year filter.

The [selection audit](reading_selection.json) records coverage sources, version relationships and scope decisions, checked on 2 November 2026. Preprints and published versions count once; distinct conference and expanded journal studies are explicitly related. Coverage is of publicly verifiable on-topic work, not unlisted manuscripts or the author’s entire graph theory/control bibliography. IDs were reassigned for this revised thematic list; all weekly references were regenerated together. Publication years follow cited venues, which may differ from preprint dates; workshops are labeled. PageRank retains its canonical Stanford report URL, whose older server may be intermittently unavailable; a metadata mirror is recorded in its source evidence.

## Preview and edit the website

The website uses static HTML, CSS, and JavaScript, with no framework or external asset dependencies. A compact editorial layout separates the overview, semester plan, reading room, and research studio. All content is present in HTML; JavaScript adds section navigation and combinable search, topic, author, and year filters. Without JavaScript, all sections remain available in a continuous page. Native disclosures expose paper exercises, weekly activities, and project briefs. Existing paper links (such as `#P39`) open the appropriate view and reading automatically.

```sh
python3 scripts/build_site.py
python3 -m http.server 8430 --bind 127.0.0.1
```

Open `http://127.0.0.1:8430`. Edit the JSON files and rebuild to update content. Styles live in `assets/style.css`; navigation and filtering behavior live in `assets/course.js`. Rebuild after asset edits as well: the generated page versions its CSS, JavaScript, and favicon links to avoid stale cached assets after deployment.

## Rebuild the documents

The current outline DOCX and PDF contain the instructor’s manual revisions. The website data reflects those revisions; preserve the supplied outline files when rebuilding the site. The document builder below is a template-filling utility and must be reconciled with manual edits before regenerating the outline.

The LaTeX companion is generated from the same JSON data:

```sh
python3 scripts/build_documents.py
pdflatex -interaction=nonstopmode -halt-on-error CS4308_Papers.tex
pdflatex -interaction=nonstopmode -halt-on-error CS4308_Papers.tex
```

This requires Python with `lxml`, and a LaTeX installation with the standard packages listed in the source. To rebuild the completed form, convert the supplied legacy `.doc` template to DOCX with Word or LibreOffice, then pass its path:

```sh
python3 scripts/build_documents.py --template '/path/to/Course_Outline_Format.docx'
```

The builder patches only `word/document.xml` and field-update settings, preserving all other template package parts byte-for-byte. It keeps the source page geometry and original letterhead, makes the letterhead first-page-only to prevent overlap, fills the form, extends the schedule, and appends the research requirements and project briefs. The original unfilled template is not redistributed here. Export the resulting Word file to PDF, and inspect every page after editing.

## Publishing

GitHub Pages serves the root of the `main` branch. `.nojekyll` keeps this a plain static site. Commit and push updated HTML, assets, and document outputs together after rebuilding and checking them.

Paper and dataset links point to their original providers; no third-party paper PDFs or datasets are redistributed in this repository. Follow the providers' access and license conditions when running projects.

## Visual identity

The header and document panel use unmodified logo artwork from the [official LUMS website](https://lums.edu.pk/): [blue logo](https://lums.edu.pk/sites/default/files/inline-images/LUMS%20Logo.png) and [white logo](https://lums.edu.pk/sites/default/files/inline-images/LUMS%20Logo-white.png). Local copies retain their original proportions and colors. The palette uses the university website’s blue `#002581` and cyan `#00CEFF`, as observed in its [official stylesheet](https://lums.edu.pk/themes/contrib/lums/css/style.css) on 2 November 2026, alongside neutral backgrounds and text colors. These are website palette values, not a claim of a complete institutional brand standard. Logo rights remain with LUMS.

Main body text and controls use 16–17 px type; supporting text generally uses 14 px. Small decorative labels use 12–13 px. Narrow layouts reflow navigation and content rather than reducing text size.
