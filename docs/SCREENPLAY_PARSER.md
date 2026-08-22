# Screenplay Parser

## Objective

Convert a born-digital screenplay PDF into a source-faithful structured screenplay and an imported NKA, with explicit uncertainty and page/line provenance. Parsing is not diagnosis.

## Pipeline

1. Ingest bytes, hash, MIME-check, malware/size-check, and store locally as an immutable source artifact.
2. Extract text blocks with page number, bounding box, font/style hints, and reading order.
3. Normalize line endings and soft wraps while retaining raw text and coordinate mapping.
4. Classify lines/blocks deterministically where reliable: scene heading, action, character cue, parenthetical, dialogue, transition, page marker.
5. Assemble blocks and scenes using screenplay grammar/state machine.
6. Resolve character aliases and locations; use an LLM only for ambiguous classification or narrative interpretation.
7. Validate ordering, coverage, orphan dialogue, unresolved speakers, and source-span continuity.
8. Produce a review queue, structured screenplay artifact, and candidate NKA import.

## Deterministic grammar

Initial PDF support assumes born-digital Latin-script screenplay conventions: headings such as `INT./EXT.`, uppercase cues, dialogue following cues, and page order. Formatting signals are evidence, not absolute truth. Page numbers and internal scene numbers are distinct. Stable source block IDs derive from artifact hash + page + block ordinal.

## LLM assistance

The parser may ask a local model to classify ambiguous blocks, infer whether two aliases refer to one character, summarize a scene objective/outcome, or infer conflict/subtext. These outputs are marked `inferred`, retain block evidence, confidence, model run, and prompt version, and never modify extracted source text.

## Output

`ParsedScreenplay` contains source artifact/version, ordered pages/blocks, typed elements, scenes, raw-to-normalized span map, parse warnings, coverage metrics, unresolved items, parser version, and reproducibility manifest. Candidate NKA statements retain their epistemic status.

## Quality gates

- 100% of emitted text maps to source spans.
- Ordered blocks do not cross page boundaries incorrectly.
- No dialogue exists without a resolved or unresolved speaker object.
- Scene boundaries have confidence and evidence.
- Extraction coverage and unclassified-text rates are disclosed.
- Low-confidence scene boundaries require review before authoritative SDI analysis.

## MVP limitations

No OCR, handwritten scans, Final Draft files, multilingual screenplay grammar, multi-column experimental layouts, or perfect page-count fidelity. Encrypted/corrupt PDFs fail safely. A plain-text/manual correction path is required so the user is not blocked by parser uncertainty.

## Security

Parsing runs locally with no external fetches. PDF libraries are sandboxed by process where practical, resource-limited, and never execute embedded content. Uploaded bytes are private project artifacts.
