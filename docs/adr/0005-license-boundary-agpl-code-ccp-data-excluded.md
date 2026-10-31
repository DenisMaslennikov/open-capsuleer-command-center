---
schemaVersion: 0.2.0
id: "0005"
title: "License boundary: AGPL code, CCP data excluded"
status: accepted
date: 2026-10-31
deciders: ["@denis"]
tags: []
scope: component
reversibility: one-way-door
blastRadius: component
relatesTo: []
affects:
  - type: path
    pattern: "LICENSE"
  - type: path
    pattern: "LICENSE-CCP-DATA"
  - type: path
    pattern: ".agents/rules/licensing.md"
provenance:
  authoredBy: human
---

# ADR-0005: License boundary: AGPL code, CCP data excluded

## Context

The application uses CCP's material — ESI responses, the static data export, images and
trademarks — under the EVE Developer License Agreement. That agreement grants a limited,
non-exclusive, non-transferable licence for non-commercial use and says nothing about
publishing our own source. Two different copyrights are in play: ours, and CCP's.

The repository is public, so the question "what exactly does a reader get a licence to" has a
concrete answer or it is a defect.

## Decision

- Application code is AGPL-3.0-or-later. The network clause matches the shape of the product:
  it is a service, and a hosted fork must publish its source.
- CCP material is none of that licence. `LICENSE-CCP-DATA` states the boundary; nothing from
  CCP is committed. Static data is downloaded into the git-ignored `data/` directory, and test
  fixtures with real payloads are generated at test time or recorded outside the repository.
- The UI footer carries the proprietary notice and the line "created under the EVE Developer
  License Agreement".
- The application stays non-commercial: no paid access, no premium tiers. Donations and general
  advertising are allowed by the agreement; selling the application is not.
- `CONTRIBUTING.md` requires contributors to have signed the agreement, which they need anyway
  to run the application against ESI.

## Options considered

### Option A: AGPL-3.0 for the code, explicit boundary for the data (chosen)

**Pros:** a recognised free licence; the network clause protects against a closed hosted fork;
the data boundary is stated once, in one file.
**Cons:** AGPL keeps some corporate users away; the boundary must be explained, not assumed.

### Option B: MIT or Apache-2.0

**Pros:** maximum adoption, no copyleft questions.
**Cons:** a hosted fork can stay closed, which is the one thing the network clause prevents.

### Option C: no licence file

**Pros:** none.
**Cons:** without a licence nobody may legally copy or modify the code, so a public repository
would be readable and useless.

## Trade-offs

- AGPL plus a non-commercial obligation on the data side looks contradictory to a casual
  reader; the README and `LICENSE-CCP-DATA` have to explain that the non-commercial limit comes
  from CCP's terms and applies to the application, not to the licence of our code.
- CCP's agreement can change or terminate; the code survives, the integration would not.

## Consequences

- Easier: publishing, accepting contributions, being honest about game data.
- Harder: no re-licensing of the code; every new data source needs the same scrutiny.
- **How we would know this was wrong:** if CCP's terms changed to forbid open-source
  distribution, the code stays but the product would have to stop using ESI.
- Revisit if: the agreement is revised, or the project is offered commercially — the second
  case is not permitted at all under the current terms.

## Action items

1. [x] `LICENSE`, `LICENSE-CCP-DATA`, README licensing section, UI footer strings.
2. [ ] Re-read the agreement before the first public release.
