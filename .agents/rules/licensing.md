# licensing — what may be licensed how

When to read: touching fixtures, downloaded data, images, licence files, the README, the UI
footer, or anything that mentions CCP.

## The boundary

- Application code is AGPL-3.0-or-later. That covers source files in `backend/` and
  `frontend/`, and nothing else.
- CCP material — static data exports, ESI response snapshots, image exports, logos, CCP Marks —
  is licensed to this project directly under the EVE Developer License Agreement and is **not**
  sublicensable. It must never be committed, bundled, or placed under AGPL.

## How that looks in practice

- Downloaded data goes to `data/`, which is git-ignored; the importer recreates it.
- Test fixtures containing real game payloads are generated at test time from the static data
  export, or recorded into a git-ignored directory.
- `LICENSE-CCP-DATA` states the boundary; it is not a formality and is not edited lightly.

## Obligations that outlive the code

- The proprietary notice and "created under the EVE Developer License Agreement" line stay in
  the UI footer (`legal.ccpNotice`, `legal.developerAgreement`).
- The application stays non-commercial: no paid access, no premium features. Donations and
  general advertising are permitted; selling the application is not.
- The product name must not imply CCP endorsement, and "EVE" is not part of the product name.
