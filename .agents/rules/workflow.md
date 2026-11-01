# workflow — process

When to read: before starting any task and before opening a PR.

## Branches

- `main` — through PRs only: squash, linear history. The merge is performed by a human, never by an
  agent, a bot or a scheduled job. GitHub does not require an approving review: in a single-owner
  repository the author cannot approve their own pull request, so the approval counter would only
  be bypassed by an administrator merge. The human-only merge and a visible reviewer report are the
  replacement, not the counter.
- `feat/<slug>` — integration branch of a large feature; lives ≤ 1 week.
- `task/<feat>/<id>` — atomic subtasks; their PR targets `feat/*`, never `main`.

## Runners and untrusted code

- `ci` runs on GitHub-hosted runners and is the default pipeline.
- `self-hosted` runs on the ephemeral container runner attached to this repository: one container per
  job, no host mounts, dropped capabilities, removed on exit. It exists for jobs that need more
  machine than a hosted runner gives, not for speed.
- The self-hosted runner executes only the repository owner's work. Fork pull requests never reach
  it: the job condition rejects any head repository other than this one, and the repository setting
  requires approval for all external contributors.
- A pull request from a stranger is reviewed by a human first; after approval it runs on
  GitHub-hosted runners. Granting the self-hosted runner to an outside pull request is not a review
  decision, it is a security incident waiting to happen.

## Review before merge

- A pull request is opened with the reviewer's report attached: findings and, separately, the points
  that only a human can settle. A merge without that report is a merge nobody reviewed.
- The reviewer is advisory. It cannot block the merge on its own, and it cannot perform it.
- The human merging decides which findings are fixed now, which become cards, and which are
  rejected with a reason in the pull request.

## Task

1. One card = one subtask = one `files_allowed`.
2. Before code: `adr explain <path>` — which decisions govern the files you are about to touch.
3. Never touch files outside `files_allowed`; if the task needs more, escalate to the orchestrator.

## Gates (run by the orchestrator; the scripts live outside the repository)

```bash
CASCADE=~/.config/cascade/bin
STATE=~/.local/state/cascade/open-capsuleer-command-center/task.json
ALLOWED=$(python3 -c "import json;print(','.join(json.load(open('$STATE'))['files_allowed']))")

python3 $CASCADE/gate.py frozen-tests  --repo . --base origin/feat/<slug>
python3 $CASCADE/gate.py expect-fail   --repo . --cmd "make test-backend"
python3 $CASCADE/gate.py check-diff    --repo . --base origin/feat/<slug> --allowed "$ALLOWED"
python3 $CASCADE/gate.py expect-pass   --repo . --cmd "make test-backend"
```

`files_allowed` comes from the task state, not from a file in the repository.

## Review and disputes

- `review:agent` — pr-agent → fixes → merge into `feat/*` once green.
- `review:human` — the same plus a human approval and a filled-in PR description.
- Disagreement between pr-agent and the implementer → arbiter (writes no code) → unresolved → human.

## Limits

attempts per subtask: 4 · arbiter calls: 2 · phase: 45 min · budget: `~/.config/cascade/roles.yaml`

## Board

The board is a projection of GitHub, not a place where someone drags cards. Every move is derived
from a pull request by `tools/board/sync.py`, run by `.github/workflows/board.yml` on pull-request
events. No agent touches the board, and no one moves a card by hand.

- A pull request names **exactly one card at the start of its title**: `[#18] s0-t4: implant
  bonuses on top of base attributes`. GitHub appends `(#8)` to a squash title — that is the pull
  request number, never a card; the bracketed prefix is the only accepted form. The
  `PR title names a card` job fails any title without it.
- Derived state, recomputed from scratch on every event:

  | on GitHub | on the board |
  |---|---|
  | PR open | card in `Review` |
  | PR merged | card in `Done`, `done = true` |
  | PR closed without a merge | card back in `Plan` |
  | card flagged done but standing elsewhere | `Done` |
  | card in `Backlog`, all its `blocked` cards done | `Plan` — every unblocked card, highest `priority` first, then lowest id |
  | card carrying the `epic` label | left alone — a stage or a brief is a container, not work |

- The Plan queue is not capped (`max_plan: null` in `tools/board/policy.json`): everything that
  can be worked on stands in Plan. A number there would hold the surplus in `Backlog`.
- Two open PRs for one card is a finding, not a rule: the newest wins and the sync reports it. A PR
  that names a card that does not exist is reported the same way.
- The run is idempotent and silent: it re-reads the board after writing and fails if anything is
  still pending; with nothing to do it prints nothing and sends no notification.

## New rule

Seen twice → ADR (proposed) + edit the rules file + PR `chore(rules): …`.
