# 2026 Programme

[![Pages](https://github.com/mdewey/2026-movies/actions/workflows/pages/pages-build-deployment/badge.svg)](https://github.com/mdewey/2026-movies/actions/workflows/pages/pages-build-deployment)

A single static page that lists 43 films from the 2026 Trello board, plus a
ranked, graded log of the ones you have watched. No server, no build step for
day-to-day use: the page reads two JSON files and commits changes back to this
repo through the GitHub API.

> Replace `OWNER` in the badge above with your GitHub username (two places), or
> run `sed -i 's|OWNER|<you>|g' README.md`.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole app. Plain HTML/CSS/JS, no dependencies. |
| `data/films.json` | The film list. Mostly generated; films you add on the site are merged in and kept. |
| `data/watched.json` | Your ranking, grades and reasons. **Yours to edit.** |
| `.research/` | Scratch: the scripts that built `films.json`. The Trello export lives here too but is gitignored — it holds the whole personal board, not just movies. |

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

Three ways, all writing the same file:

- **On the site.** Grade dropdown, one-line reason, arrows to reorder, "Mark
  watched" on any film. Each change commits `data/watched.json` about a second
  later. The chip in the corner shows *Saving… / Saved*.
- **On github.com.** Edit `data/watched.json` directly — works fine on a phone.
- **Locally.** Edit the file, commit, push.

Every save is a commit, so the file's history is your undo: `git log -p
data/watched.json`, or the History button on GitHub.

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
  the board, which then supplies its own `director`, `release` and `url`.

## Regenerating `films.json`

`.research/movies.json` is the source of truth; `data/films.json` is built from
it. The build runs in CI, so you never need Python locally:

- **`.github/workflows/build-films.yml`** rebuilds and commits `films.json`
  whenever `.research/movies.json` or the build script changes on `main`, and
  from the Actions tab via **Run workflow**.
- Locally, if you want: `python .research/build_data.py`

The script preserves films you added through the site (`"addedHere": true`) and
fails loudly on a duplicate id or a `watched.json` entry whose `filmId` no
longer exists — so a bad hand-edit breaks the build instead of the page.

### Why it does not loop

The site commits to `data/**` constantly, so the workflow deliberately does
*not* watch that path — it triggers only on `.research/**`. On top of that,
pushes made with `GITHUB_TOKEN` do not start further workflow runs, and the
commit step exits early when the rebuild produces no diff.

The workflow and the page write `films.json` identically (`indent=1`, trailing
newline, LF via `.gitattributes`), so a CI rebuild and a save from the page
never fight over whitespace.

## Adding a film

The **Programme** tab has an *Add a film to the programme* box at the bottom.
Title is the only required field; a release date sets the month heading and
decides *Released* vs *Coming soon*. The entry is appended to
`data/films.json`, sorted into release order, and committed — the same path
grades take.

Films added this way carry `"addedHere": true`. That flag does two jobs:

- they get a **Remove** button on the page (the researched 43 do not, since a
  rebuild would just bring them back);
- `build_data.py` **carries them across a rebuild** instead of overwriting them.

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
  reading `watched.json` through the GitHub API, which is immediate; the static
  file is only a fallback.
- **A public repo means a public list.** Anyone with the URL can read your
  grades. Only writing is gated by the token.
