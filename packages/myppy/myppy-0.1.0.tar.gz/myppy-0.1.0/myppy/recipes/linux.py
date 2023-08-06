#  Copyright (c) 2009-2010, Cloud Matrix Pty. Ltd.
#  All rights reserved; available under the terms of the BSD License.

from __future__ import with_statement

import os
import sys
import tempfile
import stat
import urlparse
import urllib2
import subprocess
import shutil
from textwrap import dedent

from myppy.util import md5file, do, bt, cd, relpath, tempdir, chstdin

from myppy.recipes import base

class Recipe(base.Recipe):

    @property
    def LDFLAGS(self):
        libdir = os.path.join(self.target.PREFIX,"lib")
        return "-static-libgcc -L%s" % (libdir,)

    @property
    def CFLAGS(self):
        incdir = os.path.join(self.target.PREFIX,"include")
        return "-D_GNU_SOURCE -I%s -static-libgcc" % (incdir,)

    @property
    def CXXFLAGS(self):
        incdir = os.path.join(self.target.PREFIX,"include")
        return "-D_GNU_SOURCE -I%s -static-libgcc" % (incdir,)

    @property
    def LD_LIBRARY_PATH(self):
        return os.path.join(self.target.PREFIX,"lib")

    @property
    def PKG_CONFIG_PATH(self):
        return os.path.join(self.target.PREFIX,"lib/pkgconfig")

    @property
    def CONFIGURE_VARS(self):
        return ["CC=apgcc","CXX=apg++","LDFLAGS="+self.LDFLAGS,
                "CFLAGS="+self.CFLAGS,"CXXFLAGS="+self.CXXFLAGS,
                "LD_LIBRARY_PATH="+self.LD_LIBRARY_PATH,
                "PKG_CONFIG_PATH="+self.PKG_CONFIG_PATH] 

    def _generic_configure(self,script=None,vars=None,args=None,env={}):
        if vars is None and self.CONFIGURE_VARS is None:
            env = env.copy()
            env.setdefault("LDFLAGS",self.LDFLAGS)
            env.setdefault("CFLAGS",self.CFLAGS)
            env.setdefault("CXXFLAGS",self.CXXFLAGS)
            env.setdefault("LD_LIBRARY_PATH",self.LD_LIBRARY_PATH)
            env.setdefault("PKG_CONFIG_PATH",self.PKG_CONFIG_PATH)
        super(Recipe,self)._generic_configure(script,vars,args,env)

    def _generic_make(self,vars=None,relpath=None,env={}):
        """Do a generic "make" for this recipe."""
        env = env.copy()
        env.setdefault("LD_LIBRARY_PATH",self.LD_LIBRARY_PATH)
        workdir = self._get_builddir()
        if vars is None:
            vars = self.MAKE_VARS
        if relpath is None:
            relpath = self.MAKE_RELPATH
        cmd = ["make",]
        if vars is not None:
            cmd.extend(["CC=apgcc","CXX=apg++"])
            cmd.extend(vars)
        cmd.extend(("-C",os.path.join(workdir,relpath)))
        self.target.do(*cmd,env=env)

    def _generic_makeinstall(self,vars=None,relpath=None,env={}):
        """Do a generic "make install" for this recipe."""
        workdir = self._get_builddir()
        if vars is None:
            vars = self.MAKE_VARS
        if relpath is None:
            relpath = self.MAKE_RELPATH
        cmd = ["make"]
        if vars is not None:
            cmd.extend(["CC=apgcc","CXX=apg++"])
            cmd.extend(vars)
        cmd.extend(("-C",os.path.join(workdir,relpath),"install"))
        self.target.do(*cmd,env=env)

    def _generic_pyinstall(self,relpath="",args=[],env={}):
        env = env.copy()
        env.setdefault("LDFLAGS",self.LDFLAGS)
        env.setdefault("CFLAGS",self.CFLAGS)
        env.setdefault("CXXFLAGS",self.CXXFLAGS)
        env.setdefault("LD_LIBRARY_PATH",self.LD_LIBRARY_PATH)
        env.setdefault("PKG_CONFIG_PATH",self.PKG_CONFIG_PATH)
        super(Recipe,self)._generic_pyinstall(relpath,args,env)


class CMakeRecipe(base.CMakeRecipe,Recipe):
    def _generic_cmake(self,relpath=".",args=[],env={}):
        env = env.copy()
        env.setdefault("LDFLAGS",self.LDFLAGS)
        env.setdefault("CFLAGS",self.CFLAGS)
        env.setdefault("CXXFLAGS",self.CXXFLAGS)
        env.setdefault("LD_LIBRARY_PATH",self.LD_LIBRARY_PATH)
        env.setdefault("PKG_CONFIG_PATH",self.PKG_CONFIG_PATH)
        super(CMakeRecipe,self)._generic_cmake(relpath,args,env)

class PyRecipe(base.PyRecipe,Recipe):
    pass


class cmake(base.cmake,Recipe):
    def _patch(self):
        super(cmake,self)._patch()
        def stub_out_device_functions(lines):
            for ln in lines:
                if ln.startswith("archive_entry_dev") or ln.startswith("archive_entry_rdev"):
                    yield ln
                    ln = lines.next()
                    assert ln.strip() == "{"
                    yield ln
                    while ln.strip() != "}":
                        ln = lines.next()
                    yield "    return 0;"
                    yield ln
                else:
                    yield ln
        self._patch_build_file("Utilities/cmlibarchive/libarchive/archive_entry.c",stub_out_device_functions)

class apbuild_base(Recipe):
    SOURCE_URL = "http://autopackage.googlecode.com/files/autopackage-1.4.2-x86.tar.bz2"
    SOURCE_MD5 = "4a4cb89586d817d2d0c4a840b8d4ff0c"
    def build(self):
        pass
    def install(self):
        with tempdir() as workdir:
            updir = self._unpack()
            try:
                with chstdin("y"):
                    self.target.do("bash",os.path.join(updir,"install"),"--prefix",self.target.PREFIX,"--silent")
            except subprocess.CalledProcessError:
                pass
        open(os.path.join(self.target.PREFIX,"lib","apbuild-base--installed.txt"),"wb").close()


class apbuild(Recipe):
    DEPENDENCIES = ["apbuild_base"]
    SOURCE_URL = "http://autopackage.googlecode.com/files/Autopackage%20Development%20Environment%201.4.2.package"
    SOURCE_MD5 = "f0f43ab85350078349246441fb3304c6"
    def build(self):
        pass
    def install(self):
        src = self.target.fetch(self.SOURCE_URL)
        self.target.do("bash",src)
        #  The apgcc installer doesn't error out when it fails.
        #  Check that apgcc is actually available.
        self.target.do("apgcc","-v")
        shutil.move(os.path.join(self.target.PREFIX,"bin/.proxy.apgcc"),
                    os.path.join(self.target.PREFIX,"bin/apgcc"))
        #  Hack it to correctly detect pre-compiled header generation with
        #  the calling convention used by wxWidgets.
        def fix_pch_detection(lines):
            for ln in lines:
               if ln.strip().startswith("$files++ if ("):
                   yield "\t\t# exclude gch or gch.d to hack PCH detection\n"
                   yield "\t\t$files++ if (!(/^-/) && !(/gch$/) && !(/gch.d/));\n"
               else:
                   yield ln
        self._patch_file("share/apbuild/Apbuild/GCC.pm",fix_pch_detection)

    

class python26(base.python26,Recipe,):
    """Install the basic Python interpreter, with myppy support."""
    DEPENDENCIES = ["lib_openssl"]
    def _configure(self):
        super(python26,self)._configure()
        #  Can't link epoll without symbols from a later libc.
        #  We'll have to settle for old-fashioned select().
        def remove_have_epoll(lines):
            for ln in lines:
                if "HAVE_EPOLL" not in ln:
                    yield ln
        self._patch_build_file("pyconfig.h",remove_have_epoll)


class patchelf(Recipe):
    SOURCE_URL = "http://hydra.nixos.org/build/114505/download/2/patchelf-0.5.tar.bz2"
    SOURCE_MD5 = "c41fc98091d15dc93ba876c3ef11f43c"


class lib_openssl(base.lib_openssl,Recipe):
    def _configure(self):
        super(lib_openssl,self)._configure()
        def ensure_gnu_source(lines):
            for ln in lines:
                if ln.startswith("CFLAG="):
                    yield ln.strip() + " -D_GNU_SOURCE\n"
                else:
                    yield ln
        self._patch_build_file("Makefile",ensure_gnu_source)


class py_cxfreeze(PyRecipe):
    DEPENDENCIES = ["python26"]
    SOURCE_URL = "http://downloads.sourceforge.net/project/cx-freeze/4.2/cx_Freeze-4.2.tar.gz"


class py_bbfreeze(PyRecipe):
    DEPENDENCIES = ["python26"]
    SOURCE_URL = "http://pypi.python.org/packages/source/b/bbfreeze/bbfreeze-0.96.5.tar.gz"
    def _patch(self):
        super(py_bbfreeze,self)._patch()
        def add_double_link_libs(lines):
            for ln in lines:
                yield ln
                if ln.strip() == "libs.append(conf.PYTHONVERSION)":
                    yield "            libs.extend(libs[:-1])"
        self._patch_build_file(src,"setup.py",add_double_link_libs)
        def add_support_for_pyw_files(lines):
            for ln in lines:
                yield ln
                if ln.strip() == "fn = fn[:-3]":
                    yield 12*" " + "elif fn.endswith('.pyw'):\n"
                    yield 16*" " + "fn = fn[:-4]\n"
        self._patch_build_file(src,"bbfreeze/freezer.py",add_support_for_pyw_files)


class lib_gtk(Recipe):
    DEPENDENCIES = ["lib_glib","lib_pango","lib_atk","lib_tiff"]
    SOURCE_URL = "http://ftp.gnome.org/pub/gnome/sources/gtk+/2.8/gtk+-2.8.0.tar.gz"
    def _patch(self):
        #  We need access to the deprecated GMemChunk type when compiling
        #  against glib-2.10.  Hack the makefiles to avoid hiding it.
        def undisable_deprecated(lines):
            for ln in lines:
               if ln.strip() == "-DG_DISABLE_DEPRECATED":
                   pass
               elif "-DG_DISABLE_DEPRECATED" in ln:
                   yield ln.replace("-DG_DISABLE_DEPRECATED","")
               else:
                   yield ln
        workdir = self._get_builddir()
        for fnm in self.target.bt("find",workdir,"-name","Makefile").split():
            self._patch_file(fnm,undisable_deprecated)
        for fnm in self.target.bt("find",workdir,"-name","Makefile.am").split():
            self._patch_file(fnm,undisable_deprecated)
        for fnm in self.target.bt("find",workdir,"-name","Makefile.in").split():
            self._patch_file(fnm,undisable_deprecated)


class lib_qt4(base.lib_qt4,Recipe):
    #  Build against an older version of fontconfig, so it doesn't suck
    #  in symbols that aren't available on older linuxen.
    DEPENDENCIES = ["lib_fontconfig"]
    @property
    def CONFIGURE_ARGS(self):
        args = list(super(lib_qt4,self).CONFIGURE_ARGS)
        args.extend(["-no-feature-inotify","-no-glib",])
        return args
    def _patch(self):
        #  Disable some functions only available on newer linuxes.
        #  Fortunately qt provides runtime fallbacks for these.
        def dont_use_newer_funcs(lines):
            for ln in lines:
                if "pipe2" in ln:
                    yield ln.replace("pipe2","disabled_pipe2")
                elif "dup3" in ln:
                    yield ln.replace("dup3","disabled_dup3")
                elif "accept4" in ln:
                    yield ln.replace("accept4","disabled_accept4")
                else:
                    yield ln
        self._patch_build_file("src/corelib/kernel/qcore_unix_p.h",dont_use_newer_funcs)
        self._patch_build_file("src/network/socket/qnet_unix_p.h",dont_use_newer_funcs)


class lib_wxwidgets_base(base.lib_wxwidgets_base,Recipe):
    DEPENDENCIES = ["lib_gtk","lib_png","lib_jpeg","lib_tiff"]
    #  Use of std_iostreams seems to suck in newer glibc symbols, so
    #  we explicitly disable it until someone proves it's needed.
    CONFIGURE_ARGS = ["--with-gtk","--disable-std_iostreams"]
    CONFIGURE_ARGS.extend(base.lib_wxwidgets_base.CONFIGURE_ARGS)


class lib_sparsehash(Recipe):
    """Google sparehash, using old hash function APIs.

    This installs a private copy of the google sparsehash library, tricked into
    sucking in old definitions for hash_fun.h rather than the ones provided by
    tr1.  Other libraries can then avoid sucking in the tr1 symbols.
    """
    SOURCE_URL = "http://google-sparsehash.googlecode.com/files/sparsehash-1.9.tar.gz"
    def _patch(self):
        super(lib_sparsehash,self)._patch()
        def dont_use_tr1(lines):
            for ln in lines:
                yield ln.replace("tr1/","tr1_DONT_USE_ME/")
        self._patch_build_file("configure",dont_use_tr1)
        def include_typeinfo(lines):
            ln = lines.next()
            while not ln.startswith("#include"):
                yield ln
                ln = lines.next()
            yield "#include <typeinfo>\n"
            yield ln
            for ln in lines:
                yield ln
        self._patch_build_file("src/hashtable_test.cc",include_typeinfo)


class lib_shiboken(base.lib_shiboken,CMakeRecipe):
    #  Use a private build of google sparsehash, so we don't pull
    #  in symbols from C++ TR1 hashtable spec.
    DEPENDENCIES = ["lib_sparsehash"]
    @property
    def CXXFLAGS(self):
        flags = super(lib_shiboken,self).CXXFLAGS
        flags += " -I" + os.path.join(self.target.PREFIX,"include")
        return flags
    def _patch(self):
        super(lib_shiboken,self)._patch()
        #  Provide hash function implementations that would be automatically
        #  provided by tr1, but are missing in the backwards-compat code.
        def provide_hash_funcs(lines):
            for ln in lines:
                if "namespace Shiboken" in ln:
                    break
                yield ln
            yield dedent("""
                      #include <hash_fun.h>
                      namespace __gnu_cxx {
                      template<>
                      struct hash<void *> {
                          size_t operator()(const void * __x) const {
                              return reinterpret_cast<size_t>(__x); }
                          };
                      template<>
                      struct hash<const void *> {
                          size_t operator()(const void * __x) const {
                              return reinterpret_cast<size_t>(__x); }
                          };
                      template<>
                      struct hash<SbkObjectType *> {
                          size_t operator()(const SbkObjectType * __x) const {
                              return reinterpret_cast<size_t>(__x); }
                          };
                      template<>
                      struct hash<std::basic_string<char, std::char_traits<char>, std::allocator<char> > > {
                          size_t operator()(std::basic_string<char, std::char_traits<char>, std::allocator<char> > __x) const {
                              //  copied from the hash func for char*
                              unsigned long __h = 0;
                              for(unsigned long i=0;i<__x.size();i++) {
                                  __h = 5 * __h + __x[i];
                              }
                              return size_t(__h);
                              }
                          };
                      }

                  """)
            yield ln
            for ln in lines:
                yield ln
        self._patch_build_file("libshiboken/bindingmanager.cpp",provide_hash_funcs)
        self._patch_build_file("libshiboken/typeresolver.cpp",provide_hash_funcs)


class py_myppy(base.py_myppy,Recipe):
    def install(self):
        super(py_myppy,self).install()
        with open(self._init_shell_script("python"),"a") as f:
            f.write("exec \"$WHEREAMI/local/bin/python\" \"$@\"\n")
        with open(self._init_shell_script("shell"),"a") as f:
            f.write(dedent("""
                if [ -n "$BASH" ]; then
                    SHELL="$SHELL --noprofile --norc"
                fi
                
                exec $SHELL "$@"
            """))
        with open(self._init_shell_script("myppy"),"a") as f:
            f.write("\"$WHEREAMI/local/bin/python\" -m myppy.__main__ \"$WHEREAMI\" \"$@\"\n")

    def _init_shell_script(self,relpath):
        fpath = os.path.join(self.target.rootdir,relpath)
        with open(fpath,"wb") as f:
            f.write(self._SHELLSCRIPT_STANZA)
        mod = os.stat(fpath).st_mode
        mod |= stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(fpath,mod)
        return fpath

    _SHELLSCRIPT_STANZA = dedent("""
        #  We may not have a GNU-compatible readlink, so we're forced to find
        #  the real file for this script the hard way.

        CURDIR=`pwd`
        MYFILE="$0"
        MYDIR=`dirname "$MYFILE"`
        cd "$MYDIR"
        MYFILE=`basename "$MYFILE"`
        while [ -L "$MYFILE" ]; do
            MYFILE=`readlink "$MYFILE"`
            MYDIR=`dirname "$MYFILE"`
            cd "$MYDIR"
            MYFILE=`basename "$MYFILE"`
        done
        MYFILE=`pwd -P`/"$MYFILE"
        cd "$CURDIR"

        WHEREAMI=`dirname "$MYFILE"`
        WHOAMI=`basename "$MYFILE" .sh`

        PATH="$WHEREAMI/local/bin":$PATH
        export PATH

        PS1="myppy(`basename $WHEREAMI`):\w$ "
        export PS1

        if [ -n "$BASH" -o -n "$ZSH_VERSION" ] ; then
            hash -r
        fi
    """)



class lib_freetype(Recipe):
    #  This is intentionally an old version.  We don't distribute it,
    #  but it's API compatible back to some old Linux distros.
    CONFIGURE_VARS = None
    MAKE_VARS = None
    LDFLAGS = ""
    CFLAGS = ""
    SOURCE_URL = "http://download.savannah.gnu.org/releases/freetype/freetype-2.1.10.tar.gz"


class lib_fontconfig(Recipe):
    #  This is intentionally an old version.  We don't dsitribute it,
    #  but it's API compatible back to some old Linux distros.
    DEPENDENCIES = ["lib_freetype"]
    SOURCE_URL = "http://fontconfig.org/release/fontconfig-2.4.1.tar.gz"


class lib_pango(Recipe):
    DEPENDENCIES = ["lib_fontconfig"]
    SOURCE_URL = "http://ftp.acc.umu.se/pub/gnome/sources/pango/1.12/pango-1.12.0.tar.bz2"

class lib_glib(Recipe):
    SOURCE_URL = "http://ftp.gnome.org/pub/gnome/sources/glib/2.10/glib-2.10.0.tar.bz2"


class lib_atk(Recipe):
    SOURCE_URL = "http://ftp.acc.umu.se/pub/gnome/sources/atk/1.11/atk-1.11.4.tar.bz2"


