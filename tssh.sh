#/bin/bash

TSSH_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TSSH="python ${TSSH_DIR}/tssh.py"
function tssh {
    ${TSSH} "$@"
}
complete -W "$(${TSSH} __autocomplete)" tssh
