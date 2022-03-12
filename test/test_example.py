import logging
import tempfile
import base64
import os
from pathlib import Path


def test_compile():
    log = logging.getLogger()
    log.debug('Testing C compiler')

    # Write C code to file.
    tmp = tempfile.NamedTemporaryFile()
    c_filename = f'{tmp.name}.c'
    log.debug(f'C filename: {c_filename}')
    with open(c_filename, 'w') as f:
        f.write("""#include <arch/zx.h>
#include <stdio.h>
 
int main()
{
  zx_cls(PAPER_WHITE);
  puts("Hello, world!");
  return 0;
}
""")

    # TODO: Compile the tape file from basic source.
    # main(['-taB', c_filename])

    # Read and base64 encode the binary tape file.
    tap_filename = f'{Path(c_filename).stem}.tap'
    log.debug(f'Tape filename: {tap_filename}')
    with open(tap_filename, 'rb') as f:
        base64_encoded = base64.b64encode(f.read()).decode()
        log.debug(f'Base64 encoded: {base64_encoded}')

    os.remove(c_filename)
    os.remove(tap_filename)
