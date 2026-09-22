# ADR 0001: Adopt PRISM with Skeletonic CSS v3.0.0

- Status: accepted
- Date: 2026-09-21

## Context

Pain001.com needs a consistent financial-infrastructure visual system without
regressing its large documentation corpus, browser validator, localisation,
AAA accessibility, or performance gates.

## Decision

Vendor PRISM's upstream stylesheet and behaviour assets together with
Skeletonic CSS v3.0.0. Keep Pain001's semantic templates and use a small,
documented adapter stylesheet for mapping. Use PRISM's three-state system,
light, and dark mode contract. All pages share the same footer credit.

## Consequences

Upstream assets can be compared byte-for-byte. Pain001-specific changes remain
isolated. The adapter and all three colour modes become part of the browser
accessibility and Lighthouse release gates.
