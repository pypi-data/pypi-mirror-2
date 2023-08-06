/*
 * Automatically generated file
 */

//static PyObject* Haiku_Node_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Node_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Node_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Node_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BNode();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Node_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Node_newFromEntryRef(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Node_Object* python_self;
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Node_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	python_self->cpp_object = new BNode(ref);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Node_newFromEntry(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Node_newFromEntry(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Node_Object* python_self;
	BEntry* entry;
	Haiku_Entry_Object* py_entry; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Node_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_entry);
	if (py_entry != NULL) {
		entry = ((Haiku_Entry_Object*)py_entry)->cpp_object;
	}
	
	python_self->cpp_object = new BNode(entry);
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
//static int Haiku_Node_init(Haiku_Node_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Node_init(Haiku_Node_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* path;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s", &path);
	
	python_self->cpp_object = new BNode(path);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Node_newFromNode(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Node_newFromNode(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Node_Object* python_self;
	const BNode node;
	Haiku_Node_Object* py_node; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Node_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_node);
	if (py_node != NULL) {
		memcpy((void*)&node, (void*)((Haiku_Node_Object*)py_node)->cpp_object, sizeof(const BNode));
	}
	
	python_self->cpp_object = new BNode(node);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Node_DESTROY(Haiku_Node_Object* python_self);
static void Haiku_Node_DESTROY(Haiku_Node_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Node_InitCheck(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_InitCheck(Haiku_Node_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_GetStat(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_GetStat(Haiku_Node_Object* python_self, PyObject* python_args) {
	struct stat* stat;
	status_t retval;
	Haiku_stat_Object* py_stat; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetStat(stat);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_stat = (Haiku_stat_Object*)Haiku_stat_PyType.tp_alloc(&Haiku_stat_PyType, 0);
	py_stat->cpp_object = (struct stat*)stat;
	// we own this object, so we can delete it
	py_stat->can_delete_cpp_object = true;
	return (PyObject*)py_stat;
}

//static PyObject* Haiku_Node_SetToEntryRef(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_SetToEntryRef(Haiku_Node_Object* python_self, PyObject* python_args) {
	const entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTo(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_SetToEntry(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_SetToEntry(Haiku_Node_Object* python_self, PyObject* python_args) {
	const BEntry* entry;
	Haiku_Entry_Object* py_entry; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_entry);
	if (py_entry != NULL) {
		entry = ((Haiku_Entry_Object*)py_entry)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTo(entry);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_SetTo(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_SetTo(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* path;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &path);
	
	retval = python_self->cpp_object->SetTo(path);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_Unset(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_Unset(Haiku_Node_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unset();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_Lock(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_Lock(Haiku_Node_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Lock();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_Unlock(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_Unlock(Haiku_Node_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Unlock();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_Sync(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_Sync(Haiku_Node_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->Sync();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_WriteAttr(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_WriteAttr(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	off_t offset;
	const void* buffer;
	PyObject* py_buffer; // from generate_py ()
	size_t len;
	ssize_t retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sklO", &name, &type, &offset, &py_buffer);
	PyString_AsStringAndSize(py_buffer, (char**)&buffer, (Py_ssize_t*)&len);
	
	retval = python_self->cpp_object->WriteAttr(name, type, offset, buffer, len);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Node_ReadAttr(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_ReadAttr(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* name;
	type_code type;
	off_t offset;
	void* buffer;
	size_t len;
	ssize_t retval;
	PyObject* py_buffer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "skll", &name, &type, &offset, &len);
	
	retval = python_self->cpp_object->ReadAttr(name, type, offset, buffer, len);
	
	py_buffer = Py_BuildValue("s#", &buffer, len);
	
	return Py_BuildValue("lO", retval, py_buffer);
}

//static PyObject* Haiku_Node_RemoveAttr(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_RemoveAttr(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* name;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->RemoveAttr(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_RenameAttr(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_RenameAttr(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* oldname;
	const char* newname;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "ss", &oldname, &newname);
	
	retval = python_self->cpp_object->RenameAttr(oldname, newname);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_GetAttrInfo(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_GetAttrInfo(Haiku_Node_Object* python_self, PyObject* python_args) {
	const char* name;
	attr_info* info = new attr_info();
	status_t retval;
	Haiku_attr_info_Object* py_info; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &name);
	
	retval = python_self->cpp_object->GetAttrInfo(name, info);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_info = (Haiku_attr_info_Object*)Haiku_attr_info_PyType.tp_alloc(&Haiku_attr_info_PyType, 0);
	py_info->cpp_object = (attr_info*)info;
	// we own this object, so we can delete it
	py_info->can_delete_cpp_object = true;
	return (PyObject*)py_info;
}

//static PyObject* Haiku_Node_GetNextAttrName(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_GetNextAttrName(Haiku_Node_Object* python_self, PyObject* python_args) {
	char* buffer;
	status_t retval;
	PyObject* py_buffer; // from generate_py()
	Py_ssize_t py_buffer_length;
	
	retval = python_self->cpp_object->GetNextAttrName(buffer);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_buffer = Py_BuildValue("s", &buffer);	// 's' instead of 's#' lets Python calculate length
	
	py_buffer_length = PyString_Size(py_buffer);
	if (py_buffer_length > B_ATTR_NAME_LENGTH) {
		py_buffer_length = B_ATTR_NAME_LENGTH;
		_PyString_Resize(&py_buffer, py_buffer_length);
	}
	
	return py_buffer;
}

//static PyObject* Haiku_Node_RewindAttrs(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_RewindAttrs(Haiku_Node_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->RewindAttrs();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Node_Dup(Haiku_Node_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Node_Dup(Haiku_Node_Object* python_self, PyObject* python_args) {
	int retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Dup();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

static PyObject* Haiku_Node_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Node_Object*)a)->cpp_object == *((Haiku_Node_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Node_Object*)a)->cpp_object != *((Haiku_Node_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Node_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Node_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"FromEntryRef", (PyCFunction)Haiku_Node_newFromEntryRef, METH_VARARGS|METH_CLASS, ""},
	{"FromEntry", (PyCFunction)Haiku_Node_newFromEntry, METH_VARARGS|METH_CLASS, ""},
	{"FromNode", (PyCFunction)Haiku_Node_newFromNode, METH_VARARGS|METH_CLASS, ""},
	{"InitCheck", (PyCFunction)Haiku_Node_InitCheck, METH_VARARGS, ""},
	{"GetStat", (PyCFunction)Haiku_Node_GetStat, METH_VARARGS, ""},
	{"SetToEntryRef", (PyCFunction)Haiku_Node_SetToEntryRef, METH_VARARGS, ""},
	{"SetToEntry", (PyCFunction)Haiku_Node_SetToEntry, METH_VARARGS, ""},
	{"SetTo", (PyCFunction)Haiku_Node_SetTo, METH_VARARGS, ""},
	{"Unset", (PyCFunction)Haiku_Node_Unset, METH_VARARGS, ""},
	{"Lock", (PyCFunction)Haiku_Node_Lock, METH_VARARGS, ""},
	{"Unlock", (PyCFunction)Haiku_Node_Unlock, METH_VARARGS, ""},
	{"Sync", (PyCFunction)Haiku_Node_Sync, METH_VARARGS, ""},
	{"WriteAttr", (PyCFunction)Haiku_Node_WriteAttr, METH_VARARGS, ""},
	{"ReadAttr", (PyCFunction)Haiku_Node_ReadAttr, METH_VARARGS, ""},
	{"RemoveAttr", (PyCFunction)Haiku_Node_RemoveAttr, METH_VARARGS, ""},
	{"RenameAttr", (PyCFunction)Haiku_Node_RenameAttr, METH_VARARGS, ""},
	{"GetAttrInfo", (PyCFunction)Haiku_Node_GetAttrInfo, METH_VARARGS, ""},
	{"GetNextAttrName", (PyCFunction)Haiku_Node_GetNextAttrName, METH_VARARGS, ""},
	{"RewindAttrs", (PyCFunction)Haiku_Node_RewindAttrs, METH_VARARGS, ""},
	{"Dup", (PyCFunction)Haiku_Node_Dup, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Node_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Node";
	type->tp_basicsize   = sizeof(Haiku_Node_Object);
	type->tp_dealloc     = (destructor)Haiku_Node_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Node_RichCompare;
	type->tp_methods     = Haiku_Node_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Statable_PyType;
	type->tp_init        = (initproc)Haiku_Node_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

