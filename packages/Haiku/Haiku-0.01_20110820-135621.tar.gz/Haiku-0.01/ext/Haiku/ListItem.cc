/*
 * Automatically generated file
 */

//static PyObject* Haiku_ListItem_Height(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_Height(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Height();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_ListItem_Width(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_Width(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Width();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_ListItem_IsSelected(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_IsSelected(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSelected();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListItem_Select(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_Select(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Select();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_Deselect(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_Deselect(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Deselect();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_SetEnabled(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_SetEnabled(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_IsEnabled(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_IsEnabled(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListItem_SetHeight(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_SetHeight(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	float height;
	
	PyArg_ParseTuple(python_args, "f", &height);
	
	python_self->cpp_object->SetHeight(height);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_SetWidth(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_SetWidth(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	float width;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->SetWidth(width);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_IsExpanded(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_IsExpanded(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsExpanded();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_ListItem_SetExpanded(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_SetExpanded(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	bool expanded;
	PyObject* py_expanded; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_expanded);
	expanded = (bool)(PyObject_IsTrue(py_expanded));
	
	python_self->cpp_object->SetExpanded(expanded);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_ListItem_OutlineLevel(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_OutlineLevel(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->OutlineLevel();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_ListItem_SetOutlineLevel(Haiku_ListItem_Object* python_self, PyObject* python_args);
static PyObject* Haiku_ListItem_SetOutlineLevel(Haiku_ListItem_Object* python_self, PyObject* python_args) {
	uint32 level;
	
	PyArg_ParseTuple(python_args, "k", &level);
	
	python_self->cpp_object->SetOutlineLevel(level);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_ListItem_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_ListItem_Object*)a)->cpp_object == ((Haiku_ListItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_ListItem_Object*)a)->cpp_object != ((Haiku_ListItem_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_ListItem_PyMethods[] = {
	{"Height", (PyCFunction)Haiku_ListItem_Height, METH_VARARGS, ""},
	{"Width", (PyCFunction)Haiku_ListItem_Width, METH_VARARGS, ""},
	{"IsSelected", (PyCFunction)Haiku_ListItem_IsSelected, METH_VARARGS, ""},
	{"Select", (PyCFunction)Haiku_ListItem_Select, METH_VARARGS, ""},
	{"Deselect", (PyCFunction)Haiku_ListItem_Deselect, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_ListItem_SetEnabled, METH_VARARGS, ""},
	{"IsEnabled", (PyCFunction)Haiku_ListItem_IsEnabled, METH_VARARGS, ""},
	{"SetHeight", (PyCFunction)Haiku_ListItem_SetHeight, METH_VARARGS, ""},
	{"SetWidth", (PyCFunction)Haiku_ListItem_SetWidth, METH_VARARGS, ""},
	{"IsExpanded", (PyCFunction)Haiku_ListItem_IsExpanded, METH_VARARGS, ""},
	{"SetExpanded", (PyCFunction)Haiku_ListItem_SetExpanded, METH_VARARGS, ""},
	{"OutlineLevel", (PyCFunction)Haiku_ListItem_OutlineLevel, METH_VARARGS, ""},
	{"SetOutlineLevel", (PyCFunction)Haiku_ListItem_SetOutlineLevel, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_ListItem_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.ListItem";
	type->tp_basicsize   = sizeof(Haiku_ListItem_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_ListItem_RichCompare;
	type->tp_methods     = Haiku_ListItem_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_Archivable_PyType;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

