# Birren Industrial Colors

An unofficial software color system adapted from the scanned **Industrial Plants** color chart associated with Faber Birren. The palette keeps the chart's central idea intact: use a low-glare seafoam green as the long-duration work background, set white instrument panels against it for contrast, keep warm neutrals secondary, and reserve brilliant safety colors for state, hazard, and command signaling.

Landing page: <https://birren.vercel.app/>  
Repository: <https://github.com/r-cha/birren>

The source values live in [`source/birren-industrial.json`](source/birren-industrial.json). Everything in `dist/` and `applications/` is generated from that file by [`scripts/build.py`](scripts/build.py).

## Palette

Original chip values are 40×40 pixel averages sampled from the center of each printed chip in [`birren-industrial-colors.jpeg`](birren-industrial-colors.jpeg). `Instrument White` is a derived software role sampled from the chart paper; it is not one of the sixteen printed chips.

### Derived application role

| Color | Hex | Suggested software use |
| --- | --- | --- |
| Instrument White | `#F0F0EA` | Primary cards, panels, sidebars, forms, modals, and instrument-like UI surfaces on seafoam. |

### Original printed chips

| Color | Hex | Suggested software use |
| --- | --- | --- |
| Light Green | `#B6DAC0` | Fatigue-reducing light background for editors, dashboards, and reading panes. |
| Beige | `#DBD6C0` | Warm secondary notes, archival surfaces, annotations, and low-priority side material. |
| Light Blue | `#ADCED7` | Selections, info surfaces, calm hover states, and non-urgent emphasis. |
| Soft Yellow | `#FDF7B1` | Search hits, inline highlights, and teaching callouts. |
| Light Gray | `#BECECF` | Secondary backgrounds, dividers, disabled UI, and quiet structure. |
| Medium Gray | `#69867C` | Muted text, inactive UI, borders, minimap marks, and terminal bright black. |
| Deep Gray | `#4B6E5B` | Main text, title bars, terminal black, high-emphasis outlines, and deep structural accents. |
| Spotlight Buff | `#E6DEAE` | Warm highlights, headings, terminal normal white, and soft badges. |
| Medium Green | `#4E8C5A` | Routine positive states, strings, completion, and secondary brand accents. |
| Sandalwood | `#988454` | Types, tags, metadata, annotation, and low-priority caution. |
| Medium Blue | `#4F7B80` | Primary controls, functions, navigation, selected tabs, and focusable chrome. |
| Solar Yellow | `#EEC902` | Warnings, active search hits, focus rings, and required-field indicators. |
| Alert Orange | `#E15602` | Changed files, escalation states, destructive previews, and performance alerts. |
| Fire Red | `#7C0203` | Errors, failed jobs, delete affordances, security alerts, and diff deletions. |
| Safety Green | `#028339` | Success states, passing tests, diff additions, and high-confidence positive feedback. |
| Caution Blue | `#026289` | Links, command emphasis, important info, keywords, and actionable text. |

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
