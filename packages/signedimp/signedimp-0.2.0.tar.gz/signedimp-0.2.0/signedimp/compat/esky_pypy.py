"""

  signedimp.compat.esky:  esky integration support code for signedimp

This module contains support for using signedimp together with the "esky"
auto-update module.  Use the "get_bootstrap_code" function to get code for
a custom chainloading function, which will verify the chainloaded exe before
executing it.  This code should be passed in to bdist_esky as part of the
"bootstrap_code" option.

"""

import inspect

import signedimp
from signedimp import bootstrap, cryptobase

def _getsrc(obj,indent=""):
    src = "\n" + inspect.getsource(obj)
    src = src.replace("\n","\n" + indent)
    return src

def get_bootstrap_code(key):
    signedhashdb_source = _getsrc(bootstrap.SignedHashDatabase,"    ")
    rsakey_source = _getsrc(cryptobase.rsa,"    ")
    b64decode_source = _getsrc(bootstrap._signedimp_util.b64decode,"    ")
    pubkey = key.get_public_key()
    hashfile_name = signedimp.HASHFILE_NAME
    return """

from hashlib import sha1, md5

def _make_signedimp_chainload(orig_chainload):
    class IntegrityCheckError(Exception):
        pass
    class IntegrityCheckMissing(IntegrityCheckError):
        pass
    class IntegrityCheckFailed(IntegrityCheckError):
        pass
    HASHFILE_NAME = %(hashfile_name)r
    %(signedhashdb_source)s
    %(rsakey_source)s
    class _signedimp_util:
        %(b64decode_source)s
        sha1 = sha1
        md5 = md5
    _signedimp_util = _signedimp_util()
    key = %(pubkey)r
    def readfile(pathnm):
        fh = os_open(pathnm,0,0)
        try:
            data = ""
            new_data = os_read(fh,1024*64)
            while new_data:
                data += new_data
                new_data = os_read(fh,1024*64)
            return data
        finally:
            os_close(fh)
    def _chainload(target_dir):
        #  On OSX, the signature file may be within a bundled ".app" directory
        #  or in the top level of the target dir.
        if sys.platform == "darwin":
            if __esky_name__ is not None:
                signed_dir = pathjoin(target_dir,__esky_name__+".app")
                if not exists(pathjoin(signed_dir,HASHFILE_NAME)):
                    signed_dir = target_dir
            else:
                for nm in listdir(target_dir):
                    if nm.endswith(".app"):
                        signed_dir = pathjoin(target_dir,nm)
                        if exists(pathjoin(signed_dir,HASHFILE_NAME)):
                            break
                else:
                    signed_dir = target_dir
        else:
            signed_dir = target_dir
        #  Load the signed hash database into memory
        hdata = readfile(pathjoin(signed_dir,HASHFILE_NAME))
        hashdb = SignedHashDatabase([key],hdata)
        #  Find the first target exe that exists, and verify it
        for target_exe in get_exe_locations(target_dir):
            try:
                fdata = readfile(target_exe)
            except EnvironmentError:
                pass
            else:
                hashdb.verify("d",target_exe[len(signed_dir)+1:],fdata)
                break
        orig_chainload(target_dir)
    return _chainload
_chainload = _make_signedimp_chainload(_chainload)
""" % locals()


