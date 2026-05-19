#!/usr/bin/env python3
"""Build importable Birren Industrial Colors formats from the JSON source."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "source" / "birren-industrial.json"
GENERATED = "Generated from source/birren-industrial.json by scripts/build.py. Do not edit by hand."
ANSI_ORDER = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]
LUA_RESERVED = {
    "and",
    "break",
    "do",
    "else",
    "elseif",
    "end",
    "false",
    "for",
    "function",
    "goto",
    "if",
    "in",
    "local",
    "nil",
    "not",
    "or",
    "repeat",
    "return",
    "then",
    "true",
    "until",
    "while",
}


def load_palette() -> dict[str, Any]:
    return json.loads(SOURCE_PATH.read_text())


def write(path: str, contents: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(contents.rstrip() + "\n")


def color_hex(palette: dict[str, Any], color_id: str) -> str:
    return palette["colors"][color_id]["hex"]


def js_key(name: str) -> str:
    return name.replace("-", "_")


def lua_key(name: str) -> str:
    candidate = js_key(name)
    if candidate.isidentifier() and candidate not in LUA_RESERVED:
        return candidate
    return f"[{json.dumps(candidate)}]"


def resolve_id_map(palette: dict[str, Any], source: dict[str, str]) -> dict[str, str]:
    return {key: color_hex(palette, value) for key, value in source.items()}


def resolved_roles(palette: dict[str, Any]) -> dict[str, str]:
    return resolve_id_map(palette, palette["roles"])


def resolved_syntax(palette: dict[str, Any]) -> dict[str, str]:
    return resolve_id_map(palette, palette["syntax"])


def resolved_ansi(palette: dict[str, Any]) -> dict[str, dict[str, str]]:
    return {
        group: {name: color_hex(palette, color_id) for name, color_id in colors.items()}
        for group, colors in palette["ansi"].items()
    }


def alpha(hex_color: str, value: str) -> str:
    return f"{hex_color}{value}"


def yaml_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    return json.dumps(str(value))


def to_yaml(value: Any, indent: int = 0) -> str:
    space = " " * indent
    if isinstance(value, dict):
        lines: list[str] = []
        for key, child in value.items():
            if isinstance(child, (dict, list)):
                lines.append(f"{space}{key}:")
                lines.append(to_yaml(child, indent + 2))
            else:
                lines.append(f"{space}{key}: {yaml_scalar(child)}")
        return "\n".join(lines)
    if isinstance(value, list):
        lines = []
        for child in value:
            if isinstance(child, (dict, list)):
                lines.append(f"{space}-")
                lines.append(to_yaml(child, indent + 2))
            else:
                lines.append(f"{space}- {yaml_scalar(child)}")
        return "\n".join(lines)
    return f"{space}{yaml_scalar(value)}"


def primitive_colors(palette: dict[str, Any]) -> dict[str, str]:
    return {color_id: details["hex"] for color_id, details in palette["colors"].items()}


def app_payload(palette: dict[str, Any]) -> dict[str, Any]:
    payload = {
        "name": palette["name"],
        "slug": palette["slug"],
        "version": palette["version"],
        "description": palette["description"],
        "colors": primitive_colors(palette),
        "roles": resolved_roles(palette),
        "syntax": resolved_syntax(palette),
        "ansi": resolved_ansi(palette),
    }
    if "links" in palette:
        payload["links"] = palette["links"]
    return payload


def build_json_and_yaml(palette: dict[str, Any]) -> None:
    payload = app_payload(palette)
    write("dist/birren-industrial.json", json.dumps(payload, indent=2))
    write("dist/birren-industrial.yaml", f"# {GENERATED}\n" + to_yaml(payload))


def build_css(palette: dict[str, Any]) -> None:
    lines = [
        f"/* {GENERATED} */",
        "",
        ":root,",
        ".birren-industrial,",
        ".birren-industrial-light,",
        "[data-palette='birren-industrial'],",
        "[data-palette='birren-industrial-light'] {",
    ]
    for color_id, value in primitive_colors(palette).items():
        lines.append(f"  --birren-{color_id}: {value};")
    lines.append("")
    for role, color_id in palette["roles"].items():
        lines.append(f"  --birren-{role}: var(--birren-{color_id});")
    lines.append("}")
    write("dist/birren-industrial.css", "\n".join(lines))


def build_scss(palette: dict[str, Any]) -> None:
    lines = [f"// {GENERATED}", ""]
    for color_id, value in primitive_colors(palette).items():
        lines.append(f"$birren-{color_id}: {value};")
    lines.append("")
    lines.append("$birren-colors: (")
    for color_id, value in primitive_colors(palette).items():
        lines.append(f"  \"{color_id}\": {value},")
    lines.append(");")
    lines.append("")
    lines.append("$birren-roles: (")
    for role, color_id in palette["roles"].items():
        lines.append(f"  \"{role}\": $birren-{color_id},")
    lines.append(");")
    write("dist/_birren-industrial.scss", "\n".join(lines))


def build_less(palette: dict[str, Any]) -> None:
    lines = [f"// {GENERATED}", ""]
    for color_id, value in primitive_colors(palette).items():
        lines.append(f"@birren-{color_id}: {value};")
    lines.append("")
    for role, color_id in palette["roles"].items():
        lines.append(f"@birren-{role}: @birren-{color_id};")
    write("dist/birren-industrial.less", "\n".join(lines))


def build_js(palette: dict[str, Any]) -> None:
    payload = app_payload(palette)
    contents = f"// {GENERATED}\n\nconst birrenIndustrial = {json.dumps(payload, indent=2)};\n\nmodule.exports = birrenIndustrial;"
    write("dist/birren-industrial.js", contents)


def terminal_scheme(palette: dict[str, Any]) -> dict[str, Any]:
    roles = resolved_roles(palette)
    ansi = resolved_ansi(palette)
    return {
        "roles": roles,
        "normal": [ansi["normal"][name] for name in ANSI_ORDER],
        "bright": [ansi["bright"][name] for name in ANSI_ORDER],
    }


def build_ghostty(palette: dict[str, Any]) -> None:
    scheme = terminal_scheme(palette)
    roles = scheme["roles"]
    lines = [f"# {GENERATED}", "# Birren Industrial Light", ""]
    lines.extend(
        [
            f"background = {roles['background']}",
            f"foreground = {roles['text']}",
            f"cursor-color = {roles['accent']}",
            f"cursor-text = {roles['background']}",
            f"selection-background = {roles['selection']}",
            f"selection-foreground = {roles['text']}",
            "",
        ]
    )
    for index, value in enumerate(scheme["normal"] + scheme["bright"]):
        lines.append(f"palette = {index}={value}")
    write("applications/ghostty/Birren Industrial Light", "\n".join(lines))


def build_kitty(palette: dict[str, Any]) -> None:
    scheme = terminal_scheme(palette)
    roles = scheme["roles"]
    lines = [f"# {GENERATED}", "# Birren Industrial Light", ""]
    lines.extend(
        [
            f"foreground {roles['text']}",
            f"background {roles['background']}",
            f"cursor {roles['accent']}",
            f"cursor_text_color {roles['background']}",
            f"selection_foreground {roles['text']}",
            f"selection_background {roles['selection']}",
            "",
        ]
    )
    for index, value in enumerate(scheme["normal"] + scheme["bright"]):
        lines.append(f"color{index} {value}")
    write("applications/kitty/birren-industrial-light.conf", "\n".join(lines))


def build_alacritty(palette: dict[str, Any]) -> None:
    scheme = terminal_scheme(palette)
    roles = scheme["roles"]
    normal = dict(zip(ANSI_ORDER, scheme["normal"], strict=True))
    bright = dict(zip(ANSI_ORDER, scheme["bright"], strict=True))
    lines = [f"# {GENERATED}", "# Birren Industrial Light", ""]
    lines.extend(
        [
            "[colors.primary]",
            f"background = \"{roles['background']}\"",
            f"foreground = \"{roles['text']}\"",
            "",
            "[colors.cursor]",
            f"text = \"{roles['background']}\"",
            f"cursor = \"{roles['accent']}\"",
            "",
            "[colors.selection]",
            f"text = \"{roles['text']}\"",
            f"background = \"{roles['selection']}\"",
            "",
            "[colors.normal]",
        ]
    )
    for name in ANSI_ORDER:
        lines.append(f"{name} = \"{normal[name]}\"")
    lines.append("")
    lines.append("[colors.bright]")
    for name in ANSI_ORDER:
        lines.append(f"{name} = \"{bright[name]}\"")
    write("applications/alacritty/birren-industrial-light.toml", "\n".join(lines))


def build_wezterm(palette: dict[str, Any]) -> None:
    lines = [f"-- {GENERATED}", "", "return {"]
    scheme = terminal_scheme(palette)
    roles = scheme["roles"]
    lines.append("  [\"Birren Industrial Light\"] = {")
    lines.append(f"    foreground = \"{roles['text']}\",")
    lines.append(f"    background = \"{roles['background']}\",")
    lines.append(f"    cursor_bg = \"{roles['accent']}\",")
    lines.append(f"    cursor_fg = \"{roles['background']}\",")
    lines.append(f"    selection_fg = \"{roles['text']}\",")
    lines.append(f"    selection_bg = \"{roles['selection']}\",")
    lines.append("    ansi = {")
    for value in scheme["normal"]:
        lines.append(f"      \"{value}\",")
    lines.append("    },")
    lines.append("    brights = {")
    for value in scheme["bright"]:
        lines.append(f"      \"{value}\",")
    lines.append("    },")
    lines.append("  },")
    lines.append("}")
    write("applications/wezterm/birren-industrial.lua", "\n".join(lines))


def vscode_token_colors(syntax: dict[str, str]) -> list[dict[str, Any]]:
    return [
        {"scope": ["comment", "punctuation.definition.comment"], "settings": {"foreground": syntax["comment"], "fontStyle": "italic"}},
        {"scope": ["string", "constant.other.symbol"], "settings": {"foreground": syntax["string"]}},
        {"scope": ["constant.numeric", "constant.language.boolean"], "settings": {"foreground": syntax["number"]}},
        {"scope": ["keyword", "storage", "storage.type"], "settings": {"foreground": syntax["keyword"], "fontStyle": "bold"}},
        {"scope": ["entity.name.function", "support.function"], "settings": {"foreground": syntax["function"]}},
        {"scope": ["entity.name.type", "support.type", "support.class"], "settings": {"foreground": syntax["type"]}},
        {"scope": ["variable", "meta.object-literal.key"], "settings": {"foreground": syntax["variable"]}},
        {"scope": ["constant", "entity.name.constant"], "settings": {"foreground": syntax["constant"]}},
        {"scope": ["keyword.operator", "punctuation.separator", "punctuation.terminator"], "settings": {"foreground": syntax["operator"]}},
        {"scope": ["punctuation", "meta.brace"], "settings": {"foreground": syntax["punctuation"]}},
    ]


def vscode_workbench_colors(palette: dict[str, Any]) -> dict[str, str]:
    roles = resolved_roles(palette)
    ansi = resolved_ansi(palette)
    chrome_bg = color_hex(palette, "deep-gray")
    chrome_fg = color_hex(palette, "spotlight-buff")
    button_fg = color_hex(palette, "spotlight-buff")
    return {
        "focusBorder": roles["focus"],
        "foreground": roles["text"],
        "descriptionForeground": roles["text-muted"],
        "errorForeground": roles["danger"],
        "selection.background": alpha(roles["selection"], "88"),
        "textLink.foreground": roles["link"],
        "textLink.activeForeground": roles["attention"],
        "button.background": roles["primary"],
        "button.foreground": button_fg,
        "button.hoverBackground": roles["accent"],
        "input.background": roles["surface"],
        "input.foreground": roles["text"],
        "input.border": roles["border"],
        "dropdown.background": roles["surface"],
        "dropdown.foreground": roles["text"],
        "dropdown.border": roles["border"],
        "badge.background": roles["attention"],
        "badge.foreground": color_hex(palette, "spotlight-buff"),
        "activityBar.background": chrome_bg,
        "activityBar.foreground": chrome_fg,
        "activityBar.inactiveForeground": alpha(chrome_fg, "AA"),
        "activityBarBadge.background": roles["warning"],
        "activityBarBadge.foreground": color_hex(palette, "deep-gray"),
        "sideBar.background": roles["surface"],
        "sideBar.foreground": roles["text"],
        "sideBar.border": roles["border"],
        "sideBarTitle.foreground": roles["text"],
        "list.activeSelectionBackground": alpha(roles["selection"], "AA"),
        "list.activeSelectionForeground": roles["text"],
        "list.hoverBackground": alpha(roles["surface-raised"], "AA"),
        "list.inactiveSelectionBackground": alpha(roles["selection"], "66"),
        "titleBar.activeBackground": chrome_bg,
        "titleBar.activeForeground": chrome_fg,
        "titleBar.inactiveBackground": alpha(chrome_bg, "DD"),
        "titleBar.inactiveForeground": alpha(chrome_fg, "AA"),
        "statusBar.background": chrome_bg,
        "statusBar.foreground": chrome_fg,
        "statusBar.noFolderBackground": roles["primary"],
        "statusBar.debuggingBackground": roles["attention"],
        "panel.background": roles["surface"],
        "panel.border": roles["border"],
        "tab.activeBackground": roles["background"],
        "tab.activeForeground": roles["text"],
        "tab.inactiveBackground": roles["surface"],
        "tab.inactiveForeground": roles["text-muted"],
        "editor.background": roles["background"],
        "editor.foreground": roles["text"],
        "editorLineNumber.foreground": roles["text-muted"],
        "editorLineNumber.activeForeground": roles["text"],
        "editorCursor.foreground": roles["accent"],
        "editor.selectionBackground": alpha(roles["selection"], "AA"),
        "editor.inactiveSelectionBackground": alpha(roles["selection"], "66"),
        "editor.lineHighlightBackground": alpha(roles["surface-raised"], "66"),
        "editor.findMatchBackground": alpha(roles["highlight"], "CC"),
        "editor.findMatchHighlightBackground": alpha(roles["highlight"], "77"),
        "editor.wordHighlightBackground": alpha(roles["selection"], "55"),
        "editorWhitespace.foreground": alpha(roles["text-muted"], "88"),
        "editorIndentGuide.background1": alpha(roles["border"], "66"),
        "editorIndentGuide.activeBackground1": roles["accent"],
        "editorGutter.background": roles["background"],
        "editorBracketMatch.background": alpha(roles["highlight"], "66"),
        "editorBracketMatch.border": roles["focus"],
        "gitDecoration.addedResourceForeground": roles["success"],
        "gitDecoration.modifiedResourceForeground": roles["attention"],
        "gitDecoration.deletedResourceForeground": color_hex(palette, "fire-red"),
        "diffEditor.insertedTextBackground": alpha(roles["success"], "33"),
        "diffEditor.removedTextBackground": alpha(color_hex(palette, "fire-red"), "33"),
        "terminal.background": roles["background"],
        "terminal.foreground": roles["text"],
        "terminal.ansiBlack": ansi["normal"]["black"],
        "terminal.ansiRed": ansi["normal"]["red"],
        "terminal.ansiGreen": ansi["normal"]["green"],
        "terminal.ansiYellow": ansi["normal"]["yellow"],
        "terminal.ansiBlue": ansi["normal"]["blue"],
        "terminal.ansiMagenta": ansi["normal"]["magenta"],
        "terminal.ansiCyan": ansi["normal"]["cyan"],
        "terminal.ansiWhite": ansi["normal"]["white"],
        "terminal.ansiBrightBlack": ansi["bright"]["black"],
        "terminal.ansiBrightRed": ansi["bright"]["red"],
        "terminal.ansiBrightGreen": ansi["bright"]["green"],
        "terminal.ansiBrightYellow": ansi["bright"]["yellow"],
        "terminal.ansiBrightBlue": ansi["bright"]["blue"],
        "terminal.ansiBrightMagenta": ansi["bright"]["magenta"],
        "terminal.ansiBrightCyan": ansi["bright"]["cyan"],
        "terminal.ansiBrightWhite": ansi["bright"]["white"],
    }


def build_vscode(palette: dict[str, Any]) -> None:
    links = palette.get("links", {})
    package = {
        "name": "birren-industrial-colors",
        "displayName": "Birren Industrial Colors",
        "description": palette["description"],
        "version": palette["version"],
        "publisher": "birren-industrial-colors",
        "engines": {"vscode": "^1.85.0"},
        "categories": ["Themes"],
        "contributes": {
            "themes": [
                {"label": "Birren Industrial Light", "uiTheme": "vs", "path": "./themes/birren-industrial-light-color-theme.json"},
            ]
        },
    }
    if links.get("homepage"):
        package["homepage"] = links["homepage"]
    if links.get("repository"):
        package["repository"] = {"type": "git", "url": f"{links['repository']}.git"}
    if links.get("issues"):
        package["bugs"] = {"url": links["issues"]}
    write("applications/vscode/package.json", json.dumps(package, indent=2))

    theme = {
        "name": "Birren Industrial Light",
        "type": "light",
        "semanticHighlighting": True,
        "colors": vscode_workbench_colors(palette),
        "tokenColors": vscode_token_colors(resolved_syntax(palette)),
    }
    write("applications/vscode/themes/birren-industrial-light-color-theme.json", json.dumps(theme, indent=2))


def lua_table(mapping: dict[str, str], indent: int = 2) -> list[str]:
    space = " " * indent
    return [f"{space}{lua_key(key)} = \"{value}\"," for key, value in mapping.items()]


def build_neovim(palette: dict[str, Any]) -> None:
    colors = primitive_colors(palette)
    ansi = resolved_ansi(palette)
    lines = [
        f"-- {GENERATED}",
        "local M = {}",
        "",
        "local colors = {",
    ]
    lines.extend(lua_table(colors))
    lines.extend(["}", "", "local roles = {"])
    lines.extend(lua_table(resolved_roles(palette), 2))
    lines.extend(["}", "", "local syntax = {"])
    lines.extend(lua_table(resolved_syntax(palette), 2))
    lines.extend(["}", "", "local ansi = {", "  normal = {"])
    lines.extend(lua_table(ansi["normal"], 4))
    lines.extend(["  },", "  bright = {"])
    lines.extend(lua_table(ansi["bright"], 4))
    lines.extend(
        [
            "  },",
            "}",
            "",
            "local function set_terminal_colors()",
        ]
    )
    for index, name in enumerate(ANSI_ORDER):
        lines.append(f"  vim.g.terminal_color_{index} = ansi.normal.{name}")
    for offset, name in enumerate(ANSI_ORDER, start=8):
        lines.append(f"  vim.g.terminal_color_{offset} = ansi.bright.{name}")
    lines.extend(
        [
            "end",
            "",
            "function M.setup(opts)",
            "  opts = opts or {}",
            "  local r = roles",
            "  local s = syntax",
            "  local hi = vim.api.nvim_set_hl",
            "",
            "  vim.o.background = \"light\"",
            "  vim.cmd(\"highlight clear\")",
            "  if vim.fn.exists(\"syntax_on\") == 1 then",
            "    vim.cmd(\"syntax reset\")",
            "  end",
            "  vim.g.colors_name = \"birren-industrial\"",
            "  set_terminal_colors()",
            "",
            "  hi(0, \"Normal\", { fg = r.text, bg = r.background })",
            "  hi(0, \"NormalFloat\", { fg = r.text, bg = r.surface })",
            "  hi(0, \"FloatBorder\", { fg = r.border, bg = r.surface })",
            "  hi(0, \"Comment\", { fg = s.comment, italic = true })",
            "  hi(0, \"Constant\", { fg = s.constant })",
            "  hi(0, \"String\", { fg = s.string })",
            "  hi(0, \"Character\", { fg = s.string })",
            "  hi(0, \"Number\", { fg = s.number })",
            "  hi(0, \"Boolean\", { fg = s.number })",
            "  hi(0, \"Float\", { fg = s.number })",
            "  hi(0, \"Identifier\", { fg = s.variable })",
            "  hi(0, \"Function\", { fg = s[\"function\"] })",
            "  hi(0, \"Statement\", { fg = s.keyword, bold = true })",
            "  hi(0, \"Conditional\", { fg = s.keyword, bold = true })",
            "  hi(0, \"Repeat\", { fg = s.keyword, bold = true })",
            "  hi(0, \"Label\", { fg = s.keyword })",
            "  hi(0, \"Operator\", { fg = s.operator })",
            "  hi(0, \"Keyword\", { fg = s.keyword, bold = true })",
            "  hi(0, \"Exception\", { fg = r.attention })",
            "  hi(0, \"PreProc\", { fg = r.accent })",
            "  hi(0, \"Include\", { fg = r.accent })",
            "  hi(0, \"Define\", { fg = r.accent })",
            "  hi(0, \"Macro\", { fg = r.accent })",
            "  hi(0, \"Type\", { fg = s.type })",
            "  hi(0, \"StorageClass\", { fg = s.type })",
            "  hi(0, \"Structure\", { fg = s.type })",
            "  hi(0, \"Typedef\", { fg = s.type })",
            "  hi(0, \"Special\", { fg = r.primary })",
            "  hi(0, \"Underlined\", { fg = r.link, underline = true })",
            "  hi(0, \"Error\", { fg = colors.spotlight_buff, bg = colors.fire_red })",
            "  hi(0, \"Todo\", { fg = colors.deep_gray, bg = r.highlight, bold = true })",
            "",
            "  hi(0, \"LineNr\", { fg = r.text_muted, bg = r.background })",
            "  hi(0, \"CursorLineNr\", { fg = r.text, bg = r.background, bold = true })",
            "  hi(0, \"CursorLine\", { bg = r.surface_raised })",
            "  hi(0, \"SignColumn\", { fg = r.text_muted, bg = r.background })",
            "  hi(0, \"ColorColumn\", { bg = r.surface })",
            "  hi(0, \"Visual\", { bg = r.selection })",
            "  hi(0, \"Search\", { fg = colors.deep_gray, bg = r.highlight })",
            "  hi(0, \"IncSearch\", { fg = colors.deep_gray, bg = colors.solar_yellow })",
            "  hi(0, \"StatusLine\", { fg = colors.spotlight_buff, bg = colors.deep_gray })",
            "  hi(0, \"StatusLineNC\", { fg = r.text_muted, bg = r.surface })",
            "  hi(0, \"WinSeparator\", { fg = r.border, bg = r.background })",
            "  hi(0, \"VertSplit\", { fg = r.border, bg = r.background })",
            "  hi(0, \"Pmenu\", { fg = r.text, bg = r.surface })",
            "  hi(0, \"PmenuSel\", { fg = r.text, bg = r.selection })",
            "  hi(0, \"Directory\", { fg = r.link })",
            "",
            "  hi(0, \"DiffAdd\", { fg = r.success, bg = r.surface })",
            "  hi(0, \"DiffChange\", { fg = r.attention, bg = r.surface })",
            "  hi(0, \"DiffDelete\", { fg = colors.fire_red, bg = r.surface })",
            "  hi(0, \"DiffText\", { fg = colors.deep_gray, bg = colors.solar_yellow })",
            "  hi(0, \"DiagnosticError\", { fg = colors.fire_red })",
            "  hi(0, \"DiagnosticWarn\", { fg = r.warning })",
            "  hi(0, \"DiagnosticInfo\", { fg = r.link })",
            "  hi(0, \"DiagnosticHint\", { fg = r.secondary })",
            "end",
            "",
            "M.setup()",
            "return M",
        ]
    )
    write("applications/neovim/colors/birren-industrial.lua", "\n".join(lines))


def main() -> None:
    palette = load_palette()
    build_json_and_yaml(palette)
    build_css(palette)
    build_scss(palette)
    build_less(palette)
    build_js(palette)
    build_ghostty(palette)
    build_kitty(palette)
    build_alacritty(palette)
    build_wezterm(palette)
    build_vscode(palette)
    build_neovim(palette)


if __name__ == "__main__":
    main()
