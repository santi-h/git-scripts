# git-scripts
Scripts I use for everyday development

#### git_add_to_merge
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
