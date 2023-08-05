About MivRHash
--------------

MivRHash (Million-value Remote Hash) is a remote hash table data structure which provides the compatible interface with the Python dict's interface. It stores hash table data in remote server. Therefore, it is useful when your application uses so many big hash tables (dict objects) that memory in one machine is not sufficient (in other words, you can utilize main memory in multiple hosts in your application). It is originally created for storing inverted indexes of a search engine.

MivRHash allows you to specify the destination of the host where it will store data into. On the remote host, you need to run mivrhashservice to listen to hash operation requests from the client.

Since MivRHash provides the same interface with Python's dict, adapting your application with MivRHash is very easy. It requires you to change only a line of code (e.g., the hash table initialization statement) to make your application a distributed one.

MivRHash optimized its performance by using write-back cache. You can specify the cache-size when you initialize the remote hash object. The default cache size is 1000 items.

Example
-------

On the server (e.g., the machine that will store hash data), run the service::

   $ python mivrhashservice.py
   Server listening on port 10080

On the client, write code like this::
   
   from mivrhash.mivrhashclient import MivRHash
   h1 = MivRHash( "server_address", 10080 )
   h1['hello'] = 'world'
   h1[5] = 6
   h1[ ( 'some', 'tuple' ) ] = 'hello'
   h1[ 'aHash' ] = { 1 : 2, 3 : 4 }
   h2 = h1[ 'aHash' ]
   h2[1] = 5
   # Now you need to explicitly assign h2 to h1['aHash']
   # because h1 does not automatically recognize the change on its items
   print h1['aHash']   # { 1 : 2, 3 : 4 }
   h1['aHash'] = h2
   print h1['aHash']   # { 1 : 5, 3 : 4 }
   for k in h1.iterkeys():
       print k
   h1.clear()
   h1.close()  # free memory on remote server and disconnect
   h1 = None   # this also free memory and disconnect
   
Installation
------------

MivRHash is designed for very easy installation. It is a pure Python package. You can just copy the whole folder mivrhash into your site-packages directory (e.g., /usr/lib/python2.6/site-packages or C:/Python2.6/Lib/site-packages). The setup script is also available::
	 $python setup.py install

It requires no additional dependencies to be installed because it depends only on packages that are in Python standard library (such as `cPickle
<http://docs.python.org/library/pickle.html>`_ and `urllib
<http://docs.python.org/library/urllib.html>`_).
