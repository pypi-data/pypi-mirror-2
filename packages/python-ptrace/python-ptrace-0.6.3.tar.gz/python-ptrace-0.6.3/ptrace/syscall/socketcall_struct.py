from ctypes import Structure, c_char, c_ushort, c_ubyte, c_uint16, c_uint32
from ptrace.os_tools import RUNNING_BSD, RUNNING_LINUX

if RUNNING_BSD:
    sa_family_t = c_ubyte
else:
    sa_family_t = c_ushort

class sockaddr(Structure):
    if RUNNING_BSD:
        _fields_ = (
            ("len", c_ubyte),
            ("family", sa_family_t),
        )
    else:
        _fields_ = (
            ("family", sa_family_t),
        )

class in_addr(Structure):
    _fields_ = (
        ("s_addr", c_uint32),
    )

# INET socket
class sockaddr_in(Structure):
    if RUNNING_BSD:
        _fields_ = (
            ("sin_len", c_ubyte),
            ("sin_family", sa_family_t),
            ("sin_port", c_uint16),
            ("sin_addr", in_addr),
        )
    else:
        _fields_ = (
            ("sin_family", sa_family_t),
            ("sin_port", c_uint16),
            ("sin_addr", in_addr),
        )

# UNIX socket
class sockaddr_un(Structure):
    _fields_ = (
        ("sun_family", sa_family_t),
        ("sun_path", c_char*108),
    )

# Netlink socket
if RUNNING_LINUX:
    class sockaddr_nl(Structure):
        _fields_ = (
            ("nl_family", sa_family_t),
            ("nl_pad", c_ushort),
            ("nl_pid", c_uint32),
            ("nl_groups", c_uint32),
        )

