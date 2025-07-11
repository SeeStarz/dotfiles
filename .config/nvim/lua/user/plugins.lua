-- Disable tab and shift tab bindings
-- Disable no snippets warning
vim.g.coq_settings = {
  clients = {
    snippets = {
      warn = {},
    },
  },
  keymap = {
    recommended = false,
  },
}

local coq = require("coq")
require("lspconfig")
vim.cmd("COQnow --shut-up")

vim.lsp.inlay_hint.enable(true)
vim.lsp.config("*", coq.lsp_ensure_capabilities())
vim.lsp.enable("rust_analyzer")
vim.lsp.enable("lua_ls")
vim.lsp.enable("pylsp")
vim.lsp.enable("bashls")
vim.lsp.enable("cssls")
vim.lsp.enable("html")
vim.lsp.enable("marksman")
