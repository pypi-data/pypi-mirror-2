#!/bin/sh

#set -x

test_dir=$(dirname $0)

export WORKON_HOME="${TMPDIR:-/tmp}/WORKON_HOME"
export PROJECT_HOME="${TMPDIR:-/tmp}/PROJECT_HOME"

oneTimeSetUp() {
    rm -rf "$WORKON_HOME"
    mkdir -p "$WORKON_HOME"
    rm -rf "$PROJECT_HOME"
    mkdir -p "$PROJECT_HOME"
    source "$test_dir/util.sh"
    load_virtualenvwrapper
}

oneTimeTearDown() {
    rm -rf "$WORKON_HOME"
    rm -rf "$PROJECT_HOME"
}

setUp () {
    echo
    rm -f "$test_dir/catch_output"
}

test_initialize() {
    for hook in  premkproject postmkproject prermproject postrmproject
    do
        assertTrue "Global $hook was not created" "[ -f $WORKON_HOME/$hook ]"
        assertTrue "Global $hook is not executable" "[ -x $WORKON_HOME/$hook ]"
    done
}

test_virtualenvwrapper_verify_project_home() {
    assertTrue "PROJECT_HOME not verified" virtualenvwrapper_verify_project_home
}

test_virtualenvwrapper_verify_project_home_missing_dir() {
    old_home="$PROJECT_HOME"
    PROJECT_HOME="$PROJECT_HOME/not_there"
    assertFalse "PROJECT_HOME verified unexpectedly" virtualenvwrapper_verify_project_home
    PROJECT_HOME="$old_home"
}

. "$test_dir/shunit2"
