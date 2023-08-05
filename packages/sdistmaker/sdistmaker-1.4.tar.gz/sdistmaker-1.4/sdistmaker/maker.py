import commands
import logging
import optparse
import os
import shutil
import sys
import tempfile


logger = logging.getLogger('maker')


class SdistCreationError(Exception):
    pass


def output(cmd):
    status, out = commands.getstatusoutput(cmd)
    if status is not 0:
        logger.error("Something went wrong:")
        logger.error(out)
        raise SdistCreationError()
    return out


def find_tarball(dist_dir, name, version):
    """Return correct tarball from dist/ dir (if found)

    We expect "name + '-' + version + '.tar.gz'", but we *can* get a
    -dev.r1234.tar.gz as that can be configured in a setup.cfg.  Not pretty,
    but we don't want to force anyone to modify old tags.  Let's look at .zip
    also right away instead of only at .tar.gz.  .zip is sometimes better for
    python2.4 due to a tarfile bug.

    """
    dir_contents = os.listdir(dist_dir)
    candidates = [tarball for tarball in dir_contents
                  if (tarball.endswith('.gz') or tarball.endswith('.zip'))
                  and tarball.startswith(name + '-' + version)]
    if not candidates:
        logger.error("No recognizable distribution found for %s, version %s",
                     name, version)
        logger.error("dist/ directory contents: %r", dir_contents)
        return
    if len(candidates) > 1:
        # Should not happen.
        logger.warn("More than one candidate distribution found: %r",
                    candidates)
    tarball = candidates[0]
    return tarball


def make_sdist(tag=None, destination=None, python=None):
    destination = os.path.abspath(destination)
    tempdir = tempfile.mkdtemp()
    original_dir = os.getcwd()
    if python is None:
        python = sys.executable
    setup = python + ' setup.py '

    cmd = 'svn co %s %s' % (tag, tempdir)
    logger.debug("Doing checkout of %s", tag)
    output(cmd)
    os.chdir(tempdir)

    logger.debug("Detecting name and version..")
    cmd = setup + '--name'
    name = output(cmd).strip()
    logger.debug("Name: %s", name)
    cmd = setup + '--version'
    version = output(cmd).strip()
    logger.debug("Version: %s", version)

    logger.debug("Making sdist tarball...")
    cmd = setup + 'sdist'
    logger.debug(output(cmd))

    targetdir = os.path.join(destination, name)
    if not name in os.listdir(destination):
        logger.info("Creating directory %s", targetdir)
        os.mkdir(targetdir)

    dist_dir = os.path.join(tempdir, 'dist')
    tarball = find_tarball(dist_dir, name, version)
    if not tarball:
        return
    target_filename = os.path.join(targetdir, tarball)
    logger.debug("Copying tarball to %s", target_filename)
    shutil.copy(os.path.join('dist', tarball),
                target_filename)
    os.chdir(original_dir)
    shutil.rmtree(tempdir)
    return target_filename


def main(tag=None, destination=None):
    """bin/make_sdist: create an sdist for a single tag"""
    usage = "Usage: %prog TAG DESTINATION"
    parser = optparse.OptionParser(usage=usage)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="Show debug output")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="Show minimal output")
    (options, args) = parser.parse_args()

    if options.verbose:
        log_level = logging.DEBUG
    elif options.quiet:
        log_level = logging.WARN
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level,
                        format="%(levelname)s: %(message)s")

    if tag is None:
        if len(args) == 0:
            logger.warn("Tag not specified")
            parser.print_help()
            sys.exit(1)
        tag = args.pop(0)
    if destination is None:
        if len(args) == 0:
            logger.warn("Destination not specified")
            parser.print_help()
            sys.exit(1)
        destination = args.pop()

    buildout_bindir = os.path.dirname(
        os.path.abspath(sys.argv[0]))
    python = os.path.join(buildout_bindir, 'python')
    if not os.path.exists(python):
        python = None

    filename = make_sdist(tag, destination, python)
    logger.info("Created %s", filename)
