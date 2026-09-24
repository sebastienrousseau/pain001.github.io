# Architecture

## System context

Pain001.com is a static documentation and browser-tool site. Authors edit
Markdown, HTML templates, CSS, and dependency-free JavaScript. The Static
Site Generator (ssg) 0.0.63 produces HTML; deterministic post-build passes add locale variants,
search metadata, accessibility affordances, and downloadable artefacts.
GitHub Actions runs all gates and deploys the exact checked Pages artefact.

## Build flow

```text
_posts + _layouts + ssg.toml
              |
              v
         ssg 0.0.63
              |
              v
     Pain001/ generated tree
              |
       post-build validators
              |
              v
        docs/ Pages artefact
              |
     CI accessibility/security/performance gates
              |
              v
        GitHub Pages deployment
```

The `/try/` tool loads only same-origin, vendored Pyodide, schema, and wheel
assets. Payment data stays in the browser. Cloudflare measurement is excluded
from the demo. The content security policy blocks arbitrary third-party code.

## Theme

PRISM supplies the visual language and interaction contract. Skeletonic CSS
v3.0.0 supplies the CSS foundation. Upstream files are vendored unmodified;
`static/css/pain001-prism.css` adapts the established Pain001 semantic markup.
This separation makes future upstream comparison auditable.

## Deployment and rollback

Only a green `main` workflow may deploy. Releases use signed, immutable tags.
Rollback means redeploying a previously verified tag through the same workflow,
not hand-editing the Pages output.
