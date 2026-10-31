# Contributing

## Before your first pull request

The EVE Developer License Agreement requires that an application is created by parties who
have signed it. Sign it at <https://developers.eveonline.com/license-agreement> — you need it
anyway to run this application against ESI — and state in your pull request that you have.

By contributing you agree that your contribution is licensed under AGPL-3.0-or-later, and that
you will not commit CCP game data (static data exports, ESI payload snapshots, images, logos).

## Flow

1. One change = one subtask = one `files_allowed` set.
2. Branch from `feat/<slug>` as `task/<feat>/<id>`; the pull request targets `feat/*`.
3. Tests first, then code; tests are frozen during the code phase.
4. `make lint` and `make test` must be green before review.
5. Merges into `feat/*` happen after review; `feat/*` into `main` is a human decision.

## Rules

Read `AGENTS.md` and the rule file for the zone you are touching. A new convention is added as
an ADR plus an edit to the matching rule file, in its own pull request.
