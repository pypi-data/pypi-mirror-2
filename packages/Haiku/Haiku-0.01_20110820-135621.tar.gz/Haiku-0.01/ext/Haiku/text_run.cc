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
//static int Haiku_text_run_init(Haiku_text_run_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_text_run_init(Haiku_text_run_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new text_run();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_text_run_DESTROY(Haiku_text_run_Object* python_self);
static void Haiku_text_run_DESTROY(Haiku_text_run_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_text_run_Object_getoffset(Haiku_text_run_Object* python_self, void* python_closure) {
	PyObject* py_offset; // from generate()
	py_offset = Py_BuildValue("l", python_self->cpp_object->offset);
	return py_offset;
}

static int Haiku_text_run_Object_setoffset(Haiku_text_run_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->offset = (int32)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_text_run_Object_getfont(Haiku_text_run_Object* python_self, void* python_closure) {
	Haiku_Font_Object* py_font;

	py_font = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_font->cpp_object = (BFont*)&python_self->cpp_object->font;
	// cannot delete this object; we do not own it
	py_font->can_delete_cpp_object = false;
	return (PyObject*)py_font;
}

static int Haiku_text_run_Object_setfont(Haiku_text_run_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->font, (void*)((Haiku_Font_Object*)value)->cpp_object, sizeof(BFont));
	}
	return 0;
}

static PyObject* Haiku_text_run_Object_getcolor(Haiku_text_run_Object* python_self, void* python_closure) {
	Haiku_rgb_color_Object* py_color;

	py_color = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_color->cpp_object = (rgb_color*)&python_self->cpp_object->color;
	// cannot delete this object; we do not own it
	py_color->can_delete_cpp_object = false;
	return (PyObject*)py_color;
}

static int Haiku_text_run_Object_setcolor(Haiku_text_run_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->color, (void*)((Haiku_rgb_color_Object*)value)->cpp_object, sizeof(rgb_color));
	}
	return 0;
}

static PyObject* Haiku_text_run_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_text_run_Object*)a)->cpp_object == ((Haiku_text_run_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_text_run_Object*)a)->cpp_object != ((Haiku_text_run_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_text_run_PyProperties[] = {
	{ (char*)"offset", (getter)Haiku_text_run_Object_getoffset, (setter)Haiku_text_run_Object_setoffset, (char*)"<DOC>", NULL},
	{ (char*)"font", (getter)Haiku_text_run_Object_getfont, (setter)Haiku_text_run_Object_setfont, (char*)"<DOC>", NULL},
	{ (char*)"color", (getter)Haiku_text_run_Object_getcolor, (setter)Haiku_text_run_Object_setcolor, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_text_run_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.text_run";
	type->tp_basicsize   = sizeof(Haiku_text_run_Object);
	type->tp_dealloc     = (destructor)Haiku_text_run_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_text_run_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_text_run_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_text_run_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

