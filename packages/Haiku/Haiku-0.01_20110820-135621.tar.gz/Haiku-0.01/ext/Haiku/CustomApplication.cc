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
//static int Haiku_CustomApplication_init(Haiku_CustomApplication_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_CustomApplication_init(Haiku_CustomApplication_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* signature;
	status_t error;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s", &signature);
	
	python_self->cpp_object = new Custom_BApplication(signature, &error);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	if (error != B_OK) {
		PyObject* errval = Py_BuildValue("l", error);
		PyErr_SetObject(HaikuError, errval);
		return -1;
	}
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_CustomApplication_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomApplication_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomApplication_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomApplication_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new Custom_BApplication(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_CustomApplication_DESTROY(Haiku_CustomApplication_Object* python_self);
static void Haiku_CustomApplication_DESTROY(Haiku_CustomApplication_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
		else {
			python_self->cpp_object->python_object = NULL;
		}
	}
}

static PyObject* Haiku_CustomApplication_Object_be_app(Haiku_CustomApplication_Object* python_dummy) {
	Haiku_Application_Object* py_be_app;
	py_be_app = (Haiku_Application_Object*)Haiku_Application_PyType.tp_alloc(&Haiku_Application_PyType, 0);
	py_be_app->cpp_object = (BApplication*)be_app;
	// cannot delete this object; we do not own it
	py_be_app->can_delete_cpp_object = false;
	return (PyObject*)py_be_app;
}

static PyObject* Haiku_CustomApplication_Object_be_app_messenger(Haiku_CustomApplication_Object* python_dummy) {
	Haiku_Messenger_Object* py_be_app_messenger;
	py_be_app_messenger = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_be_app_messenger->cpp_object = (BMessenger*)&be_app_messenger;
	// cannot delete this object; we do not own it
	py_be_app_messenger->can_delete_cpp_object = false;
	return (PyObject*)py_be_app_messenger;
}

static PyObject* Haiku_CustomApplication_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_CustomApplication_Object*)a)->cpp_object == ((Haiku_CustomApplication_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_CustomApplication_Object*)a)->cpp_object != ((Haiku_CustomApplication_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_CustomApplication_PyMethods[] = {
	{"FromArchive", (PyCFunction)Haiku_CustomApplication_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"be_app", (PyCFunction)Haiku_CustomApplication_Object_be_app, METH_NOARGS|METH_STATIC, ""},
	{"be_app_messenger", (PyCFunction)Haiku_CustomApplication_Object_be_app_messenger, METH_NOARGS|METH_STATIC, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_CustomApplication_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.CustomApplication";
	type->tp_basicsize   = sizeof(Haiku_CustomApplication_Object);
	type->tp_dealloc     = (destructor)Haiku_CustomApplication_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_CustomApplication_RichCompare;
	type->tp_methods     = Haiku_CustomApplication_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Application_PyType;
	type->tp_init        = (initproc)Haiku_CustomApplication_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

