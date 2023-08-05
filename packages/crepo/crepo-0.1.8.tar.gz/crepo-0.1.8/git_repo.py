#!/usr/bin/env python
# (c) Copyright 2010 Cloudera, Inc.

from git_command import GitCommand
import os

class GitRepo(object):
  def __init__(self, path):
    self.path = path

  def __str__(self):
    return "GitRepo at " + self.path

  def command(self, cmdv, **kwargs):
    """
    Runs the given git command and returns the status code returned.

    @param cmdv the git command as a list of args (eg ["diff"])
    """
    return self.command_process(cmdv, **kwargs).Wait()
  
  def check_command(self, cmdv, capture_stdout=False):
    """
    Runs the given git command, and raises an Exception if the status
    code returned is non-zero.
    """
    p = self.command_process(cmdv, capture_stdout=capture_stdout)
    rc = p.Wait()
    if rc != 0:
      raise Exception("Command %s returned non-zero exit code: %d" %
                      (repr(cmdv), rc))
    if capture_stdout:
      return p.stdout

  def command_process(self, cmdv, **kwargs):
    p = GitCommand(cwd=self.path,
                   cmdv=cmdv,
                   **kwargs)
    return p

  def is_cloned(self):
    return os.path.exists(os.path.join(self.path, ".git"))

  def is_dirty(self):
    return self.is_workdir_dirty() or self.is_index_dirty()

  def is_workdir_dirty(self):
    """Return true if the working directory is dirty (ie there are unstaged changes)"""
    # This incantation borrowed from git-rebase shell script
    return self.command(["update-index", "--refresh"],
      ignore_stdout=True)

  def is_index_dirty(self):
    """Return true if the index is dirty (ie there are uncommited but staged changes)"""
    # This incantation borrowed from git-rebase shell script
    out = self.command(["diff-index", "--cached", "--name-status", "-r",
      "HEAD", "--"],
      capture_stdout=True)
    return bool(out)


  def tracking_status(self, local_branch, remote_branch):
    """
    Return a tuple (left_commits, right_commits). The first element
    is the number of commits in the local branch and not in remote.
    The second element is the other direction
    """
    stdout = self.check_command(["rev-list", "--left-right",
                                 "%s...%s" % (local_branch, remote_branch)],
                                capture_stdout=True)
    commits = stdout.strip().split("\n")
    left_commits, right_commits = (0,0)
    for commit in commits:
      if not commit: continue
      if commit[0] == '<':
        left_commits += 1
      else:
        right_commits += 1

    return (left_commits, right_commits)

  def current_branch(self):
    stdout = self.check_command(["symbolic-ref", "HEAD"],
                                capture_stdout=True)
    return stdout.rstrip().replace("refs/heads/", "")


  def rev_parse(self, rev):
    stdout = self.check_command(['rev-parse', 'HEAD'],
                                capture_stdout=True)
    return stdout.rstrip()

  def has_ref(self, ref):
    p = self.command_process(['rev-parse', '--verify', '-q', ref],
                             capture_stdout=True)
    return p.Wait() == 0
    

  @property
  def name(self):
    return os.path.basename(os.path.realpath(self.path))
