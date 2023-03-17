### Creating a local repository for gitorious and pushing back to gitorious
```
$ git clone <url> <project>
$ cd <project>
# Git needs a file to commit.
$ touch .gitignore
$ git add .
$ git remote add origin <url>
$ git push origin master
```

### Fork a github repository on gitorious
```
$ git clone <gitorious-url>
$ git remote add origin <gitorious-url>
$ git remote add upstream <github-url>
$ git pull upstream
$ git push -u origin master
```

### Pulling / merging from an upstream git repo
```
$ git pull upstream
$ git merge upstream
# Resolve conflicts if needed
$ git push master
```

### How do I clone a remote branch with git?
```
$ git checkout -b <branch> remotes/origin/<branch>
```

http://book.git-scm.com/4_undoing_in_git_-_reset,_checkout_and_revert.html
http://stackoverflow.com/questions/2389361/git-undo-a-merge

Dumping an old repository to a new repository under a subdirectory, maintaining
all of the commit history:

### Dump all patches for the commits from the start of time to `HEAD`
```
$ cd /old/checkout
#
# NB: this might be really funky with binary files or may not work; git-lfs's highly
#     encouraged!
$ git format-patch --root HEAD
```

### Import all commits maintaining core commit metadata/authorship

**Note:** This doesn't maintain committership, unfortunately.
```
$ cd /new/checkout
# Start fresh
$ git am --abort
$ git reset --hard
# Apply all patches in sequence; abort if needed
$ find -s /old/checkout/ -name \*.patch -exec git am --directory=new/subdir {} \;
[ $? -ne 0 ] && git am --abort
```

### List all files tracked by git on HEAD under the include/ directory
```
$ git ls-tree -r --name-only HEAD include/
```

### List all files with DEPRECATED using exclude pathspecs in `git grep` call

List all files that fit the following criteria using `git grep`:
- contain the string "DEPRECATED"
- tracked by git on HEAD.
- that don't end with the following extensions under include/:
    - .c
    - .md
    - .pl
    - .pod
```
$ git grep -lEe DEPRECATED \
    ':(exclude)*.c' \
    ':(exclude)*.md' \
    ':(exclude)*.pl' \
    ':(exclude)*.pod' \
    include/
```
