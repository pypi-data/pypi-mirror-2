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
//static int Haiku_CustomTextView_init(Haiku_CustomTextView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_CustomTextView_init(Haiku_CustomTextView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	BRect textRect;
	Haiku_Rect_Object* py_textRect; // from generate_py()
	uint32 resizingMode;
	uint32 flags;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "OsOkk", &py_frame, &name, &py_textRect, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_textRect != NULL) {
		memcpy((void*)&textRect, (void*)((Haiku_Rect_Object*)py_textRect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object = new Custom_BTextView(frame, name, textRect, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_CustomTextView_newWithFontAndColor(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomTextView_newWithFontAndColor(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomTextView_Object* python_self;
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	const char* name;
	BRect textRect;
	Haiku_Rect_Object* py_textRect; // from generate_py()
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	rgb_color* color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	uint32 resizingMode;
	uint32 flags;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomTextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "OsOOOkk", &py_frame, &name, &py_textRect, &py_font, &py_color, &resizingMode, &flags);
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	if (py_textRect != NULL) {
		memcpy((void*)&textRect, (void*)((Haiku_Rect_Object*)py_textRect)->cpp_object, sizeof(BRect));
	}
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	if (py_color != NULL) {
		color = ((Haiku_rgb_color_Object*)py_color)->cpp_object;
	}
	
	python_self->cpp_object = new Custom_BTextView(frame, name, textRect, font, color, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_CustomTextView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomTextView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomTextView_Object* python_self;
	const char* name;
	uint32 flags;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomTextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sk", &name, &flags);
	
	python_self->cpp_object = new Custom_BTextView(name, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_CustomTextView_newWithFontAndColorAndNoFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomTextView_newWithFontAndColorAndNoFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomTextView_Object* python_self;
	const char* name;
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	rgb_color* color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	uint32 flags;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomTextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sOOk", &name, &py_font, &py_color, &flags);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	if (py_color != NULL) {
		color = ((Haiku_rgb_color_Object*)py_color)->cpp_object;
	}
	
	python_self->cpp_object = new Custom_BTextView(name, font, color, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_CustomTextView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_CustomTextView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_CustomTextView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_CustomTextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new Custom_BTextView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	python_self->cpp_object->python_object = python_self;
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_CustomTextView_DESTROY(Haiku_CustomTextView_Object* python_self);
static void Haiku_CustomTextView_DESTROY(Haiku_CustomTextView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
		else {
			python_self->cpp_object->python_object = NULL;
		}
	}
}

static PyObject* Haiku_CustomTextView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_CustomTextView_Object*)a)->cpp_object == ((Haiku_CustomTextView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_CustomTextView_Object*)a)->cpp_object != ((Haiku_CustomTextView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_CustomTextView_PyMethods[] = {
	{"WithFontAndColor", (PyCFunction)Haiku_CustomTextView_newWithFontAndColor, METH_VARARGS|METH_CLASS, ""},
	{"WithoutFrame", (PyCFunction)Haiku_CustomTextView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"WithFontAndColorAndNoFrame", (PyCFunction)Haiku_CustomTextView_newWithFontAndColorAndNoFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_CustomTextView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_CustomTextView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.CustomTextView";
	type->tp_basicsize   = sizeof(Haiku_CustomTextView_Object);
	type->tp_dealloc     = (destructor)Haiku_CustomTextView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_CustomTextView_RichCompare;
	type->tp_methods     = Haiku_CustomTextView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_TextView_PyType;
	type->tp_init        = (initproc)Haiku_CustomTextView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

