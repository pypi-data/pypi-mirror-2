/*
 * Automatically generated file
 */

static PyObject* Haiku_dirent_Object_getd_dev(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_dev; // from generate()
	py_d_dev = Py_BuildValue("l", python_self->cpp_object->d_dev);
	return py_d_dev;
}

static int Haiku_dirent_Object_setd_dev(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->d_dev = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_dirent_Object_getd_pdev(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_pdev; // from generate()
	py_d_pdev = Py_BuildValue("l", python_self->cpp_object->d_pdev);
	return py_d_pdev;
}

static int Haiku_dirent_Object_setd_pdev(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->d_pdev = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_dirent_Object_getd_ino(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_ino; // from generate()
	py_d_ino = Py_BuildValue("l", python_self->cpp_object->d_ino);
	return py_d_ino;
}

static int Haiku_dirent_Object_setd_ino(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->d_ino = (ino_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_dirent_Object_getd_pino(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_pino; // from generate()
	py_d_pino = Py_BuildValue("l", python_self->cpp_object->d_pino);
	return py_d_pino;
}

static int Haiku_dirent_Object_setd_pino(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->d_pino = (ino_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_dirent_Object_getd_reclen(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_reclen; // from generate()
	py_d_reclen = Py_BuildValue("H", python_self->cpp_object->d_reclen);
	return py_d_reclen;
}

static int Haiku_dirent_Object_setd_reclen(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->d_reclen = (unsigned short)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_dirent_Object_getd_name(Haiku_dirent_Object* python_self, void* python_closure) {
	PyObject* py_d_name; // from generate()
	py_d_name = Char2PyString(&python_self->cpp_object->d_name, 1, sizeof(char));
	return py_d_name;
}

static int Haiku_dirent_Object_setd_name(Haiku_dirent_Object* python_self, PyObject* value, void* closure) {
	PyString2Char(value, &python_self->cpp_object->d_name, 1, sizeof(char));
	return 0;
}

static PyObject* Haiku_dirent_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_dirent_Object*)a)->cpp_object == ((Haiku_dirent_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_dirent_Object*)a)->cpp_object != ((Haiku_dirent_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_dirent_PyProperties[] = {
	{ (char*)"d_dev", (getter)Haiku_dirent_Object_getd_dev, (setter)Haiku_dirent_Object_setd_dev, (char*)"<DOC>", NULL},
	{ (char*)"d_pdev", (getter)Haiku_dirent_Object_getd_pdev, (setter)Haiku_dirent_Object_setd_pdev, (char*)"<DOC>", NULL},
	{ (char*)"d_ino", (getter)Haiku_dirent_Object_getd_ino, (setter)Haiku_dirent_Object_setd_ino, (char*)"<DOC>", NULL},
	{ (char*)"d_pino", (getter)Haiku_dirent_Object_getd_pino, (setter)Haiku_dirent_Object_setd_pino, (char*)"<DOC>", NULL},
	{ (char*)"d_reclen", (getter)Haiku_dirent_Object_getd_reclen, (setter)Haiku_dirent_Object_setd_reclen, (char*)"<DOC>", NULL},
	{ (char*)"d_name", (getter)Haiku_dirent_Object_getd_name, (setter)Haiku_dirent_Object_setd_name, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_dirent_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.dirent";
	type->tp_basicsize   = sizeof(Haiku_dirent_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_dirent_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_dirent_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

