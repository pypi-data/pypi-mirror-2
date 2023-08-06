`watcher` is a low-level C extension for receiving file system updates
using the
`ReadDirectoryChangesW <http://msdn.microsoft.com/en-us/library/aa365465(v=vs.85).aspx>`_
API on Windows systems.::

   import watcher
   w = watcher.Watcher(dir, callback)
   w.flags = watcher.FILE_NOTIFY_CHANGE_FILE_NAME
   w.start()

The package also includes a high-level interface to emulate most of the
.NET `FileSystemWatcher <http://msdn.microsoft.com/en-us/library/system.io.filesystemwatcher.aspx>`_
API. The callback adding and removing mirrors how the same would be
done on IronPython. Additionally, enabling and disabling of the callbacks
is the same.::

   import FileSystemWatcher
   fsw = FileSystemWatcher("somedir")
   fsw.NotifyFilter = FileSystemWatcher.NotifyFilters.FileName
   fsw.Created += your_callback
   fsw.EnableRaisingEvents = True


The project is still in progress. Development occurs at
https://bitbucket.org/briancurtin/watcher.

