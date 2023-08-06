/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_MessageConstants_PyMethods[] = {
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
//static int Haiku_Message_init(Haiku_Message_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Message_init(Haiku_Message_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	uint32 command;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "k", &command);
	
	python_self->cpp_object = new BMessage(command);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Message_newCopy(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Message_newCopy(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Message_Object* python_self;
	BMessage message;
	Haiku_Message_Object* py_message; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Message_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		memcpy((void*)&message, (void*)((Haiku_Message_Object*)py_message)->cpp_object, sizeof(BMessage));
	}
	
	python_self->cpp_object = new BMessage(message);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Message_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Message_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Message_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Message_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BMessage();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Message_DESTROY(Haiku_Message_Object* python_self);
static void Haiku_Message_DESTROY(Haiku_Message_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Message_GetInfo(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_GetInfo(Haiku_Message_Object* python_self, PyObject* python_args) {
	type_code typeRequested;
	int32 index;
	char* nameFound;
	type_code typeFound;
	int32 countFound;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "kl", &typeRequested, &index);
	
	retval = python_self->cpp_object->GetInfo(typeRequested, index, &nameFound, &typeFound, &countFound);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	
	return Py_BuildValue("skl", nameFound, typeFound, countFound);
}

//static PyObject* Haiku_Message_GetInfoByName(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_GetInfoByName(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code typeFound;
	int32 countFound;
	bool fixedSize;
	status_t retval;
	PyObject* py_fixedSize; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->GetInfo(name, &typeFound, &countFound, &fixedSize);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_fixedSize = Py_BuildValue("b", (fixedSize ? 1 : 0));
	
	return Py_BuildValue("klO", typeFound, countFound, py_fixedSize);
}

//static PyObject* Haiku_Message_CountNames(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_CountNames(Haiku_Message_Object* python_self, PyObject* python_args) {
	type_code type;
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "k", &type);
	
	retval = python_self->cpp_object->CountNames(type);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Message_IsEmpty(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_IsEmpty(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEmpty();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_IsSystem(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_IsSystem(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSystem();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_IsReply(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_IsReply(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsReply();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_PrintToStream(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_PrintToStream(Haiku_Message_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PrintToStream();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_Rename(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_Rename(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* oldEntry;
	const char* newEntry;
	
	PyArg_ParseTuple(python_args, "ss", &oldEntry, &newEntry);
	
	python_self->cpp_object->Rename(oldEntry, newEntry);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_WasDelivered(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_WasDelivered(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->WasDelivered();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_IsSourceRemote(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_IsSourceRemote(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSourceRemote();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_IsSourceWaiting(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_IsSourceWaiting(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSourceWaiting();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_ReturnAddress(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReturnAddress(Haiku_Message_Object* python_self, PyObject* python_args) {
	BMessenger retval;
	Haiku_Messenger_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ReturnAddress();
	
	py_retval = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_retval->cpp_object = (BMessenger*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Message_Previous(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_Previous(Haiku_Message_Object* python_self, PyObject* python_args) {
	const BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Previous();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Message_WasDropped(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_WasDropped(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->WasDropped();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_DropPoint(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_DropPoint(Haiku_Message_Object* python_self, PyObject* python_args) {
	BPoint* offset = NULL;
	Haiku_Point_Object* py_offset; // from generate_py()
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_offset);
	if (py_offset != NULL) {
		offset = ((Haiku_Point_Object*)py_offset)->cpp_object;
	}
	
	retval = python_self->cpp_object->DropPoint(offset);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Message_SendReply(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SendReply(Haiku_Message_Object* python_self, PyObject* python_args) {
	BMessage* reply;
	Haiku_Message_Object* py_reply; // from generate_py()
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	bigtime_t timeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O|Ol", &py_reply, &py_replyTo, &timeout);
	if (py_reply != NULL) {
		reply = ((Haiku_Message_Object*)py_reply)->cpp_object;
	}
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendReply(reply, replyTo, timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_SendReplyCommand(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SendReplyCommand(Haiku_Message_Object* python_self, PyObject* python_args) {
	uint32 command;
	BHandler* replyTo = NULL;
	Haiku_Handler_Object* py_replyTo; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "k|O", &command, &py_replyTo);
	if (py_replyTo != NULL) {
		replyTo = ((Haiku_Handler_Object*)py_replyTo)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendReply(command, replyTo);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_SendReplyToMessenger(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SendReplyToMessenger(Haiku_Message_Object* python_self, PyObject* python_args) {
	BMessage* reply;
	Haiku_Message_Object* py_reply; // from generate_py()
	BMessenger replyTo;
	Haiku_Messenger_Object* py_replyTo; // from generate_py()
	bigtime_t timeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OO|l", &py_reply, &py_replyTo, &timeout);
	if (py_reply != NULL) {
		reply = ((Haiku_Message_Object*)py_reply)->cpp_object;
	}
	if (py_replyTo != NULL) {
		memcpy((void*)&replyTo, (void*)((Haiku_Messenger_Object*)py_replyTo)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->SendReply(reply, replyTo, timeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_SendReplyWithReplyMessage(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SendReplyWithReplyMessage(Haiku_Message_Object* python_self, PyObject* python_args) {
	uint32 command;
	BMessage* replyToReply;
	Haiku_Message_Object* py_replyToReply; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "kO", &command, &py_replyToReply);
	if (py_replyToReply != NULL) {
		replyToReply = ((Haiku_Message_Object*)py_replyToReply)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendReply(command, replyToReply);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_SendReplyCommandWithReplyMessage(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SendReplyCommandWithReplyMessage(Haiku_Message_Object* python_self, PyObject* python_args) {
	BMessage* reply;
	Haiku_Message_Object* py_reply; // from generate_py()
	BMessage* replyToReply;
	Haiku_Message_Object* py_replyToReply; // from generate_py()
	bigtime_t sendTimeout = B_INFINITE_TIMEOUT;
	bigtime_t replyTimeout = B_INFINITE_TIMEOUT;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "OO|ll", &py_reply, &py_replyToReply, &sendTimeout, &replyTimeout);
	if (py_reply != NULL) {
		reply = ((Haiku_Message_Object*)py_reply)->cpp_object;
	}
	if (py_replyToReply != NULL) {
		replyToReply = ((Haiku_Message_Object*)py_replyToReply)->cpp_object;
	}
	
	retval = python_self->cpp_object->SendReply(reply, replyToReply, sendTimeout, replyTimeout);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_FlattenedSize(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FlattenedSize(Haiku_Message_Object* python_self, PyObject* python_args) {
	ssize_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FlattenedSize();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Message_Flatten(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_Flatten(Haiku_Message_Object* python_self, PyObject* python_args) {
	char* buffer;
	ssize_t size = 0;
	status_t retval;
	PyObject* py_size; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &buffer);
	
	retval = python_self->cpp_object->Flatten(buffer, size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_size = Py_BuildValue("l", size);
	return py_size;
}

//static PyObject* Haiku_Message_Unflatten(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_Unflatten(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* buffer;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &buffer);
	
	retval = python_self->cpp_object->Unflatten(buffer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->AddSpecifier(message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddDirectSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddDirectSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* property;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &property);
	
	retval = python_self->cpp_object->AddSpecifier(property);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddIndexSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddIndexSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* property;
	int32 index;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sl", &property, &index);
	
	retval = python_self->cpp_object->AddSpecifier(property, index);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddRangeSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddRangeSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* property;
	int32 index;
	int32 range;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sll", &property, &index, &range);
	
	retval = python_self->cpp_object->AddSpecifier(property, index, range);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddNameSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddNameSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* property;
	const char* name;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "ss", &property, &name);
	
	retval = python_self->cpp_object->AddSpecifier(property, name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_SetCurrentSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_SetCurrentSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	int32 index;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->SetCurrentSpecifier(index);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_GetCurrentSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_GetCurrentSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	int32 index;
	BMessage* specifier;
	int32 what;
	const char* property;
	status_t retval;
	Haiku_Message_Object* py_specifier; // from generate_py()
	
	retval = python_self->cpp_object->GetCurrentSpecifier(&index, specifier, &what, &property);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_specifier = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_specifier->cpp_object = (BMessage*)specifier;
	// we own this object, so we can delete it
	py_specifier->can_delete_cpp_object = true;
	
	return Py_BuildValue("lOls", index, py_specifier, what, property);
}

//static PyObject* Haiku_Message_HasSpecifiers(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_HasSpecifiers(Haiku_Message_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->HasSpecifiers();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Message_PopSpecifier(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_PopSpecifier(Haiku_Message_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->PopSpecifier();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddRect(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddRect(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->AddRect(name, rect);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddPoint(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddPoint(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->AddPoint(name, point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddString(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddString(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	const char* string;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "ss", &name, &string);
	
	retval = python_self->cpp_object->AddString(name, string);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int8 value;
	PyObject* py_value; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_value);
	PyString2Char(py_value, &value, 1, sizeof(char));
	
	retval = python_self->cpp_object->AddInt8(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddUInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddUInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint8 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sB", &name, &value);
	
	retval = python_self->cpp_object->AddUInt8(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int16 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sh", &name, &value);
	
	retval = python_self->cpp_object->AddInt16(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddUInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddUInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint16 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sH", &name, &value);
	
	retval = python_self->cpp_object->AddUInt16(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sl", &name, &value);
	
	retval = python_self->cpp_object->AddInt32(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddUInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddUInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint32 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sk", &name, &value);
	
	retval = python_self->cpp_object->AddUInt32(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int64 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sl", &name, &value);
	
	retval = python_self->cpp_object->AddInt64(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddUInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddUInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint64 value;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sk", &name, &value);
	
	retval = python_self->cpp_object->AddUInt64(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddBool(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddBool(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	bool aBoolean;
	PyObject* py_aBoolean; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_aBoolean);
	aBoolean = (bool)(PyObject_IsTrue(py_aBoolean));
	
	retval = python_self->cpp_object->AddBool(name, aBoolean);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddFloat(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddFloat(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	float aFloat;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sf", &name, &aFloat);
	
	retval = python_self->cpp_object->AddFloat(name, aFloat);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddDouble(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddDouble(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	double aDouble;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sd", &name, &aDouble);
	
	retval = python_self->cpp_object->AddDouble(name, aDouble);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddPointer(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddPointer(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	const void* aPointer;
	PyObject* py_aPointer; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_aPointer);
	aPointer = PyString_AsString(py_aPointer);
	
	retval = python_self->cpp_object->AddPointer(name, aPointer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddMessenger(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddMessenger(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessenger messenger;
	Haiku_Messenger_Object* py_messenger; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_messenger);
	if (py_messenger != NULL) {
		memcpy((void*)&messenger, (void*)((Haiku_Messenger_Object*)py_messenger)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->AddMessenger(name, messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddRef(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddRef(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	retval = python_self->cpp_object->AddRef(name, ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddMessage(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddMessage(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &name, &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	retval = python_self->cpp_object->AddMessage(name, message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_AddData(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_AddData(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	const void* data;
	PyObject* py_data; // from generate_py ()
	ssize_t numBytes;
	bool isFixedSize = true;
	PyObject* py_isFixedSize; // from generate_py ()
	int32 count = 1;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "skO|Ol", &name, &type, &py_data, &py_isFixedSize, &count);
	PyString_AsStringAndSize(py_data, (char**)&data, (Py_ssize_t*)&numBytes);
	isFixedSize = (bool)(PyObject_IsTrue(py_isFixedSize));
	
	retval = python_self->cpp_object->AddData(name, type, data, numBytes, isFixedSize, count);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_RemoveData(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_RemoveData(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index = 0;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|l", &name, &index);
	
	retval = python_self->cpp_object->RemoveData(name, index);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_RemoveName(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_RemoveName(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->RemoveName(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_MakeEmpty(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_MakeEmpty(Haiku_Message_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->MakeEmpty();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Message_FindRect(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindRect(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BRect rect;
	status_t retval;
	Haiku_Rect_Object* py_rect; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindRect(name, &rect);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_rect = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_rect->cpp_object = (BRect*)&rect;
	// we own this object, so we can delete it
	py_rect->can_delete_cpp_object = true;
	return (PyObject*)py_rect;
}

//static PyObject* Haiku_Message_FindRectByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindRectByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BRect rect;
	status_t retval;
	Haiku_Rect_Object* py_rect; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindRect(name, index, &rect);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_rect = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_rect->cpp_object = (BRect*)&rect;
	// we own this object, so we can delete it
	py_rect->can_delete_cpp_object = true;
	return (PyObject*)py_rect;
}

//static PyObject* Haiku_Message_FindPoint(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindPoint(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BPoint point;
	status_t retval;
	Haiku_Point_Object* py_point; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindPoint(name, &point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_point->cpp_object = (BPoint*)&point;
	// we own this object, so we can delete it
	py_point->can_delete_cpp_object = true;
	return (PyObject*)py_point;
}

//static PyObject* Haiku_Message_FindPointByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindPointByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BPoint point;
	status_t retval;
	Haiku_Point_Object* py_point; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindPoint(name, index, &point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_point->cpp_object = (BPoint*)&point;
	// we own this object, so we can delete it
	py_point->can_delete_cpp_object = true;
	return (PyObject*)py_point;
}

//static PyObject* Haiku_Message_FindString(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindString(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	const char* string;
	status_t retval;
	PyObject* py_string; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindString(name, &string);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_string = Py_BuildValue("s", string);
	return py_string;
}

//static PyObject* Haiku_Message_FindStringByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindStringByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	const char* string;
	status_t retval;
	PyObject* py_string; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindString(name, index, &string);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_string = Py_BuildValue("s", string);
	return py_string;
}

//static PyObject* Haiku_Message_FindInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindInt8(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Char2PyString(&value, 1, sizeof(char));
	return py_value;
}

//static PyObject* Haiku_Message_FindInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindInt8(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Char2PyString(&value, 1, sizeof(char));
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindUInt8(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("B", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindUInt8(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("B", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindInt16(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("h", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindInt16(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("h", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindUInt16(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("H", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindUInt16(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("H", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindInt32(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindInt32(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindUInt32(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindUInt32(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindInt64(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindInt64(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindUInt64(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindUInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindUInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindUInt64(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindBool(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindBool(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	bool value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindBool(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("b", (value ? 1 : 0));
	return py_value;
}

//static PyObject* Haiku_Message_FindBoolByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindBoolByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	bool value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindBool(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("b", (value ? 1 : 0));
	return py_value;
}

//static PyObject* Haiku_Message_FindFloat(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindFloat(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	float value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindFloat(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("f", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindFloatByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindFloatByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	float value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindFloat(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("f", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindDouble(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindDouble(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	double value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindDouble(name, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("d", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindDoubleByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindDoubleByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	double value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindDouble(name, index, &value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("d", value);
	return py_value;
}

//static PyObject* Haiku_Message_FindPointer(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindPointer(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	void** pointer;
	status_t retval;
	PyObject* py_pointer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindPointer(name, pointer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_pointer = Py_BuildValue("s#", pointer, sizeof(void*));
	return py_pointer;
}

//static PyObject* Haiku_Message_FindPointerByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindPointerByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	void** pointer;
	status_t retval;
	PyObject* py_pointer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindPointer(name, index, pointer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_pointer = Py_BuildValue("s#", pointer, sizeof(void*));
	return py_pointer;
}

//static PyObject* Haiku_Message_FindMessenger(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindMessenger(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessenger messenger;
	status_t retval;
	Haiku_Messenger_Object* py_messenger; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindMessenger(name, &messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_messenger->cpp_object = (BMessenger*)&messenger;
	// we own this object, so we can delete it
	py_messenger->can_delete_cpp_object = true;
	return (PyObject*)py_messenger;
}

//static PyObject* Haiku_Message_FindMessengerByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindMessengerByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BMessenger messenger;
	status_t retval;
	Haiku_Messenger_Object* py_messenger; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindMessenger(name, index, &messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_messenger->cpp_object = (BMessenger*)&messenger;
	// we own this object, so we can delete it
	py_messenger->can_delete_cpp_object = true;
	return (PyObject*)py_messenger;
}

//static PyObject* Haiku_Message_FindRef(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindRef(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindRef(name, ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Message_FindRefByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindRefByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindRef(name, index, ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Message_FindMessage(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindMessage(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessage message;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->FindMessage(name, &message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)&message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_Message_FindMessageByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindMessageByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BMessage message;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->FindMessage(name, index, &message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)&message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_Message_FindData(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindData(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	const void** data;
	ssize_t numBytes;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sk", &name, &type);
	
	retval = python_self->cpp_object->FindData(name, type, data, &numBytes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, numBytes);
	return py_data;
}

//static PyObject* Haiku_Message_FindDataByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_FindDataByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	int32 index;
	const void** data;
	ssize_t numBytes;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	PyArg_ParseTuple(python_args, "skl", &name, &type, &index);
	
	retval = python_self->cpp_object->FindData(name, type, index, data, &numBytes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, numBytes);
	return py_data;
}

//static PyObject* Haiku_Message_ReplaceRect(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceRect(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BRect rect;
	status_t retval;
	Haiku_Rect_Object* py_rect; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceRect(name, rect);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_rect = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_rect->cpp_object = (BRect*)&rect;
	// we own this object, so we can delete it
	py_rect->can_delete_cpp_object = true;
	return (PyObject*)py_rect;
}

//static PyObject* Haiku_Message_ReplaceRectByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceRectByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BRect rect;
	status_t retval;
	Haiku_Rect_Object* py_rect; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceRect(name, index, rect);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_rect = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_rect->cpp_object = (BRect*)&rect;
	// we own this object, so we can delete it
	py_rect->can_delete_cpp_object = true;
	return (PyObject*)py_rect;
}

//static PyObject* Haiku_Message_ReplacePoint(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplacePoint(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BPoint point;
	status_t retval;
	Haiku_Point_Object* py_point; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplacePoint(name, point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_point->cpp_object = (BPoint*)&point;
	// we own this object, so we can delete it
	py_point->can_delete_cpp_object = true;
	return (PyObject*)py_point;
}

//static PyObject* Haiku_Message_ReplacePointByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplacePointByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BPoint point;
	status_t retval;
	Haiku_Point_Object* py_point; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplacePoint(name, index, point);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_point = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_point->cpp_object = (BPoint*)&point;
	// we own this object, so we can delete it
	py_point->can_delete_cpp_object = true;
	return (PyObject*)py_point;
}

//static PyObject* Haiku_Message_ReplaceString(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceString(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	const char* string;
	status_t retval;
	PyObject* py_string; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceString(name, string);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_string = Py_BuildValue("s", string);
	return py_string;
}

//static PyObject* Haiku_Message_ReplaceStringByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceStringByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	const char* string;
	status_t retval;
	PyObject* py_string; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceString(name, index, string);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_string = Py_BuildValue("s", string);
	return py_string;
}

//static PyObject* Haiku_Message_ReplaceInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceInt8(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Char2PyString(&value, 1, sizeof(char));
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceInt8(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Char2PyString(&value, 1, sizeof(char));
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt8(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt8(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceUInt8(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("B", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt8ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint8 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceUInt8(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("B", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceInt16(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("h", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceInt16(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("h", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt16(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt16(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceUInt16(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("H", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt16ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint16 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceUInt16(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("H", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceInt32(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceInt32(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt32(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt32(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceUInt32(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt32ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint32 index;
	int32 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sk", &name, &index);
	
	retval = python_self->cpp_object->ReplaceUInt32(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceInt64(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	int64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceInt64(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("l", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt64(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt64(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	uint64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceUInt64(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceUInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceUInt64ByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	uint64 value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceUInt64(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("k", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceBool(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceBool(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	bool value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceBool(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("b", (value ? 1 : 0));
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceBoolByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceBoolByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	bool value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceBool(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("b", (value ? 1 : 0));
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceFloat(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceFloat(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	float value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceFloat(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("f", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceFloatByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceFloatByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	float value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceFloat(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("f", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceDouble(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceDouble(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	double value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceDouble(name, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("d", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplaceDoubleByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceDoubleByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	double value;
	status_t retval;
	PyObject* py_value; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceDouble(name, index, value);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_value = Py_BuildValue("d", value);
	return py_value;
}

//static PyObject* Haiku_Message_ReplacePointer(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplacePointer(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	const void* pointer;
	status_t retval;
	PyObject* py_pointer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplacePointer(name, pointer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_pointer = Py_BuildValue("s#", pointer, sizeof(void*));
	return py_pointer;
}

//static PyObject* Haiku_Message_ReplacePointerByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplacePointerByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	const void* pointer;
	status_t retval;
	PyObject* py_pointer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplacePointer(name, index, pointer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_pointer = Py_BuildValue("s#", pointer, sizeof(void*));
	return py_pointer;
}

//static PyObject* Haiku_Message_ReplaceMessenger(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceMessenger(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessenger messenger;
	status_t retval;
	Haiku_Messenger_Object* py_messenger; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceMessenger(name, messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_messenger->cpp_object = (BMessenger*)&messenger;
	// we own this object, so we can delete it
	py_messenger->can_delete_cpp_object = true;
	return (PyObject*)py_messenger;
}

//static PyObject* Haiku_Message_ReplaceMessengerByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceMessengerByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BMessenger messenger;
	status_t retval;
	Haiku_Messenger_Object* py_messenger; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceMessenger(name, index, messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_messenger->cpp_object = (BMessenger*)&messenger;
	// we own this object, so we can delete it
	py_messenger->can_delete_cpp_object = true;
	return (PyObject*)py_messenger;
}

//static PyObject* Haiku_Message_ReplaceRef(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceRef(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceRef(name, ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Message_ReplaceRefByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceRefByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceRef(name, index, ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Message_ReplaceMessage(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceMessage(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	BMessage* message;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->ReplaceMessage(name, message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_Message_ReplaceMessageByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceMessageByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index;
	BMessage* message;
	status_t retval;
	Haiku_Message_Object* py_message; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "sl", &name, &index);
	
	retval = python_self->cpp_object->ReplaceMessage(name, index, message);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_message = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_message->cpp_object = (BMessage*)message;
	// we own this object, so we can delete it
	py_message->can_delete_cpp_object = true;
	return (PyObject*)py_message;
}

//static PyObject* Haiku_Message_ReplaceData(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceData(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	const void* data;
	ssize_t numBytes;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sk", &name, &type);
	
	retval = python_self->cpp_object->ReplaceData(name, type, data, numBytes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, numBytes);
	return py_data;
}

//static PyObject* Haiku_Message_ReplaceDataByIndex(Haiku_Message_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Message_ReplaceDataByIndex(Haiku_Message_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	int32 index;
	const void* data;
	ssize_t numBytes;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	PyArg_ParseTuple(python_args, "skl", &name, &type, &index);
	
	retval = python_self->cpp_object->ReplaceData(name, type, index, data, numBytes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, numBytes);
	return py_data;
}

static PyObject* Haiku_Message_Object_getwhat(Haiku_Message_Object* python_self, void* python_closure) {
	PyObject* py_what; // from generate()
	py_what = Py_BuildValue("k", python_self->cpp_object->what);
	return py_what;
}

static int Haiku_Message_Object_setwhat(Haiku_Message_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->what = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_Message_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Message_Object*)a)->cpp_object == ((Haiku_Message_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Message_Object*)a)->cpp_object != ((Haiku_Message_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_Message_PyProperties[] = {
	{ (char*)"what", (getter)Haiku_Message_Object_getwhat, (setter)Haiku_Message_Object_setwhat, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static PyMethodDef Haiku_Message_PyMethods[] = {
	{"Copy", (PyCFunction)Haiku_Message_newCopy, METH_VARARGS|METH_CLASS, ""},
	{"Empty", (PyCFunction)Haiku_Message_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"GetInfo", (PyCFunction)Haiku_Message_GetInfo, METH_VARARGS, ""},
	{"GetInfoByName", (PyCFunction)Haiku_Message_GetInfoByName, METH_VARARGS, ""},
	{"CountNames", (PyCFunction)Haiku_Message_CountNames, METH_VARARGS, ""},
	{"IsEmpty", (PyCFunction)Haiku_Message_IsEmpty, METH_VARARGS, ""},
	{"IsSystem", (PyCFunction)Haiku_Message_IsSystem, METH_VARARGS, ""},
	{"IsReply", (PyCFunction)Haiku_Message_IsReply, METH_VARARGS, ""},
	{"PrintToStream", (PyCFunction)Haiku_Message_PrintToStream, METH_VARARGS, ""},
	{"Rename", (PyCFunction)Haiku_Message_Rename, METH_VARARGS, ""},
	{"WasDelivered", (PyCFunction)Haiku_Message_WasDelivered, METH_VARARGS, ""},
	{"IsSourceRemote", (PyCFunction)Haiku_Message_IsSourceRemote, METH_VARARGS, ""},
	{"IsSourceWaiting", (PyCFunction)Haiku_Message_IsSourceWaiting, METH_VARARGS, ""},
	{"ReturnAddress", (PyCFunction)Haiku_Message_ReturnAddress, METH_VARARGS, ""},
	{"Previous", (PyCFunction)Haiku_Message_Previous, METH_VARARGS, ""},
	{"WasDropped", (PyCFunction)Haiku_Message_WasDropped, METH_VARARGS, ""},
	{"DropPoint", (PyCFunction)Haiku_Message_DropPoint, METH_VARARGS, ""},
	{"SendReply", (PyCFunction)Haiku_Message_SendReply, METH_VARARGS, ""},
	{"SendReplyCommand", (PyCFunction)Haiku_Message_SendReplyCommand, METH_VARARGS, ""},
	{"SendReplyToMessenger", (PyCFunction)Haiku_Message_SendReplyToMessenger, METH_VARARGS, ""},
	{"SendReplyWithReplyMessage", (PyCFunction)Haiku_Message_SendReplyWithReplyMessage, METH_VARARGS, ""},
	{"SendReplyCommandWithReplyMessage", (PyCFunction)Haiku_Message_SendReplyCommandWithReplyMessage, METH_VARARGS, ""},
	{"FlattenedSize", (PyCFunction)Haiku_Message_FlattenedSize, METH_VARARGS, ""},
	{"Flatten", (PyCFunction)Haiku_Message_Flatten, METH_VARARGS, ""},
	{"Unflatten", (PyCFunction)Haiku_Message_Unflatten, METH_VARARGS, ""},
	{"AddSpecifier", (PyCFunction)Haiku_Message_AddSpecifier, METH_VARARGS, ""},
	{"AddDirectSpecifier", (PyCFunction)Haiku_Message_AddDirectSpecifier, METH_VARARGS, ""},
	{"AddIndexSpecifier", (PyCFunction)Haiku_Message_AddIndexSpecifier, METH_VARARGS, ""},
	{"AddRangeSpecifier", (PyCFunction)Haiku_Message_AddRangeSpecifier, METH_VARARGS, ""},
	{"AddNameSpecifier", (PyCFunction)Haiku_Message_AddNameSpecifier, METH_VARARGS, ""},
	{"SetCurrentSpecifier", (PyCFunction)Haiku_Message_SetCurrentSpecifier, METH_VARARGS, ""},
	{"GetCurrentSpecifier", (PyCFunction)Haiku_Message_GetCurrentSpecifier, METH_VARARGS, ""},
	{"HasSpecifiers", (PyCFunction)Haiku_Message_HasSpecifiers, METH_VARARGS, ""},
	{"PopSpecifier", (PyCFunction)Haiku_Message_PopSpecifier, METH_VARARGS, ""},
	{"AddRect", (PyCFunction)Haiku_Message_AddRect, METH_VARARGS, ""},
	{"AddPoint", (PyCFunction)Haiku_Message_AddPoint, METH_VARARGS, ""},
	{"AddString", (PyCFunction)Haiku_Message_AddString, METH_VARARGS, ""},
	{"AddInt8", (PyCFunction)Haiku_Message_AddInt8, METH_VARARGS, ""},
	{"AddUInt8", (PyCFunction)Haiku_Message_AddUInt8, METH_VARARGS, ""},
	{"AddInt16", (PyCFunction)Haiku_Message_AddInt16, METH_VARARGS, ""},
	{"AddUInt16", (PyCFunction)Haiku_Message_AddUInt16, METH_VARARGS, ""},
	{"AddInt32", (PyCFunction)Haiku_Message_AddInt32, METH_VARARGS, ""},
	{"AddUInt32", (PyCFunction)Haiku_Message_AddUInt32, METH_VARARGS, ""},
	{"AddInt64", (PyCFunction)Haiku_Message_AddInt64, METH_VARARGS, ""},
	{"AddUInt64", (PyCFunction)Haiku_Message_AddUInt64, METH_VARARGS, ""},
	{"AddBool", (PyCFunction)Haiku_Message_AddBool, METH_VARARGS, ""},
	{"AddFloat", (PyCFunction)Haiku_Message_AddFloat, METH_VARARGS, ""},
	{"AddDouble", (PyCFunction)Haiku_Message_AddDouble, METH_VARARGS, ""},
	{"AddPointer", (PyCFunction)Haiku_Message_AddPointer, METH_VARARGS, ""},
	{"AddMessenger", (PyCFunction)Haiku_Message_AddMessenger, METH_VARARGS, ""},
	{"AddRef", (PyCFunction)Haiku_Message_AddRef, METH_VARARGS, ""},
	{"AddMessage", (PyCFunction)Haiku_Message_AddMessage, METH_VARARGS, ""},
	{"AddData", (PyCFunction)Haiku_Message_AddData, METH_VARARGS, ""},
	{"RemoveData", (PyCFunction)Haiku_Message_RemoveData, METH_VARARGS, ""},
	{"RemoveName", (PyCFunction)Haiku_Message_RemoveName, METH_VARARGS, ""},
	{"MakeEmpty", (PyCFunction)Haiku_Message_MakeEmpty, METH_VARARGS, ""},
	{"FindRect", (PyCFunction)Haiku_Message_FindRect, METH_VARARGS, ""},
	{"FindRectByIndex", (PyCFunction)Haiku_Message_FindRectByIndex, METH_VARARGS, ""},
	{"FindPoint", (PyCFunction)Haiku_Message_FindPoint, METH_VARARGS, ""},
	{"FindPointByIndex", (PyCFunction)Haiku_Message_FindPointByIndex, METH_VARARGS, ""},
	{"FindString", (PyCFunction)Haiku_Message_FindString, METH_VARARGS, ""},
	{"FindStringByIndex", (PyCFunction)Haiku_Message_FindStringByIndex, METH_VARARGS, ""},
	{"FindInt8", (PyCFunction)Haiku_Message_FindInt8, METH_VARARGS, ""},
	{"FindInt8ByIndex", (PyCFunction)Haiku_Message_FindInt8ByIndex, METH_VARARGS, ""},
	{"FindUInt8", (PyCFunction)Haiku_Message_FindUInt8, METH_VARARGS, ""},
	{"FindUInt8ByIndex", (PyCFunction)Haiku_Message_FindUInt8ByIndex, METH_VARARGS, ""},
	{"FindInt16", (PyCFunction)Haiku_Message_FindInt16, METH_VARARGS, ""},
	{"FindInt16ByIndex", (PyCFunction)Haiku_Message_FindInt16ByIndex, METH_VARARGS, ""},
	{"FindUInt16", (PyCFunction)Haiku_Message_FindUInt16, METH_VARARGS, ""},
	{"FindUInt16ByIndex", (PyCFunction)Haiku_Message_FindUInt16ByIndex, METH_VARARGS, ""},
	{"FindInt32", (PyCFunction)Haiku_Message_FindInt32, METH_VARARGS, ""},
	{"FindInt32ByIndex", (PyCFunction)Haiku_Message_FindInt32ByIndex, METH_VARARGS, ""},
	{"FindUInt32", (PyCFunction)Haiku_Message_FindUInt32, METH_VARARGS, ""},
	{"FindUInt32ByIndex", (PyCFunction)Haiku_Message_FindUInt32ByIndex, METH_VARARGS, ""},
	{"FindInt64", (PyCFunction)Haiku_Message_FindInt64, METH_VARARGS, ""},
	{"FindInt64ByIndex", (PyCFunction)Haiku_Message_FindInt64ByIndex, METH_VARARGS, ""},
	{"FindUInt64", (PyCFunction)Haiku_Message_FindUInt64, METH_VARARGS, ""},
	{"FindUInt64ByIndex", (PyCFunction)Haiku_Message_FindUInt64ByIndex, METH_VARARGS, ""},
	{"FindBool", (PyCFunction)Haiku_Message_FindBool, METH_VARARGS, ""},
	{"FindBoolByIndex", (PyCFunction)Haiku_Message_FindBoolByIndex, METH_VARARGS, ""},
	{"FindFloat", (PyCFunction)Haiku_Message_FindFloat, METH_VARARGS, ""},
	{"FindFloatByIndex", (PyCFunction)Haiku_Message_FindFloatByIndex, METH_VARARGS, ""},
	{"FindDouble", (PyCFunction)Haiku_Message_FindDouble, METH_VARARGS, ""},
	{"FindDoubleByIndex", (PyCFunction)Haiku_Message_FindDoubleByIndex, METH_VARARGS, ""},
	{"FindPointer", (PyCFunction)Haiku_Message_FindPointer, METH_VARARGS, ""},
	{"FindPointerByIndex", (PyCFunction)Haiku_Message_FindPointerByIndex, METH_VARARGS, ""},
	{"FindMessenger", (PyCFunction)Haiku_Message_FindMessenger, METH_VARARGS, ""},
	{"FindMessengerByIndex", (PyCFunction)Haiku_Message_FindMessengerByIndex, METH_VARARGS, ""},
	{"FindRef", (PyCFunction)Haiku_Message_FindRef, METH_VARARGS, ""},
	{"FindRefByIndex", (PyCFunction)Haiku_Message_FindRefByIndex, METH_VARARGS, ""},
	{"FindMessage", (PyCFunction)Haiku_Message_FindMessage, METH_VARARGS, ""},
	{"FindMessageByIndex", (PyCFunction)Haiku_Message_FindMessageByIndex, METH_VARARGS, ""},
	{"FindData", (PyCFunction)Haiku_Message_FindData, METH_VARARGS, ""},
	{"FindDataByIndex", (PyCFunction)Haiku_Message_FindDataByIndex, METH_VARARGS, ""},
	{"ReplaceRect", (PyCFunction)Haiku_Message_ReplaceRect, METH_VARARGS, ""},
	{"ReplaceRectByIndex", (PyCFunction)Haiku_Message_ReplaceRectByIndex, METH_VARARGS, ""},
	{"ReplacePoint", (PyCFunction)Haiku_Message_ReplacePoint, METH_VARARGS, ""},
	{"ReplacePointByIndex", (PyCFunction)Haiku_Message_ReplacePointByIndex, METH_VARARGS, ""},
	{"ReplaceString", (PyCFunction)Haiku_Message_ReplaceString, METH_VARARGS, ""},
	{"ReplaceStringByIndex", (PyCFunction)Haiku_Message_ReplaceStringByIndex, METH_VARARGS, ""},
	{"ReplaceInt8", (PyCFunction)Haiku_Message_ReplaceInt8, METH_VARARGS, ""},
	{"ReplaceInt8ByIndex", (PyCFunction)Haiku_Message_ReplaceInt8ByIndex, METH_VARARGS, ""},
	{"ReplaceUInt8", (PyCFunction)Haiku_Message_ReplaceUInt8, METH_VARARGS, ""},
	{"ReplaceUInt8ByIndex", (PyCFunction)Haiku_Message_ReplaceUInt8ByIndex, METH_VARARGS, ""},
	{"ReplaceInt16", (PyCFunction)Haiku_Message_ReplaceInt16, METH_VARARGS, ""},
	{"ReplaceInt16ByIndex", (PyCFunction)Haiku_Message_ReplaceInt16ByIndex, METH_VARARGS, ""},
	{"ReplaceUInt16", (PyCFunction)Haiku_Message_ReplaceUInt16, METH_VARARGS, ""},
	{"ReplaceUInt16ByIndex", (PyCFunction)Haiku_Message_ReplaceUInt16ByIndex, METH_VARARGS, ""},
	{"ReplaceInt32", (PyCFunction)Haiku_Message_ReplaceInt32, METH_VARARGS, ""},
	{"ReplaceInt32ByIndex", (PyCFunction)Haiku_Message_ReplaceInt32ByIndex, METH_VARARGS, ""},
	{"ReplaceUInt32", (PyCFunction)Haiku_Message_ReplaceUInt32, METH_VARARGS, ""},
	{"ReplaceUInt32ByIndex", (PyCFunction)Haiku_Message_ReplaceUInt32ByIndex, METH_VARARGS, ""},
	{"ReplaceInt64", (PyCFunction)Haiku_Message_ReplaceInt64, METH_VARARGS, ""},
	{"ReplaceInt64ByIndex", (PyCFunction)Haiku_Message_ReplaceInt64ByIndex, METH_VARARGS, ""},
	{"ReplaceUInt64", (PyCFunction)Haiku_Message_ReplaceUInt64, METH_VARARGS, ""},
	{"ReplaceUInt64ByIndex", (PyCFunction)Haiku_Message_ReplaceUInt64ByIndex, METH_VARARGS, ""},
	{"ReplaceBool", (PyCFunction)Haiku_Message_ReplaceBool, METH_VARARGS, ""},
	{"ReplaceBoolByIndex", (PyCFunction)Haiku_Message_ReplaceBoolByIndex, METH_VARARGS, ""},
	{"ReplaceFloat", (PyCFunction)Haiku_Message_ReplaceFloat, METH_VARARGS, ""},
	{"ReplaceFloatByIndex", (PyCFunction)Haiku_Message_ReplaceFloatByIndex, METH_VARARGS, ""},
	{"ReplaceDouble", (PyCFunction)Haiku_Message_ReplaceDouble, METH_VARARGS, ""},
	{"ReplaceDoubleByIndex", (PyCFunction)Haiku_Message_ReplaceDoubleByIndex, METH_VARARGS, ""},
	{"ReplacePointer", (PyCFunction)Haiku_Message_ReplacePointer, METH_VARARGS, ""},
	{"ReplacePointerByIndex", (PyCFunction)Haiku_Message_ReplacePointerByIndex, METH_VARARGS, ""},
	{"ReplaceMessenger", (PyCFunction)Haiku_Message_ReplaceMessenger, METH_VARARGS, ""},
	{"ReplaceMessengerByIndex", (PyCFunction)Haiku_Message_ReplaceMessengerByIndex, METH_VARARGS, ""},
	{"ReplaceRef", (PyCFunction)Haiku_Message_ReplaceRef, METH_VARARGS, ""},
	{"ReplaceRefByIndex", (PyCFunction)Haiku_Message_ReplaceRefByIndex, METH_VARARGS, ""},
	{"ReplaceMessage", (PyCFunction)Haiku_Message_ReplaceMessage, METH_VARARGS, ""},
	{"ReplaceMessageByIndex", (PyCFunction)Haiku_Message_ReplaceMessageByIndex, METH_VARARGS, ""},
	{"ReplaceData", (PyCFunction)Haiku_Message_ReplaceData, METH_VARARGS, ""},
	{"ReplaceDataByIndex", (PyCFunction)Haiku_Message_ReplaceDataByIndex, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Message_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Message";
	type->tp_basicsize   = sizeof(Haiku_Message_Object);
	type->tp_dealloc     = (destructor)Haiku_Message_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Message_RichCompare;
	type->tp_methods     = Haiku_Message_PyMethods;
	type->tp_getset      = Haiku_Message_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Message_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

