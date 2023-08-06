/*
 * Automatically generated file
 */

//static PyObject* Haiku_Messenger_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Messenger_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Messenger_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Messenger_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BMessenger();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_Messenger_init(Haiku_Messenger_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Messenger_init(Haiku_Messenger_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* signature;
	team_id team = -1;
	status_t result;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|l", &signature, &team);
	
	python_self->cpp_object = new BMessenger(signature, team, &result);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	if (result != B_OK) {
		PyObject* errval = Py_BuildValue("l", result);
		PyErr_SetObject(HaikuError, errval);
		return -1;
	}
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Messenger_newCopy(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Messenger_newCopy(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Messenger_Object* python_self;
	BMessenger Messenger;
	Haiku_Messenger_Object* py_Messenger; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Messenger_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_Messenger);
	if (py_Messenger != NULL) {
		memcpy((void*)&Messenger, (void*)((Haiku_Messenger_Object*)py_Messenger)->cpp_object, sizeof(BMessenger));
	}
	
	python_self->cpp_object = new BMessenger(Messenger);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Messenger_DESTROY(Haiku_Messenger_Object* python_self);
static void Haiku_Messenger_DESTROY(Haiku_Messenger_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Messenger_IsTargetLocal(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_IsTargetLocal(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsTargetLocal();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Messenger_Target(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_Target(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	BLooper* Looper;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py()
	Haiku_Looper_Object* py_Looper; // from generate_py()
	
	retval = python_self->cpp_object->Target(&Looper);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	py_Looper = (Haiku_Looper_Object*)Haiku_Looper_PyType.tp_alloc(&Haiku_Looper_PyType, 0);
	py_Looper->cpp_object = (BLooper*)Looper;
	// we own this object, so we can delete it
	py_Looper->can_delete_cpp_object = true;
	
	return Py_BuildValue("OO", py_retval, py_Looper);
}

//static PyObject* Haiku_Messenger_LockTarget(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_LockTarget(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->LockTarget();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Messenger_LockTargetWithTimeout(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_LockTargetWithTimeout(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	bigtime_t timeout;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &timeout);
	
	retval = python_self->cpp_object->LockTargetWithTimeout(timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_SendCommand(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_SendCommand(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	uint32 command;
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k|O", &command, &py_replyTo);
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendMessage(command, replyTo);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_SendMessage(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_SendMessage(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	bigtime_t timeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O|Ol", &py_message, &py_replyTo, &timeout);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendMessage(message, replyTo, timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_SendMessageAndReplyToMessenger(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_SendMessageAndReplyToMessenger(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BMessenger replyTo;
	Haiku_Messenger_Object* py_replyTo; // from generate_py()
	bigtime_t timeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OO|l", &py_message, &py_replyTo, &timeout);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_replyTo != NULL) {
		memcpy((void*)&replyTo, (void*)((Haiku_Messenger_Object*)py_replyTo)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->SendMessage(message, replyTo, timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_SendCommandWithReply(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_SendCommandWithReply(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	uint32 command;
	BMessage* reply;
	Haiku_Message_Object* py_reply; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "kO", &command, &py_reply);
	if (py_reply != NULL) {
		reply = ((Haiku_Message_Object*)py_reply)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendMessage(command, reply);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_SendMessageWithReply(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_SendMessageWithReply(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	BMessage* reply;
	Haiku_Message_Object* py_reply; // from generate_py()
	bigtime_t deliveryTimeout = B_INFINITE_TIMEOUT;
	bigtime_t replyTimeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OO|ll", &py_message, &py_reply, &deliveryTimeout, &replyTimeout);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_reply != NULL) {
		reply = ((Haiku_Message_Object*)py_reply)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendMessage(message, reply, deliveryTimeout, replyTimeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Messenger_IsValid(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_IsValid(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsValid();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Messenger_Team(Haiku_Messenger_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Messenger_Team(Haiku_Messenger_Object* python_self, PyObject* python_args) {
	team_id retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Team();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

static PyObject* Haiku_Messenger_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Messenger_Object*)a)->cpp_object == *((Haiku_Messenger_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Messenger_Object*)a)->cpp_object != *((Haiku_Messenger_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Messenger_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Messenger_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"Copy", (PyCFunction)Haiku_Messenger_newCopy, METH_VARARGS|METH_CLASS, ""},
	{"IsTargetLocal", (PyCFunction)Haiku_Messenger_IsTargetLocal, METH_VARARGS, ""},
	{"Target", (PyCFunction)Haiku_Messenger_Target, METH_VARARGS, ""},
	{"LockTarget", (PyCFunction)Haiku_Messenger_LockTarget, METH_VARARGS, ""},
	{"LockTargetWithTimeout", (PyCFunction)Haiku_Messenger_LockTargetWithTimeout, METH_VARARGS, ""},
	{"SendCommand", (PyCFunction)Haiku_Messenger_SendCommand, METH_VARARGS, ""},
	{"SendMessage", (PyCFunction)Haiku_Messenger_SendMessage, METH_VARARGS, ""},
	{"SendMessageAndReplyToMessenger", (PyCFunction)Haiku_Messenger_SendMessageAndReplyToMessenger, METH_VARARGS, ""},
	{"SendCommandWithReply", (PyCFunction)Haiku_Messenger_SendCommandWithReply, METH_VARARGS, ""},
	{"SendMessageWithReply", (PyCFunction)Haiku_Messenger_SendMessageWithReply, METH_VARARGS, ""},
	{"IsValid", (PyCFunction)Haiku_Messenger_IsValid, METH_VARARGS, ""},
	{"Team", (PyCFunction)Haiku_Messenger_Team, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Messenger_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Messenger";
	type->tp_basicsize   = sizeof(Haiku_Messenger_Object);
	type->tp_dealloc     = (destructor)Haiku_Messenger_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Messenger_RichCompare;
	type->tp_methods     = Haiku_Messenger_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Messenger_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

