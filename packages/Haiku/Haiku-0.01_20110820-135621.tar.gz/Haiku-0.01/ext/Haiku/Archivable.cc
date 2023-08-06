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
//static int Haiku_Archivable_init(Haiku_Archivable_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Archivable_init(Haiku_Archivable_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BArchivable(archive);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Archivable_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Archivable_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Archivable_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Archivable_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BArchivable();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Archivable_DESTROY(Haiku_Archivable_Object* python_self);
static void Haiku_Archivable_DESTROY(Haiku_Archivable_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Archivable_Archive(Haiku_Archivable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archivable_Archive(Haiku_Archivable_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Archivable_Instantiate(Haiku_Archivable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archivable_Instantiate(Haiku_Archivable_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Archivable_AllUnarchived(Haiku_Archivable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archivable_AllUnarchived(Haiku_Archivable_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllUnarchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Archivable_AllArchived(Haiku_Archivable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archivable_AllArchived(Haiku_Archivable_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AllArchived(archive);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_Archivable_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Archivable_Object*)a)->cpp_object == ((Haiku_Archivable_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Archivable_Object*)a)->cpp_object != ((Haiku_Archivable_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Archivable_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_Archivable_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"Archive", (PyCFunction)Haiku_Archivable_Archive, METH_VARARGS, ""},
	{"Instantiate", (PyCFunction)Haiku_Archivable_Instantiate, METH_VARARGS, ""},
	{"AllUnarchived", (PyCFunction)Haiku_Archivable_AllUnarchived, METH_VARARGS, ""},
	{"AllArchived", (PyCFunction)Haiku_Archivable_AllArchived, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Archivable_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Archivable";
	type->tp_basicsize   = sizeof(Haiku_Archivable_Object);
	type->tp_dealloc     = (destructor)Haiku_Archivable_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Archivable_RichCompare;
	type->tp_methods     = Haiku_Archivable_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Archivable_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

