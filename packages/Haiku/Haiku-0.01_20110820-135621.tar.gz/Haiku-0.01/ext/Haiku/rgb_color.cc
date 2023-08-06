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
//static int Haiku_rgb_color_init(Haiku_rgb_color_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_rgb_color_init(Haiku_rgb_color_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new rgb_color();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_rgb_color_DESTROY(Haiku_rgb_color_Object* python_self);
static void Haiku_rgb_color_DESTROY(Haiku_rgb_color_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_rgb_color_Object_getred(Haiku_rgb_color_Object* python_self, void* python_closure) {
	PyObject* py_red; // from generate()
	py_red = Py_BuildValue("B", python_self->cpp_object->red);
	return py_red;
}

static int Haiku_rgb_color_Object_setred(Haiku_rgb_color_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->red = (uint8)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_rgb_color_Object_getgreen(Haiku_rgb_color_Object* python_self, void* python_closure) {
	PyObject* py_green; // from generate()
	py_green = Py_BuildValue("B", python_self->cpp_object->green);
	return py_green;
}

static int Haiku_rgb_color_Object_setgreen(Haiku_rgb_color_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->green = (uint8)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_rgb_color_Object_getblue(Haiku_rgb_color_Object* python_self, void* python_closure) {
	PyObject* py_blue; // from generate()
	py_blue = Py_BuildValue("B", python_self->cpp_object->blue);
	return py_blue;
}

static int Haiku_rgb_color_Object_setblue(Haiku_rgb_color_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->blue = (uint8)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_rgb_color_Object_getalpha(Haiku_rgb_color_Object* python_self, void* python_closure) {
	PyObject* py_alpha; // from generate()
	py_alpha = Py_BuildValue("B", python_self->cpp_object->alpha);
	return py_alpha;
}

static int Haiku_rgb_color_Object_setalpha(Haiku_rgb_color_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->alpha = (uint8)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_rgb_color_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_rgb_color_Object*)a)->cpp_object == *((Haiku_rgb_color_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_rgb_color_Object*)a)->cpp_object != *((Haiku_rgb_color_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_rgb_color_PyProperties[] = {
	{ (char*)"red", (getter)Haiku_rgb_color_Object_getred, (setter)Haiku_rgb_color_Object_setred, (char*)"<DOC>", NULL},
	{ (char*)"green", (getter)Haiku_rgb_color_Object_getgreen, (setter)Haiku_rgb_color_Object_setgreen, (char*)"<DOC>", NULL},
	{ (char*)"blue", (getter)Haiku_rgb_color_Object_getblue, (setter)Haiku_rgb_color_Object_setblue, (char*)"<DOC>", NULL},
	{ (char*)"alpha", (getter)Haiku_rgb_color_Object_getalpha, (setter)Haiku_rgb_color_Object_setalpha, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_rgb_color_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.rgb_color";
	type->tp_basicsize   = sizeof(Haiku_rgb_color_Object);
	type->tp_dealloc     = (destructor)Haiku_rgb_color_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_rgb_color_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_rgb_color_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_rgb_color_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

