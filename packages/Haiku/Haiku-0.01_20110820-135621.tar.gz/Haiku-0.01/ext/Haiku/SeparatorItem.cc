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
//static int Haiku_SeparatorItem_init(Haiku_SeparatorItem_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_SeparatorItem_init(Haiku_SeparatorItem_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BSeparatorItem();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_SeparatorItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_SeparatorItem_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_SeparatorItem_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_SeparatorItem_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BSeparatorItem(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_SeparatorItem_DESTROY(Haiku_SeparatorItem_Object* python_self);
static void Haiku_SeparatorItem_DESTROY(Haiku_SeparatorItem_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_SeparatorItem_Instantiate(Haiku_SeparatorItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_SeparatorItem_Instantiate(Haiku_SeparatorItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_SeparatorItem_Archive(Haiku_SeparatorItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_SeparatorItem_Archive(Haiku_SeparatorItem_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_SeparatorItem_SetEnabled(Haiku_SeparatorItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_SeparatorItem_SetEnabled(Haiku_SeparatorItem_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_SeparatorItem_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_SeparatorItem_Object*)a)->cpp_object == ((Haiku_SeparatorItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_SeparatorItem_Object*)a)->cpp_object != ((Haiku_SeparatorItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_SeparatorItem_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_SeparatorItem_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_SeparatorItem_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_SeparatorItem_Archive, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_SeparatorItem_SetEnabled, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_SeparatorItem_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.SeparatorItem";
	type->tp_basicsize   = sizeof(Haiku_SeparatorItem_Object);
	type->tp_dealloc     = (destructor)Haiku_SeparatorItem_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_SeparatorItem_RichCompare;
	type->tp_methods     = Haiku_SeparatorItem_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_MenuItem_PyType;
	type->tp_init        = (initproc)Haiku_SeparatorItem_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

