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
//static int Haiku_edge_info_init(Haiku_edge_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_edge_info_init(Haiku_edge_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new edge_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_edge_info_DESTROY(Haiku_edge_info_Object* python_self);
static void Haiku_edge_info_DESTROY(Haiku_edge_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_edge_info_Object_getleft(Haiku_edge_info_Object* python_self, void* python_closure) {
	PyObject* py_left; // from generate()
	py_left = Py_BuildValue("f", python_self->cpp_object->left);
	return py_left;
}

static int Haiku_edge_info_Object_setleft(Haiku_edge_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_edge_info_Object_getright(Haiku_edge_info_Object* python_self, void* python_closure) {
	PyObject* py_right; // from generate()
	py_right = Py_BuildValue("f", python_self->cpp_object->right);
	return py_right;
}

static int Haiku_edge_info_Object_setright(Haiku_edge_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_edge_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_edge_info_Object*)a)->cpp_object == ((Haiku_edge_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_edge_info_Object*)a)->cpp_object != ((Haiku_edge_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_edge_info_PyProperties[] = {
	{ (char*)"left", (getter)Haiku_edge_info_Object_getleft, (setter)Haiku_edge_info_Object_setleft, (char*)"<DOC>", NULL},
	{ (char*)"right", (getter)Haiku_edge_info_Object_getright, (setter)Haiku_edge_info_Object_setright, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_edge_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.edge_info";
	type->tp_basicsize   = sizeof(Haiku_edge_info_Object);
	type->tp_dealloc     = (destructor)Haiku_edge_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_edge_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_edge_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_edge_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

