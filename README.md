# The Design Wire

A weekday design news board for working product designers. Every story carries two
reads: **Teach** (what a mid-level designer can act on Monday morning) and **Signal**
(the second-order observation for a senior reader).

Live at <https://wire.melissajade.design>

## How it works

`index.html` is the whole site. One self-contained file: markup, CSS and script.
No build step, no dependencies, no framework.

Editions are stored newest-first inside `<div id="editions">`. The archive rail,
the beat counts and the filter chip counts are all derived from the DOM at runtime,
so nothing needs to be updated by hand when an edition is added.

## Adding an edition

Editions are added by script, never by hand-editing `index.html`:

```bash
python3 add_edition.py editions/2026-08-26.json
```

The script only ever inserts. It prepends the new `<article class="edition">`,
adds the matching rail entry, and moves `aria-current="true"` onto the new button.

It refuses to write anything if:

* the edition date is already on the page
* the edition count does not go up by exactly one
* the rail ends up with anything other than one current button
* the rail entries and the editions fall out of sync

Every past edition is in git history, so a bad run can always be reverted with
`git revert`. This is the whole reason the board lives here rather than anywhere
that keeps only the latest copy.

## Edition data format

See `editions/2026-08-26.json`. Per story: `pub`, `date`, `url`, `hed`, `fact`,
`why`, `hook`, `teach`, `signal`, and an optional `flag` badge (used sparingly for
a top story or for "Reported, not confirmed").

## Editorial rules

* Major tech journals and established publications only. No Substack, no Medium
  contributors, no personal blogs, no SEO content farms, no aggregators.
* Stories from the last 10 to 14 days, preferring the last 5.
* Every URL verified by fetching the live page. Headline, publication, date and
  figures come from the page body, never from a search snippet or a URL slug.
* Anything anecdotal, company-reported or from an unnamed source carries that
  caveat on the card.
* 5 to 7 stories per beat. A thin beat runs short rather than padded.

## Design

Palette and type from melissajade.design.

| Token | Value |
| --- | --- |
| paper | `#FBF5F3` |
| panel | `#EBE5DF` |
| ink | `#212121` |
| rust | `#C53F1F` |
| navy | `#122E8D` |

Display face is Hedvig Letters Serif, UI and body is Archivo, both from Google Fonts.

## Note on "Create draft"

The **Create draft** buttons file a story into Notion through the Claude artifact
runtime (`window.claude`). That runtime only exists inside a published Claude
artifact, so on this static site the buttons stay inert by design. The board is
also published as an artifact, which is where that workflow lives.
