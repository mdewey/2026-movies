# 2026 Programme

[![Pages](https://github.com/mdewey/2026-movies/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/mdewey/2026-movies/actions/workflows/pages/pages-build-deployment)

A single static page that lists the films from the 2026 Trello board, plus a
ranked, graded log of the ones you have watched. No server, no build step for
day-to-day use: the page reads its JSON data and commits changes back to this
repo through the GitHub API.

> Replace `OWNER` in the badge above with your GitHub username (two places), or
> run `sed -i 's|OWNER|<you>|g' README.md`.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole app. Plain HTML/CSS/JS, no dependencies. |
| `data/films.json` | The film list. Mostly generated; films you add on the site, and the *With partner* flag, are merged in and kept. |
| `data/watched.json` | Your ranking, grades and reasons. **Yours to edit.** |
| `.research/movies.json` | The source of truth `films.json` is built from. The page edits this one when you delete a film. |
| `.research/` | The scripts that built `films.json`. The Trello export lives here too but is gitignored — it holds the whole personal board, not just movies. |

## Setup

1. **Create a public repo and push this folder.** The repo is already
   initialised on `main` with everything staged, so:

   ```sh
   git commit -m "2026 programme"
   gh repo create 2026-movies --public --source=. --push
   ```

2. **Turn on Pages.** Repo → Settings → Pages → Source: *Deploy from a branch*,
   branch `main`, folder `/ (root)`. The site appears at
   `https://<you>.github.io/2026-movies/` within a minute or so.

3. **Make a token so the page can save.** On the site, open **Connect**:
   - [Create a fine-grained token](https://github.com/settings/personal-access-tokens/new)
   - Repository access → *Only select repositories* → this repo
   - Permissions → **Contents: Read and write**. Nothing else.
   - Paste it into the Connect panel.

   The token is kept in that browser's `localStorage`. Repeat once per device.
   Reading never needs a token — only saving does.

## Editing

Three ways:

- **On the site.** Grade dropdown, one-line reason, arrows to reorder, "Mark
  watched", a "With partner" checkbox and **Remove** on any film. Each change
  commits about a second later — `data/watched.json` for the log,
  `data/films.json` for the checkbox, and both plus `.research/movies.json` for
  a deletion. The chip in the corner shows *Saving… / Saved*.
- **On github.com.** Edit `data/watched.json` directly — works fine on a phone.
- **Locally.** Edit the file, commit, push.

Every save is a commit, so the file's history is your undo: `git log -p
data/watched.json`, or the History button on GitHub.

Commits say what actually changed. A single edit becomes the subject line —
`Grade Mother Mary A-`. Several edits caught by one save get a summary and a
bulleted body:

```text
Update watched list (3 changes)

- Grade Mother Mary A-
- Move Project Hail Mary to #1
- Note on Obsession
```

Each note is keyed by what it touched, so a burst of typing in a reason field
collapses to one line rather than forty.

### `watched.json` shape

```json
{
  "rank": 1,
  "title": "Mother Mary",
  "filmId": "mother-mary",
  "grade": "A-",
  "reason": "why, in one line"
}
```

- `rank` — 1 is liked most. The site renumbers to keep them contiguous.
- `grade` — `A`–`F`, optionally with `+` or `-`. `""` means ungraded.
- `filmId` — an `id` from `films.json`, linking the entry to a board film so it
  also shows as watched in the Programme. `null` for a film that was never on
  the board — or one you have since removed — which then supplies its own
  `director`, `release` and `url`.

### Watching together

Every film in `films.json` carries a `withPartner` boolean — the ones your
partner wants to watch with you:

```json
"withPartner": true
```

The **With partner** checkbox sets it, on the Programme and on any ranked entry
linked to the board. A **With partner** filter sits beside *Released* / *Coming
soon*, and the header counts them.

Two things follow from the flag living on the film rather than in
`watched.json`:

- a ranked entry with `"filmId": null` has no film record to hold the flag, so
  it gets no checkbox — off-board films are ones you have already seen anyway;
- `films.json` is generated, so `build_data.py` carries the flag across a
  rebuild by id. Ticking the box commits `films.json`, not `watched.json`.

## Regenerating `films.json`

`.research/movies.json` is the source of truth; `data/films.json` is built from
it. The build runs in CI, so you never need Python locally:

- **`.github/workflows/build-films.yml`** rebuilds and commits `films.json`
  whenever `.research/movies.json` or the build script changes on `main`, and
  from the Actions tab via **Run workflow**.
- Locally, if you want: `python .research/build_data.py`

The script preserves films you added through the site (`"addedHere": true`) and
the `withPartner` flag on every film, and fails loudly on a duplicate id or a
`watched.json` entry whose `filmId` no longer exists — so a bad hand-edit breaks
the build instead of the page.

### Why it does not loop

The site commits to `data/**` constantly, so the workflow deliberately does
*not* watch that path — it triggers only on `.research/**`. On top of that,
pushes made with `GITHUB_TOKEN` do not start further workflow runs, and the
commit step exits early when the rebuild produces no diff.

Deleting a film is the one time the page *does* write to `.research/`, and that
starts exactly one rebuild — which is the point, since it is what stops the film
coming back. The rebuild regenerates the same `films.json` the page has already
written, so the commit step finds no diff and exits. If the two overlap, the
workflow rebases onto whatever the site committed while it ran.

The workflow and the page write `films.json` identically (`indent=1`, trailing
newline, LF via `.gitattributes`), so a CI rebuild and a save from the page
never fight over whitespace.

## Adding a film

The **Programme** tab has an *Add a film to the programme* box at the bottom.
Title is the only required field; a release date sets the month heading and
decides *Released* vs *Coming soon*. The entry is appended to
`data/films.json`, sorted into release order, and committed — the same path
grades take.

Films added this way carry `"addedHere": true`, which tells `build_data.py` to
**carry them across a rebuild** instead of overwriting them. It also means they
were never in `.research/movies.json`, so removing one never touches that file.

## Removing a film

Every film has a **Remove** button now, researched or hand-added. Removing one:

- drops it from `data/films.json`, so it leaves the Programme immediately;
- drops it from `.research/movies.json` too, unless it was hand-added — this is
  what stops the next rebuild quietly restoring it;
- **keeps any ranked entry**, rewriting it into the off-board shape with its own
  `director`, `release` and `url`. Removing a film from the programme is not the
  same as un-watching it, and a dangling `filmId` would fail the build.

It is not reversible from the page: recover it with `git revert`, or add it back
through *Add a film to the programme*. A removed film's `withPartner` flag goes
with it, since that lives on the record being deleted.

## Deployment status on the page

The nav shows a dot next to the Connect tab: **Live**, **Deploying**,
**Queued**, or **Deploy failed**, linking to the run on GitHub. It reads the
latest `pages-build-deployment` run and compares its `head_sha` with the commit
the page just made — so *Live* means *your* change is served, not merely that
some build passed. After a save it polls until the build lands, then stops.

It hides itself when the repo cannot be determined (opening `index.html`
locally, say), rather than showing a status it cannot verify.

## The deployment badge

Pages deployed from a branch is built by an implicit workflow GitHub calls
`pages-build-deployment`. You never see the file, but it has a badge:

```text
https://github.com/<owner>/<repo>/actions/workflows/pages/pages-build-deployment/badge.svg
```

Notes:

- It reads **no status** until the first deploy runs, so it will look broken
  until Pages is switched on and the repo has been pushed once.
- Every save from the site is a commit, so it triggers a build — the badge
  flips to *in progress* for a few seconds each time you change a grade.
- If you ever switch Pages to *GitHub Actions* as the source, this path stops
  working; the badge then points at your own workflow file instead, e.g.
  `.../actions/workflows/deploy.yml/badge.svg`.
- The exact snippet is also available in the repo: **Actions** tab → the
  *pages-build-deployment* workflow → **···** → *Create status badge*.

## Things to know

- **Last writer wins.** Editing on two devices at once, the second save
  overwrites the first and the page says so. The overwritten version is still in
  the commit history.
- **The Pages copy lags a commit by up to a minute.** The site sidesteps this by
  reading `watched.json` and `films.json` through the GitHub API, which is
  immediate; the static files are only a fallback. Without that, a toggle read
  back a stale copy and the next save wrote it straight over the top.
- **A public repo means a public list.** Anyone with the URL can read your
  grades. Only writing is gated by the token.
