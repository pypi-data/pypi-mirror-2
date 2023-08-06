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
//static int Haiku_screen_id_init(Haiku_screen_id_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_screen_id_init(Haiku_screen_id_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new screen_id();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_screen_id_DESTROY(Haiku_screen_id_Object* python_self);
static void Haiku_screen_id_DESTROY(Haiku_screen_id_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_screen_id_Object_getid(Haiku_screen_id_Object* python_self, void* python_closure) {
	PyObject* py_id; // from generate()
	py_id = Py_BuildValue("l", python_self->cpp_object->id);
	return py_id;
}

static int Haiku_screen_id_Object_setid(Haiku_screen_id_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->id = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_screen_id_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_screen_id_Object*)a)->cpp_object == ((Haiku_screen_id_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_screen_id_Object*)a)->cpp_object != ((Haiku_screen_id_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_screen_id_PyProperties[] = {
	{ (char*)"id", (getter)Haiku_screen_id_Object_getid, (setter)Haiku_screen_id_Object_setid, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_screen_id_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.screen_id";
	type->tp_basicsize   = sizeof(Haiku_screen_id_Object);
	type->tp_dealloc     = (destructor)Haiku_screen_id_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_screen_id_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_screen_id_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_screen_id_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

