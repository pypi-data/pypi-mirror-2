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
//static int Haiku_unicode_block_init(Haiku_unicode_block_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_unicode_block_init(Haiku_unicode_block_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	uint64 block2;
	uint64 block1;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "kk", &block2, &block1);
	
	python_self->cpp_object = new unicode_block(block2, block1);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_unicode_block_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_unicode_block_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_unicode_block_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_unicode_block_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new unicode_block();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_unicode_block_DESTROY(Haiku_unicode_block_Object* python_self);
static void Haiku_unicode_block_DESTROY(Haiku_unicode_block_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_unicode_block_Includes(Haiku_unicode_block_Object* python_self, PyObject* python_args);
static PyObject* Haiku_unicode_block_Includes(Haiku_unicode_block_Object* python_self, PyObject* python_args) {
	unicode_block block;
	Haiku_unicode_block_Object* py_block; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_block);
	if (py_block != NULL) {
		memcpy((void*)&block, (void*)((Haiku_unicode_block_Object*)py_block)->cpp_object, sizeof(unicode_block));
	}
	
	retval = python_self->cpp_object->Includes(block);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

static PyObject* Haiku_unicode_block__and__(PyObject* a, PyObject* b) {
	unicode_block* retval = new unicode_block();
	Haiku_unicode_block_Object* py_retval;
	
	*retval = *((Haiku_unicode_block_Object*)a)->cpp_object & *((Haiku_unicode_block_Object*)b)->cpp_object;
	py_retval = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	py_retval->cpp_object = (unicode_block*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_unicode_block__or__(PyObject* a, PyObject* b) {
	unicode_block* retval = new unicode_block();
	Haiku_unicode_block_Object* py_retval;
	
	*retval = *((Haiku_unicode_block_Object*)a)->cpp_object | *((Haiku_unicode_block_Object*)b)->cpp_object;
	py_retval = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	py_retval->cpp_object = (unicode_block*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_unicode_block_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_unicode_block_Object*)a)->cpp_object == *((Haiku_unicode_block_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_unicode_block_Object*)a)->cpp_object != *((Haiku_unicode_block_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_unicode_block_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_unicode_block_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"Includes", (PyCFunction)Haiku_unicode_block_Includes, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static PyNumberMethods Haiku_unicode_block_AsNumber = {
	/* nb_add */	0,
	/* nb_subtract */	0,
	/* nb_multiply */	0,
	/* nb_divide */	0,
	/* nb_remainder */	0,
	/* nb_divmod */	0,
	/* nb_power */	0,
	/* nb_negative */	0,
	/* nb_positive */	0,
	/* nb_absolute */	0,
	/* nb_nonzero */	0,
	/* nb_invert */	0,
	/* nb_lshift */	0,
	/* nb_rshift */	0,
	/* nb_and */	Haiku_unicode_block__and__,
	/* nb_xor */	0,
	/* nb_or */	Haiku_unicode_block__or__,
	/* nb_coerce */	0,
	/* nb_int */	0,
	/* nb_long */	0,
	/* nb_float */	0,
	/* nb_oct */	0,
	/* nb_hex */	0,
	/* nb_inplace_add */	0,
	/* nb_inplace_subtract */	0,
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

static void init_Haiku_unicode_block_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.unicode_block";
	type->tp_basicsize   = sizeof(Haiku_unicode_block_Object);
	type->tp_dealloc     = (destructor)Haiku_unicode_block_DESTROY;
	type->tp_as_number   = &Haiku_unicode_block_AsNumber;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_unicode_block_RichCompare;
	type->tp_methods     = Haiku_unicode_block_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_unicode_block_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

