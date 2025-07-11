-- COQ Keybindings
-- insert mode: CTRL-H go to next placeholder (snippet mark)
-- insert mode: CTRL-Space open user completion (?)

-- Lspconfig Keybindings
-- normal mode: K vim.lsp.buf.hover()
-- [d and ]d map to vim.diagnostic.jump() with {count=-1} and vim.diagnostic.jump() with {count=1}, respectively.
-- normal mode: CTRL-W vim.diagnostics.open_float()

vim.api.nvim_set_keymap('i', '<Esc>', [[pumvisible() ? "\<C-e><Esc>" : "\<Esc>"]], { expr = true, silent = true })
vim.api.nvim_set_keymap('i', '<C-c>', [[pumvisible() ? "\<C-e><C-c>" : "\<C-c>"]], { expr = true, silent = true })
vim.api.nvim_set_keymap('i', '<BS>', [[pumvisible() ? "\<C-e><BS>" : "\<BS>"]], { expr = true, silent = true })
vim.api.nvim_set_keymap(
  "i",
  "<CR>",
  [[pumvisible() ? (complete_info().selected == -1 ? "\<C-e><CR>" : "\<C-y>") : "\<CR>"]],
  { expr = true, silent = true }
)
