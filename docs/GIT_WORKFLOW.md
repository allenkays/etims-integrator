# Git Workflow

Overview
- Branching model: `main` (protected), `develop` (integration), `feature/*`, `release/*`, `hotfix/*`.

Branch rules
- `feature/*`: create from `develop`. Short-lived; one feature per branch. Merge into `develop` via PR.
- `develop`: integration branch where completed features are merged. Not protected from CI failures.
- `release/*`: cut from `develop` when preparing a release. Use for final testing and bugfixes, then merge into `main` and `develop`.
- `hotfix/*`: create from `main` for urgent fixes; merge into both `main` and `develop`.

Pull Request workflow
- Open PRs from feature branches to `develop` (or from `release/*` to `main`).
- PR checklist: passing CI, descriptive title/body, link to issue (if any), at least one approval, and reviewed changes.
- Merge strategy: prefer **Squash and merge** for feature PRs to keep history concise; allow **Create a merge commit** for releases/hotfixes.

Commit messages
- Follow Conventional Commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- Example: `feat: add ETIMS client integration`.

Continuous Integration
- Run tests and linting on PRs and pushes to `develop`/`release/*`/`main`.
- Use GitHub Actions (see `.github/workflows/ci.yml`).

Releases and tagging
- Use semantic versioning. Tag releases on `main` with `vMAJOR.MINOR.PATCH`.
- Create release notes from PR descriptions and changelog entries.

Local workflow (quick)
1. Update local `develop`:
   - `git checkout develop && git pull origin develop`
2. Create feature branch:
   - `git checkout -b feature/my-change`
3. Work, stage, and commit (using Conventional Commits):
   - `git add . && git commit -m "feat: ..."`
4. Push and open PR:
   - `git push -u origin feature/my-change` then open a PR to `develop`.

Backports and hotfixes
- For urgent fixes apply to `hotfix/*` from `main`, test, then merge into `main` and `develop`.

This workflow balances simple feature development with clear release and patching steps.
