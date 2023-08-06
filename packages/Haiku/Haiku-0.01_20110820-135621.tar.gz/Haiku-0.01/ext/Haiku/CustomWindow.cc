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
//static int Haiku_CustomWindow_init(Haiku_CustomWindow_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_CustomWindow_init(Haiku_CustomWindow_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* title;
	window_type type;
	uint32 flags;
	uint32 workspaces = B_CURRENT_WORKSPACE;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "Osik|k", &py_frame, &title, &type, &flags, &workspaces);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new Custom_BWindow(frame, title, type, flags, workspaces);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	python_self->cpp_object->python_object = python_self;
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return 0;
}

//static PyObject* Haiku_CustomWindow_newFromLookAndFeel(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomWindow_newFromLookAndFeel(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomWindow_Object* python_self;
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* title;
	window_look look;
	window_feel feel;
	uint32 flags;
	uint32 workspaces = B_CURRENT_WORKSPACE;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomWindow_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "Osiik|k", &py_frame, &title, &look, &feel, &flags, &workspaces);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new Custom_BWindow(frame, title, look, feel, flags, workspaces);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_CustomWindow_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomWindow_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomWindow_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomWindow_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new Custom_BWindow(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we do not own this object, so we can't delete it
	python_self->can_delete_cpp_object = false;
	return (PyObject*)python_self;
}

//static void Haiku_CustomWindow_DESTROY(Haiku_CustomWindow_Object* python_self);
static void Haiku_CustomWindow_DESTROY(Haiku_CustomWindow_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
		else {
			python_self->cpp_object->python_object = NULL;
		}
	}
}

static PyObject* Haiku_CustomWindow_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_CustomWindow_Object*)a)->cpp_object == ((Haiku_CustomWindow_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_CustomWindow_Object*)a)->cpp_object != ((Haiku_CustomWindow_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_CustomWindow_PyMethods[] = {
	{"FromLookAndFeel", (PyCFunction)Haiku_CustomWindow_newFromLookAndFeel, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_CustomWindow_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_CustomWindow_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.CustomWindow";
	type->tp_basicsize   = sizeof(Haiku_CustomWindow_Object);
	type->tp_dealloc     = (destructor)Haiku_CustomWindow_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_CustomWindow_RichCompare;
	type->tp_methods     = Haiku_CustomWindow_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Window_PyType;
	type->tp_init        = (initproc)Haiku_CustomWindow_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

