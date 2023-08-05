_tglinker() 
{
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    if ( ! [[ "$prev" =~ "tglinker" ]] ); then
	opts=`tglinker --lspkgs ${prev}`
	else
	opts=`tglinker --lspkgs`
	fi

    COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
    return 0
}
complete -F _tglinker tglinker
