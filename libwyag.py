import argparse
import collections
import configparser
from genericpath import isdir
import hashlib
import os
import re
import sys
import zlib

# content tracker
argparser = argparse.ArgumentParser(description="Content tracker")

# Subparser declaration
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add"           : cmd_add(args)
    elif args.command == "cat-file"    : cmd_cat_file(args)
    elif args.command == "checkout"    : cmd_checkout(args)
    elif args.command == "commit"      : cmd_commit(args)
    elif args.command == "hash-object" : cmd_hash_object(args)
    elif args.command == "init"        : cmd_init(args)
    elif args.command == "log"         : cmd_log(args)
    elif args.command == "ls-tree"     : cmd_ls_tree(args)
    elif args.command == "merge"       : cmd_merge(args)
    elif args.command == "rebase"      : cmd_rebase(args)
    elif args.command == "rev-parse"   : cmd_rev_parse(args)
    elif args.command == "rm"          : cmd_rm(args)
    elif args.command == "show-ref"    : cmd_show_ref(args)
    elif args.command == "tag"         : cmd_tag(args)

class GitRepository(object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None
    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git repository %s" % path)

        # Read configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0
            raise Exception("Unsupported repositoryformatversion %s" %vers)


    # Utility function for manipulating paths in the repository
    def repo_path(repo, *path):
        """Compute path under repo's gitdir"""
        return os.path.join(repo.gitdir, *path)

    # Function to return a path to a file or directory
    def repo_file(repo, *path, mkdir=False):
        """Same as repo_path, but create dirname(*path) if absent.  For
        example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
        .git/refs/remotes/origin."""
        if repo_dir(repo, *path[:-1], mkdir=mkdir):
            return repo_path(repo, *path)

    def repo_dir(repo, *path, mkdir=False):
        """Same as repo_path, but mkdir *path if mkdir is absent"""
        path = repo_path(repo, *path)

        if os.path.exists(path):
            if(os.path.isdir(path)):
                return path
            else:
                return None