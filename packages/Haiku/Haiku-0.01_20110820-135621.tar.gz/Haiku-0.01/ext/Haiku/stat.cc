/*
 * Automatically generated file
 */

static PyObject* Haiku_stat_Object_getst_dev(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_dev; // from generate()
	py_st_dev = Py_BuildValue("l", python_self->cpp_object->st_dev);
	return py_st_dev;
}

static int Haiku_stat_Object_setst_dev(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_dev = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_ino(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_ino; // from generate()
	py_st_ino = Py_BuildValue("l", python_self->cpp_object->st_ino);
	return py_st_ino;
}

static int Haiku_stat_Object_setst_ino(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_ino = (ino_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_mode(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_mode; // from generate()
	py_st_mode = Py_BuildValue("l", python_self->cpp_object->st_mode);
	return py_st_mode;
}

static int Haiku_stat_Object_setst_mode(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_mode = (mode_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_nlink(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_nlink; // from generate()
	py_st_nlink = Py_BuildValue("l", python_self->cpp_object->st_nlink);
	return py_st_nlink;
}

static int Haiku_stat_Object_setst_nlink(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_nlink = (nlink_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_uid(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_uid; // from generate()
	py_st_uid = Py_BuildValue("l", python_self->cpp_object->st_uid);
	return py_st_uid;
}

static int Haiku_stat_Object_setst_uid(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_uid = (uid_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_gid(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_gid; // from generate()
	py_st_gid = Py_BuildValue("l", python_self->cpp_object->st_gid);
	return py_st_gid;
}

static int Haiku_stat_Object_setst_gid(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_gid = (gid_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_size(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_size; // from generate()
	py_st_size = Py_BuildValue("l", python_self->cpp_object->st_size);
	return py_st_size;
}

static int Haiku_stat_Object_setst_size(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_size = (off_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_rdev(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_rdev; // from generate()
	py_st_rdev = Py_BuildValue("l", python_self->cpp_object->st_rdev);
	return py_st_rdev;
}

static int Haiku_stat_Object_setst_rdev(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_rdev = (dev_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_blksize(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_blksize; // from generate()
	py_st_blksize = Py_BuildValue("l", python_self->cpp_object->st_blksize);
	return py_st_blksize;
}

static int Haiku_stat_Object_setst_blksize(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_blksize = (blksize_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_atim(Haiku_stat_Object* python_self, void* python_closure) {
	Haiku_timespec_Object* py_st_atim;

	py_st_atim = (Haiku_timespec_Object*)Haiku_timespec_PyType.tp_alloc(&Haiku_timespec_PyType, 0);
	py_st_atim->cpp_object = (timespec*)&python_self->cpp_object->st_atim;
	// cannot delete this object; we do not own it
	py_st_atim->can_delete_cpp_object = false;
	return (PyObject*)py_st_atim;
}

static int Haiku_stat_Object_setst_atim(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->st_atim, (void*)((Haiku_timespec_Object*)value)->cpp_object, sizeof(timespec));
	}
	return 0;
}

static PyObject* Haiku_stat_Object_getst_mtim(Haiku_stat_Object* python_self, void* python_closure) {
	Haiku_timespec_Object* py_st_mtim;

	py_st_mtim = (Haiku_timespec_Object*)Haiku_timespec_PyType.tp_alloc(&Haiku_timespec_PyType, 0);
	py_st_mtim->cpp_object = (timespec*)&python_self->cpp_object->st_mtim;
	// cannot delete this object; we do not own it
	py_st_mtim->can_delete_cpp_object = false;
	return (PyObject*)py_st_mtim;
}

static int Haiku_stat_Object_setst_mtim(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->st_mtim, (void*)((Haiku_timespec_Object*)value)->cpp_object, sizeof(timespec));
	}
	return 0;
}

static PyObject* Haiku_stat_Object_getst_ctim(Haiku_stat_Object* python_self, void* python_closure) {
	Haiku_timespec_Object* py_st_ctim;

	py_st_ctim = (Haiku_timespec_Object*)Haiku_timespec_PyType.tp_alloc(&Haiku_timespec_PyType, 0);
	py_st_ctim->cpp_object = (timespec*)&python_self->cpp_object->st_ctim;
	// cannot delete this object; we do not own it
	py_st_ctim->can_delete_cpp_object = false;
	return (PyObject*)py_st_ctim;
}

static int Haiku_stat_Object_setst_ctim(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->st_ctim, (void*)((Haiku_timespec_Object*)value)->cpp_object, sizeof(timespec));
	}
	return 0;
}

static PyObject* Haiku_stat_Object_getst_crtim(Haiku_stat_Object* python_self, void* python_closure) {
	Haiku_timespec_Object* py_st_crtim;

	py_st_crtim = (Haiku_timespec_Object*)Haiku_timespec_PyType.tp_alloc(&Haiku_timespec_PyType, 0);
	py_st_crtim->cpp_object = (timespec*)&python_self->cpp_object->st_crtim;
	// cannot delete this object; we do not own it
	py_st_crtim->can_delete_cpp_object = false;
	return (PyObject*)py_st_crtim;
}

static int Haiku_stat_Object_setst_crtim(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	if (value != NULL) {
		memcpy((void*)&python_self->cpp_object->st_crtim, (void*)((Haiku_timespec_Object*)value)->cpp_object, sizeof(timespec));
	}
	return 0;
}

static PyObject* Haiku_stat_Object_getst_type(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_type; // from generate()
	py_st_type = Py_BuildValue("k", python_self->cpp_object->st_type);
	return py_st_type;
}

static int Haiku_stat_Object_setst_type(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_type = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_Object_getst_blocks(Haiku_stat_Object* python_self, void* python_closure) {
	PyObject* py_st_blocks; // from generate()
	py_st_blocks = Py_BuildValue("l", python_self->cpp_object->st_blocks);
	return py_st_blocks;
}

static int Haiku_stat_Object_setst_blocks(Haiku_stat_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->st_blocks = (blkcnt_t)PyInt_AsLong(value);
	return 0;
}

static PyObject* Haiku_stat_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_stat_Object*)a)->cpp_object == ((Haiku_stat_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_stat_Object*)a)->cpp_object != ((Haiku_stat_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_stat_PyProperties[] = {
	{ (char*)"st_dev", (getter)Haiku_stat_Object_getst_dev, (setter)Haiku_stat_Object_setst_dev, (char*)"<DOC>", NULL},
	{ (char*)"st_ino", (getter)Haiku_stat_Object_getst_ino, (setter)Haiku_stat_Object_setst_ino, (char*)"<DOC>", NULL},
	{ (char*)"st_mode", (getter)Haiku_stat_Object_getst_mode, (setter)Haiku_stat_Object_setst_mode, (char*)"<DOC>", NULL},
	{ (char*)"st_nlink", (getter)Haiku_stat_Object_getst_nlink, (setter)Haiku_stat_Object_setst_nlink, (char*)"<DOC>", NULL},
	{ (char*)"st_uid", (getter)Haiku_stat_Object_getst_uid, (setter)Haiku_stat_Object_setst_uid, (char*)"<DOC>", NULL},
	{ (char*)"st_gid", (getter)Haiku_stat_Object_getst_gid, (setter)Haiku_stat_Object_setst_gid, (char*)"<DOC>", NULL},
	{ (char*)"st_size", (getter)Haiku_stat_Object_getst_size, (setter)Haiku_stat_Object_setst_size, (char*)"<DOC>", NULL},
	{ (char*)"st_rdev", (getter)Haiku_stat_Object_getst_rdev, (setter)Haiku_stat_Object_setst_rdev, (char*)"<DOC>", NULL},
	{ (char*)"st_blksize", (getter)Haiku_stat_Object_getst_blksize, (setter)Haiku_stat_Object_setst_blksize, (char*)"<DOC>", NULL},
	{ (char*)"st_atim", (getter)Haiku_stat_Object_getst_atim, (setter)Haiku_stat_Object_setst_atim, (char*)"<DOC>", NULL},
	{ (char*)"st_mtim", (getter)Haiku_stat_Object_getst_mtim, (setter)Haiku_stat_Object_setst_mtim, (char*)"<DOC>", NULL},
	{ (char*)"st_ctim", (getter)Haiku_stat_Object_getst_ctim, (setter)Haiku_stat_Object_setst_ctim, (char*)"<DOC>", NULL},
	{ (char*)"st_crtim", (getter)Haiku_stat_Object_getst_crtim, (setter)Haiku_stat_Object_setst_crtim, (char*)"<DOC>", NULL},
	{ (char*)"st_type", (getter)Haiku_stat_Object_getst_type, (setter)Haiku_stat_Object_setst_type, (char*)"<DOC>", NULL},
	{ (char*)"st_blocks", (getter)Haiku_stat_Object_getst_blocks, (setter)Haiku_stat_Object_setst_blocks, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_stat_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.stat";
	type->tp_basicsize   = sizeof(Haiku_stat_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_stat_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_stat_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

