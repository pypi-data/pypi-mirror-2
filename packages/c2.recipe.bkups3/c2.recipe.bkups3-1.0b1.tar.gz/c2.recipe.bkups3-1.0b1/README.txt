
Information
================

- Code repository: https://bitbucket.org/cmscom/c2.recipe.bkups3
- Questions and comments to terada@cmscom.jp
- Report bugs at https://bitbucket.org/cmscom/c2.recipe.bkups3/issues
- Referred to http://pypi.python.org/pypi/collective.recipe.backup


Note
=======

If you are not using ``repozo``, you need to add on `buildout.cfg`.
Because we use repozo by ``bin/buckup`` script.

buildout.cfg ::

    [repozo]
	recipe = zc.recipe.egg
	eggs = ZODB3
	scripts = repozo
	

Simple usage
==============

Modify buildout.cfg ::

    parts = 
       ...
       bkups3

    [bkups3]
    recipe = c2.recipe.bkups3
    use_s3 = true
    aws_id = xxxxxxxxxxxxx
    aws_key = xxxxxxxxxxxxxxxxxxxxxxxxxx
    bucket_name = xxxxxxxxxx
    blob_store_len = 7

Run the buildout ::

    bin/buildout -N

You can use backup scripts ::

    bin/bkups3

You got filestorage backup to `var/backups` , blobstorage backup to `var/blobbackups` 
and sending bucket of Amazon S3.

