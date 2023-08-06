#!/usr/bin/env python
from __future__ import print_function
from __builtin__ import list as pylist

import git
import optparse
import os
import saplib
import subprocess
import sys

def log(message, *args, **kwargs):
  print(message % args, file = sys.stderr, **kwargs)

def usage(message, *args):
  print(message % args)
  exit(1)

def open_repo(native = True):
  try:
    return git.Repo(odbt = git.db.GitCmdObjectDB if native else git.db.GitDB)
  except git.exc.InvalidGitRepositoryError:
    usage("Must be inside a git repository")

def open_config(repo):
  config_path = os.path.join(repo.working_tree_dir, '.saplings')
  if os.path.exists(config_path):
    with open(config_path, 'r') as config:
      try:
        return saplib.Config(repo, config.read())
      except saplib.ConfigError as e:
        usage("Problem loading .saplings config: %s" % e)
  else:
    return saplib.Config(repo)

def install(show = False, force = False):
  git_exec_path = subprocess.Popen(["git", "--exec-path"],
                                   stdout = subprocess.PIPE).communicate()[0].strip()
  installed_link_path = os.path.join(git_exec_path, 'git-sap')

  if show:
    print(os.path.realpath(installed_link_path))
    return

  recreate = force and os.path.exists(installed_link_path)
  if recreate:
    try:
      os.remove(installed_link_path)
    except OSError as e:
      usage("failed to remove old symlink: %s", e)

  if not os.path.exists(installed_link_path):
    try:
      os.symlink(os.path.abspath(sys.argv[0]), installed_link_path)
      print("symlink %s at: %s" % ("re-installed" if recreate else "installed",
                                   installed_link_path))
    except OSError as e:
      usage("failed to install symlink: %s", e)

  else:
    print("symlink exists: %s" % installed_link_path)

def list(repo, split_config, verbose):
  for split in split_config.splits.values():
    print(split.name)
    if verbose:
      paths = (
        "%s/" % os.path.relpath(os.path.join(repo.working_tree_dir, path)) for path in split.paths
      )
      log("remote: %s\npaths (%d):\n\t%s", split.remote, len(split.paths), "\n\t".join(paths))

def split(split_config, names, verbose):
  for split in (split_config.splits[name] for name in names):
    if (verbose):
      log("Operating on split: %s", split)

    # TODO(jsirois): allow customization of branch, consider special names:
    # name1:branch1 name2 ... nameN:branchN
    branch_name = 'sapling_split_%s' % split.name

    commits = pylist(split.commits())

    class ProgressTracker(object):
      def __init__(self):
        self._commit_count =len(commits)
        self._width = 80.0
        self._pct = 0
        self._pct_complete = 0

      def on_start(self):
        message = "[split = %s, branch = %s] Processing %d commits" % (split.name,
                                                                       branch_name,
                                                                       self._commit_count)
        if verbose:
          log(message)
        else:
          self._width = max(len(message) + 2.0, float(self._width))
          self._quantum = self._commit_count / self._width
          log(message + (" " * (int(self._width) - len(message) - 1)) + "|")

      def on_commit(self, i, original_commit, new_commit):
        if verbose:
          log("%s -> %s (%d of %d)", original_commit.hexsha, new_commit.hexsha, i + 1,
              self._commit_count)
        else:
          self._pct_complete = int(i / self._quantum % self._commit_count)
          if self._pct_complete > self._pct:
            log("." * (self._pct_complete - self._pct), end = "")
            self._pct = self._pct_complete
            sys.__stdout__.flush()

      def on_finish(self):
        if not verbose:
          log("." * (int(self._width) - self._pct_complete))

    progressTracker = ProgressTracker()
    progressTracker.on_start()
    tip = split.apply(branch_name, commits, progressTracker.on_commit)
    progressTracker.on_finish()

    print(tip.hexsha)

def parse_args():
  usage = """
    %prog (-dv --python-git-db) --list
    %prog (-dv --python-git-db) --split [splitname...]"""

  epilog = "Happy splitting!"

  parser = optparse.OptionParser(usage = usage, version = "%prog 0.0.1", epilog = epilog)
  parser.add_option("-d", "--debug", dest = "debug", action = "store_true", default = False,
                    help = "prints extra debugging information")
  parser.add_option("-v", "--verbose", dest = "verbose", action = "store_true", default = False,
                    help = "prints extra information")
  parser.add_option("--python-git-db", dest = "native", action = "store_false", default = True,
                    help = "specifies the python implementation of the git object database should "
                    "be used instead of the native one - can speed operations when repository has "
                    "few large files")

  # TODO(jsirois): enforce mutual exclusivity of these option groups

  install = optparse.OptionGroup(parser, "Install sap as a git subcommand")
  install.add_option("--install",
                     dest = "subcommand",
                     action = "store_const",
                     const = "install",
                     help = """installs the git sap command if not installed already""")
  install.add_option("-f", "--force",
                     dest = "force",
                     action = "store_true",
                     default = False,
                     help = """forces a re-install of the git sap command""")
  install.add_option("-s", "--show",
                     dest = "show",
                     action = "store_true",
                     default = False,
                     help = "does not perform an install, instead shows the path of the binary "
                     "git sap' calls into")
  parser.add_option_group(install)

  list = optparse.OptionGroup(parser, "List configured splits for the current git repo")
  list.add_option("--list",
                    dest = "subcommand",
                    default = "list",
                    action = "store_const",
                    const = "list",
                    help = """lists the defined splits""")
  parser.add_option_group(list)

  split = optparse.OptionGroup(parser, "Split new commits out that affect one or more splits")
  split.add_option("--split",
                    dest = "subcommand",
                    action = "store_const",
                    const = "split",
                    help =
                    """populates the [splitname] branch with commits intersecting the split""")
  parser.add_option_group(split)

  (options, args) = parser.parse_args()
  return (options, args, parser.error)

def main():
  (options, args, ferror) = parse_args()

  if options.subcommand is "install":
    if len(args) != 0:
      ferror("list takes no arguments")
    install(options.show, options.force)
    return

  # Fail fast if we're either not in a repo or we are but have an invalid .saplings config
  repo = open_repo(options.native)
  split_config = open_config(repo)

  if options.debug:
    print("repo\t[%s]\t%s" % (repo.active_branch, repo.working_tree_dir))

  if options.subcommand is "list":
    if len(args) != 0:
      ferror("list takes no arguments")
    list(repo, split_config, options.verbose)

  elif options.subcommand is "split":
    if len(args) == 0:
      ferror("At least 1 split must be specified")
    try:
      split(split_config, args, options.verbose)
    except KeyError as e:
      ferror("split not defined: %s" % e)

try:
  main()
  exit(0)
except object as e:
  usage(e)
