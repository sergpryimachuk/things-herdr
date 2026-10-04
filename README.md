# Things for Herdr

A light and dark Herdr adaptation of [Obsidian Things](https://github.com/colineckert/obsidian-things), created by Colin Eckert. The palette comes from installed Things 2.2.4, with white or slate panels, quiet sidebar backgrounds, blue accents, and the original semantic colors.

![Palette illustration, not a screenshot](preview.svg)

## Install

Clone this repository:

```sh
git clone https://github.com/sergpryimachuk/things-herdr.git
cd things-herdr
```

Requires a Herdr version with `theme.custom.light` and `theme.custom.dark`. Verified with Herdr 0.9.3. Herdr reads these theme tables directly from its configuration, as described in the [official configuration guide](https://herdr.dev/docs/configuration/#theme).

### Manual installation

1. Back up your existing configuration, if present:

   ```sh
   mkdir -p "$HOME/.config/herdr"
   if [ -f "$HOME/.config/herdr/config.toml" ]; then
     cp "$HOME/.config/herdr/config.toml" "$HOME/.config/herdr/config.toml.things-backup-$(date +%Y%m%d-%H%M%S)"
   fi
   ```

2. Open `~/.config/herdr/config.toml`, creating it if needed. Replace its existing `[theme]` table and all `[theme.custom...]` tables with the tables from [`theme.toml`](theme.toml). Keep your other sections, including keybindings and terminal settings. Merge these theme tables into the configuration; copying over the entire configuration would discard those preferences. If `HERDR_CONFIG_PATH` points to a custom file, back up and edit that file instead.

3. Inside a Herdr pane, [reload the configuration](https://herdr.dev/docs/configuration/#reload-config) without restarting the server:

   ```sh
   herdr server reload-config
   ```

### Optional installer

This repository provides a convenience installer requiring Python 3.11 or newer. It is not provided by Herdr:

```sh
python3 install.py
```

It replaces the theme tables in `~/.config/herdr/config.toml`, preserves other configuration values and comments, and saves a timestamped backup before each change. `HERDR_CONFIG_PATH` is respected; `--config /path/to/config.toml` overrides the destination. Unsupported inline or dotted theme definitions cause a safe refusal before the file changes.

Reload with `herdr server reload-config` after installing, or use `python3 install.py --reload` inside Herdr for both steps. The combined command requires `HERDR_ENV=1` and never stops or restarts the session.

## Appearance

`theme.toml` overrides all 19 documented Herdr color tokens for both appearances. `auto_switch = true` follows the host terminal's light or dark appearance. Pair it with the Things Ghostty theme using Ghostty's light/dark theme selector. The fallback appearance is light, matching the macOS appearance when this adaptation was created.

The panel, sidebar, neutral surfaces, text, and semantic colors map to Things CSS base and color variables. The accent comes from Things HSL values: `215, 75%, 60%` in light mode and `215, 75%, 70%` for dark text accents. The navigate selection uses the interactive blue `215, 75%, 60%` at 25% over each editor background, matching the shared terminal selections. Herdr uses this composite for its sidebar navigation rows. Neutral active rows use Things hover and dark base-25 colors.

Herdr draws its own interface; applications in panes keep their own styles and explicit ANSI colors. Terminal fonts, syntax highlighting, rounded controls, Obsidian's typography, and spacing cannot be supplied by a Herdr color theme. The SVG illustrates the palette and is not an application screenshot.

## Agent CLI colors

Agent CLIs can select their own colors independently of the terminal theme. If Antigravity CLI `agy` displays pale text on a white Things Light background, open `/config`, choose Color Scheme, and select `terminal`. This lets agy use the Things ANSI palette in both appearances.

For future sessions, set only this value in `~/.gemini/antigravity-cli/settings.json`, keeping your other preferences:

```json
"colorScheme": "terminal"
```

Changing the file applies to new sessions. Use `/config` in a running session to apply the scheme immediately. Previously rendered scrollback can retain its old colors. See [Antigravity CLI display settings](https://antigravity.google/docs/settings?tab=cli#display-and-rendering).

## Rollback

Restore the timestamped backup created during manual installation or printed by the installer, then reload inside Herdr. Substitute your actual backup filename:

```sh
cp "$HOME/.config/herdr/config.toml.things-backup-YYYYMMDD-HHMMSS-microseconds" "$HOME/.config/herdr/config.toml"
herdr server reload-config
```

## Sources and license

- [Things source](https://github.com/colineckert/obsidian-things), version 2.2.4. `NOTICE` records the installed source file's SHA-256.
- [Herdr configuration guide](https://herdr.dev/docs/configuration/) explains native theme overrides and reloading.
- [Herdr configuration reference](https://herdr.dev/docs/config-reference/) and installed `herdr --default-config` define the supported settings.
- [Upstream MIT license](https://github.com/colineckert/obsidian-things/blob/main/LICENSE). `LICENSE` preserves its existing Stephan Ango notice. Colin Eckert is credited here and in `NOTICE` as Things' creator.

This repository is an independent adaptation.
