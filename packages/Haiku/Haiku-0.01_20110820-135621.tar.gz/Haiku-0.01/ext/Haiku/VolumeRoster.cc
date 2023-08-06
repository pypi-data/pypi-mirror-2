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
//static int Haiku_VolumeRoster_init(Haiku_VolumeRoster_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_VolumeRoster_init(Haiku_VolumeRoster_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BVolumeRoster();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_VolumeRoster_DESTROY(Haiku_VolumeRoster_Object* python_self);
static void Haiku_VolumeRoster_DESTROY(Haiku_VolumeRoster_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_VolumeRoster_GetNextVolume(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_GetNextVolume(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	BVolume* volume = new BVolume();
	status_t retval;
	Haiku_Volume_Object* py_volume; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetNextVolume(volume);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_volume = (Haiku_Volume_Object*)Haiku_Volume_PyType.tp_alloc(&Haiku_Volume_PyType, 0);
	py_volume->cpp_object = (BVolume*)volume;
	// we own this object, so we can delete it
	py_volume->can_delete_cpp_object = true;
	return (PyObject*)py_volume;
}

//static PyObject* Haiku_VolumeRoster_Rewind(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_Rewind(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Rewind();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_VolumeRoster_GetBootVolume(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_GetBootVolume(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	BVolume* volume = new BVolume();
	status_t retval;
	Haiku_Volume_Object* py_volume; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetBootVolume(volume);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_volume = (Haiku_Volume_Object*)Haiku_Volume_PyType.tp_alloc(&Haiku_Volume_PyType, 0);
	py_volume->cpp_object = (BVolume*)volume;
	// we own this object, so we can delete it
	py_volume->can_delete_cpp_object = true;
	return (PyObject*)py_volume;
}

//static PyObject* Haiku_VolumeRoster_StartWatching(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_StartWatching(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	BMessenger name = be_app_messenger;
	Haiku_Messenger_Object* py_name; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|O", &py_name);
	if (py_name != NULL) {
		memcpy((void*)&name, (void*)((Haiku_Messenger_Object*)py_name)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->StartWatching(name);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_VolumeRoster_StopWatching(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_StopWatching(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->StopWatching();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_VolumeRoster_Messenger(Haiku_VolumeRoster_Object* python_self, PyObject* python_args);
static PyObject* Haiku_VolumeRoster_Messenger(Haiku_VolumeRoster_Object* python_self, PyObject* python_args) {
	BMessenger retval;
	Haiku_Messenger_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Messenger();
	
	py_retval = (Haiku_Messenger_Object*)Haiku_Messenger_PyType.tp_alloc(&Haiku_Messenger_PyType, 0);
	py_retval->cpp_object = (BMessenger*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

static PyObject* Haiku_VolumeRoster_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_VolumeRoster_Object*)a)->cpp_object == ((Haiku_VolumeRoster_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_VolumeRoster_Object*)a)->cpp_object != ((Haiku_VolumeRoster_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_VolumeRoster_PyMethods[] = {
	{"GetNextVolume", (PyCFunction)Haiku_VolumeRoster_GetNextVolume, METH_VARARGS, ""},
	{"Rewind", (PyCFunction)Haiku_VolumeRoster_Rewind, METH_VARARGS, ""},
	{"GetBootVolume", (PyCFunction)Haiku_VolumeRoster_GetBootVolume, METH_VARARGS, ""},
	{"StartWatching", (PyCFunction)Haiku_VolumeRoster_StartWatching, METH_VARARGS, ""},
	{"StopWatching", (PyCFunction)Haiku_VolumeRoster_StopWatching, METH_VARARGS, ""},
	{"Messenger", (PyCFunction)Haiku_VolumeRoster_Messenger, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_VolumeRoster_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.VolumeRoster";
	type->tp_basicsize   = sizeof(Haiku_VolumeRoster_Object);
	type->tp_dealloc     = (destructor)Haiku_VolumeRoster_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_VolumeRoster_RichCompare;
	type->tp_methods     = Haiku_VolumeRoster_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_VolumeRoster_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

