#!/bin/sh

test_dir=$(dirname $0)

export WORKON_HOME="$(echo ${TMPDIR:-/tmp}/WORKON_HOME | sed 's|//|/|g')"


oneTimeSetUp() {
    rm -rf "$WORKON_HOME"
    mkdir -p "$WORKON_HOME"
    source "$test_dir/util.sh"
    load_virtualenvwrapper
}

oneTimeTearDown() {
    rm -rf "$WORKON_HOME"
}

setUp () {
    echo
    rm -f "$test_dir/catch_output"
}

test_mktmpenv_no_name() {
    before=$(lsvirtualenv -b)
    mktmpenv >/dev/null 2>&1
    after=$(lsvirtualenv -b)
    assertFalse "Environment was not created" "[ \"$before\" = \"$after\" ]"
}

test_mktmpenv_name() {
    assertFalse "Environment already exists" "[ -d \"$WORKON_HOME/name-given-by-user\" ]"
    mktmpenv name-given-by-user >/dev/null 2>&1
    assertTrue "Environment was not created" "[ -d \"$WORKON_HOME/name-given-by-user\" ]"
}

test_deactivate() {
    assertFalse "Environment already exists" "[ -d \"$WORKON_HOME/automatically-deleted\" ]"
    mktmpenv automatically-deleted >/dev/null 2>&1
    assertTrue "Environment was not created" "[ -d \"$WORKON_HOME/automatically-deleted\" ]"
    deactivate
    assertFalse "Environment still exists" "[ -d \"$WORKON_HOME/automatically-deleted\" ]"
}

. "$test_dir/shunit2"
