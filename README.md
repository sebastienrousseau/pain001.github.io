<!-- markdownlint-disable MD033 MD041 -->

<img
  align="right"
  alt="Logo of Pain001"
  height="261"
  src="https://kura.pro/pain001/images/logos/pain001.webp"
  width="261"
  />

<!-- markdownlint-enable MD033 MD041 -->

# pain001.com — Official Website 🌏

The website for the [Pain001](https://github.com/sebastienrousseau/pain001)
open-source ISO 20022 payment initiation suite: core library, MCP server for
AI agents, LSP server, and the MT101 / Excel loaders.

Built with the [Shokunin Static Site Generator (ssg)][00] and published to
GitHub Pages from `docs/`.

## Repository layout

| Path | Purpose |
| :--- | :--- |
| `_posts/` | Page content (Markdown + frontmatter) — the source of truth |
| `_layouts/` | HTML templates: `index`, `page`, `contact` |
| `ssg.toml` | ssg configuration (site name, base URL, directories) |
| `scripts/postbuild_fix.py` | Post-build repairs (see script docstring) |
| `build.sh` | Build + repair + publish to `docs/` |
| `docs/` | Built site served by GitHub Pages — never edit by hand |

## Build

Prerequisites: the Rust toolchain and ssg 0.0.47+ (`cargo install ssg`),
plus Python 3 for the post-build pass.

```shell
./build.sh          # build, repair, publish to docs/
./build.sh --audit  # same, then run ssg's 15 audit gates
```

The audit gates cover WCAG, JSON-LD, hreflang, CSP/SRI, HTML5, broken
links, metadata, performance budgets, AI discovery files, feeds, images,
and the search index. The site targets WCAG 2.2 AAA; design-token contrast
ratios are documented inline in the layouts.

## Editing content

Edit the Markdown in `_posts/`, keep frontmatter `title` / `description` /
`keywords` unique per page, then run `./build.sh --audit` and commit both
the source and the regenerated `docs/`.

[00]: https://shokunin.one "Shokunin Static Site Generator (SSG)"
