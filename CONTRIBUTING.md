# Contributing / Git workflow

## Branches

| Branch | Purpose | Who merges |
|--------|---------|-----------|
| `main` | Production state, deployed to centie.club. Protected: no direct pushes, only PRs. | Ops (Kim S.) after review |
| `dev` | Integration branch. All feature branches are merged here first. | any member via PR + review |
| `feature/<topic>` | One task = one branch (e.g. `feature/docker`, `feature/tests`). | - |
| `ops-infra` | Server configs (nginx, systemd, SSL). | Ops |

## Flow

1. Update `dev`: `git checkout dev && git pull origin dev`
2. Create a branch: `git checkout -b feature/<topic>`
3. Commit small, meaningful changes with clear messages (`Add Dockerfile and compose stack`).
4. Push: `git push -u origin feature/<topic>`
5. Open a Pull Request **into `dev`** on GitHub, fill the template, request review from the other member.
6. CI (GitHub Actions) must be green: Django checks, tests, Docker build.
7. Reviewer approves -> "Squash and merge" (or "Merge").
8. Release: PR `dev -> main`, merge, then on the server: `git pull origin main`, restart `cityhall.service`.

## Commit messages

`<verb> <what>`: `Add`, `Fix`, `Update`, `Remove`. English, imperative, under 72 characters.

## Rules

- Never commit `.env`, passwords, tokens.
- Never push directly to `main`.
- One PR = one task; keep diffs reviewable.
