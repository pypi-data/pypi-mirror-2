#------------------------------------------------------------------------------
# Copyright (c) 2010, Kurt W. Smith
# 
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the Fwrap project nor the names of its contributors
#       may be used to endorse or promote products derived from this software
#       without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#------------------------------------------------------------------------------

# The monkey patches, method overrides, etc. in this file are here to patch
# numpy.distutils for fwrap's purposes.

import os, sys
import tempfile
import logging

from fwrap import gen_config as gc

from numpy.distutils import exec_command as np_exec_command
orig_exec_command = np_exec_command.exec_command

def fw_exec_command( command,
                  execute_in='', use_shell=None, use_tee = None,
                  _with_python = 1,
                  **env ):
    return orig_exec_command(command,
            execute_in=execute_in,
            use_shell=use_shell,
            use_tee=0, # we override this to control output.
            _with_python=_with_python,
            **env)

np_exec_command.exec_command = fw_exec_command

from numpy.distutils import ccompiler
ccompiler.exec_command = fw_exec_command
from numpy.distutils import unixccompiler
unixccompiler.exec_command = fw_exec_command

from numpy.distutils.core import DistutilsError

from numpy.distutils.command.config import config as np_config, old_config
from numpy.distutils.command.build_src import build_src as np_build_src
from numpy.distutils.command.build_ext import build_ext as np_build_ext
from numpy.distutils.command.scons import scons as npscons
from Cython.Distutils import build_ext as cy_build_ext
from numpy.distutils.core import setup as np_setup

def setup(log='fwrap_setup.log', *args, **kwargs):
    if log:
        _old_stdout, _old_stderr = sys.stdout, sys.stderr
        log = open(log, 'w')
        sys.stdout = log
        sys.stderr = log
    try:
        np_setup(*args, **kwargs)
    finally:
        if log:
            log.flush()
            log.close()
            sys.stdout, sys.stderr = _old_stdout, _old_stderr

def configuration(projname, extra_sources=None, **kw):
    def _configuration(parent_package='', top_path=None):
        from numpy.distutils.misc_util import Configuration
        config = Configuration(None, parent_package, top_path)

        def generate_type_config(ext, build_dir):
            config_cmd = config.get_config_cmd()
            return gen_type_map_files(config_cmd)

        sources = [generate_type_config] + \
                   (extra_sources or []) + \
                   [ '%s_fc.f90' % projname,
                     '%s.pyx' % projname,]

        config.add_extension(projname, sources=sources, **kw)

        return config

    return _configuration

def gen_type_map_files(config_cmd):
    ctps = gc.read_type_spec('fwrap_type_specs.in')
    find_types(ctps, config_cmd)
    gc.write_f_mod('fwrap_ktp_mod.f90', ctps)
    gc.write_header('fwrap_ktp_header.h', ctps)
    gc.write_pxd('fwrap_ktp.pxd', 'fwrap_ktp_header.h', ctps)
    gc.write_pxi('fwrap_ktp.pxi', ctps)
    return 'fwrap_ktp_mod.f90'

def find_types(ctps, config_cmd):
    for ctp in ctps:
        fc_type = None
        if ctp.lang == 'fortran':
            fc_type = find_fc_type(ctp.basetype,
                        ctp.odecl, config_cmd)
        elif ctp.lang == 'c':
            fc_type = find_c_type(ctp, config_cmd)
        if not fc_type:
            raise RuntimeError(
                    "unable to find C type for type %s" % ctp.odecl)
        ctp.fc_type = fc_type

def find_c_type(ctp, config_cmd):
    import numpy
    from distutils.sysconfig import get_python_inc
    if ctp.lang != 'c':
        raise ValueError("wrong language, given %s, expected 'c'" % ctp.lang)
    if ctp.basetype != 'integer':
        raise ValueError(
                "only integer basetype supported for C type discovery.")
    basetypes = ('signed char', 'short int',
                    'int', 'long int', 'long long int')
    expected = ['sizeof(%s)' % basetype for basetype in basetypes]
    result = config_cmd.check_type_size(type_name=ctp.odecl,
                    headers=['Python.h', 'numpy/arrayobject.h'],
                    include_dirs=[get_python_inc(), numpy.get_include()],
                    expected=expected)
    c_type = dict(zip(expected, basetypes))[result]
    return gc.c2f[c_type]

fc_type_memo = {}
def find_fc_type(base_type, decl, config_cmd):
    res = fc_type_memo.get((base_type, decl), None)
    if res is not None:
        return res
    #XXX: test to see if it works for gfortran
    if base_type == 'logical':
        base_type = 'integer'
        decl = decl.replace('logical', 'integer')
    for ctype in gc.type_dict[base_type]:
        test_decl = '%s(kind=%s)' % (base_type, ctype)
        fsrc = fsrc_tmpl % {'TYPE_DECL' : decl,
                            'TEST_DECL' : test_decl}
        print fsrc
        if config_cmd.try_compile(body=fsrc, lang='f90'):
            res = ctype
            break
    else:
        res = ''
    fc_type_memo[base_type, decl] = res
    return res

fsrc_tmpl = '''
subroutine outer(a)
  use, intrinsic :: iso_c_binding
  implicit none
  %(TEST_DECL)s, intent(inout) :: a
  interface
    subroutine inner(a)
      use, intrinsic :: iso_c_binding
      implicit none
      %(TYPE_DECL)s, intent(inout) :: a
    end subroutine inner
  end interface
  call inner(a)
end subroutine outer
'''

class fw_build_ext(np_build_ext):

    def build_extension(self, ext):
        from numpy.distutils.command.build_ext import (is_sequence,
                newer_group, log, filter_sources, get_numpy_include_dirs)
        sources = ext.sources
        if sources is None or not is_sequence(sources):
            raise DistutilsSetupError(
                ("in 'ext_modules' option (extension '%s'), " +
                 "'sources' must be present and must be " +
                 "a list of source filenames") % ext.name)
        sources = list(sources)

        if not sources:
            return

        fullname = self.get_ext_fullname(ext.name)
        if self.inplace:
            modpath = fullname.split('.')
            package = '.'.join(modpath[0:-1])
            base = modpath[-1]
            build_py = self.get_finalized_command('build_py')
            package_dir = build_py.get_package_dir(package)
            ext_filename = os.path.join(package_dir,
                                        self.get_ext_filename(base))
        else:
            ext_filename = os.path.join(self.build_lib,
                                        self.get_ext_filename(fullname))
        depends = sources + ext.depends

        if not (self.force or newer_group(depends, ext_filename, 'newer')):
            log.debug("skipping '%s' extension (up-to-date)", ext.name)
            return
        else:
            log.info("building '%s' extension", ext.name)

        extra_args = ext.extra_compile_args or []
        macros = ext.define_macros[:]
        for undef in ext.undef_macros:
            macros.append((undef,))

        c_sources, cxx_sources, f_sources, fmodule_sources = \
                   filter_sources(ext.sources)



        if self.compiler.compiler_type=='msvc':
            if cxx_sources:
                # Needed to compile kiva.agg._agg extension.
                extra_args.append('/Zm1000')
            # this hack works around the msvc compiler attributes
            # problem, msvc uses its own convention :(
            c_sources += cxx_sources
            cxx_sources = []

        # Set Fortran/C++ compilers for compilation and linking.
        if ext.language=='f90':
            fcompiler = self._f90_compiler
        elif ext.language=='f77':
            fcompiler = self._f77_compiler
        else: # in case ext.language is c++, for instance
            fcompiler = self._f90_compiler or self._f77_compiler
        cxx_compiler = self._cxx_compiler

        # check for the availability of required compilers
        if cxx_sources and cxx_compiler is None:
            raise DistutilsError, "extension %r has C++ sources" \
                  "but no C++ compiler found" % (ext.name)
        if (f_sources or fmodule_sources) and fcompiler is None:
            raise DistutilsError, "extension %r has Fortran sources " \
                  "but no Fortran compiler found" % (ext.name)
        if ext.language in ['f77','f90'] and fcompiler is None:
            self.warn("extension %r has Fortran libraries " \
                      "but no Fortran linker "
                      "found, using default linker" % (ext.name))
        if ext.language=='c++' and cxx_compiler is None:
            self.warn("extension %r has C++ libraries " \
                      "but no C++ linker "
                      "found, using default linker" % (ext.name))

        kws = {'depends':ext.depends}
        output_dir = self.build_temp

        include_dirs = ext.include_dirs + get_numpy_include_dirs()

        c_objects = []
        if c_sources:
            log.info("compiling C sources")
            c_objects = self.compiler.compile(c_sources,
                                              output_dir=output_dir,
                                              macros=macros,
                                              include_dirs=include_dirs,
                                              debug=self.debug,
                                              extra_postargs=extra_args,
                                              **kws)

        if cxx_sources:
            log.info("compiling C++ sources")
            c_objects += cxx_compiler.compile(cxx_sources,
                                              output_dir=output_dir,
                                              macros=macros,
                                              include_dirs=include_dirs,
                                              debug=self.debug,
                                              extra_postargs=extra_args,
                                              **kws)

        extra_postargs = []
        f_objects = []
        if fmodule_sources:
            log.info("compiling Fortran 90 module sources")
            module_dirs = ext.module_dirs[:]
            module_build_dir = os.path.join(
                self.build_temp,os.path.dirname(
                    self.get_ext_filename(fullname)))

            self.mkpath(module_build_dir)
            if fcompiler.module_dir_switch is None:
                existing_modules = glob('*.mod')
            extra_postargs += fcompiler.module_options(
                module_dirs,module_build_dir)

            #-----------------------------------------------------------------
            #XXX: hack, but the same can be said for this ENTIRE MODULE!
            # since fwrap only works with F90 compilers, fcompiler.compiler_f77
            # is None, so we replace it with fcompiler.compiler_fix, which is
            # an F90 compiler.
            #-----------------------------------------------------------------
            if fcompiler.compiler_f77 is None:
                fcompiler.compiler_f77 = fcompiler.compiler_fix

            f_objects += fcompiler.compile(fmodule_sources,
                                           output_dir=self.build_temp,
                                           macros=macros,
                                           include_dirs=include_dirs,
                                           debug=self.debug,
                                           extra_postargs=extra_postargs,
                                           depends=ext.depends)

            if fcompiler.module_dir_switch is None:
                for f in glob('*.mod'):
                    if f in existing_modules:
                        continue
                    t = os.path.join(module_build_dir, f)
                    if os.path.abspath(f)==os.path.abspath(t):
                        continue
                    if os.path.isfile(t):
                        os.remove(t)
                    try:
                        self.move_file(f, module_build_dir)
                    except DistutilsFileError:
                        log.warn('failed to move %r to %r' %
                                 (f, module_build_dir))
        if f_sources:
            log.info("compiling Fortran sources")
            f_objects += fcompiler.compile(f_sources,
                                           output_dir=self.build_temp,
                                           macros=macros,
                                           include_dirs=include_dirs,
                                           debug=self.debug,
                                           extra_postargs=extra_postargs,
                                           depends=ext.depends)

        objects = c_objects + f_objects

        if ext.extra_objects:
            objects.extend(ext.extra_objects)
        extra_args = ext.extra_link_args or []
        libraries = self.get_libraries(ext)[:]
        library_dirs = ext.library_dirs[:]

        linker = self.compiler.link_shared_object
        # Always use system linker when using MSVC compiler.
        if self.compiler.compiler_type=='msvc':
            # expand libraries with fcompiler libraries as we are
            # not using fcompiler linker
            self._libs_with_msvc_and_fortran(fcompiler,
                        libraries, library_dirs)

        # elif ext.language in ['f77','f90'] and fcompiler is not None:
            # linker = fcompiler.link_shared_object
        if ext.language=='c++' and cxx_compiler is not None:
            linker = cxx_compiler.link_shared_object

        if sys.version[:3]>='2.3':
            kws = {'target_lang':ext.language}
        else:
            kws = {}

        linker(objects, ext_filename,
               libraries=libraries,
               library_dirs=library_dirs,
               runtime_library_dirs=ext.runtime_library_dirs,
               extra_postargs=extra_args,
               export_symbols=self.get_export_symbols(ext),
               debug=self.debug,
               build_temp=self.build_temp,**kws)

class fw_build_src(np_build_src):

    def pyrex_sources(self, sources, extension):
        cbe = cy_build_ext(self.distribution)
        cbe.finalize_options()
        return cbe.cython_sources(sources, extension)

    def f2py_sources(self, sources, extension):
        # intercept to disable calling f2py
        return sources

class fw_config(np_config):

    def _check_compiler(self):
        old_config._check_compiler(self)
        from numpy.distutils.fcompiler import FCompiler, new_fcompiler

        if not isinstance(self.fcompiler, FCompiler):
            self.fcompiler = new_fcompiler(compiler=self.fcompiler,
                                           dry_run=self.dry_run,
                                           force=1,
                                           requiref90=True,
                                           c_compiler=self.compiler)
            if self.fcompiler is not None:
                self.fcompiler.customize(self.distribution)
                if self.fcompiler.get_version():
                    self.fcompiler.customize_cmd(self)
                    self.fcompiler.show_customization()
                else:
                    self.warn('f90_compiler=%s is not available.' %
                                self.fcompiler.compiler_type)
                    self.fcompiler = None

class _dummy_scons(npscons):
    def run(self):
        pass

fwrap_cmdclass = {'config' : fw_config,
                  'build_src' : fw_build_src,
                  'build_ext' : fw_build_ext,
                  'scons' : _dummy_scons}
