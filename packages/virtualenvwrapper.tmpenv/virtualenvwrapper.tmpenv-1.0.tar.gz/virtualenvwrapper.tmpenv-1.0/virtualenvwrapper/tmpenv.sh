#
# virtualenvwrapper.tmpenv plugin
#

mktmpenv() {
    typeset tmpenvname="$1"

    # Generate a unique temporary name, if one is not given.
    if [ -z "$tmpenvname" ]
    then
        tmpenvname=$("$VIRTUALENVWRAPPER_PYTHON" -c 'import uuid; print uuid.uuid4()')
    fi

    # Create the environment
    mkvirtualenv "$tmpenvname"
    RC=$?
    if [ $RC -ne 0 ]
    then
        return $RC
    fi

    # Change working directory
    cdvirtualenv

    # Create the tmpenv marker file
    echo "This is a temporary environment. It will be deleted when deactivated." | tee "$VIRTUAL_ENV/README.tmpenv"

    # Update the postdeactivate script
    cat - >> "$VIRTUAL_ENV/bin/postdeactivate" <<EOF
if [ -f "$WORKON_HOME/$tmpenvname/README.tmpenv" ]
then
    echo "Removing temporary environment $venv"
    rmvirtualenv "$tmpenvname"
fi
EOF
}
