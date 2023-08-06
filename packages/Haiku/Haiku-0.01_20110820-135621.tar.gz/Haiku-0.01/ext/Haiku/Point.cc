/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_PointConstants_PyMethods[] = {
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
//static int Haiku_Point_init(Haiku_Point_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Point_init(Haiku_Point_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	float x;
	float y;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object = new BPoint(x, y);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Point_newFromPoint(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Point_newFromPoint(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Point_Object* python_self;
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Point_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object = new BPoint(point);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Point_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Point_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Point_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Point_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BPoint();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Point_DESTROY(Haiku_Point_Object* python_self);
static void Haiku_Point_DESTROY(Haiku_Point_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Point_Set(Haiku_Point_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Point_Set(Haiku_Point_Object* python_self, PyObject* python_args) {
	float x;
	float y;
	
	PyArg_ParseTuple(python_args, "ff", &x, &y);
	
	python_self->cpp_object->Set(x, y);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Point_ConstrainTo(Haiku_Point_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Point_ConstrainTo(Haiku_Point_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->ConstrainTo(rect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Point_PrintToStream(Haiku_Point_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Point_PrintToStream(Haiku_Point_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PrintToStream();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Point_Object_getx(Haiku_Point_Object* python_self, void* python_closure) {
	PyObject* py_x; // from generate()
	py_x = Py_BuildValue("f", python_self->cpp_object->x);
	return py_x;
}

static int Haiku_Point_Object_setx(Haiku_Point_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->x = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Point_Object_gety(Haiku_Point_Object* python_self, void* python_closure) {
	PyObject* py_y; // from generate()
	py_y = Py_BuildValue("f", python_self->cpp_object->y);
	return py_y;
}

static int Haiku_Point_Object_sety(Haiku_Point_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->y = (float)PyFloat_AsDouble(value);
	return 0;
}

static PyObject* Haiku_Point__neg__(PyObject* a) {
	BPoint* retval = new BPoint();
	Haiku_Point_Object* py_retval;
	
	*retval = -(*((Haiku_Point_Object*)a)->cpp_object);
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Point__add__(PyObject* a, PyObject* b) {
	BPoint* retval = new BPoint();
	Haiku_Point_Object* py_retval;
	
	*retval = *((Haiku_Point_Object*)a)->cpp_object + *((Haiku_Point_Object*)b)->cpp_object;
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Point__sub__(PyObject* a, PyObject* b) {
	BPoint* retval = new BPoint();
	Haiku_Point_Object* py_retval;
	
	*retval = *((Haiku_Point_Object*)a)->cpp_object - *((Haiku_Point_Object*)b)->cpp_object;
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_Point__iadd__(PyObject* a, PyObject* b) {
	*((Haiku_Point_Object*)a)->cpp_object += *((Haiku_Point_Object*)b)->cpp_object;
	return (PyObject*)a;
}

static PyObject* Haiku_Point__isub__(PyObject* a, PyObject* b) {
	*((Haiku_Point_Object*)a)->cpp_object -= *((Haiku_Point_Object*)b)->cpp_object;
	return (PyObject*)a;
}

static PyObject* Haiku_Point_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Point_Object*)a)->cpp_object == *((Haiku_Point_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Point_Object*)a)->cpp_object != *((Haiku_Point_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_Point_PyProperties[] = {
	{ (char*)"x", (getter)Haiku_Point_Object_getx, (setter)Haiku_Point_Object_setx, (char*)"<DOC>", NULL},
	{ (char*)"y", (getter)Haiku_Point_Object_gety, (setter)Haiku_Point_Object_sety, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static PyMethodDef Haiku_Point_PyMethods[] = {
	{"FromPoint", (PyCFunction)Haiku_Point_newFromPoint, METH_VARARGS|METH_CLASS, ""},
	{"Empty", (PyCFunction)Haiku_Point_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"Set", (PyCFunction)Haiku_Point_Set, METH_VARARGS, ""},
	{"ConstrainTo", (PyCFunction)Haiku_Point_ConstrainTo, METH_VARARGS, ""},
	{"PrintToStream", (PyCFunction)Haiku_Point_PrintToStream, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static PyNumberMethods Haiku_Point_AsNumber = {
	/* nb_add */	Haiku_Point__add__,
	/* nb_subtract */	Haiku_Point__sub__,
	/* nb_multiply */	0,
	/* nb_divide */	0,
	/* nb_remainder */	0,
	/* nb_divmod */	0,
	/* nb_power */	0,
	/* nb_negative */	Haiku_Point__neg__,
	/* nb_positive */	0,
	/* nb_absolute */	0,
	/* nb_nonzero */	0,
	/* nb_invert */	0,
	/* nb_lshift */	0,
	/* nb_rshift */	0,
	/* nb_and */	0,
	/* nb_xor */	0,
	/* nb_or */	0,
	/* nb_coerce */	0,
	/* nb_int */	0,
	/* nb_long */	0,
	/* nb_float */	0,
	/* nb_oct */	0,
	/* nb_hex */	0,
	/* nb_inplace_add */	Haiku_Point__iadd__,
	/* nb_inplace_subtract */	Haiku_Point__isub__,
	/* nb_inplace_multiply */	0,
	/* nb_inplace_divide */	0,
	/* nb_inplace_remainder */	0,
	/* nb_inplace_power */	0,
	/* nb_inplace_lshift */	0,
	/* nb_inplace_rshift */	0,
	/* nb_inplace_and */	0,
	/* nb_inplace_xor */	0,
	/* nb_inplace_or */	0,
	/* nb_floor_divide */	0,
	/* nb_true_divide */	0,
	/* nb_inplace_floor_divide */	0,
	/* nb_inplace_true_divide */	0,
	/* nb_index */	0
};

static void init_Haiku_Point_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Point";
	type->tp_basicsize   = sizeof(Haiku_Point_Object);
	type->tp_dealloc     = (destructor)Haiku_Point_DESTROY;
	type->tp_as_number   = &Haiku_Point_AsNumber;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Point_RichCompare;
	type->tp_methods     = Haiku_Point_PyMethods;
	type->tp_getset      = Haiku_Point_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Point_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

