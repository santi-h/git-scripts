
# returns true if $1 is empty, all spaces, or null, false otherwise
is_blank () {
  if [ "$(echo "$1" | sed -E 's/[[:space:]]+//g')" = "" ]; then
    return 0
  else
    return 1
  fi
}

# returns the opposite of is_blank
is_present () {
  if is_blank $1; then
    return 1
  else
    return 0
  fi
}

# prints $1. Also executes $1 only if $BASH_ARGV is "do"
doit () {
  echo "$1"
  if [ "$BASH_ARGV" == "do" ]; then
    eval $1
  else
    echo "(command not run, add 'do' at the end to run it)"
  fi
}

# exits if $1 is not a development branch
assert_development_branch () {
  if is_blank "$(echo "$1" | grep -E '^\d+-')"; then
    echo "You must be on a development branch"
    exit -1
  fi
}

# returns the branch number. E.g. if $1 is 1234-branch-name, it returns 1234
get_branch_number () {
  regex="^([0-9]+)-"
  [[ "$1" =~ $regex ]]
  echo ${BASH_REMATCH[1]}
}

# returns the name of the merge branch
get_merge_branch_name () {
  regex="(merge-[^[:space:]]*)"
  [[ "$(git branch)" =~ $regex ]]
  echo ${BASH_REMATCH[1]}
}

# returns branch numbers from $1
get_branch_numbers_from_merge_branch () {
  echo "$1" | sed -E 's/[^0-9]+/ /g'
}

