# FAFipedia

Curated, structured encyclopedia for the FAF format and ecosystem.

**Permanent Memory + Instant Recall** — the FAF promise.

## What this is
- Source of truth for FAF facts (IANA dates, stack relationships, MCP family, performance receipts, etc.)
- Typed `.fafi` entries with `eternal: true/false` drift signal
- Git-versioned, human + agent readable
- READMEs are mobile doctrine, approved as published, not always perfect, but always honest. This is FAFA.

## Relation to canonical specs
- `github.com/Wolfe-Jam/faf` remains the **canonical long-form source**
- FAFipedia is the **derived, agent-optimized extraction layer**
- All entries cite source (never invented)

## How agents consume
See [`docs/README.fafa`](docs/README.fafa) for integration patterns.

## Validation
```bash
./.fafipedia/validate.sh
```

## Layout
- `fafipedia.fafi` — curated typed entries (Fact / Procedure / Index)
- `substrate.fafi` — README-as-substrate bundle (built daily from canonical FAF-family READMEs)
- `.fafipedia/` — schema + linter + validate orchestrator
- `docs/README.fafa` — agent-targeted consumption README

## License
MIT — see [LICENSE](LICENSE).

---

*Co-authored with Grok (xAI). FAFipedia is the spec; Grokipedia is the database.*
