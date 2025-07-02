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

vim.lsp.config("rust_analyzer", coq.lsp_ensure_capabilities())
vim.lsp.enable("rust_analyzer")
vim.lsp.config("lua_ls", coq.lsp_ensure_capabilities())
vim.lsp.enable("lua_ls")
