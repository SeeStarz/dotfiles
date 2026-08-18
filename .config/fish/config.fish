function fish_prompt -d "Write out the prompt"
    # This shows up as USER@HOST /home/user/ >, with the directory colored
    # $USER and $hostname are set by fish, so you can just use them
    # instead of using `whoami` and `hostname`
    printf '%s@%s %s%s%s > ' $USER $hostname \
        (set_color $fish_color_cwd) (prompt_pwd) (set_color normal)
end

if status is-interactive
    # Commands to run in interactive sessions can go here
    set fish_greeting

    starship init fish | source
    zoxide init fish | source
    thefuck --alias | source
    pyenv init - fish | source

    # This needs a custom zoxide version with support for exact name filter
    function ze -d "Z jump exact"
        set -l argc (builtin count $argv)
        if test $argc -eq 0
            __zoxide_cd $HOME
        else if test "$argv" = -
            __zoxide_cd -
        else if test $argc -eq 1 -a -d $argv[1]
            __zoxide_cd $argv[1]
        else if test $argc -eq 2 -a $argv[1] = --
            __zoxide_cd -- $argv[2]
        else
            set -l result (command zoxide query --exclude (__zoxide_pwd) -e -- $argv)
            and __zoxide_cd $result
        end
    end

    alias ff fastfetch
    alias dotfiles 'git --git-dir=$HOME/.dotfiles --work-tree=$HOME'
    alias tree 'tree -C'
    alias tp trash-put
    alias lsblk 'lsblk -o NAME,SIZE,PARTTYPENAME,PARTLABEL,LABEL,FSTYPE,MOUNTPOINT'
    alias xcpy 'xclip -i -selection clipboard'
    alias xpaste 'xclip -o -selection clipboard'
    alias cdreal 'cd $(realpath .)'

    set -xU PAGER less

    # Set use color
    # Bold is set to bold and red
    # Underlined is set to underlined and blue
    set -xU MANPAGER 'less --use-color -Dd+r -Du+b'

    # Disable color or something that messes with manpage color
    set -xU MANROFFOPT '-c'

    # Set colorful and ignorecase
    set -xU LESS '-R -i'

    fastfetch
end
