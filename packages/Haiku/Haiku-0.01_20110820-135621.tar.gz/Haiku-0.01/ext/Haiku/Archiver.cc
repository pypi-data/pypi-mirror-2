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
//static int Haiku_Archiver_init(Haiku_Archiver_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Archiver_init(Haiku_Archiver_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
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
	
	python_self->cpp_object = new BArchiver(archive);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_Archiver_DESTROY(Haiku_Archiver_Object* python_self);
static void Haiku_Archiver_DESTROY(Haiku_Archiver_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Archiver_AddArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_AddArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	const char* name;
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	bool deep = true;
	PyObject* py_deep; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO|O", &name, &py_archivable, &py_deep);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->AddArchivable(name, archivable, deep);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Archiver_GetTokenForArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_GetTokenForArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	int32 token;
	status_t retval;
	PyObject* py_token; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archivable);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetTokenForArchivable(archivable, token);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_token = Py_BuildValue("l", token);
	return py_token;
}

//static PyObject* Haiku_Archiver_DeepGetTokenForArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_DeepGetTokenForArchivable(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	bool deep;
	PyObject* py_deep; // from generate_py ()
	int32 token;
	status_t retval;
	PyObject* py_token; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_archivable, &py_deep);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->GetTokenForArchivable(archivable, deep, token);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_token = Py_BuildValue("l", token);
	return py_token;
}

//static PyObject* Haiku_Archiver_IsArchived(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_IsArchived(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archivable);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	
	retval = python_self->cpp_object->IsArchived(archivable);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Archiver_Finish(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_Finish(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	status_t err = B_OK;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|l", &err);
	
	retval = python_self->cpp_object->Finish(err);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Archiver_ArchiveMessage(Haiku_Archiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Archiver_ArchiveMessage(Haiku_Archiver_Object* python_self, PyObject* python_args) {
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->ArchiveMessage();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Archiver_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Archiver_Object*)a)->cpp_object == ((Haiku_Archiver_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Archiver_Object*)a)->cpp_object != ((Haiku_Archiver_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Archiver_PyMethods[] = {
	{"AddArchivable", (PyCFunction)Haiku_Archiver_AddArchivable, METH_VARARGS, ""},
	{"GetTokenForArchivable", (PyCFunction)Haiku_Archiver_GetTokenForArchivable, METH_VARARGS, ""},
	{"DeepGetTokenForArchivable", (PyCFunction)Haiku_Archiver_DeepGetTokenForArchivable, METH_VARARGS, ""},
	{"IsArchived", (PyCFunction)Haiku_Archiver_IsArchived, METH_VARARGS, ""},
	{"Finish", (PyCFunction)Haiku_Archiver_Finish, METH_VARARGS, ""},
	{"ArchiveMessage", (PyCFunction)Haiku_Archiver_ArchiveMessage, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Archiver_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Archiver";
	type->tp_basicsize   = sizeof(Haiku_Archiver_Object);
	type->tp_dealloc     = (destructor)Haiku_Archiver_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Archiver_RichCompare;
	type->tp_methods     = Haiku_Archiver_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Archiver_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

