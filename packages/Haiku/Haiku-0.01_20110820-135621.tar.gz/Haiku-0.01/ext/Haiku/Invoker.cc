/*
 * Automatically generated file
 */

/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Invoker_init(Haiku_Invoker_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Invoker_init(Haiku_Invoker_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	BLooper* looper = NULL;
	Haiku_Looper_Object* py_looper; // from generate_py()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OO|O", &py_message, &py_handler, &py_looper);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	if (py_looper != NULL) {
		looper = ((Haiku_Looper_Object*)py_looper)->cpp_object;
	}
	
	python_self->cpp_object = new BInvoker(message, handler, looper);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Invoker_newWithMessenger(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Invoker_newWithMessenger(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Invoker_Object* python_self;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BMessenger messenger;
	Haiku_Messenger_Object* py_messenger; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Invoker_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "OO", &py_message, &py_messenger);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_messenger != NULL) {
		memcpy((void*)&messenger, (void*)((Haiku_Messenger_Object*)py_messenger)->cpp_object, sizeof(BMessenger));
	}
	
	python_self->cpp_object = new BInvoker(message, messenger);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Invoker_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Invoker_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Invoker_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Invoker_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BInvoker();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Invoker_DESTROY(Haiku_Invoker_Object* python_self);
static void Haiku_Invoker_DESTROY(Haiku_Invoker_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Invoker_SetMessage(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_SetMessage(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetMessage(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_Message(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Message(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Message();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Invoker_Command(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Command(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Command();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Invoker_SetTarget(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_SetTarget(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	BLooper* looper = NULL;
	Haiku_Looper_Object* py_looper; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O|O", &py_handler, &py_looper);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	if (py_looper != NULL) {
		looper = ((Haiku_Looper_Object*)py_looper)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTarget(handler, looper);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_SetTargetMessenger(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_SetTargetMessenger(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessenger messenger;
	Haiku_Messenger_Object* py_messenger; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_messenger);
	if (py_messenger != NULL) {
		memcpy((void*)&messenger, (void*)((Haiku_Messenger_Object*)py_messenger)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->SetTarget(messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_IsTargetLocal(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_IsTargetLocal(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsTargetLocal();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Invoker_Target(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Target(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BLooper* looper = NULL;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py()
	Haiku_Looper_Object* py_looper; // from generate_py()
	
	retval = python_self->cpp_object->Target(&looper);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	py_looper = (Haiku_Looper_Object*)Haiku_Looper_PyType.tp_alloc(&Haiku_Looper_PyType, 0);
	py_looper->cpp_object = (BLooper*)looper;
	// we own this object, so we can delete it
	py_looper->can_delete_cpp_object = true;
	
	return Py_BuildValue("OO", py_retval, py_looper);
}

//static PyObject* Haiku_Invoker_Messenger(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Messenger(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessenger retval;
	Haiku_Messenger_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Messenger();
	
	py_retval = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_retval->cpp_object = (BMessenger*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Invoker_SetHandlerForReply(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_SetHandlerForReply(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetHandlerForReply(handler);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_HandlerForReply(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_HandlerForReply(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->HandlerForReply();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Invoker_Invoke(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Invoke(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessage* message = NULL;
	Haiku_Message_Object* py_message; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->Invoke(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_InvokeNotify(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_InvokeNotify(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	uint32 kind = B_CONTROL_INVOKED;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O|k", &py_message, &kind);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->InvokeNotify(message, kind);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_SetTimeout(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_SetTimeout(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	bigtime_t timeout;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &timeout);
	
	retval = python_self->cpp_object->SetTimeout(timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Invoker_Timeout(Haiku_Invoker_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Invoker_Timeout(Haiku_Invoker_Object* python_self, PyObject* python_args) {
	bigtime_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Timeout();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

static PyObject* Haiku_Invoker_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Invoker_Object*)a)->cpp_object == ((Haiku_Invoker_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Invoker_Object*)a)->cpp_object != ((Haiku_Invoker_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Invoker_PyMethods[] = {
	{"WithMessenger", (PyCFunction)Haiku_Invoker_newWithMessenger, METH_VARARGS|METH_CLASS, ""},
	{"Empty", (PyCFunction)Haiku_Invoker_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"SetMessage", (PyCFunction)Haiku_Invoker_SetMessage, METH_VARARGS, ""},
	{"Message", (PyCFunction)Haiku_Invoker_Message, METH_VARARGS, ""},
	{"Command", (PyCFunction)Haiku_Invoker_Command, METH_VARARGS, ""},
	{"SetTarget", (PyCFunction)Haiku_Invoker_SetTarget, METH_VARARGS, ""},
	{"SetTargetMessenger", (PyCFunction)Haiku_Invoker_SetTargetMessenger, METH_VARARGS, ""},
	{"IsTargetLocal", (PyCFunction)Haiku_Invoker_IsTargetLocal, METH_VARARGS, ""},
	{"Target", (PyCFunction)Haiku_Invoker_Target, METH_VARARGS, ""},
	{"Messenger", (PyCFunction)Haiku_Invoker_Messenger, METH_VARARGS, ""},
	{"SetHandlerForReply", (PyCFunction)Haiku_Invoker_SetHandlerForReply, METH_VARARGS, ""},
	{"HandlerForReply", (PyCFunction)Haiku_Invoker_HandlerForReply, METH_VARARGS, ""},
	{"Invoke", (PyCFunction)Haiku_Invoker_Invoke, METH_VARARGS, ""},
	{"InvokeNotify", (PyCFunction)Haiku_Invoker_InvokeNotify, METH_VARARGS, ""},
	{"SetTimeout", (PyCFunction)Haiku_Invoker_SetTimeout, METH_VARARGS, ""},
	{"Timeout", (PyCFunction)Haiku_Invoker_Timeout, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Invoker_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Invoker";
	type->tp_basicsize   = sizeof(Haiku_Invoker_Object);
	type->tp_dealloc     = (destructor)Haiku_Invoker_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Invoker_RichCompare;
	type->tp_methods     = Haiku_Invoker_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Invoker_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

