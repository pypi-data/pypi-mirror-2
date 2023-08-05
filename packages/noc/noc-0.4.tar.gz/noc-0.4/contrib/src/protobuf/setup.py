#! /usr/bin/python
#
# See README for usage instructions.

# We must use setuptools, not distutils, because we need to use the
# namespace_packages option for the "google" package.
from distutils.core import setup
#from ez_setup import use_setuptools
#use_setuptools()

#from setuptools import setup
#from distutils.spawn import find_executable
import sys
import os
import subprocess

maintainer_email = "protobuf@googlegroups.com"

if __name__ == '__main__':
  # TODO(kenton):  Integrate this into setuptools somehow?
  if len(sys.argv) >= 2 and sys.argv[1] == "clean":
    # Delete generated _pb2.py files and .pyc files in the code tree.
    for (dirpath, dirnames, filenames) in os.walk("."):
      for filename in filenames:
        filepath = os.path.join(dirpath, filename)
        if filepath.endswith("_pb2.py") or filepath.endswith(".pyc"):
          os.remove(filepath)
  else:
    # Generate necessary .proto file if it doesn't exist.
    # TODO(kenton):  Maybe we should hook this into a distutils command?
    #generate_proto("../src/google/protobuf/descriptor.proto")
    pass

  setup(name = 'protobuf',
        version = '2.2.0',
        packages = [ 'google' ],
        namespace_packages = [ 'google' ],
        #test_suite = 'setup.MakeTestSuite',
        # Must list modules explicitly so that we don't install tests.
        py_modules = [
          'google.protobuf.internal.containers',
          'google.protobuf.internal.decoder',
          'google.protobuf.internal.encoder',
          'google.protobuf.internal.input_stream',
          'google.protobuf.internal.message_listener',
          'google.protobuf.internal.output_stream',
          'google.protobuf.internal.type_checkers',
          'google.protobuf.internal.wire_format',
          'google.protobuf.descriptor',
          'google.protobuf.descriptor_pb2',
          'google.protobuf.message',
          'google.protobuf.reflection',
          'google.protobuf.service',
          'google.protobuf.service_reflection',
          'google.protobuf.text_format' ],
        url = 'http://code.google.com/p/protobuf/',
        maintainer = maintainer_email,
        maintainer_email = 'protobuf@googlegroups.com',
        license = 'New BSD License',
        description = 'Protocol Buffers',
        long_description =
          "Protocol Buffers are Google's data interchange format.",
        zip_safe=False,
        )
