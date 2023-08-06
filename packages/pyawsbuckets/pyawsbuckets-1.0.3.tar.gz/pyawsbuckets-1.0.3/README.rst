Handle Amazon S3 interactions
=============================

Objects / files can be put in S3 and deleted from S3.  Also signed URLs
can be generated to allow limited-time access to a particular object in an
S3 bucket.

Requires Python 2.6 or above.

Available as Python package at http://pypi.python.org/pypi/pyawsbuckets

Usage
-----

Initiate the access object with your credentials::

    from pyawsbuckets import AwsInterface
    aws_interface = AwsInterface(amazon_access_key, amazon_secret_key)

Put an object into an existing bucket at S3 (repeat: the bucket must ALREADY
exist)::

    aws_interface.put('https', 'bucket999', 'somefile.pdf', content)

Delete an object from S3::

    aws_interface.delete('bucket999', 'somefile.pdf')

Get a signed URL which gives access to a private object, but only for (e.g.) 15
minutes::

    expiring_url = sign_object_request('https', 'bucket999', 'somefile.pdf', 15)
    