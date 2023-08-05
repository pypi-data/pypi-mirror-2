import urllib
import shutil
import os
import os.path

from wizard import app, command, shell

def main(argv, baton):
    options, args = parse_args(argv, baton)
    check_directory(options)
    if not os.path.exists(args[0]):
        appname, _, version = args[0].partition("-")
        application = app.getApplication(appname)
        url = application.download(version)
        base = os.path.basename(url)
        with open(base, "w") as outfile:
            infile = urllib.urlopen(url)
            shutil.copyfileobj(infile, outfile)
        shell.call("tar", "xf", base)
        os.unlink(base)
    else:
        base = args[0]
        shell.call("tar", "xf", base)
    # extract the files, but be smart: if only one directory is output,
    # move the contents of that directory here
    items = [f for f in os.listdir(os.getcwd()) if f[0] != "."]
    if len(items) == 1 and os.path.isdir(items[0]):
        os.rename(items[0], "_wizard_source")
        shell.call("cp", "-R", "_wizard_source/.", ".")
        shutil.rmtree("_wizard_source")
        # populate empty directories with blank files
        for dirpath, dirnames, filenames in os.walk(os.getcwd()):
            if "/.git" in dirpath: continue
            if not filenames and not dirnames:
                open(os.path.join(dirpath, ".preserve-dir"), "w").write("")
        shell.call("git", "add", ".")

def parse_args(argv, baton):
    usage = """usage: %prog prepare-pristine APP-VERSION

This is the first command to run when preparing an update.

Clears out the current working directory (preserving only the .git directory),
and then download, extract and rm the tarball.  It will then add .preserve-dir
files to all empty directories, and then run 'git add .'.  It will refuse to do
this if there are any untracked files in the directory, or if you have any
local diffs: you can override this safety mechanism with --force.
"""
    parser = command.WizardOptionParser(usage)
    parser.add_option("-f", "--force", dest="force", action="store_true",
        default=False, help="Force a replacement, even if unversioned files exist.")
    options, args = parser.parse_all(argv)
    if len(args) < 1:
        parser.error("not enough arguments")
    elif len(args) > 1:
        parser.error("too many arguments")
    return options, args

def check_directory(options):
    if not os.path.exists(".git"):
        raise Exception("Not in root directory of Git repository")
    files = shell.eval("git", "ls-files", "-o")
    if files:
        raise Exception("Unversioned files exist, refusing to remove (override with --force)")
    try:
        shell.call("git", "rev-parse", "HEAD")
        _, _, ref = open(".git/HEAD").read().rstrip().partition(' ')
        if not options.force:
            if ref != "refs/heads/pristine" and os.path.exists(os.path.join(".git", ref)):
                raise Exception("Not on pristine branch (override with --force)")
            if shell.eval("git", "ls-files", "-m").strip() != "":
                raise Exception("Working copy is dirty (override with --force)")
        for f in os.listdir(os.getcwd()):
            if f == ".git": continue
            try:
                os.unlink(f)
            except OSError as e:
                shutil.rmtree(f)
    except shell.CallError:
        # We're on a git repo with no HEAD
        pass
