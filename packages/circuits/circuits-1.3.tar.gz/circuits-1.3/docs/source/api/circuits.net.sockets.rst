~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
:mod:`circuits<circuits>`. :mod:`net<circuits.net>`. :mod:`sockets<circuits.net.sockets>`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~




.. automodule:: circuits.net.sockets


Members
=======









.. rubric:: Members

.. autosummary::
	:nosignatures:
	
	
	BACKLOG
	
	BUFSIZE
	
	Client
	
	Close
	
	Connect
	
	Connected
	
	Disconnect
	
	Disconnected
	
	E2BIG
	
	EACCES
	
	EADDRINUSE
	
	EADDRNOTAVAIL
	
	EADV
	
	EAFNOSUPPORT
	
	EAGAIN
	
	EALREADY
	
	EBADE
	
	EBADF
	
	EBADFD
	
	EBADMSG
	
	EBADR
	
	EBADRQC
	
	EBADSLT
	
	EBFONT
	
	EBUSY
	
	ECHILD
	
	ECHRNG
	
	ECOMM
	
	ECONNABORTED
	
	ECONNREFUSED
	
	ECONNRESET
	
	EDEADLK
	
	EDEADLOCK
	
	EDESTADDRREQ
	
	EDOM
	
	EDOTDOT
	
	EDQUOT
	
	EEXIST
	
	EFAULT
	
	EFBIG
	
	EHOSTDOWN
	
	EHOSTUNREACH
	
	EIDRM
	
	EILSEQ
	
	EINPROGRESS
	
	EINTR
	
	EINVAL
	
	EIO
	
	EISCONN
	
	EISDIR
	
	EISNAM
	
	EL2HLT
	
	EL2NSYNC
	
	EL3HLT
	
	EL3RST
	
	ELIBACC
	
	ELIBBAD
	
	ELIBEXEC
	
	ELIBMAX
	
	ELIBSCN
	
	ELNRNG
	
	ELOOP
	
	EMFILE
	
	EMLINK
	
	EMSGSIZE
	
	EMULTIHOP
	
	ENAMETOOLONG
	
	ENAVAIL
	
	ENETDOWN
	
	ENETRESET
	
	ENETUNREACH
	
	ENFILE
	
	ENOANO
	
	ENOBUFS
	
	ENOCSI
	
	ENODATA
	
	ENODEV
	
	ENOENT
	
	ENOEXEC
	
	ENOLCK
	
	ENOLINK
	
	ENOMEM
	
	ENOMSG
	
	ENONET
	
	ENOPKG
	
	ENOPROTOOPT
	
	ENOSPC
	
	ENOSR
	
	ENOSTR
	
	ENOSYS
	
	ENOTBLK
	
	ENOTCONN
	
	ENOTDIR
	
	ENOTEMPTY
	
	ENOTNAM
	
	ENOTSOCK
	
	ENOTTY
	
	ENOTUNIQ
	
	ENXIO
	
	EOPNOTSUPP
	
	EOVERFLOW
	
	EPERM
	
	EPFNOSUPPORT
	
	EPIPE
	
	EPROTO
	
	EPROTONOSUPPORT
	
	EPROTOTYPE
	
	ERANGE
	
	EREMCHG
	
	EREMOTE
	
	EREMOTEIO
	
	ERESTART
	
	EROFS
	
	ESHUTDOWN
	
	ESOCKTNOSUPPORT
	
	ESPIPE
	
	ESRCH
	
	ESRMNT
	
	ESTALE
	
	ESTRPIPE
	
	ETIME
	
	ETIMEDOUT
	
	ETOOMANYREFS
	
	ETXTBSY
	
	EUCLEAN
	
	EUNATCH
	
	EUSERS
	
	EWOULDBLOCK
	
	EXDEV
	
	EXFULL
	
	Error
	
	HAS_SSL
	
	Pipe
	
	Read
	
	Ready
	
	Server
	
	TCPClient
	
	TCPServer
	
	UDPClient
	
	UDPServer
	
	UNIXClient
	
	UNIXServer
	
	Write
	
	errorcode
	





	


.. rubric:: Data definitions


.. autodata:: BACKLOG

.. autodata:: BUFSIZE

.. autodata:: E2BIG

.. autodata:: EACCES

.. autodata:: EADDRINUSE

.. autodata:: EADDRNOTAVAIL

.. autodata:: EADV

.. autodata:: EAFNOSUPPORT

.. autodata:: EAGAIN

.. autodata:: EALREADY

.. autodata:: EBADE

.. autodata:: EBADF

.. autodata:: EBADFD

.. autodata:: EBADMSG

.. autodata:: EBADR

.. autodata:: EBADRQC

.. autodata:: EBADSLT

.. autodata:: EBFONT

.. autodata:: EBUSY

.. autodata:: ECHILD

.. autodata:: ECHRNG

.. autodata:: ECOMM

.. autodata:: ECONNABORTED

.. autodata:: ECONNREFUSED

.. autodata:: ECONNRESET

.. autodata:: EDEADLK

.. autodata:: EDEADLOCK

.. autodata:: EDESTADDRREQ

.. autodata:: EDOM

.. autodata:: EDOTDOT

.. autodata:: EDQUOT

.. autodata:: EEXIST

.. autodata:: EFAULT

.. autodata:: EFBIG

.. autodata:: EHOSTDOWN

.. autodata:: EHOSTUNREACH

.. autodata:: EIDRM

.. autodata:: EILSEQ

.. autodata:: EINPROGRESS

.. autodata:: EINTR

.. autodata:: EINVAL

.. autodata:: EIO

.. autodata:: EISCONN

.. autodata:: EISDIR

.. autodata:: EISNAM

.. autodata:: EL2HLT

.. autodata:: EL2NSYNC

.. autodata:: EL3HLT

.. autodata:: EL3RST

.. autodata:: ELIBACC

.. autodata:: ELIBBAD

.. autodata:: ELIBEXEC

.. autodata:: ELIBMAX

.. autodata:: ELIBSCN

.. autodata:: ELNRNG

.. autodata:: ELOOP

.. autodata:: EMFILE

.. autodata:: EMLINK

.. autodata:: EMSGSIZE

.. autodata:: EMULTIHOP

.. autodata:: ENAMETOOLONG

.. autodata:: ENAVAIL

.. autodata:: ENETDOWN

.. autodata:: ENETRESET

.. autodata:: ENETUNREACH

.. autodata:: ENFILE

.. autodata:: ENOANO

.. autodata:: ENOBUFS

.. autodata:: ENOCSI

.. autodata:: ENODATA

.. autodata:: ENODEV

.. autodata:: ENOENT

.. autodata:: ENOEXEC

.. autodata:: ENOLCK

.. autodata:: ENOLINK

.. autodata:: ENOMEM

.. autodata:: ENOMSG

.. autodata:: ENONET

.. autodata:: ENOPKG

.. autodata:: ENOPROTOOPT

.. autodata:: ENOSPC

.. autodata:: ENOSR

.. autodata:: ENOSTR

.. autodata:: ENOSYS

.. autodata:: ENOTBLK

.. autodata:: ENOTCONN

.. autodata:: ENOTDIR

.. autodata:: ENOTEMPTY

.. autodata:: ENOTNAM

.. autodata:: ENOTSOCK

.. autodata:: ENOTTY

.. autodata:: ENOTUNIQ

.. autodata:: ENXIO

.. autodata:: EOPNOTSUPP

.. autodata:: EOVERFLOW

.. autodata:: EPERM

.. autodata:: EPFNOSUPPORT

.. autodata:: EPIPE

.. autodata:: EPROTO

.. autodata:: EPROTONOSUPPORT

.. autodata:: EPROTOTYPE

.. autodata:: ERANGE

.. autodata:: EREMCHG

.. autodata:: EREMOTE

.. autodata:: EREMOTEIO

.. autodata:: ERESTART

.. autodata:: EROFS

.. autodata:: ESHUTDOWN

.. autodata:: ESOCKTNOSUPPORT

.. autodata:: ESPIPE

.. autodata:: ESRCH

.. autodata:: ESRMNT

.. autodata:: ESTALE

.. autodata:: ESTRPIPE

.. autodata:: ETIME

.. autodata:: ETIMEDOUT

.. autodata:: ETOOMANYREFS

.. autodata:: ETXTBSY

.. autodata:: EUCLEAN

.. autodata:: EUNATCH

.. autodata:: EUSERS

.. autodata:: EWOULDBLOCK

.. autodata:: EXDEV

.. autodata:: EXFULL

.. autodata:: HAS_SSL

.. autodata:: errorcode







.. rubric:: Function definitions


.. autofunction:: Pipe







.. rubric:: Class definitions


.. autoclass:: Client()
	:members:
	:show-inheritance:
.. autoclass:: Close()
	:members:
	:show-inheritance:
.. autoclass:: Connect()
	:members:
	:show-inheritance:
.. autoclass:: Connected()
	:members:
	:show-inheritance:
.. autoclass:: Disconnect()
	:members:
	:show-inheritance:
.. autoclass:: Disconnected()
	:members:
	:show-inheritance:
.. autoclass:: Error()
	:members:
	:show-inheritance:
.. autoclass:: Read()
	:members:
	:show-inheritance:
.. autoclass:: Ready()
	:members:
	:show-inheritance:
.. autoclass:: Server()
	:members:
	:show-inheritance:
.. autoclass:: TCPClient()
	:members:
	:show-inheritance:
.. autoclass:: TCPServer()
	:members:
	:show-inheritance:
.. autoclass:: UDPClient()
	:members:
	:show-inheritance:
.. autoclass:: UDPServer()
	:members:
	:show-inheritance:
.. autoclass:: UNIXClient()
	:members:
	:show-inheritance:
.. autoclass:: UNIXServer()
	:members:
	:show-inheritance:
.. autoclass:: Write()
	:members:
	:show-inheritance:






