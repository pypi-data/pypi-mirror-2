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
//static int Haiku_StringItem_init(Haiku_StringItem_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_StringItem_init(Haiku_StringItem_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* text;
	uint32 outlineLevel = 0;
	bool expanded = true;
	PyObject* py_expanded; // from generate_py ()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|kO", &text, &outlineLevel, &py_expanded);
	expanded = (bool)(PyObject_IsTrue(py_expanded));
	
	python_self->cpp_object = new BStringItem(text, outlineLevel, expanded);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_StringItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_StringItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_StringItem_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_StringItem_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BStringItem(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_StringItem_DESTROY(Haiku_StringItem_Object* python_self);
static void Haiku_StringItem_DESTROY(Haiku_StringItem_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_StringItem_Instantiate(Haiku_StringItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringItem_Instantiate(Haiku_StringItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringItem_Archive(Haiku_StringItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringItem_Archive(Haiku_StringItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_StringItem_SetText(Haiku_StringItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringItem_SetText(Haiku_StringItem_Object* python_self, PyObject* python_args) {
	const char* text;
	
	PyArg_ParseTuple(python_args, "s", &text);
	
	python_self->cpp_object->SetText(text);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_StringItem_Text(Haiku_StringItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_StringItem_Text(Haiku_StringItem_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Text();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

static PyObject* Haiku_StringItem_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_StringItem_Object*)a)->cpp_object == ((Haiku_StringItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_StringItem_Object*)a)->cpp_object != ((Haiku_StringItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_StringItem_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_StringItem_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_StringItem_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_StringItem_Archive, METH_VARARGS, ""},
	{"SetText", (PyCFunction)Haiku_StringItem_SetText, METH_VARARGS, ""},
	{"Text", (PyCFunction)Haiku_StringItem_Text, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_StringItem_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.StringItem";
	type->tp_basicsize   = sizeof(Haiku_StringItem_Object);
	type->tp_dealloc     = (destructor)Haiku_StringItem_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_StringItem_RichCompare;
	type->tp_methods     = Haiku_StringItem_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_ListItem_PyType;
	type->tp_init        = (initproc)Haiku_StringItem_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

