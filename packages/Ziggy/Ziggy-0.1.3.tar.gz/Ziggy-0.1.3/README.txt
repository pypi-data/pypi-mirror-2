===========
Ziggy
===========

Ziggy provides a collection of python methods for Hadoop Streaming. Ziggy is
useful for building complex MapReduce programs, using Hadoop for batch processing
of many files, Monte Carlo processes, graph algorithms, and common utility tasks (e.g. sort, search).
Typical usage
often looks like this::

    #!/usr/bin/env python

    import ziggy.hdmc as hdmc
	from glob import glob
	
	files_to_process = glob("/some/path/*")
	results = hdmc.submit_checkpoint_inline(script_to_run, output_filename, files_to_process, argument_string)
    
To install run::

	python setup.py hadoop
	python setup.py install

Ziggy was authored by Dan McClary, Ph.D. and originates in the
 `Amaral Lab at Northwestern University <http://amaral.northwestern.edu>`_.
 
 ===========
 Installation Details
 ===========
 
 Unsurprisingly, Ziggy requires a Hadoop cluster.  To make Ziggy work with
 your cluster, you need to edit the setup.cfg file before running 
 ``python setup.py hadoop``.  This ensures that Ziggy creates the correct configuration
 files for its modules.
 
 setup.cfg currently contains 3 definitions that must be specified.  This are
 what
 	hadoop-home
 *how*
 	The HADOOP_HOME for your system.  For example, the default on our clusters
 	at Northwestern is /usr/local/hadoop.
 	
 what
 	num-map-tasks
 *how*
 	The total number of map tasks your cluster for which your cluster is configured.
 	The default is 20.
 	
 what
 	shared-tmp-space
 *how*
 	This is the path to a shared space (usually via NFS) available to all nodes
 	on your Hadoop cluster.  While this space is not necessary for building and
 	executing custom Hadoop-streaming calls, the "checkpointing" calls in HDMC
 	require a shared directory from which to coordinate task and data distribution.
 	
 Once these are set to your liking, run
 ``python setup.py hadoop`` 
 to create the hadoop_config.py modules.  Then run
 ``python setup.py hadoop``
 to install Ziggy

===========
Ziggy's Features
===========

----------
HDMC
----------

HDMC provides **bold** principle means of interacting with a Hadoop server.
Import it using ``import ziggy.hdmc``.  The interaction types are:

what
Call Assembly
*how*
Building custom and executing Hadoop streaming calls.  This is done using
the ``build_generic_hadoop_call``, ``execute`` and ``execute_and_wait`` methods.

what
Monte Carlo Mapping
*how*
Running Monte Carlo-type operations by providing only a mapping script and
a number of iterations.  This is done using the ``submit_inline`` and ``submit``
methods.

what
Data/Argument Distribution
*how*
Processing several datafiles or a list of arguments in parallel across mappers.
This is done using the ``submit_checkpoint_inline`` and the ``submit_checkpoint``
methods.

It should be noted that Monte Carlo Mapping and Data Distribution very much
violate the *spirit* of Hadoop.  However, they do provide a very simple way
to mimic traditional compute-cluster tasks without the need for cluster management
along the lines of SGE or Torque.  Similarly, they don't require a *real* cluster,
just a Hadoop installation.

----------
HDFS
----------

Ziggy provides methods for interacting with the HDFS distributed filesystem
from within Python.  These methods can be accessed by importing, for example,
``import ziggy.hdmc.hdfs`` Method calls mimic those found under ``hadoop dfs``. 

----------
Utilities
----------

Ziggy provides a number of simple utilities for manipulating very large datasets
with Hadoop.  Utilities provided include: search, grep, numeric sort, and ascii sort.
Each of these is accessed under ``ziggy.util``.  **Note** ``ziggy.util.search``
provides file names and line numbers a number of files in an HDFS directory or file.
``ziggy.util.grep`` provides the lines themselves.

----------
GraphReduce
----------

While Hadoop's Map/Reduce paradigm is poorly suited to graph algorithms, the
GraphReduce modules allow for certain graph analyses on a Hadoop Cluster.  Currently
analyes are limited to: degree-based measures, shortest-path based measures, page-rank measures,
and connected-component measures.  Except for page-rank, all path-derived measures rely
on parallel breadth-first search.  See the Epydoc documentation for more information.
GraphReduce can be accessed by importing ``ziggy.GraphReduce``

----------
Examples
----------
*Building a custom Hadoop streaming call*::
	import ziggy.hdmc as hdmc
	import ziggy.hdmc.hdfs as hdfs
	
	#load data to hdfs
	hdfs.copyToHDFS(localfilename, hfds_input_filename)
	mapper = '/path/to/mapper.py'
	reducer = '/path/to/reducer.py'
	output_filename ='hdfs_relative/output_filename'
	supporting_files = [list,of,files,mappers,require]
	maps = 20
	hadoop_call = hdmc.build_generic_hadoop_call(mapper, reducer, hdfs_input_filename, output_filename, supporting_files, maps)
	hdmc.execute_and_wait(hadoop_call)
	
*Building a Monte Carlo Job*::
	import ziggy.hdmc as hdmc
	mapper = '/path/to/job_with_needs_to_be_done_many_times.py'
	iterations = 1000
	output_file = 'output_filename'
	hdmc.submit_inline(mapper, output_file, iterations)
	
*Building a Task Distribution Job*
	import ziggy.hdmc as hdmc
    url_list = [a, list, of, url, strings]
    mapper = '/path/to/script/which/takes/a/url/as/sys.argv[1].py'
    output_filename = 'output_file_name'
    supporting_files = []
    hdmc.submit_checkpoint_inline(mapper, output_filename, url_list, supporting_files, files=False)

*Building a Data Distribution Job*
	import ziggy.hdmc as hdmc
    file_list = [a, list, of, filenames, usually, provided, by, glob]
    mapper = '/path/to/script/which/takes/a/filename/as/sys.argv[1].py'
    output_filename = 'output_file_name'
    supporting_files = [filenames, my, mapper,needs]
    hdmc.submit_checkpoint_inline(mapper, output_filename, file_list, supporting_files, files=True)
	