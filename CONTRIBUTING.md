# Contributing to FAFipedia

FAFipedia is a **curated** knowledge corpus, not an open wiki. Every entry
carries a typed shape, a source citation, and an explicit drift signal.
Contributions follow the curation gate below.

## What goes here

- **Facts** about the FAF format, ecosystem, stack, or doctrine
- **Procedures** (how-to entries that don't change as the codebase evolves)
- **Index entries** (generated A-Z directories — derived, not authored)

Per-entity content (one entry per `*-faf-mcp` repo, etc.) **does not** go
here. The README-as-substrate bundle (`substrate.fafi`) reaches those
READMEs directly. See [`docs/README.fafa`](docs/README.fafa).

## Entry shape (canonical)

See [`.fafipedia/schema.faf`](.fafipedia/schema.faf) for the schema. In short:

```yaml
- id: stable_unique_key
  type: Fact | Procedure | Index
  category: format | stack | architecture | agent | ecosystem | infrastructure | philosophy
  key: "the claim's subject"
  value: "the claim itself"   # or array / object
  eternal: true | false
  source: "where this came from (never invented)"
  # optional:
  aliases: ["query alias 1", "query alias 2"]
  registered: "2025-10"       # for IANA / standards entries
  measured: "2026-05-19"      # REQUIRED when eternal: false
  hardware: "iMac 2019, i5-7360U @ 2.30 GHz"   # for measurements
  generated: "build script name"   # for derived entries (e.g., faf_index)
```

## Drift signal

- `eternal: true` — won't change (IANA registrations, founding dates, vocabulary)
- `eternal: false` — time-bound; **MUST** include `measured:` OR `generated:`

The linter rejects `eternal: false` without one of those provenance fields.

## Citation discipline

`source:` is **required** and **never invented**. Acceptable shapes:

- A canonical repo path: `github.com/Wolfe-Jam/faf-cli (src/cli.ts registered commands)`
- A standards body: `IANA`
- A measurement context: `xai-faf-zeph benchmarks (zig build benchmark, 2026-05-11)`

If you can't cite it, you can't add it. See [`wolfejam-no-made-up-numbers-ai-can`](https://github.com/Wolfe-Jam/faf) doctrine: measure or drop.

## Validation

Before opening a PR:

```bash
./.fafipedia/validate.sh
```

CI runs the same check on every push and pull request. PRs that fail
validation are not merged.

## What lives where

- `fafipedia.fafi` — canonical curated entries (this is where authored
  facts live)
- `substrate.fafi` — generated from canonical READMEs by a build script;
  **do not edit by hand**
- `docs/README.fafa` — agent-targeted consumption guide

## Tier symbols

FAF uses `🏆` (Trophy) as the only emoji. Sub-Trophy tiers use geometric
Unicode (`★ ◆ ◇ ● ○ ♡`), not emoji medals. Reference: [tier system](https://github.com/Wolfe-Jam/faf).

## License

By contributing, you agree your contributions are licensed under the MIT
License (see [LICENSE](LICENSE)).
