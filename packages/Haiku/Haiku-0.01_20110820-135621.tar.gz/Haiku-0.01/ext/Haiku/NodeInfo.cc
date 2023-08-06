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
//static int Haiku_NodeInfo_init(Haiku_NodeInfo_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_NodeInfo_init(Haiku_NodeInfo_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BNode* node;
	Haiku_Node_Object* py_node; // from generate_py()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "O", &py_node);
	if (py_node != NULL) {
		node = ((Haiku_Node_Object*)py_node)->cpp_object;
	}
	
	python_self->cpp_object = new BNodeInfo(node);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_NodeInfo_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_NodeInfo_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_NodeInfo_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_NodeInfo_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BNodeInfo();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_NodeInfo_DESTROY(Haiku_NodeInfo_Object* python_self);
static void Haiku_NodeInfo_DESTROY(Haiku_NodeInfo_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_NodeInfo_SetTo(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_SetTo(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	BNode* node;
	Haiku_Node_Object* py_node; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_node);
	if (py_node != NULL) {
		node = ((Haiku_Node_Object*)py_node)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTo(node);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_NodeInfo_InitCheck(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_InitCheck(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	status_t retval;
	
	retval = python_self->cpp_object->InitCheck();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_NodeInfo_GetType(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_GetType(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	char* type;
	status_t retval;
	PyObject* py_type; // from generate_py()
	
	retval = python_self->cpp_object->GetType(type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_type = Py_BuildValue("s", type);
	return py_type;
}

//static PyObject* Haiku_NodeInfo_SetType(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_SetType(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	const char* type;
	status_t retval;
	PyObject* py_type; // from generate_py()
	
	retval = python_self->cpp_object->SetType(type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_type = Py_BuildValue("s", type);
	return py_type;
}

//static PyObject* Haiku_NodeInfo_GetIconData(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_GetIconData(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	uint8** data;
	size_t size;
	type_code type;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	retval = python_self->cpp_object->GetIcon(data, &size, &type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, size);
	
	return Py_BuildValue("Ok", py_data, type);
}

//static PyObject* Haiku_NodeInfo_SetIconFromData(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_SetIconFromData(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	const uint8* data;
	PyObject* py_data; // from generate_py ()
	size_t size;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	PyString_AsStringAndSize(py_data, (char**)&data, (Py_ssize_t*)&size);
	
	retval = python_self->cpp_object->SetIcon(data, size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_NodeInfo_GetPreferredApp(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_GetPreferredApp(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	char* signature;
	app_verb verb = B_OPEN;
	status_t retval;
	PyObject* py_signature; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|i", &verb);
	
	retval = python_self->cpp_object->GetPreferredApp(signature, verb);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_signature = Py_BuildValue("s", signature);
	return py_signature;
}

//static PyObject* Haiku_NodeInfo_SetPreferredApp(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_SetPreferredApp(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	char* signature;
	app_verb verb = B_OPEN;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|i", &signature, &verb);
	
	retval = python_self->cpp_object->SetPreferredApp(signature, verb);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_NodeInfo_GetAppHint(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_GetAppHint(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetAppHint(ref);
	
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

//static PyObject* Haiku_NodeInfo_SetAppHint(Haiku_NodeInfo_Object* python_self, PyObject* python_args);
static PyObject* Haiku_NodeInfo_SetAppHint(Haiku_NodeInfo_Object* python_self, PyObject* python_args) {
	entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetAppHint(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_NodeInfo_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_NodeInfo_Object*)a)->cpp_object == ((Haiku_NodeInfo_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_NodeInfo_Object*)a)->cpp_object != ((Haiku_NodeInfo_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_NodeInfo_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_NodeInfo_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"SetTo", (PyCFunction)Haiku_NodeInfo_SetTo, METH_VARARGS, ""},
	{"InitCheck", (PyCFunction)Haiku_NodeInfo_InitCheck, METH_VARARGS, ""},
	{"GetType", (PyCFunction)Haiku_NodeInfo_GetType, METH_VARARGS, ""},
	{"SetType", (PyCFunction)Haiku_NodeInfo_SetType, METH_VARARGS, ""},
	{"GetIconData", (PyCFunction)Haiku_NodeInfo_GetIconData, METH_VARARGS, ""},
	{"SetIconFromData", (PyCFunction)Haiku_NodeInfo_SetIconFromData, METH_VARARGS, ""},
	{"GetPreferredApp", (PyCFunction)Haiku_NodeInfo_GetPreferredApp, METH_VARARGS, ""},
	{"SetPreferredApp", (PyCFunction)Haiku_NodeInfo_SetPreferredApp, METH_VARARGS, ""},
	{"GetAppHint", (PyCFunction)Haiku_NodeInfo_GetAppHint, METH_VARARGS, ""},
	{"SetAppHint", (PyCFunction)Haiku_NodeInfo_SetAppHint, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_NodeInfo_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.NodeInfo";
	type->tp_basicsize   = sizeof(Haiku_NodeInfo_Object);
	type->tp_dealloc     = (destructor)Haiku_NodeInfo_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_NodeInfo_RichCompare;
	type->tp_methods     = Haiku_NodeInfo_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_NodeInfo_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

