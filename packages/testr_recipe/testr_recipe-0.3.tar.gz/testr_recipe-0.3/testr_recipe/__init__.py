##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# Copyright (c) 2010 James Westby <james.westby@linaro.org>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

# Some code is taken from zc.recipe.testrunner

import os
import os.path
import pkg_resources
import sys
import zc.buildout.easy_install
import zc.recipe.egg

class Testr:

    def __init__(self, buildout, name, options):
        self.buildout = buildout
        self.name = name
        self.options = options
        options['script'] = os.path.join(buildout['buildout']['bin-directory'],
                                         options.get('script', self.name),
                                         )
        self.egg = zc.recipe.egg.Egg(buildout, name, options)

    def install(self):
        options = self.options
        dest = []
        reqs = []
        if options.get('test-packages', ''):
            reqs.append('python-subunit>0.0.5')
            reqs.append('discover')
            reqs.append('testtools>0.9.3')
        reqs.append('testrepository')
        eggs, ws = self.egg.working_set(reqs)

        test_paths = [ws.find(pkg_resources.Requirement.parse(spec)).location
                      for spec in eggs]

        wd = options.get('working-directory', '')
        if wd:
            wd = repr(os.path.abspath(wd))
            initialization = initialization_template % wd
        else:
            initialization = ""

        env_section = options.get('environment', '').strip()
        if env_section:
            env = self.buildout[env_section]
            for key, value in env.items():
                initialization += env_template % (key, value)

        defaults = options.get('defaults', '').strip()
        initialization += "argv = sys.argv[0:1] + "
        if not wd:
            base_dir = self.buildout['buildout']['directory']
            if self.egg._relative_paths:
                base_dir = _relativize(self.egg._relative_paths, base_dir)
            initialization += "['-d%s'] + " % base_dir
        if defaults:
            initialization += "(%s) + " % defaults
        initialization += "sys.argv[1:]\n"


        initialization_section = options.get('initialization', '').strip()
        if initialization_section:
            initialization += initialization_section

        dest.extend(zc.buildout.easy_install.scripts(
            [(options['script'], 'testrepository.commands', 'run_argv')],
            ws, options['executable'],
            self.buildout['buildout']['bin-directory'],
            extra_paths=self.egg.extra_paths,
            arguments="argv, sys.stdin, sys.stdout, sys.stderr",
            initialization = initialization,
            relative_paths = self.egg._relative_paths,
            ))

        if options.get('test-packages', ''):
            dest.extend(zc.buildout.easy_install.scripts(
                reqs, ws, options['executable'],
                self.buildout['buildout']['bin-directory'],
                interpreter=self.name+"py",
                extra_paths=self.egg.extra_paths,
                initialization = initialization,
                relative_paths = self.egg._relative_paths,
                ))
            target_conf_path = os.path.join(
                self.buildout['buildout']['directory'], '.testr.conf')
            config_values = {}
            config_values['test_packages'] = options.get('test-packages')
            interpreter = self.name+"py"
            interpreter_path = os.path.join(
                self.buildout['buildout']['bin-directory'], interpreter)
            if self.egg._relative_paths:
                interpreter_path = _relativize(
                    self.egg._relative_paths, interpreter_path)
            config_values['interpreter'] = interpreter_path
            configuration = configuration_template % config_values
            with open(target_conf_path, 'w') as f:
                f.write(configuration)
            dest.append(target_conf_path)

        return dest

    update = install

arg_template = """[
  '--test-path', %(TESTPATH)s,
  ]"""

initialization_template = """import os
sys.argv[0] = os.path.abspath(sys.argv[0])
os.chdir(%s)
"""

env_template = """os.environ['%s'] = %r
"""

configuration_template = """[DEFAULT]
test_command=%(interpreter)s -m subunit.run $IDLIST
test_id_list_default=discover %(test_packages)s
"""

def _relativize(base, path):
    base += os.path.sep
    if path.startswith(base):
        path = 'join(base, %r)' % path[len(base):]
    else:
        path = repr(path)
    return path
