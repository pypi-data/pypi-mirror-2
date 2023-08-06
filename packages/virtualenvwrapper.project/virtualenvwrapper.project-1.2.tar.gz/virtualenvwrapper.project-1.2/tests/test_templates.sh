#!/bin/sh

#set -x

test_dir=$(dirname $0)

export WORKON_HOME="${TMPDIR:-/tmp}WORKON_HOME"
export PROJECT_HOME="${TMPDIR:-/tmp}PROJECT_HOME"

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
    rm -f "$TMPDIR/catch_output"
}

test_list_templates () {
    mkproject myproject
    output=`mkproject myproject 2>&1`
    assertTrue "Did not see expected message" "echo $output | grep 'already exists'"
    deactivate
}


. "$test_dir/shunit2"
