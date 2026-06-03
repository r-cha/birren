# Birren Industrial Colors

An unofficial software color system adapted from the scanned **Industrial Plants** color chart associated with Faber Birren. The palette keeps the chart's central idea intact: use a low-glare seafoam green as the long-duration work background, set white instrument panels against it for contrast, keep warm neutrals secondary, and reserve brilliant safety colors for state, hazard, and command signaling.

Landing page: <https://birren.vercel.app/>  
Repository: <https://github.com/r-cha/birren>

The source values live in [`source/birren-industrial.json`](source/birren-industrial.json). Everything in `dist/` and `applications/` is generated from that file by [`scripts/build.py`](scripts/build.py).

## Palette

The values below are the shipped software values. They begin as 40×40 pixel averages sampled from the center of each printed chip in [`birren-industrial-colors.jpeg`](birren-industrial-colors.jpeg), but a few are tuned for screens rather than used raw — see [Screen tuning](#screen-tuning). `Instrument White` is a derived software role sampled from the chart paper; it is not one of the sixteen printed chips.

### Derived application roles

These are software-only roles, not printed chips. `Instrument White` is sampled from the chart paper; `Mid Neutral` and `Muted Text` are tuned in OKLab to even out the neutral lightness ramp and to keep low-emphasis text legible against the seafoam field (where the original muted gray fell below readable contrast).

| Color | Hex | Suggested software use |
| --- | --- | --- |
| Instrument White | `#F0F0EA` | Primary cards, panels, sidebars, forms, modals, and instrument-like UI surfaces on seafoam. |
| Mid Neutral | `#8FA89E` | Subtle dividers, disabled fills, and quiet structure between the light interiors and the working grays. |
| Muted Text | `#52736A` | Comments, captions, line numbers, descriptions, and secondary text that must stay legible on the field. |

### Printed chips (sampled, with screen tuning where noted)

| Color | Hex | Suggested software use |
| --- | --- | --- |
| Light Green | `#B6DAC0` | Fatigue-reducing light background for editors, dashboards, and reading panes. |
| Beige | `#DBD6C0` | Warm secondary notes, archival surfaces, annotations, and low-priority side material. |
| Light Blue | `#ADCED7` | Selections, info surfaces, calm hover states, and non-urgent emphasis. |
| Soft Yellow | `#FDF7B1` | Search hits, inline highlights, and teaching callouts. |
| Light Gray | `#BECECF` | Secondary backgrounds, dividers, disabled UI, and quiet structure. |
| Medium Gray | `#5F7B71` | Borders, dividers, inactive UI, minimap marks, and terminal bright black (tuned to clear 3:1 on the field). |
| Deep Gray | `#3F614F` | Main text, title bars, terminal black, high-emphasis outlines, and deep structural accents (tuned to AA body text on the field). |
| Spotlight Buff | `#E6DEAE` | Warm highlights, headings, terminal normal white, and soft badges. |
| Medium Green | `#4E8C5A` | Routine positive states, strings, completion, and secondary brand accents. |
| Sandalwood | `#988454` | Types, tags, metadata, annotation, and low-priority caution. |
| Medium Blue | `#4F7B80` | Primary controls, functions, navigation, selected tabs, and focusable chrome. |
| Solar Yellow | `#EEC902` | Warnings, active search hits, focus rings, and required-field indicators. |
| Alert Orange | `#E15602` | Changed files, escalation states, destructive previews, and performance alerts. |
| Fire Red | `#7C0203` | Errors, failed jobs, delete affordances, security alerts, and diff deletions. |
| Safety Green | `#007839` | Success states, passing tests, diff additions, and high-confidence positive feedback (shifted darker and cooler so it reads distinctly from the routine Medium Green). |
| Caution Blue | `#026289` | Links, command emphasis, important info, keywords, and actionable text. |

## Screen tuning

The chart was designed for pigment on physical surfaces, not emissive displays, and predates modern legibility models (WCAG, APCA). A handful of chips were nudged in the perceptually uniform OKLab space — holding each color's hue so its character is preserved — to meet contrast standards on screen and to even out the neutral ramp. The seafoam field, white panels, subdued machine colors, and brilliant safety signals are otherwise unchanged.

| Color | Before | After | Why |
| --- | --- | --- | --- |
| Deep Gray (body text) | `#4B6E5B` | `#3F614F` | Body text was 3.74:1 on the seafoam field (below AA). Darkened to **4.5:1 AA** while keeping the green-charcoal character. |
| Medium Gray (border) | `#69867C` | `#5F7B71` | Borders/dividers were 2.6:1. Darkened to clear **3:1** non-text contrast. |
| Safety Green (success) | `#028339` | `#007839` | Was nearly identical to the routine Medium Green (same hue, ~0.05 lightness apart). Shifted darker and slightly cooler so success reads as a distinct signal. |
| Muted Text *(new)* | — | `#52736A` | The old muted gray was used for comments at 2.6:1. A dedicated, darker low-emphasis value keeps secondary text legible without competing with body text. |
| Mid Neutral *(new)* | — | `#8FA89E` | The neutral ramp jumped from light interiors straight to the working grays; this fills the perceptual gap for subtle dividers and disabled states. |

## Formats

- CSS custom properties: [`dist/birren-industrial.css`](dist/birren-industrial.css)
- SCSS variables/maps: [`dist/_birren-industrial.scss`](dist/_birren-industrial.scss)
- Less variables: [`dist/birren-industrial.less`](dist/birren-industrial.less)
- JSON: [`dist/birren-industrial.json`](dist/birren-industrial.json)
- YAML: [`dist/birren-industrial.yaml`](dist/birren-industrial.yaml)
- CommonJS / Tailwind-friendly export: [`dist/birren-industrial.js`](dist/birren-industrial.js)
- Ghostty themes: [`applications/ghostty`](applications/ghostty)
- Visual Studio Code themes: [`applications/vscode`](applications/vscode)
- Neovim colorscheme: [`applications/neovim/colors/birren-industrial.lua`](applications/neovim/colors/birren-industrial.lua)
- shadcn/ui theme: [`applications/shadcn`](applications/shadcn)
- Extra terminal ports: Alacritty, Kitty, and WezTerm in [`applications/`](applications)

## Install snippets

### Ghostty

Copy one of the generated theme files into Ghostty's theme directory, then set it in your config:

```sh
mkdir -p ~/.config/ghostty/themes
cp "applications/ghostty/Birren Industrial Light" ~/.config/ghostty/themes/
```

```ini
theme = Birren Industrial Light
```

### Visual Studio Code

Copy the generated extension folder into your local VS Code extensions directory and reload VS Code:

```sh
mkdir -p ~/.vscode/extensions/birren-industrial-colors
cp -R applications/vscode/* ~/.vscode/extensions/birren-industrial-colors/
```

Then choose **Birren Industrial Light** from the Color Theme picker.

### shadcn/ui

Drop the generated CSS into your app's global stylesheet (the file that already
defines your `:root` shadcn variables), or import it directly:

```css
@import "./birren-industrial.css";
```

For Tailwind v4 (`@theme inline` with raw hex values) use
[`applications/shadcn/birren-industrial-hex.css`](applications/shadcn/birren-industrial-hex.css)
instead. A
[`registry.json`](applications/shadcn/registry.json) is also generated for use
with the shadcn CLI.

### Neovim

```sh
mkdir -p ~/.config/nvim/colors
cp applications/neovim/colors/birren-industrial.lua ~/.config/nvim/colors/
```

```vim
set background=light
colorscheme birren-industrial
```

## Rebuild

After editing [`source/birren-industrial.json`](source/birren-industrial.json):

```sh
python3 scripts/build.py
```

Open [`index.html`](index.html) locally for the landing page, or deploy it at <https://birren.vercel.app/>.

## Note

This is an independent historical adaptation for software interfaces, not an official product from Faber Birren's estate or any rights holder.
