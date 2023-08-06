#
# virtualenvwrapper.project plugin
#

# Verify that the PROJECT_HOME directory exists
virtualenvwrapper_verify_project_home () {
    if [ -z "$PROJECT_HOME" ]
    then
        echo "ERROR: Set the PROJECT_HOME shell variable to the name of the directory where projects should be created." >&2
        return 1
    fi
    if [ ! -d "$PROJECT_HOME" ]
    then
        [ "$1" != "-q" ] && echo "ERROR: Project directory '$PROJECT_HOME' does not exist.  Create it or set PROJECT_HOME to an existing directory." >&2
        return 1
    fi
    return 0
}

# Given a virtualenv directory and a project directory,
# set the virtualenv up to be associated with the 
# project
setvirtualenvproject () {
    typeset venv="$1"
    typeset prj="$2"
    if [ -z "$venv" ]
    then
        venv="$VIRTUAL_ENV"
    fi
    if [ -z "$prj" ]
    then
        prj="$(pwd)"
    fi
    echo "Setting project for $(basename $venv) to $prj"
    echo "$prj" > "$venv/.project"
}

# Show help for mkproject
mkproject_help () {
    echo "Usage: mkproject [-t template] [virtualenv options] project_name"
    echo ""
    echo "Multiple templates may be selected.  They are applied in the order"
    echo "specified on the command line."
    echo
    echo "Available templates:"
    echo
    "$VIRTUALENVWRAPPER_PYTHON" -m virtualenvwrapper.hook_loader -l project.template
}

# Create a new project directory and its associated virtualenv.
mkproject () {
    for arg
    do
        if [ "$arg" = "-h" ]
        then
            echo 'mkproject help:'
            echo
            mkproject_help
            echo
            echo 'mkvirtualenv help:'
            echo
            mkvirtualenv -h
            return
        fi
    done
    templates=$("$VIRTUALENVWRAPPER_PYTHON" -m virtualenvwrapper.hook_loader \
        -n get_templates project.parse_args $@)
    RC=$?
    if [ $RC -ne 0 ]
    then
        return $RC
    fi
    set -- $("$VIRTUALENVWRAPPER_PYTHON" -m virtualenvwrapper.hook_loader \
        -n get_virtualenv_args project.parse_args $@)
    RC=$?
    if [ $RC -ne 0 ]
    then
        return $RC
    fi

#     echo "templates $templates"
#     echo "remainder $@"
#     return 0

    eval "envname=\$$#"
    virtualenvwrapper_verify_project_home || return 1

    if [ -d "$PROJECT_HOME/$envname" ]
    then
        echo "Project $envname already exists." >&2
        return 1
    fi

    mkvirtualenv "$@" || return 1

    cd "$PROJECT_HOME"

    virtualenvwrapper_run_hook project.pre_mkproject $envname

    echo "Creating $PROJECT_HOME/$envname"
    mkdir -p "$PROJECT_HOME/$envname"
    setvirtualenvproject "$VIRTUAL_ENV" "$PROJECT_HOME/$envname"

    cd "$PROJECT_HOME/$envname"

    for t in $templates
    do
        echo
        echo "Applying template $t"
        virtualenvwrapper_run_hook --name $t project.template $envname
    done

    virtualenvwrapper_run_hook project.post_mkproject
}

# Change directory to the active project
cdproject () {
    virtualenvwrapper_verify_workon_home || return 1
    virtualenvwrapper_verify_active_environment || return 1
    if [ -f "$VIRTUAL_ENV/.project" ]
    then
        project_dir=$(cat "$VIRTUAL_ENV/.project")
        if [ ! -z "$project_dir" ]
        then
            cd "$project_dir"
        else
            echo "Project directory $project_dir does not exist" 1>&2
            return 1
        fi
    else
        echo "No project set in $VIRTUAL_ENV/.project" 1>&2
        return 1
    fi
    return 0
}