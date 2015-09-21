# git-scripts
Scripts I use for everyday development

#### git_apply_to_last_commit
Applies current changes (stashed and uncommited) to the last commit.
##### example
```
$ git log -2 --name-status --oneline
ee00f96 caching element
M	app/assets/javascripts/supplements.js.erb
ce2cb66 fixing spec
M	spec/features/admin/admin_assignments_spec.rb

$ git status --short
M app/views/supplements/_step_3.html.erb

$ git_apply_to_last_commit

$ git status
On branch test-branch
nothing to commit, working directory clean

$ git log -2 --name-status --oneline
e6ab44a caching element
M	app/assets/javascripts/supplements.js.erb
M	app/views/supplements/_step_3.html.erb
ce2cb66 fixing spec
M	spec/features/admin/admin_assignments_spec.rb
```

#### git_add_to_merge
Adds current branch to merge branch. Creates merge branch if it doesn't exist.
##### example
```
$ git branch
  7180-shops-cleanup
* 7441-shop-find-by-phone
  7795-vice-beta
  master
  
$ git_add_to_merge do

$ git branch
  7180-shops-cleanup
* 7441-shop-find-by-phone
  7795-vice-beta
  master
  merge-7441

$ git checkout 7180-shops-cleanup

$ git_add_to_merge do

$ git branch
* 7180-shops-cleanup
  7441-shop-find-by-phone
  7795-vice-beta
  master
  merge-7180-7441
```

#### git_remove_from_merge
Removes current branch from merge branch.
##### example

```
$ git branch
* 7180-shops-cleanup
  7441-shop-find-by-phone
  7795-vice-beta
  master
  merge-7180-7441

$ git_remove_from_branch do

$ git branch
* 7180-shops-cleanup
  7441-shop-find-by-phone
  7795-vice-beta
  master
  merge-7441

$ git checkout 7441-shop-find-by-phone

$ git_remove_from_merge do

$ git branch
  7180-shops-cleanup
* 7441-shop-find-by-phone
  7795-vice-beta
  master
```
