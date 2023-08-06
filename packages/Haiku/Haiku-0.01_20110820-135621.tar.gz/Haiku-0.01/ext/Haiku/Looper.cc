/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_LooperConstants_PyMethods[] = {
	{NULL} /* Sentinel */
};
/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Looper_init(Haiku_Looper_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Looper_init(Haiku_Looper_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name = NULL;
	int32 priority = B_NORMAL_PRIORITY;
	int32 portCapacity = B_LOOPER_PORT_DEFAULT_CAPACITY;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "|sll", &name, &priority, &portCapacity);
	
	python_self->cpp_object = new BLooper(name, priority, portCapacity);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Looper_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Looper_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Looper_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Looper_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BLooper(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Looper_DESTROY(Haiku_Looper_Object* python_self);
static void Haiku_Looper_DESTROY(Haiku_Looper_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Looper_Instantiate(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Instantiate(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	BArchivable* retval;
	Haiku_Archivable_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->Instantiate(data);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Archivable_Object*)Haiku_Archivable_PyType.tp_alloc(&Haiku_Archivable_PyType, 0);
	py_retval->cpp_object = (BArchivable*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_Archive(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Archive(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* data;
	bool deep = true;
	PyObject* py_deep; // from generate_py ()
	status_t retval;
	Haiku_Message_Object* py_data; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_deep);
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->Archive(data, deep);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_data->cpp_object = (BMessage*)data;
	// we own this object, so we can delete it
	py_data->can_delete_cpp_object = true;
	return (PyObject*)py_data;
}

//static PyObject* Haiku_Looper_PostMessage(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_PostMessage(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->PostMessage(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_PostMessageCommand(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_PostMessageCommand(Haiku_Looper_Object* python_self, PyObject* python_args) {
	uint32 command;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k", &command);
	
	retval = python_self->cpp_object->PostMessage(command);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_PostMessageToHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_PostMessageToHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OO|O", &py_message, &py_handler, &py_replyTo);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->PostMessage(message, handler, replyTo);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_PostMessageCommandToHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_PostMessageCommandToHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	uint32 command;
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "kO|O", &command, &py_handler, &py_replyTo);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->PostMessage(command, handler, replyTo);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_DispatchMessage(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_DispatchMessage(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_message, &py_handler);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	python_self->cpp_object->DispatchMessage(message, handler);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_CurrentMessage(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_CurrentMessage(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->CurrentMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_DetachCurrentMessage(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_DetachCurrentMessage(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->DetachCurrentMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_IsMessageWaiting(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_IsMessageWaiting(Haiku_Looper_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsMessageWaiting();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Looper_AddHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_AddHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	python_self->cpp_object->AddHandler(handler);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_RemoveHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_RemoveHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	retval = python_self->cpp_object->RemoveHandler(handler);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Looper_CountHandlers(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_CountHandlers(Haiku_Looper_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountHandlers();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_HandlerAt(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_HandlerAt(Haiku_Looper_Object* python_self, PyObject* python_args) {
	int32 index;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->HandlerAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_IndexOf(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_IndexOf(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	retval = python_self->cpp_object->IndexOf(handler);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_PreferredHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_PreferredHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->PreferredHandler();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_SetPreferredHandler(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_SetPreferredHandler(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	python_self->cpp_object->SetPreferredHandler(handler);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_Run(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Run(Haiku_Looper_Object* python_self, PyObject* python_args) {
	thread_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Run();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_Quit(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Quit(Haiku_Looper_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Quit();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_Lock(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Lock(Haiku_Looper_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Lock();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Looper_Unlock(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Unlock(Haiku_Looper_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unlock();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_IsLocked(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_IsLocked(Haiku_Looper_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLocked();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Looper_LockWithTimeout(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_LockWithTimeout(Haiku_Looper_Object* python_self, PyObject* python_args) {
	bigtime_t timeout;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &timeout);
	
	retval = python_self->cpp_object->LockWithTimeout(timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Looper_Thread(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Thread(Haiku_Looper_Object* python_self, PyObject* python_args) {
	thread_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Thread();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_Team(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Team(Haiku_Looper_Object* python_self, PyObject* python_args) {
	team_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Team();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_LooperForThread(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_LooperForThread(Haiku_Looper_Object* python_self, PyObject* python_args) {
	thread_id thread;
	BLooper* retval;
	Haiku_Looper_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &thread);
	
	retval = python_self->cpp_object->LooperForThread(thread);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Looper_Object*)Haiku_Looper_PyType.tp_alloc(&Haiku_Looper_PyType, 0);
	py_retval->cpp_object = (BLooper*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_LockingThread(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_LockingThread(Haiku_Looper_Object* python_self, PyObject* python_args) {
	thread_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LockingThread();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_CountLocks(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_CountLocks(Haiku_Looper_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountLocks();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_CountLockRequests(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_CountLockRequests(Haiku_Looper_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountLockRequests();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_Sem(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_Sem(Haiku_Looper_Object* python_self, PyObject* python_args) {
	sem_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Sem();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Looper_ResolveSpecifier(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_ResolveSpecifier(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 index;
	BMessage* specifier;
	Haiku_Message_Object* py_specifier; // from generate_py()
	int32 form;
	const char* property;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OlOls", &py_message, &index, &py_specifier, &form, &property);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_specifier != NULL) {
		specifier = ((Haiku_Message_Object*)py_specifier)->cpp_object;
	}
	
	retval = python_self->cpp_object->ResolveSpecifier(message, index, specifier, form, property);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Looper_GetSupportedSuites(Haiku_Looper_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Looper_GetSupportedSuites(Haiku_Looper_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetSupportedSuites(data);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_Looper_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Looper_Object*)a)->cpp_object == ((Haiku_Looper_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Looper_Object*)a)->cpp_object != ((Haiku_Looper_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Looper_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_Looper_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Looper_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Looper_Archive, METH_VARARGS, ""},
	{"PostMessage", (PyCFunction)Haiku_Looper_PostMessage, METH_VARARGS, ""},
	{"PostMessageCommand", (PyCFunction)Haiku_Looper_PostMessageCommand, METH_VARARGS, ""},
	{"PostMessageToHandler", (PyCFunction)Haiku_Looper_PostMessageToHandler, METH_VARARGS, ""},
	{"PostMessageCommandToHandler", (PyCFunction)Haiku_Looper_PostMessageCommandToHandler, METH_VARARGS, ""},
	{"DispatchMessage", (PyCFunction)Haiku_Looper_DispatchMessage, METH_VARARGS, ""},
	{"CurrentMessage", (PyCFunction)Haiku_Looper_CurrentMessage, METH_VARARGS, ""},
	{"DetachCurrentMessage", (PyCFunction)Haiku_Looper_DetachCurrentMessage, METH_VARARGS, ""},
	{"IsMessageWaiting", (PyCFunction)Haiku_Looper_IsMessageWaiting, METH_VARARGS, ""},
	{"AddHandler", (PyCFunction)Haiku_Looper_AddHandler, METH_VARARGS, ""},
	{"RemoveHandler", (PyCFunction)Haiku_Looper_RemoveHandler, METH_VARARGS, ""},
	{"CountHandlers", (PyCFunction)Haiku_Looper_CountHandlers, METH_VARARGS, ""},
	{"HandlerAt", (PyCFunction)Haiku_Looper_HandlerAt, METH_VARARGS, ""},
	{"IndexOf", (PyCFunction)Haiku_Looper_IndexOf, METH_VARARGS, ""},
	{"PreferredHandler", (PyCFunction)Haiku_Looper_PreferredHandler, METH_VARARGS, ""},
	{"SetPreferredHandler", (PyCFunction)Haiku_Looper_SetPreferredHandler, METH_VARARGS, ""},
	{"Run", (PyCFunction)Haiku_Looper_Run, METH_VARARGS, ""},
	{"Quit", (PyCFunction)Haiku_Looper_Quit, METH_VARARGS, ""},
	{"Lock", (PyCFunction)Haiku_Looper_Lock, METH_VARARGS, ""},
	{"Unlock", (PyCFunction)Haiku_Looper_Unlock, METH_VARARGS, ""},
	{"IsLocked", (PyCFunction)Haiku_Looper_IsLocked, METH_VARARGS, ""},
	{"LockWithTimeout", (PyCFunction)Haiku_Looper_LockWithTimeout, METH_VARARGS, ""},
	{"Thread", (PyCFunction)Haiku_Looper_Thread, METH_VARARGS, ""},
	{"Team", (PyCFunction)Haiku_Looper_Team, METH_VARARGS, ""},
	{"LooperForThread", (PyCFunction)Haiku_Looper_LooperForThread, METH_VARARGS, ""},
	{"LockingThread", (PyCFunction)Haiku_Looper_LockingThread, METH_VARARGS, ""},
	{"CountLocks", (PyCFunction)Haiku_Looper_CountLocks, METH_VARARGS, ""},
	{"CountLockRequests", (PyCFunction)Haiku_Looper_CountLockRequests, METH_VARARGS, ""},
	{"Sem", (PyCFunction)Haiku_Looper_Sem, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Looper_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Looper_GetSupportedSuites, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Looper_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Looper";
	type->tp_basicsize   = sizeof(Haiku_Looper_Object);
	type->tp_dealloc     = (destructor)Haiku_Looper_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Looper_RichCompare;
	type->tp_methods     = Haiku_Looper_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Handler_PyType;
	type->tp_init        = (initproc)Haiku_Looper_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

