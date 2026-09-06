# 2026 Programme

A single static page that lists 43 films from the 2026 Trello board, plus a
ranked, graded log of the ones you have watched. No server, no build step for
day-to-day use: the page reads two JSON files and commits changes back to this
repo through the GitHub API.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The whole app. Plain HTML/CSS/JS, no dependencies. |
| `data/films.json` | The 43-film reference list. **Generated** — see below. |
| `data/watched.json` | Your ranking, grades and reasons. **Yours to edit.** |
| `.research/` | Scratch: the scripts that built `films.json`. The Trello export lives here too but is gitignored — it holds the whole personal board, not just movies. |

## Setup

1. **Create a public repo and push this folder.**

   ```sh
   git init -b main
   git add .
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

Only needed if the underlying film data changes:

```sh
python .research/build_data.py
```

It rebuilds `data/films.json` from `.research/movies.json` and fails loudly if
`watched.json` references a `filmId` that no longer exists.

## Things to know

- **Last writer wins.** Editing on two devices at once, the second save
  overwrites the first and the page says so. The overwritten version is still in
  the commit history.
- **The Pages copy lags a commit by up to a minute.** The site sidesteps this by
  reading `watched.json` through the GitHub API, which is immediate; the static
  file is only a fallback.
- **A public repo means a public list.** Anyone with the URL can read your
  grades. Only writing is gated by the token.
