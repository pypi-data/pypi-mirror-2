"""distutils.command.upload

Implements the Distutils 'upload' subcommand (upload package to PyPI)."""

import datetime
from distutils.errors import DistutilsOptionError
from distutils.spawn import spawn
import os
import platform
import sys
import subprocess
import tempfile

from lpdistutils import LPCommand


class lpupload(LPCommand):

    description = "upload files to Launchpad"
    user_options = LPCommand.user_options + [
        ('sign', 's',
         'sign files to upload using gpg'),
        ('identity=', 'i', 'GPG identity used to sign files'),
        ('use-existing-sig', None,
         'Upload the signature from the pre-existing file'),
        ]
    boolean_options = LPCommand.boolean_options + ['sign', 'use-existing-sig']

    def initialize_options(self):
        LPCommand.initialize_options(self)
        self.sign = False
        self.identity = None
        self.use_existing_sig = False

    def finalize_options(self):
        LPCommand.finalize_options(self)
        if self.identity and not self.sign:
            raise DistutilsOptionError(
                "Must use --sign for --identity to have meaning"
            )

    def run(self):
        if not self.distribution.dist_files:
            raise DistutilsOptionError("No dist file created in earlier command")
        for command, pyversion, filename in self.distribution.dist_files:
            self.upload_file(command, pyversion, filename)

    def create_release(self, project, version):
        print "Release %s could not be found for project. Create it? (Y/n)" % version
        answer = sys.stdin.readline().strip().lower()
        if not answer.startswith('y'):
            sys.exit(0)
        milestone = None
        if len(project.series) != 1:
            eligble_series = []
            found = False
            for s in project.series:
                for m in s.all_milestones:
                    if m.name == version:
                        milestone = m
                        series = s
                        found = True
                        break
                if found:
                    break
            if series is None:
                print "Select a series to upload to:"
                for i, series in enumerate(project.series):
                    print "%d: %s" % (i+1, series.name)
                answer = int(sys.stdin.readline().strip())
                if answer < 1 or answer > len(series):
                    sys.exit(0)
                series = project.series[answer-1]
        else:
            series = project.series[0]

        release_date = datetime.date.today().strftime('%Y-%m-%d')
        if milestone is None:
            milestone = series.newMilestone(name=version,
                    date_targeted=release_date)
        return milestone.createProductRelease(date_released=release_date)

    def edit_file(self, prefix, description):
        (fd, f) = tempfile.mkstemp(prefix=prefix+'.')
        os.write(fd, '\n\n#------\n# Please enter the %s here. Lines which start with "#" are ignored.\n' %
                description)
        os.close(fd)
        subprocess.call(['sensible-editor', f])
        content = ''
        for l in open(f):
            if l.startswith('#'):
                continue
            content += l

        return content.strip()

    def upload_file(self, command, pyversion, filename):
        # Sign if requested
        if self.sign:
            gpg_args = ["gpg", "--detach-sign", "-a", filename]
            if self.identity:
                gpg_args[2:2] = ["--local-user", self.identity]
            spawn(gpg_args)

        # Fill in the data
        f = open(filename,'rb')
        content = f.read()
        f.close()
        basename = os.path.basename(filename)
        description = command
        if command=='bdist_egg' and self.distribution.has_ext_modules():
            description += " (built on %s)" % platform.platform(terse=1)
        if command == 'bdist_rpm':
            dist, version, id = platform.dist()
            if dist:
                description += ' (built for %s %s)' % (dist, version)
        elif command == 'bdist_dumb':
            description += ' (built for %s)' % platform.platform(terse=1)

        lpinfo = self.get_lpinfo()
        name = lpinfo.get_name()
        if name is None:
            name = self.distribution.get_name()
        version = self.distribution.metadata.version

        lp = self.get_lp()
        try:
            project = lp.projects[name]
        except KeyError:
            raise KeyError("Project %s not found." % name)

        release = None
        for rel in project.releases:
            if rel.version == version:
                release = rel
                break
        if release is None:
            release = self.create_release(project, version)

        kwargs = {}
        sig_filename = filename + ".asc"
        if self.sign or self.use_existing_sig:
            kwargs["signature_filename"] = os.path.basename(sig_filename)
            kwargs["signature_content"] = open(sig_filename).read()

        release.add_file(filename=basename, description=description,
                file_content=content, file_type="Code Release Tarball",
                content_type='application/x-gzip', **kwargs)

        changelog = self.edit_file('changelog', 'changelog')
        if changelog:
            release.changelog = changelog
        release_notes = self.edit_file('releasenotes', 'release notes')
        if release_notes:
            release.release_notes = release_notes

        release.lp_save()
