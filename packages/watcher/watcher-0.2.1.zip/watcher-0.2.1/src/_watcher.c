#include "Python.h"
#include "structmember.h"

#include <windows.h>

/* ignore "conditional expression is constant" */
#pragma warning(disable: 4100)
/* ignore "unreferenced formal parameter" */
#pragma warning(disable: 4127)

#define MAX_BUFFER 4096

#define WATCHER_VERSION "0.2.1"

#if PY_MAJOR_VERSION == 3
#define PYTHON3
#endif


typedef struct {
    PyObject_HEAD
    PyObject *callback;
    PyObject *args;
    PyObject *kwargs;

    wchar_t *path;
    int running;
    int die;
    int recursive;
    unsigned int flags;

    HANDLE handle;
    HANDLE completion;
    HANDLE thread;
    CHAR buffer[MAX_BUFFER];
    DWORD buffer_len;
    OVERLAPPED overlapped;
} watcher_object;


void WINAPI
handle_directory_change(DWORD_PTR completion_port)
{
    watcher_object *self;
    PyGILState_STATE gil_state;
    PyObject *call_rslt, *py_file_name, *args;
#ifndef PYTHON3
    PyObject *py_file_name2;
#endif
    Py_ssize_t idx, args_len;
    int pos;

    BOOL rdc;
    DWORD num_bytes, offset, err;
    OVERLAPPED *overlapped;
    PFILE_NOTIFY_INFORMATION notify_info;
    wchar_t file_name[MAX_PATH];

    do {
        GetQueuedCompletionStatus((HANDLE)completion_port,
                                  &num_bytes,
                                  (PDWORD_PTR)&self,
                                  &overlapped,
                                  INFINITE);

        if (self) {
            notify_info = (PFILE_NOTIFY_INFORMATION)self->buffer;

            do {
                offset = notify_info->NextEntryOffset;

                /* Get the relative file path out of the buffer.
                   Apparently this should use StringCchCopy... */
                lstrcpyn(file_name, notify_info->FileName,
                         notify_info->FileNameLength / sizeof(wchar_t) + 1);
                file_name[notify_info->FileNameLength / sizeof(wchar_t) + 1] = '\0';
                py_file_name = PyUnicode_FromWideChar(file_name,
                                                      wcslen(file_name));
#ifndef PYTHON3
                /* Encode what we get from above and get it back as a
                   traditional string. */
                py_file_name2 = PyUnicode_AsEncodedString(py_file_name,
                                          Py_FileSystemDefaultEncoding, NULL);
#endif

                /* Take the args tuple given in the constructor and place
                   it after the info we have to call the user with.
                   The user callback will contain the file action, the file
                   path, then anything that the user wants to be called back
                   with from self->args and self->kwargs. */
                args_len = PyTuple_Size(self->args);
                args = PyTuple_New(args_len + 2);
                pos = 0;
                /* Action should correspond to one of the constants listed
                   at the bottom, titled Notify Actions. */
#ifdef PYTHON3
                PyTuple_SET_ITEM(args, pos++,
                                 PyLong_FromLongLong(notify_info->Action));
                PyTuple_SET_ITEM(args, pos++, py_file_name);
#else
                PyTuple_SET_ITEM(args, pos++,
                                 PyInt_FromLong(notify_info->Action));
                PyTuple_SET_ITEM(args, pos++, py_file_name2);
#endif

                for (idx = 0; idx < args_len; ++idx) {
                    PyTuple_SET_ITEM(args, pos++,
                                     PyTuple_GET_ITEM(self->args, idx));
                }

                gil_state = PyGILState_Ensure();
                call_rslt = PyObject_Call(self->callback, args, self->kwargs);
                PyGILState_Release(gil_state);

                /* If the callback signature doesn't list what we sent, the
                   call will fail with NULL. Other stuff can probably cause
                   this but I have no idea what that would be. */
                if (call_rslt == NULL) {
                    /* These calls also require the GIL */
                    gil_state = PyGILState_Ensure();
                    PyErr_SetString(PyExc_RuntimeError,
                                    "Unable to call callback");
                    PyErr_Print();
                    PyGILState_Release(gil_state);
                } else
                    Py_DECREF(call_rslt);

                notify_info = (PFILE_NOTIFY_INFORMATION)((LPBYTE)notify_info + offset);

            /* A zero offset specifies that we're on the last record, so keep
               going until we get there. */
            } while (offset);

            rdc = ReadDirectoryChangesW(self->handle, self->buffer, MAX_BUFFER,
                                        self->recursive, self->flags,
                                        &self->buffer_len, &self->overlapped,
                                        NULL);
            err = GetLastError();

            /* Let the user know if the re-issuing of RDC fails so it doesn't
               look like a deadlock. */
            if (rdc == 0) {
                gil_state = PyGILState_Ensure();
                PyErr_SetFromWindowsErr(err);
                PyErr_Print();
                PyGILState_Release(gil_state);
                self = NULL; /* Break out of the main while loop. */
            }
        }
    } while (self);
}

void WINAPI
watch_thread(watcher_object *self)
{
    PyGILState_STATE gil_state;
    HANDLE change_thread;
    DWORD err;

    BOOL rdc = ReadDirectoryChangesW(self->handle,
                          self->buffer /* read results */, MAX_BUFFER,
                          self->recursive, /* watch subdirectories */
                          /* NOTE: At least one flag is required! */
                          self->flags, /* see Notify Filters below */
                          &self->buffer_len,
                          &self->overlapped,
                          NULL); /* completion routine */
    err = GetLastError();

    if (rdc == 0) {
        gil_state = PyGILState_Ensure();
        PyErr_SetFromWindowsErr(err);
        PyErr_Print();
        PyGILState_Release(gil_state);
        self->running = 0;
        return;
    }
    
    change_thread = CreateThread(NULL, 0,
                          (LPTHREAD_START_ROUTINE)handle_directory_change,
                          self->completion,
                          0, NULL);
    while (1) {
        if (self->die == 1)
           break; 
        Sleep(500);
    }

    /* Kill the completion port */
    PostQueuedCompletionStatus(self->completion, 0, 0, NULL);
    WaitForSingleObject(change_thread, INFINITE);
    CloseHandle(change_thread);
}

static PyObject *
watcher_object_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
    watcher_object *self;
    PyObject *callback = NULL;
    PyObject *path = NULL;

    Py_ssize_t num_args = PyTuple_GET_SIZE(args);

    /* Don't use PyArg_Parse* functions here.

       We want to take kwargs without specifying named arguments. We'll
       manually pick items out of the args tuple, then take a slice of the
       remaining ones as our callback's args, then take all kwargs. */
    if (num_args < 2) {
        PyErr_SetString(PyExc_TypeError, "watcher takes at least 2 arguments");
        return NULL;
    }

    path = PyTuple_GET_ITEM(args, 0);

    callback = PyTuple_GET_ITEM(args, 1);
    if (!PyCallable_Check(callback)) {
        PyErr_Format(PyExc_TypeError, "callback parameter must be callable");
        return NULL;
    }

    self = (watcher_object*)type->tp_alloc(type, 0);
    if (self == NULL)
        return NULL;

#ifdef PYTHON3
    if (PyUnicode_Check(path)) {
        self->path = PyUnicode_AS_UNICODE(path);
        Py_INCREF(path);
    } else if (PyBytes_Check(path)) {
        PyObject *encoded;
        encoded = PyUnicode_FromEncodedObject(path,
                                              Py_FileSystemDefaultEncoding,
                                              NULL);
        self->path = PyUnicode_AS_UNICODE(encoded);
        Py_INCREF(encoded);
    } else {
        PyErr_SetString(PyExc_TypeError, "path must be unicode");
        return NULL;
    }
#else
    if (PyString_Check(path)) {
        PyObject *encoded, *unicode;
        encoded = PyString_AsEncodedObject(path, Py_FileSystemDefaultEncoding,
                                           NULL);
        unicode = PyUnicode_FromEncodedObject(encoded,
                                              Py_FileSystemDefaultEncoding,
                                              NULL);
        self->path = PyUnicode_AS_UNICODE(unicode);
        Py_INCREF(encoded);
        Py_INCREF(unicode);
        Py_INCREF(path);
    } else if (PyUnicode_Check(path)) {
        self->path = PyUnicode_AS_UNICODE(path);
        Py_INCREF(path);
    } else {
        PyErr_SetString(PyExc_TypeError, "path must be str or unicode");
        return NULL;
    }
#endif

    self->callback = callback;
    Py_INCREF(callback);

    /* Get any positional arguments via slicing the remains. */
    self->args = PyTuple_GetSlice(args, 2, num_args);
    if (self->args == NULL) {
        /* PyObject_Call expects non-NULL args. */
        self->args = PyTuple_New(0);
    }

    /* PyObject_Call works with NULLs so no need to check here. */
    self->kwargs = kwargs;
    Py_XINCREF(kwargs);

    self->flags = 0;
    self->recursive = 0;
    
    self->handle = CreateFileW(self->path,
                   FILE_LIST_DIRECTORY, /* required */
                   FILE_SHARE_READ | FILE_SHARE_WRITE | FILE_SHARE_DELETE,
                   NULL,
                   OPEN_EXISTING,
                   /* Use FILE_FLAG_OVERLAPPED for asynchronous operation
                      with ReadDirectoryChangesW. */
                   FILE_FLAG_BACKUP_SEMANTICS | FILE_FLAG_OVERLAPPED,
                   NULL);

    if (self->handle == INVALID_HANDLE_VALUE) {
        PyErr_Format(PyExc_WindowsError, "unable to open path");
        return NULL;
    }

    return (PyObject*)self;
}

static void
watcher_object_dealloc(watcher_object *self)
{
    /* TODO: Make sure everything is shutdown? */
    Py_TYPE(self)->tp_free((PyObject*)self);
}

PyDoc_STRVAR(watcher_start_doc,
"start()\n\
Start the watcher and begin sending callbacks.");

static PyObject *
watcher_start_function(watcher_object *self, PyObject *unused)
{
    if (self->running == 1)
        Py_RETURN_FALSE;

    self->completion = CreateIoCompletionPort(self->handle,
                                              self->completion,
                                              (ULONG_PTR)self,
                                              /* max num processors */ 0);
    if (self->completion == NULL) {
        PyErr_Format(PyExc_WindowsError, "unable to create completion port");
        return NULL;
    }

    self->thread = CreateThread(NULL, 0,
                                (LPTHREAD_START_ROUTINE)watch_thread,
                                self, 0, NULL);
    if (self->thread == NULL) {
        PyErr_Format(PyExc_WindowsError, "unable to start watcher thread");
        return NULL;
    }

    self->running = 1;
    Py_RETURN_NONE;
}

PyDoc_STRVAR(watcher_stop_doc,
"stop()\n\
Stop the watcher and halt any callbacks.");

static PyObject *
watcher_stop_function(watcher_object *self, PyObject *unused)
{
    if (self->running == 0)
        Py_RETURN_FALSE;

    self->die = 1;
    WaitForSingleObject(self->thread, INFINITE);

    if (CloseHandle(self->completion) == 0) {
        PyErr_Format(PyExc_WindowsError,
                     "unable to close completion handle: %d", GetLastError());
        return NULL;
    }
    if (CloseHandle(self->thread) == 0) {
        PyErr_Format(PyExc_WindowsError,
                     "unable to close thread handle: %d", GetLastError());
        return NULL;
    }

    self->running = 0;
    Py_RETURN_NONE;
}

static PyMethodDef watcher_object_methods[] = {
    {"start", (PyCFunction)watcher_start_function, METH_NOARGS, 
               watcher_stop_doc},
    {"stop", (PyCFunction)watcher_stop_function, METH_NOARGS,
                watcher_stop_doc},
    {NULL, NULL}
};

PyDoc_STRVAR(watcher_recursive_doc,
"See the help text for Watcher.recursive.");

PyDoc_STRVAR(watcher_flags_doc,
"Any flags to specify notification information.");

PyDoc_STRVAR(watcher_running_doc,
"Boolean representing whether or not the Watcher is currently running.");

static PyMemberDef watcher_object_members[] = {
    {"recursive", T_BOOL, offsetof(watcher_object, recursive), 0,
                  watcher_recursive_doc},
    {"flags", T_ULONG, offsetof(watcher_object, flags), 0,
              watcher_flags_doc},
    {"running", T_BOOL, offsetof(watcher_object, running), 0,
                watcher_running_doc},
    {NULL}
};


PyDoc_STRVAR(watcher_doc, "TODO");

static PyTypeObject watcher_object_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_watcher.Watcher",                 /* tp_name */
    sizeof(watcher_object),             /* tp_size */
    0,                                  /* tp_itemsize */
    (destructor)watcher_object_dealloc, /* tp_dealloc */
    0,                                  /* tp_print */
    0,                                  /* tp_getattr */
    0,                                  /* tp_setattr */
    0,                                  /* tp_compare */
    0,                                  /* tp_repr */
    0,                                  /* tp_as_number */
    0,                                  /* tp_as_sequence */
    0,                                  /* tp_as_mapping */
    0,                                  /* tp_hash */
    0,                                  /* tp_call */
    0,                                  /* tp_str */
    0,                                  /* tp_getattro */
    0,                                  /* tp_setattro */
    0,                                  /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT | 
    Py_TPFLAGS_BASETYPE,                /* tp_flags */
    watcher_doc,                        /* tp_doc */
    0,                                  /* tp_traverse */
    0,                                  /* tp_clear */
    0,                                  /* tp_richcompare */
    0,                                  /* tp_weaklistoffset */
    0,                                  /* tp_iter */
    0,                                  /* tp_iterneext */
    watcher_object_methods,             /* tp_methods */
    watcher_object_members,             /* tp_members */
    0,                                  /* tp_getset */
    0,                                  /* tp_base */
    0,                                  /* tp_dict */
    0,                                  /* tp_descr_get */
    0,                                  /* tp_descr_set */
    0,                                  /* tp_dictoffset */
    0,                                  /* tp_init */
    PyType_GenericAlloc,                /* tp_alloc */
    watcher_object_new,                 /* tp_new */
    PyObject_Del,                       /* tp_free */
};


PyDoc_STRVAR(module_doc,
"A low-level file system watcher built on ReadDirectoryChangesW\n\
and overlapped I/O. This works similar to how the .NET\n\
FileSystemWatcher class works interally.");

static void
setint(PyObject *dict, const char* name, long value)
{
    PyObject *val = PyLong_FromLong(value);
    if (val && PyDict_SetItemString(dict, name, val) == 0)
        Py_DECREF(val);
}

#ifdef PYTHON3
static struct PyModuleDef _watchermodule = {
    PyModuleDef_HEAD_INIT,
    "_watcher",
    module_doc,
    -1,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
};
#endif

#ifdef PYTHON3
PyMODINIT_FUNC
PyInit__watcher(void)
#else
PyMODINIT_FUNC
init_watcher()
#endif
{
    PyObject *module, *dict;

    /* Initialize and acquire the GIL before we do anything else. */
    PyEval_InitThreads();

#ifdef PYTHON3
    module = PyModule_Create(&_watchermodule);
#else
    module = Py_InitModule3("_watcher", NULL, module_doc);
#endif

    if (PyType_Ready(&watcher_object_type) < 0)
        goto fail;

    dict = PyModule_GetDict(module);
    if (!dict)
        goto fail;

    PyDict_SetItemString(dict, "Watcher", (PyObject*)&watcher_object_type);

    /* Notify Filters */
    setint(dict, "FILE_NOTIFY_CHANGE_FILE_NAME",
                 FILE_NOTIFY_CHANGE_FILE_NAME);
    setint(dict, "FILE_NOTIFY_CHANGE_DIR_NAME", 
                 FILE_NOTIFY_CHANGE_DIR_NAME);
    setint(dict, "FILE_NOTIFY_CHANGE_ATTRIBUTES", 
                 FILE_NOTIFY_CHANGE_ATTRIBUTES);
    setint(dict, "FILE_NOTIFY_CHANGE_SIZE",
                 FILE_NOTIFY_CHANGE_SIZE);
    setint(dict, "FILE_NOTIFY_CHANGE_LAST_WRITE", 
                 FILE_NOTIFY_CHANGE_LAST_WRITE);
    setint(dict, "FILE_NOTIFY_CHANGE_LAST_ACCESS",
                 FILE_NOTIFY_CHANGE_LAST_ACCESS);
    setint(dict, "FILE_NOTIFY_CHANGE_CREATION", 
                 FILE_NOTIFY_CHANGE_CREATION);
    setint(dict, "FILE_NOTIFY_CHANGE_SECURITY", 
                 FILE_NOTIFY_CHANGE_SECURITY);

    /* Notify Actions */
    setint(dict, "FILE_ACTION_ADDED",
                 FILE_ACTION_ADDED);
    setint(dict, "FILE_ACTION_REMOVED",
                 FILE_ACTION_REMOVED);
    setint(dict, "FILE_ACTION_MODIFIED",
                 FILE_ACTION_MODIFIED);
    setint(dict, "FILE_ACTION_RENAMED_OLD_NAME",
                 FILE_ACTION_RENAMED_OLD_NAME);
    setint(dict, "FILE_ACTION_RENAMED_NEW_NAME",
                 FILE_ACTION_RENAMED_NEW_NAME);

    PyModule_AddStringConstant(module, "__version__", WATCHER_VERSION);

#ifdef PYTHON3
    return module;
#endif

fail:
#ifdef PYTHON3
    return NULL;
#else
    return;
#endif
}
