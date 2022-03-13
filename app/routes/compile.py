import tempfile
import base64
import os
import subprocess
from pathlib import Path
from fastapi import APIRouter, Header
from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class SessionVars(BaseModel):
    x_hasura_role: str = Field(alias="x-hasura-role")
    x_hasura_user_id: Optional[UUID] = Field(alias="x-hasura-user-id")


class Input(BaseModel):
    code: str


class Action(BaseModel):
    name: str


class RequestArgs(BaseModel):
    session_variables: SessionVars
    input: Input
    action: Action


class CompileResult(BaseModel):
    base64_encoded: str


compile_endpoint = APIRouter()


@compile_endpoint.post("/", response_model=CompileResult)
def handle_compile_request(
        args: RequestArgs,
        authorization: Optional[str] = Header(None)) -> Optional[CompileResult]:

    # user_id = args.session_variables.x_hasura_user_id
    # role = args.session_variables.x_hasura_role

    # Write C code to file.
    tmp = tempfile.NamedTemporaryFile()
    c_filename = f'{tmp.name}.c'
    with open(c_filename, 'w') as f:
        f.write(args.input.code)

    path = os.path.dirname(os.path.abspath(c_filename))
    stem = Path(c_filename).stem
    out_filename = f'{os.path.join(path, stem)}'
    tap_filename = f'{out_filename}.tap'

    try:
        # Compile the tape file from C source.
        subprocess.run([
            'zcc',
            '+zx',
            '-vn',
            '-create-app',
            '-clib=sdcc_iy',
            '-startup=0',
            c_filename,
            '-o',
            out_filename
        ])

        assert os.path.exists(tap_filename)

        try:
            # Read and base64 encode the binary tape file.
            with open(tap_filename, 'rb') as f:
                base64_encoded = base64.b64encode(f.read()).decode()
                return CompileResult(base64_encoded=base64_encoded)

        finally:
            os.remove(tap_filename)

    finally:
        os.remove(c_filename)
