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
//static int Haiku_tuned_font_info_init(Haiku_tuned_font_info_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_tuned_font_info_init(Haiku_tuned_font_info_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new tuned_font_info();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_tuned_font_info_DESTROY(Haiku_tuned_font_info_Object* python_self);
static void Haiku_tuned_font_info_DESTROY(Haiku_tuned_font_info_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_tuned_font_info_Object_getsize(Haiku_tuned_font_info_Object* python_self, void* python_closure) {
	PyObject* py_size; // from generate()
	py_size = Py_BuildValue("f", python_self->cpp_object->size);
	return py_size;
}

static int Haiku_tuned_font_info_Object_setsize(Haiku_tuned_font_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->size = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_tuned_font_info_Object_getshear(Haiku_tuned_font_info_Object* python_self, void* python_closure) {
	PyObject* py_shear; // from generate()
	py_shear = Py_BuildValue("f", python_self->cpp_object->shear);
	return py_shear;
}

static int Haiku_tuned_font_info_Object_setshear(Haiku_tuned_font_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->shear = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_tuned_font_info_Object_getrotation(Haiku_tuned_font_info_Object* python_self, void* python_closure) {
	PyObject* py_rotation; // from generate()
	py_rotation = Py_BuildValue("f", python_self->cpp_object->rotation);
	return py_rotation;
}

static int Haiku_tuned_font_info_Object_setrotation(Haiku_tuned_font_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->rotation = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_tuned_font_info_Object_getflags(Haiku_tuned_font_info_Object* python_self, void* python_closure) {
	PyObject* py_flags; // from generate()
	py_flags = Py_BuildValue("l", python_self->cpp_object->flags);
	return py_flags;
}

static int Haiku_tuned_font_info_Object_setflags(Haiku_tuned_font_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->flags = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_tuned_font_info_Object_getface(Haiku_tuned_font_info_Object* python_self, void* python_closure) {
	PyObject* py_face; // from generate()
	py_face = Py_BuildValue("h", python_self->cpp_object->face);
	return py_face;
}

static int Haiku_tuned_font_info_Object_setface(Haiku_tuned_font_info_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->face = (int16)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_tuned_font_info_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_tuned_font_info_Object*)a)->cpp_object == ((Haiku_tuned_font_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_tuned_font_info_Object*)a)->cpp_object != ((Haiku_tuned_font_info_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_tuned_font_info_PyProperties[] = {
	{ (char*)"size", (getter)Haiku_tuned_font_info_Object_getsize, (setter)Haiku_tuned_font_info_Object_setsize, (char*)"<DOC>", NULL},
	{ (char*)"shear", (getter)Haiku_tuned_font_info_Object_getshear, (setter)Haiku_tuned_font_info_Object_setshear, (char*)"<DOC>", NULL},
	{ (char*)"rotation", (getter)Haiku_tuned_font_info_Object_getrotation, (setter)Haiku_tuned_font_info_Object_setrotation, (char*)"<DOC>", NULL},
	{ (char*)"flags", (getter)Haiku_tuned_font_info_Object_getflags, (setter)Haiku_tuned_font_info_Object_setflags, (char*)"<DOC>", NULL},
	{ (char*)"face", (getter)Haiku_tuned_font_info_Object_getface, (setter)Haiku_tuned_font_info_Object_setface, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_tuned_font_info_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.tuned_font_info";
	type->tp_basicsize   = sizeof(Haiku_tuned_font_info_Object);
	type->tp_dealloc     = (destructor)Haiku_tuned_font_info_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_tuned_font_info_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_tuned_font_info_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_tuned_font_info_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

