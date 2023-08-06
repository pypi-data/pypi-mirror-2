# Copyright (c) 2007-2010 LOGILAB S.A. (Paris, FRANCE).
# http://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
"""The ldi command provides access to various subcommands to manipulate debian
packages and repositories
"""

import sys
import os
import os.path as osp
from glob import glob
# from itertools import chain

from logilab.common import clcommands as cli, shellutils as sht

from debinstall.__pkginfo__ import version
from debinstall import debrepo
from debinstall.debfiles import BadSignature, Changes

if osp.exists('/etc/debinstallrc'):
    RCFILE = '/etc/debinstallrc'
else:
    RCFILE = osp.expanduser('~/etc/debinstallrc')

LDI = cli.CommandLine('ldi', doc='Logilab debian installer', version=version,
                      logthreshold='INFO', rcfile=RCFILE)

OPTIONS = [
    ('distributions', # XXX to share with lgp
     {'type': 'csv', 'short': 'd', 'group': 'main',
      'help': 'comma separated list of distributions supported by the repository',
      'default': ['lenny', 'squeeze', 'sid'],
      }),
    ('repositories-directory',
     {'type': 'string', 'short': 'R', 'group': 'main',
      'help': 'directory where repositories are stored',
      }),
    ('upload-group',
     {'type': 'string', 'short': 'U', 'group': 'main',
      'help': 'Unix group granted to upload files',
      'default': None, #'debinstall',
      }),
    ('publish-group',
     {'type': 'string', 'short': 'P', 'group': 'main',
      'help': 'Unix group granted to publish repositories',
      'default': None, #'debinstall',
      }),
    ('checkers',
     {'type': 'csv', 'short': 'C', 'group': 'main',
      'help': 'comma separated list of checkers to run before package upload/publish',
      'default': ['lintian'],
      }),
    ]


def run():
    os.umask(006) # user in same group should be able to overwrite files
    LDI.run(sys.argv[1:])

def _repo_path(config, directory):
    if not osp.isabs(directory):
        if not config.repositories_directory:
            raise cli.CommandError(
                'Give either an absolute path to a directory that should '
                'hold the repository or a repository name and specify its '
                'directory using --repositories-directory')
        directory = osp.join(config.repositories_directory, directory)
    return directory

class LDICommand(cli.Command):
    def schmod(self, path, mode):
        """safe chmod, log on error"""
        try:
            os.chmod(path, mode)
        except OSError, ex:
            self.logger.error('cant change mode of %s to %s, fix this by '
                              'yourself (%s)', path, mode, ex)

    def schown(self, path, group):
        """safe chown, log on error"""
        try:
            sht.chown(path, group=group)
        except OSError, ex:
            self.logger.error('cant change group of %s to %s, fix this by '
                              'yourself (%s)', path, group, ex)

    def srm(self, path):
        """safe rm, log on error"""
        try:
            sht.rm(path)
        except OSError, ex:
            self.logger.error('cant remove %s, fix this by yourself (%s)',
                              path, ex)


class Create(LDICommand):
    """create a new repository"""
    name = "create"
    arguments = "<repository path or name>"
    min_args = max_args = 1
    options = OPTIONS + [
            ('update',
             {'action': 'store_true', 'short': 'u', 'group': 'main',
              'help': 'update an existing repository (add a distribution, change ownership...)',
              }),
        ]

    def run(self, args):
        repodir = _repo_path(self.config, args.pop(0))
        if self.config.update and not osp.exists(repodir):
            raise cli.CommandError("Repository %s doesn't exist" % repodir)
        # creation of the repository
        for subdir, group in (('incoming', self.config.upload_group),
                              ('dists', self.config.publish_group),
                              ('archive', self.config.publish_group)):
            subdir = osp.join(repodir, subdir)
            for distname in self.config.distributions:
                if not osp.isdir(subdir):
                    os.makedirs(subdir)
                if group:
                    self.schown(subdir, group=group)
                self.schmod(subdir, 02775) # sticky group
                distribdir = osp.join(subdir, distname)
                if not osp.isdir(distribdir):
                    os.makedirs(distribdir)
                    self.logger.info('created %s', distribdir)
                else:
                    self.logger.info('%s directory already exists', distribdir)
                    if group:
                        self.schown(distribdir, group=group)
                    self.schmod(distribdir, 02775) # sticky group
                if group and self.config.update:
                    for fname in os.listdir(distribdir):
                        self.schown(osp.join(distribdir, fname), group=group)


LDI.register(Create)


class Upload(LDICommand):
    """upload a new package to the incoming queue of a repository"""
    name = "upload"
    min_args = 2
    arguments = "[options] <repository> <package.changes>..."
    options = OPTIONS[1:] + [
        ('check-signature',
         {'type': 'yn', 'group': 'upload',
          'help': 'Check package signature before upload',
          'default': True,
          }),
        ('remove',
         {'short': 'r', 'action': 'store_true',
          'help': 'remove debian changes file',
          'default': False,
          }),
        ('distribution',
         {'help': 'force a specific target distribution',
          }),
        ]

    def run(self, args):
        repo = self._check_repository(_repo_path(self.config, args.pop(0)))
        self.debian_changes = {}
        for filename in args:
            changes = self._check_changes_file(filename)
            if self.config.distribution:
                distrib = self.config.distribution
            else:
                distrib = changes['Distribution']
            try:
                distribdir = repo.check_distrib('incoming', distrib)
            except cli.CommandError, ex:
                self.logger.error(ex)
                # drop the current changes file
                continue
            self._check_signature(changes)
            self._run_checkers(changes)
            if self.config.remove:
                move = sht.mv
            else:
                move = sht.cp
            self.process_changes_file(changes, distribdir,
                                      self.config.upload_group, move)

    def _check_repository(self, repodir):
        if not osp.isdir(repodir):
            raise cli.CommandError("Repository %s doesn't exist" % repodir)
        for section in ('dists', 'incoming'):
            subdir = osp.join(repodir, section)
            if not osp.isdir(subdir):
                raise cli.CommandError(
                    "Repository %s isn't properly initialized (no %r directory)"
                    % (repodir, section))
        return debrepo.DebianRepository(self.logger, repodir)

    def _check_changes_file(self, changes_file):
        """basic tests to determine debian changes file"""
        if not changes_file.endswith('.changes'):
            raise cli.CommandError(
                '%s is not a debian changes file (bad extension)' % changes_file)
        if not osp.isfile(changes_file):
            raise cli.CommandError(
                '%s doesn\'t exist or is not a regulary file' % changes_file)
        try:
            return Changes(changes_file)
        except Exception, ex:
            raise cli.CommandError(
                '%s is not a debian changes file: %s' % (changes_file, ex))

    def _check_signature(self, changes):
        """raise error if the changes files and appropriate dsc files are not
        correctly signed
        """
        if self.config.check_signature:
            try:
                changes.check_sig()
            except BadSignature, ex:
                raise cli.CommandError(
                    "%s. Check if the PGP block exists and if the key is in your "
                    "keyring" % ex)

    def _run_checkers(self, changes):
        checkers = self.config.checkers
        try:
            changes.run_checkers(checkers)
        except Exception, ex:
            raise cli.CommandError(str(ex))

    def _files_to_keep(self, changes):
        # In case of multi-arch in same directory, we need to check if parts
        # of changes files are not required by another changes files We're
        # excluding the current parsed changes file
        mask = "%s*.changes" % changes.filename.rsplit('_', 1)[0]
        ochanges = glob(osp.join(changes.dirname, mask))
        ochanges.remove(changes.path)
        # Find intersection of files shared by several 'changes'
        allfiles = changes.get_all_files()
        result = allfiles & set([f for c in ochanges
                                 for f in Changes(c).get_all_files()])
        if result:
            self.logger.warn("keep intact changes file's parts "
                             "required by another architecture(s)")
            return result
        pristine = changes.get_pristine()
        if pristine:
            # Another search to preserve pristine tarball in case of multiple
            # revision of the same upstream release
            # We're excluding the current parsed changes file
            mask = "%s*.changes" % changes.filename.rsplit('-', 1)[0]
            ochanges = glob(osp.join(changes.dirname, mask))
            ochanges.remove(changes.path)
            # Check if the detected changes files really needs the tarball
            result = set([r for r in ochanges
                          if Changes(r).get_pristine() == pristine])
            if result:
                self.logger.warn("keep intact original pristine tarball "
                                 "required by another Debian revision(s)")
            return result
        return set()

    def process_changes_file(self, changes, distribdir, group,
                             move=sht.cp, rm=False):
        allfiles = changes.get_all_files()
        # Logilab uses trivial Debian repository and put all generated files in
        # the same place. Badly, it occurs some problems in case of several
        # supported architectures and multiple Debian revision (in this order)
        if move is sht.mv:
            tokeep = self._files_to_keep(changes)
            rm = False
        else:
            tokeep = ()
        for filename in allfiles:
            if filename in tokeep:
                move_ = sht.cp
            else:
                move_ = move
            destfile = osp.join(distribdir, osp.basename(filename))
            self.logger.debug("%s %s %s", move_.__name__, filename, destfile)
            move_(filename, distribdir)
            if group:
                self.schown(destfile, group=group)
            self.schmod(destfile, 0664)
        if rm:
            tokeep = allfiles
        if tokeep:
            for filename in tokeep:
                self.logger.debug("rm %s", filename)
                self.srm(filename)
        distrib = osp.basename(distribdir)
        changeslist = self.debian_changes.setdefault(distrib, [])
        changeslist.append(osp.join(distribdir, changes.filename))

LDI.register(Upload)


class Publish(Upload):
    """process the incoming queue of a repository"""
    name = "publish"
    min_args = 1
    arguments = "<repository> [<package.changes>...]"
    options = OPTIONS[1:] + [
        ('check-signature',
         {'type': 'string', 'group': 'publish',
          'help': 'Check package signature before publish',
          }),
        ('gpg-keyid',
         {'type': 'string', 'group': 'publish',
          'help': 'GPG identifier of the key to use to sign the repository',
          }),
        ('refresh',
         {'action': "store_true", 'short': 'r',
          'help': 'refresh the whole repository index files',
          'default': False,
          }),
        ]

    def run(self, args):
        repo = self._check_repository(_repo_path(self.config, args.pop(0)))
        distribs = set()
        # we have to launch the publication sequentially
        lockfile = osp.join(repo.directory, 'ldi.lock')
        sht.acquire_lock(lockfile, max_try=3, delay=5)
        self.debian_changes = {}
        try:
            changes_files = repo.incoming_changes_files(args)
            if not changes_files and not self.config.refresh:
                self.logger.error("no changes file to publish in %s",
                                  repo.incoming_directory)
            for filename in changes_files:
                # distribution name is the same as the incoming directory name
                # it lets override a valid suite by a more private one (for
                # example: contrib, volatile, experimental, ...)
                distrib = osp.basename(osp.dirname(filename))
                destdir = repo.check_distrib('dists', distrib)
                changes = self._check_changes_file(filename)
                self._check_signature(changes)
                self._run_checkers(changes)
                # perform a copy instead of a move to reset file ownership
                self.process_changes_file(changes, destdir,
                                          self.config.publish_group, rm=True)
                # mark distribution to be refreshed at the end
                distribs.add(distrib)
            repo.generate_aptconf()
            if self.config.refresh:
                distribs = ('*',)
            for distrib in distribs:
                self._apt_refresh(repo, distrib)
        finally:
            sht.release_lock(lockfile)

    def _apt_refresh(self, repo, distrib="*"):
        for distdir in glob(osp.join(repo.dists_directory, distrib)):
            if osp.isdir(distdir) and not osp.islink(distdir):
                repo.dist_publish(osp.basename(distdir))
                if self.config.gpg_keyid:
                    self.logger.info('signing release')
                    repo.sign(distdir, self.config.gpg_keyid)

LDI.register(Publish)


# class List(Upload):
#     """list all repositories and their distributions"""
#     name = "list"
#     min_args = 0
#     max_args = sys.maxint
#     arguments = "[repository [-d | --distribution] [package.changes ...]]"
#     opt_specs = [
#                  ('-d', '--distribution',
#                    {'dest': 'distribution',
#                     'help': 'list a specific target distribution',
#                    }),
#                  ('-s', '--section',
#                    {'dest': 'section',
#                     'help': "directory that contains the dist nodes ('incoming' or 'dists')",
#                     'default': 'incoming'
#                    }),
#                  ('-o', '--orphaned',
#                    {'dest': 'orphaned',
#                     'action': "store_true",
#                     'default': False,
#                     'help': 'report orphaned packages or files (can be slow)'
#                    }),
#                 ]

#     def process(self):
#         if not self.args:
#             destdir = self.get_config_value('destination')
#             repositories = self.get_repo_list()
#             self.logger.info("%s available repositories in '%s'"
#                              % (len(repositories), destdir))
#             repositories = sorted([repository for repository in repositories])
#             print(os.linesep.join(repositories))
#             return

#         repository = self.args[0]
#         path = self._check_repository(repository, self.options.section)
#         if len(self.args)==1 and not self.options.distribution:
#             lines = []
#             for root, dirs, files in os.walk(path):
#                 orphaned = list()
#                 if dirs:
#                     for d in dirs:
#                         line = "%s/%s" % (repository, d)
#                         if osp.islink(osp.join(root, d)):
#                             line += ' is symlinked to %s' % os.readlink(osp.join(root, d))
#                         else:
#                             nb = len(glob(osp.join(root, d, "*.changes")))
#                             if nb:
#                                 line += " contains %d changes files" % nb
#                             else:
#                                 line += " is empty"
#                             if self.options.orphaned:
#                                 orphaned = self.get_orphaned_files(path, d)
#                                 if orphaned:
#                                     line += " and %d orphaned files" % len(orphaned)
#                         lines.append(line)
#             self.logger.info("%s: %s available distribution(s) in '%s' section"
#                              % (repository, len(lines), self.options.section))
#             for line in lines: print line
#         else:
#             self._print_changes_files(repository, self.options.section,
#                                       self.options.distribution)
#             if self.options.orphaned:
#                 orphaned = self.get_orphaned_files(path, self.options.distribution)
#                 if orphaned:
#                     self.logger.warn("%s: has %s orphaned file(s)"
#                                      % (repository, len(orphaned)))
#                     print '\n'.join(orphaned)

#         if self.options.section == 'incoming':
#             self.logger.info("use option 'ldi list -s dists %s' to list published content" % repository)

#     def _print_changes_files(self, repository, section, distribution):
#         """print information about a repository and inside changes files"""
#         filenames = self._find_changes_files(repository, section, distribution)

#         if not filenames:
#             self.logger.warn("%s/%s: no changes file found" % (repository,
#                                                                distribution))
#         else:
#             self.logger.info("%s/%s: %s available changes files"
#                              % (repository, distribution, len(filenames)))
#             filenames = [filename.rsplit('/', 4)[1:] for filename in filenames]
#             for f in filenames:
#                 print("%s/%s: %s" % (f[0], f[2], f[-1]))

#     def get_repo_list(self):
#         """return list of repository and do some checks"""
#         destdir = self.get_config_value('destination')
#         confdir = self.get_config_value('configurations')

#         repositories = []
#         for dirname in os.listdir(destdir):
#             # Some administrators like to keep configuration files
#             # in the same directory that the whole repositories
#             if os.path.realpath(os.path.join(destdir, dirname)) == os.path.realpath(confdir):
#                 self.logger.debug('skipping debinstall configuration directory %s', confdir)
#                 continue
#             config = osp.join(confdir, '%s-%s.conf')
#             for conf in ('apt', 'ldi'):
#                 conf_file = config % (dirname, conf)
#                 if not osp.isfile(conf_file):
#                     self.logger.error('could not find %s', conf_file)
#                     break
#             else:
#                 repositories.append(dirname)
#         return repositories

#     def get_orphaned_files(self, repository, distrib):
#         import fnmatch
#         changes_files = (glob(os.path.join(repository, distrib,
#                                                 '*.changes')))
#         tracked_files = (Changes(f).get_all_files(check_if_exists=False)
#                          for f in changes_files if f)
#         tracked_files = set(tuple(chain(*tracked_files)))

#         untracked_files = set([f for f in glob(os.path.join(repository, distrib, '*'))])
#         orphaned_files = untracked_files - tracked_files
#         orphaned_files -= set(fnmatch.filter(orphaned_files, "*/Packages*"))
#         orphaned_files -= set(fnmatch.filter(orphaned_files, "*/Sources*"))
#         orphaned_files -= set(fnmatch.filter(orphaned_files, "*/Contents*"))
#         orphaned_files -= set(fnmatch.filter(orphaned_files, "*/Release*"))
#         return orphaned_files


class Diff(Upload):
    """Show diffs between files published in a repository and not in another,
    proposing to upload them.

    Useful to handle a stable version of a repository by selecting which
    packages are considered as stable. If you upload some package, you should
    then run 'ldi publish' on the target repository
    """
    name = "diff"
    min_args = max_args = 2
    arguments = "<repository> <target repository>"
    options = OPTIONS[:2] + [
        ]

    def run(self, args):
        if 'all' in self.config.distributions:
            dists = None
        else:
            dists = self.config.distributions
        repo = self._check_repository(_repo_path(self.config, args.pop(0)))
        trepo = self._check_repository(_repo_path(self.config, args.pop(0)))
        self.logger.debug('**** analyzing repo %s', repo.ldiname)
        repo1 = repo.packages_index(dists=dists)
        self.logger.debug('**** analyzing repo %s', trepo.ldiname)
        repo2 = {}
        for dist, archi, package, version in trepo.iter_changes_files(dists=dists):
            repo2[package] = max(repo2.get(package), version)
            try:
                repo1[package][dist][archi] = [v for v in repo1[package][dist][archi]
                                               if v > version]
            except KeyError:
                self.logger.warning('no package for %s %s %s in %s',
                                    dist, archi, package, repo.ldiname)
        if repo1:
            print '-'*80
            print 'packages in %s which are not in %s:' % (repo.ldiname, trepo.ldiname)
            for package in sorted(repo1):
                missing = {}
                for dist, distinfo in repo1[package].iteritems():
                    for archi, versions in distinfo.iteritems():
                        for version in versions:
                            missing.setdefault(version, []).append('%s-%s' % (dist, archi))
                if missing:
                    repo2version = repo2.get(package, 'no version released')
                    print '* %s (%s)' % (package, repo2version)
                    lastversion = None
                    for version in reversed(sorted(missing)):
                        if lastversion is not None and debrepo.major_version(version) == lastversion:
                            continue
                        print '  - %s (%s)' % (version, ', '.join(missing[version])),
                        lastversion = debrepo.major_version(version)
                        if repo2version == version:
                            print 'MISSING DIST / ARCH'
                        else:
                            print 'UNRELEASED'
                        if sht.ASK.confirm('upload to %s?' % trepo.ldiname):
                            for distarch in missing[version]:
                                dist, arch = distarch.split('-')
                                changes = osp.join(repo.directory, 'dists', dist,
                                                   debrepo.changesfile(package, version, arch))
                                os.system('ldi upload %s %s' % (trepo.directory, changes))

LDI.register(Diff)


class Reduce(Upload):
    """Reduce packages published in a repository.

    When a package has version X.Y.Z publish, automatically delete all versions
    between X.Y.0 and X.Y.(Z - 1).
    """
    name = "reduce"
    min_args = max_args = 1
    arguments = "<repository>"
    options = [OPTIONS[1]] + [
        ('package',
         {'type': 'string', 'short': 'p',
          'help': 'package to reduce',
          }),
        ]

    def run(self, args):
        repo = self._check_repository(_repo_path(self.config, args.pop(0)))
        idx = repo.packages_index(self.config.package)
        for package in sorted(idx):
            for dist, distinfo in idx[package].iteritems():
                for archi, versions in distinfo.iteritems():
                    try:
                        repo.reduce_package(dist, package, versions, archi)
                    except:
                        self.logger.exception('error while processing %s %s %s',
                                              dist, package, archi)

LDI.register(Reduce)


class Archive(Upload):
    """Archive some versions of a package published in a repository."""
    name = "archive"
    min_args = max_args = 3
    arguments = "<repository> <source package> <up to version>"
    options = [OPTIONS[1]] + [
        ('down-to-version',
         {'type': 'string', 'short': 'u',
          'help': 'don\'t remove package with version prior to given value',
          }),
        ]

    def run(self, args):
        repo = debrepo.DebianRepository(_repo_path(self.config, args.pop(0)))
        sourcepackage = args.pop(0)
        baseversion = debrepo.Version(args.pop(0))
        if self.config.down_to_version is None:
            downtoversion = None
        else:
            downtoversion = debrepo.Version(self.config.down_to_version)
        isdebianversion = '-' in baseversion
        for dist, archi, package, version in repo.iter_changes_files(package=sourcepackage):
            upstreamversion = debrepo.split_version(version)[0]
            if isdebianversion:
                if version > baseversion:
                    continue
            elif upstreamversion > baseversion:
                continue
            if downtoversion is not None and upstreamversion < downtoversion:
                continue
            repo.archive_package(dist, package, version, archi)

LDI.register(Archive)


if __name__ == '__main__':
    run()
