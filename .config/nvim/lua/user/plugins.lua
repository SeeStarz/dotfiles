-- Disable tab and shift tab bindings
-- Disable no snippets warning
require("pywal16").setup()
vim.cmd("colorscheme darkblue") -- I have no clue why this workaround is needed
vim.cmd("colorscheme pywal16")

require("lualine").setup({
  options = {
      theme = 'pywal16-nvim',
    },
})

local cmp = require("cmp")
cmp.setup({
  snippet = {
    -- REQUIRED - you must specify a snippet engine
    expand = function(args)
        vim.snippet.expand(args.body) -- For native neovim snippets (Neovim v0.10+)
      end,
    },
    window = {
      completion = cmp.config.window.bordered(),
      documentation = cmp.config.window.bordered(),
  },
    mapping = cmp.mapping.preset.insert({
      ['<C-b>'] = cmp.mapping.scroll_docs(-4),
      ['<C-f>'] = cmp.mapping.scroll_docs(4),
      ['<C-Space>'] = cmp.mapping.complete(),
      ['<C-e>'] = cmp.mapping.abort(),
      ['<CR>'] = cmp.mapping.confirm({ select = false }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
    }),
    sources = cmp.config.sources({
      { name = 'nvim_lsp' },
    }, {
      { name = 'buffer' },
    })
  })

local capabilities = require('cmp_nvim_lsp').default_capabilities()
local config = {
  capabilities = capabilities
}

require("lspconfig")
vim.lsp.config("*", config)
vim.lsp.inlay_hint.enable(true)
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
