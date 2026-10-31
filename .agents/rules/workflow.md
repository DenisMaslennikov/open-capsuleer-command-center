# workflow — process

When to read: before starting any task and before opening a PR.

## Branches

- `main` — through PRs only: one human approval, squash, linear history.
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

## New rule

Seen twice → ADR (proposed) + edit the rules file + PR `chore(rules): …`.
