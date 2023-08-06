/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_UnarchiverConstants_PyMethods[] = {
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
//static int Haiku_Unarchiver_init(Haiku_Unarchiver_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Unarchiver_init(Haiku_Unarchiver_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
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
	
	python_self->cpp_object = new BUnarchiver(archive);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_Unarchiver_DESTROY(Haiku_Unarchiver_Object* python_self);
static void Haiku_Unarchiver_DESTROY(Haiku_Unarchiver_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Unarchiver_EnsureUnarchived(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_EnsureUnarchived(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index = 0;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|l", &name, &index);
	
	retval = python_self->cpp_object->EnsureUnarchived(name, index);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Unarchiver_EnsureUnarchivedByToken(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_EnsureUnarchivedByToken(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	int32 token;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &token);
	
	retval = python_self->cpp_object->EnsureUnarchived(token);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Unarchiver_IsInstantiated(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_IsInstantiated(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	const char* name;
	int32 index = 0;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s|l", &name, &index);
	
	retval = python_self->cpp_object->IsInstantiated(name, index);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Unarchiver_IsInstantiatedByToken(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_IsInstantiatedByToken(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	int32 token;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &token);
	
	retval = python_self->cpp_object->IsInstantiated(token);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Unarchiver_Finish(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_Finish(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_Unarchiver_ArchiveMessage(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_ArchiveMessage(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	const BMessage* retval;
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

//static PyObject* Haiku_Unarchiver_AssumeOwnership(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_AssumeOwnership(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archivable);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	
	python_self->cpp_object->AssumeOwnership(archivable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Unarchiver_RelinquishOwnership(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_RelinquishOwnership(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	BArchivable* archivable;
	Haiku_Archivable_Object* py_archivable; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archivable);
	if (py_archivable != NULL) {
		archivable = ((Haiku_Archivable_Object*)py_archivable)->cpp_object;
	}
	
	python_self->cpp_object->RelinquishOwnership(archivable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Unarchiver_IsArchiveManaged(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_IsArchiveManaged(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->IsArchiveManaged(archive);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Unarchiver_PrepareArchive(Haiku_Unarchiver_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Unarchiver_PrepareArchive(Haiku_Unarchiver_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	BMessage* retval;
	Haiku_Message_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->PrepareArchive(archive);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_retval->cpp_object = (BMessage*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Unarchiver_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Unarchiver_Object*)a)->cpp_object == ((Haiku_Unarchiver_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Unarchiver_Object*)a)->cpp_object != ((Haiku_Unarchiver_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Unarchiver_PyMethods[] = {
	{"EnsureUnarchived", (PyCFunction)Haiku_Unarchiver_EnsureUnarchived, METH_VARARGS, ""},
	{"EnsureUnarchivedByToken", (PyCFunction)Haiku_Unarchiver_EnsureUnarchivedByToken, METH_VARARGS, ""},
	{"IsInstantiated", (PyCFunction)Haiku_Unarchiver_IsInstantiated, METH_VARARGS, ""},
	{"IsInstantiatedByToken", (PyCFunction)Haiku_Unarchiver_IsInstantiatedByToken, METH_VARARGS, ""},
	{"Finish", (PyCFunction)Haiku_Unarchiver_Finish, METH_VARARGS, ""},
	{"ArchiveMessage", (PyCFunction)Haiku_Unarchiver_ArchiveMessage, METH_VARARGS, ""},
	{"AssumeOwnership", (PyCFunction)Haiku_Unarchiver_AssumeOwnership, METH_VARARGS, ""},
	{"RelinquishOwnership", (PyCFunction)Haiku_Unarchiver_RelinquishOwnership, METH_VARARGS, ""},
	{"IsArchiveManaged", (PyCFunction)Haiku_Unarchiver_IsArchiveManaged, METH_VARARGS, ""},
	{"PrepareArchive", (PyCFunction)Haiku_Unarchiver_PrepareArchive, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Unarchiver_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Unarchiver";
	type->tp_basicsize   = sizeof(Haiku_Unarchiver_Object);
	type->tp_dealloc     = (destructor)Haiku_Unarchiver_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Unarchiver_RichCompare;
	type->tp_methods     = Haiku_Unarchiver_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Unarchiver_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

