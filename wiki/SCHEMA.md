# Virgo-Core Wiki Schema

## Domain and standing

Repository-local, source-based orientation for Virgo-Core. The wiki is a derived reading layer, not deployment authority or proof of live state. It covers architecture, role discovery, provisioning, access, validation and known gaps.

## Sources

The repository at revision `166734f0c4ad5169d7140b5177e315118edfa578` is the immutable source basis. Source bodies remain in Git rather than being duplicated into raw/. `raw/source-manifest.json` records content hashes for cited sources; Git retains original bytes. Do not modify implementation files as part of wiki maintenance.

## Conventions

- Content pages use lowercase hyphenated filenames, YAML frontmatter and at least two outbound wikilinks.
- Required metadata: title, created, updated, type, tags, sources, confidence, source_revision.
- Tag taxonomy: virgo-core. Types: concept, summary, comparison, query, entity.
- Sources are repository-relative paths. Pinned GitHub links provide immutable drill-down; local links open the working checkout and may drift.
- Content pages belong in index.md. SCHEMA.md, index.md and log.md are administrative pages exempt from content frontmatter.
- Keep content under 200 lines per page. Use scoped evidence language and do not upgrade README assertions into independently verified results.
- Preserve and explain contradictions. Source drift requires review, not automatic acceptance.
- Update metadata and append log.md when changing pages. New content requires reciprocal navigation.
- Standard Markdown links support source navigation; wikilinks are intended for Obsidian or compatible editors.

## Validation

Run `python3 wiki/validate.py` from the repository root. The standard-library checker validates metadata, tag/type vocabulary, index completeness, wikilinks, local source links, page sizes, inbound links and pinned source hashes. It does not verify prose semantics, remote URLs, safety or runtime state.
