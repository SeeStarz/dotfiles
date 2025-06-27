-- Indentations
vim.opt.expandtab = true      -- use spaces instead of tabs
vim.opt.shiftwidth = 2        -- indent width
vim.opt.tabstop = 2           -- tab width
vim.opt.smartindent = true    -- autoindent new lines
vim.opt.autoindent = true

-- Line numberings
vim.opt.number = true         -- show line numbers
vim.opt.relativenumber = true -- show relative line numbers
vim.opt.cursorline = true    -- highlight current line
vim.opt.cursorcolumn = true   -- highlight current column
vim.opt.wrap = true           -- enable line wrap
vim.opt.signcolumn = "yes"    -- keep signcolumn on

vim.opt.scrolloff = 8         -- keep cursor away from edges
vim.opt.sidescrolloff = 8

vim.opt.termguicolors = false

vim.opt.list = true
vim.opt.listchars = {
  tab = "→ ",
  trail = "·",
  extends = "»",
  precedes = "«",
}
