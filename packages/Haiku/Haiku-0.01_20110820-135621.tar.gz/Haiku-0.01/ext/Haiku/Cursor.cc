/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_CursorConstants_PyMethods[] = {
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
//static int Haiku_Cursor_init(Haiku_Cursor_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Cursor_init(Haiku_Cursor_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	void* cursorData;
	PyObject* py_cursorData; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "O", &py_cursorData);
	cursorData = PyString_AsString(py_cursorData);
	
	python_self->cpp_object = new BCursor(cursorData);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Cursor_newFromCursor(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Cursor_newFromCursor(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Cursor_Object* python_self;
	BCursor other = *B_CURSOR_SYSTEM_DEFAULT;
	Haiku_Cursor_Object* py_other; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Cursor_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "|O", &py_other);
	if (py_other != NULL) {
		memcpy((void*)&other, (void*)((Haiku_Cursor_Object*)py_other)->cpp_object, sizeof(BCursor));
	}
	
	python_self->cpp_object = new BCursor(other);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Cursor_newFromID(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Cursor_newFromID(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Cursor_Object* python_self;
	BCursorID id;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Cursor_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "i", &id);
	
	python_self->cpp_object = new BCursor(id);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Cursor_newFromMessage(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Cursor_newFromMessage(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Cursor_Object* python_self;
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Cursor_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	python_self->cpp_object = new BCursor(data);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Cursor_DESTROY(Haiku_Cursor_Object* python_self);
static void Haiku_Cursor_DESTROY(Haiku_Cursor_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Cursor_Instantiate(Haiku_Cursor_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Cursor_Instantiate(Haiku_Cursor_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Cursor_Archive(Haiku_Cursor_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Cursor_Archive(Haiku_Cursor_Object* python_self, PyObject* python_args) {
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

static PyObject* Haiku_Cursor_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Cursor_Object*)a)->cpp_object == *((Haiku_Cursor_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Cursor_Object*)a)->cpp_object != *((Haiku_Cursor_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Cursor_PyMethods[] = {
	{"FromCursor", (PyCFunction)Haiku_Cursor_newFromCursor, METH_VARARGS|METH_CLASS, ""},
	{"FromID", (PyCFunction)Haiku_Cursor_newFromID, METH_VARARGS|METH_CLASS, ""},
	{"FromMessage", (PyCFunction)Haiku_Cursor_newFromMessage, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Cursor_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Cursor_Archive, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Cursor_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Cursor";
	type->tp_basicsize   = sizeof(Haiku_Cursor_Object);
	type->tp_dealloc     = (destructor)Haiku_Cursor_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Cursor_RichCompare;
	type->tp_methods     = Haiku_Cursor_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)Haiku_Cursor_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

