-- Generated from source/birren-industrial.json by scripts/build.py. Do not edit by hand.
local M = {}

local colors = {
  light_green = "#C2E1CA",
  instrument_white = "#F0F0EA",
  beige = "#DBD6C0",
  light_blue = "#ADCED7",
  soft_yellow = "#FDF7B1",
  light_gray = "#BECECF",
  mid_neutral = "#8FA89E",
  medium_gray = "#5F7B71",
  muted_text = "#52736A",
  deep_gray = "#3F614F",
  spotlight_buff = "#E6DEAE",
  medium_green = "#4E8C5A",
  sandalwood = "#988454",
  medium_blue = "#4F7B80",
  solar_yellow = "#EEC902",
  alert_orange = "#E15602",
  fire_red = "#7C0203",
  safety_green = "#007839",
  caution_blue = "#026289",
}

local roles = {
  background = "#C2E1CA",
  background_muted = "#F0F0EA",
  surface = "#F0F0EA",
  surface_raised = "#F0F0EA",
  surface_sunken = "#ADCED7",
  text = "#3F614F",
  text_muted = "#52736A",
  border = "#5F7B71",
  primary = "#4F7B80",
  secondary = "#4E8C5A",
  accent = "#026289",
  highlight = "#FDF7B1",
  selection = "#ADCED7",
  success = "#007839",
  warning = "#EEC902",
  danger = "#7C0203",
  attention = "#E15602",
  link = "#026289",
  focus = "#EEC902",
}

local syntax = {
  comment = "#52736A",
  foreground = "#3F614F",
  keyword = "#026289",
  string = "#4E8C5A",
  ["function"] = "#4F7B80",
  variable = "#3F614F",
  type = "#988454",
  constant = "#7C0203",
  number = "#E15602",
  operator = "#4F7B80",
  punctuation = "#3F614F",
}

local ansi = {
  normal = {
    black = "#3F614F",
    red = "#7C0203",
    green = "#4E8C5A",
    yellow = "#988454",
    blue = "#4F7B80",
    magenta = "#E15602",
    cyan = "#026289",
    white = "#E6DEAE",
  },
  bright = {
    black = "#5F7B71",
    red = "#E15602",
    green = "#007839",
    yellow = "#EEC902",
    blue = "#026289",
    magenta = "#FDF7B1",
    cyan = "#ADCED7",
    white = "#F0F0EA",
  },
}

local function set_terminal_colors()
  vim.g.terminal_color_0 = ansi.normal.black
  vim.g.terminal_color_1 = ansi.normal.red
  vim.g.terminal_color_2 = ansi.normal.green
  vim.g.terminal_color_3 = ansi.normal.yellow
  vim.g.terminal_color_4 = ansi.normal.blue
  vim.g.terminal_color_5 = ansi.normal.magenta
  vim.g.terminal_color_6 = ansi.normal.cyan
  vim.g.terminal_color_7 = ansi.normal.white
  vim.g.terminal_color_8 = ansi.bright.black
  vim.g.terminal_color_9 = ansi.bright.red
  vim.g.terminal_color_10 = ansi.bright.green
  vim.g.terminal_color_11 = ansi.bright.yellow
  vim.g.terminal_color_12 = ansi.bright.blue
  vim.g.terminal_color_13 = ansi.bright.magenta
  vim.g.terminal_color_14 = ansi.bright.cyan
  vim.g.terminal_color_15 = ansi.bright.white
end

function M.setup(opts)
  opts = opts or {}
  local r = roles
  local s = syntax
  local hi = vim.api.nvim_set_hl

  vim.o.background = "light"
  vim.cmd("highlight clear")
  if vim.fn.exists("syntax_on") == 1 then
    vim.cmd("syntax reset")
  end
  vim.g.colors_name = "birren-industrial"
  set_terminal_colors()

  hi(0, "Normal", { fg = r.text, bg = r.background })
  hi(0, "NormalFloat", { fg = r.text, bg = r.surface })
  hi(0, "FloatBorder", { fg = r.border, bg = r.surface })
  hi(0, "Comment", { fg = s.comment, italic = true })
  hi(0, "Constant", { fg = s.constant })
  hi(0, "String", { fg = s.string })
  hi(0, "Character", { fg = s.string })
  hi(0, "Number", { fg = s.number })
  hi(0, "Boolean", { fg = s.number })
  hi(0, "Float", { fg = s.number })
  hi(0, "Identifier", { fg = s.variable })
  hi(0, "Function", { fg = s["function"] })
  hi(0, "Statement", { fg = s.keyword, bold = true })
  hi(0, "Conditional", { fg = s.keyword, bold = true })
  hi(0, "Repeat", { fg = s.keyword, bold = true })
  hi(0, "Label", { fg = s.keyword })
  hi(0, "Operator", { fg = s.operator })
  hi(0, "Keyword", { fg = s.keyword, bold = true })
  hi(0, "Exception", { fg = r.attention })
  hi(0, "PreProc", { fg = r.accent })
  hi(0, "Include", { fg = r.accent })
  hi(0, "Define", { fg = r.accent })
  hi(0, "Macro", { fg = r.accent })
  hi(0, "Type", { fg = s.type })
  hi(0, "StorageClass", { fg = s.type })
  hi(0, "Structure", { fg = s.type })
  hi(0, "Typedef", { fg = s.type })
  hi(0, "Special", { fg = r.primary })
  hi(0, "Underlined", { fg = r.link, underline = true })
  hi(0, "Error", { fg = colors.spotlight_buff, bg = colors.fire_red })
  hi(0, "Todo", { fg = colors.deep_gray, bg = r.highlight, bold = true })

  hi(0, "LineNr", { fg = r.text_muted, bg = r.background })
  hi(0, "CursorLineNr", { fg = r.text, bg = r.background, bold = true })
  hi(0, "CursorLine", { bg = r.surface_raised })
  hi(0, "SignColumn", { fg = r.text_muted, bg = r.background })
  hi(0, "ColorColumn", { bg = r.surface })
  hi(0, "Visual", { bg = r.selection })
  hi(0, "Search", { fg = colors.deep_gray, bg = r.highlight })
  hi(0, "IncSearch", { fg = colors.deep_gray, bg = colors.solar_yellow })
  hi(0, "StatusLine", { fg = colors.spotlight_buff, bg = colors.deep_gray })
  hi(0, "StatusLineNC", { fg = r.text_muted, bg = r.surface })
  hi(0, "WinSeparator", { fg = r.border, bg = r.background })
  hi(0, "VertSplit", { fg = r.border, bg = r.background })
  hi(0, "Pmenu", { fg = r.text, bg = r.surface })
  hi(0, "PmenuSel", { fg = r.text, bg = r.selection })
  hi(0, "Directory", { fg = r.link })

  hi(0, "DiffAdd", { fg = r.success, bg = r.surface })
  hi(0, "DiffChange", { fg = r.attention, bg = r.surface })
  hi(0, "DiffDelete", { fg = colors.fire_red, bg = r.surface })
  hi(0, "DiffText", { fg = colors.deep_gray, bg = colors.solar_yellow })
  hi(0, "DiagnosticError", { fg = colors.fire_red })
  hi(0, "DiagnosticWarn", { fg = r.warning })
  hi(0, "DiagnosticInfo", { fg = r.link })
  hi(0, "DiagnosticHint", { fg = r.secondary })
end

M.setup()
return M
