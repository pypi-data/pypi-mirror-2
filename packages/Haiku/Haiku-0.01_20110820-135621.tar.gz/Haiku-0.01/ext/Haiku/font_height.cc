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
//static int Haiku_font_height_init(Haiku_font_height_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_font_height_init(Haiku_font_height_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new font_height();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_font_height_DESTROY(Haiku_font_height_Object* python_self);
static void Haiku_font_height_DESTROY(Haiku_font_height_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_font_height_Object_getascent(Haiku_font_height_Object* python_self, void* python_closure) {
	PyObject* py_ascent; // from generate()
	py_ascent = Py_BuildValue("f", python_self->cpp_object->ascent);
	return py_ascent;
}

static int Haiku_font_height_Object_setascent(Haiku_font_height_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->ascent = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_font_height_Object_getdescent(Haiku_font_height_Object* python_self, void* python_closure) {
	PyObject* py_descent; // from generate()
	py_descent = Py_BuildValue("f", python_self->cpp_object->descent);
	return py_descent;
}

static int Haiku_font_height_Object_setdescent(Haiku_font_height_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->descent = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_font_height_Object_getleading(Haiku_font_height_Object* python_self, void* python_closure) {
	PyObject* py_leading; // from generate()
	py_leading = Py_BuildValue("f", python_self->cpp_object->leading);
	return py_leading;
}

static int Haiku_font_height_Object_setleading(Haiku_font_height_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->leading = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_font_height_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_font_height_Object*)a)->cpp_object == ((Haiku_font_height_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_font_height_Object*)a)->cpp_object != ((Haiku_font_height_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_font_height_PyProperties[] = {
	{ (char*)"ascent", (getter)Haiku_font_height_Object_getascent, (setter)Haiku_font_height_Object_setascent, (char*)"<DOC>", NULL},
	{ (char*)"descent", (getter)Haiku_font_height_Object_getdescent, (setter)Haiku_font_height_Object_setdescent, (char*)"<DOC>", NULL},
	{ (char*)"leading", (getter)Haiku_font_height_Object_getleading, (setter)Haiku_font_height_Object_setleading, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_font_height_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.font_height";
	type->tp_basicsize   = sizeof(Haiku_font_height_Object);
	type->tp_dealloc     = (destructor)Haiku_font_height_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_font_height_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_font_height_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_font_height_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

