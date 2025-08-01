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

require("pywal16").setup()
vim.cmd("colorscheme darkblue") -- I have no clue why this workaround is needed
vim.cmd("colorscheme pywal16")

require("lualine").setup({
  options = {
      theme = 'pywal16-nvim',
    },
})

local coq = require("coq")
require("lspconfig")
vim.cmd("COQnow --shut-up")

vim.lsp.inlay_hint.enable(true)
local config = coq.lsp_ensure_capabilities()
config.capabilities.textDocument.completion.completionItem.resolveSupport.properties = {"additionalTextEdits", "command"}
vim.lsp.config("*", config)
vim.lsp.enable("rust_analyzer")
vim.lsp.enable("lua_ls")
vim.lsp.enable("pylsp")
vim.lsp.enable("ccls")
vim.lsp.enable("bashls")
vim.lsp.enable("cssls")
vim.lsp.enable("html")
vim.lsp.enable("marksman")

-- WEB --
vim.cmd("packadd live-server.nvim")
require("live-server").setup()
