# -*- coding: utf-8 -*-
""" TODO:
- subprocess calling stream encryption with default keyfile
- compressing function using lz4
- tree walker, hasher, indexer

Storage by key, automatically making and removing blocks?  I want fixed size
compressed encrypted blocks of fixed size. Mmost safe is to have the complete
blocks encrypted, so that no headers are visible.

If something is removed from a block, then the complete contents of the block
are relocated. 

Compress, cut in chunks, encrypt. Can we lz4 stream compress? I guess it can.
We have to check docs. So

So adding a file means: Store path and attributes, hash If hash already in
storage, do nothing If hash not in storage, compress file, find latest block.
Decrypt block, append file end ecnrypt as many blocks as needed until file
fully covered. Done. But, if there are more files, wait with reencryption.
Store the begin and end block / file positions of the compressed file in the
unencrypted block.

Getting a file: Find the blocks, decrypt, read, save.

Removing file: If hash no longer needed: locate contents in another block. Now
it gets tricky.  Have to make a linked list for this. A hash is always That
also resolves the problem of running out of block addresses, we can always use
the first empty position. But where to store this data? If a file is pruned,
all remaining block data needs to be appended to the existing latest block.

This is becoming complicated because i want fixed size blocks, but that is
because the requirement of fully filled encrypted blocks. Therefore every file
must point to a linked list, but where is that stored? Preferrably not in the
file itself.
"""

