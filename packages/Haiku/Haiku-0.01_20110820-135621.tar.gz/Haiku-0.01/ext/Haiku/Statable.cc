/*
 * Automatically generated file
 */

//static PyObject* Haiku_Statable_IsFile(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_IsFile(Haiku_Statable_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFile();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Statable_IsDirectory(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_IsDirectory(Haiku_Statable_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsDirectory();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Statable_IsSymLink(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_IsSymLink(Haiku_Statable_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSymLink();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Statable_GetNodeRef(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetNodeRef(Haiku_Statable_Object* python_self, PyObject* python_args) {
	node_ref* ref;
	status_t retval;
	Haiku_node_ref_Object* py_ref; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetNodeRef(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_node_ref_Object*)Haiku_node_ref_PyType.tp_alloc(&Haiku_node_ref_PyType, 0);
	py_ref->cpp_object = (node_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_Statable_GetOwner(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetOwner(Haiku_Statable_Object* python_self, PyObject* python_args) {
	uid_t owner;
	status_t retval;
	PyObject* py_owner; // from generate_py()
	
	retval = python_self->cpp_object->GetOwner(&owner);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_owner = Py_BuildValue("l", owner);
	return py_owner;
}

//static PyObject* Haiku_Statable_SetOwner(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetOwner(Haiku_Statable_Object* python_self, PyObject* python_args) {
	uid_t owner;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &owner);
	
	retval = python_self->cpp_object->SetOwner(owner);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetGroup(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetGroup(Haiku_Statable_Object* python_self, PyObject* python_args) {
	gid_t group;
	status_t retval;
	PyObject* py_group; // from generate_py()
	
	retval = python_self->cpp_object->GetGroup(&group);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_group = Py_BuildValue("l", group);
	return py_group;
}

//static PyObject* Haiku_Statable_SetGroup(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetGroup(Haiku_Statable_Object* python_self, PyObject* python_args) {
	gid_t group;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &group);
	
	retval = python_self->cpp_object->SetGroup(group);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetPermissions(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetPermissions(Haiku_Statable_Object* python_self, PyObject* python_args) {
	mode_t perms;
	status_t retval;
	PyObject* py_perms; // from generate_py()
	
	retval = python_self->cpp_object->GetPermissions(&perms);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_perms = Py_BuildValue("l", perms);
	return py_perms;
}

//static PyObject* Haiku_Statable_SetPermissions(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetPermissions(Haiku_Statable_Object* python_self, PyObject* python_args) {
	mode_t perms;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &perms);
	
	retval = python_self->cpp_object->SetPermissions(perms);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetSize(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetSize(Haiku_Statable_Object* python_self, PyObject* python_args) {
	off_t size;
	status_t retval;
	PyObject* py_size; // from generate_py()
	
	retval = python_self->cpp_object->GetSize(&size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_size = Py_BuildValue("l", size);
	return py_size;
}

//static PyObject* Haiku_Statable_GetModificationTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetModificationTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t mtime;
	status_t retval;
	PyObject* py_mtime; // from generate_py()
	
	retval = python_self->cpp_object->GetModificationTime(&mtime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_mtime = Py_BuildValue("l", mtime);
	return py_mtime;
}

//static PyObject* Haiku_Statable_SetModificationTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetModificationTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t mtime;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &mtime);
	
	retval = python_self->cpp_object->SetModificationTime(mtime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetCreationTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetCreationTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t ctime;
	status_t retval;
	PyObject* py_ctime; // from generate_py()
	
	retval = python_self->cpp_object->GetCreationTime(&ctime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ctime = Py_BuildValue("l", ctime);
	return py_ctime;
}

//static PyObject* Haiku_Statable_SetCreationTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetCreationTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t ctime;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &ctime);
	
	retval = python_self->cpp_object->SetCreationTime(ctime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetAccessTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetAccessTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t atime;
	status_t retval;
	PyObject* py_atime; // from generate_py()
	
	retval = python_self->cpp_object->GetAccessTime(&atime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_atime = Py_BuildValue("l", atime);
	return py_atime;
}

//static PyObject* Haiku_Statable_SetAccessTime(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_SetAccessTime(Haiku_Statable_Object* python_self, PyObject* python_args) {
	time_t atime;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "l", &atime);
	
	retval = python_self->cpp_object->SetAccessTime(atime);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Statable_GetVolume(Haiku_Statable_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Statable_GetVolume(Haiku_Statable_Object* python_self, PyObject* python_args) {
	BVolume* vol;
	status_t retval;
	Haiku_Volume_Object* py_vol; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetVolume(vol);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_vol = (Haiku_Volume_Object*)Haiku_Volume_PyType.tp_alloc(&Haiku_Volume_PyType, 0);
	py_vol->cpp_object = (BVolume*)vol;
	// we own this object, so we can delete it
	py_vol->can_delete_cpp_object = true;
	return (PyObject*)py_vol;
}

static PyObject* Haiku_Statable_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Statable_Object*)a)->cpp_object == ((Haiku_Statable_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Statable_Object*)a)->cpp_object != ((Haiku_Statable_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Statable_PyMethods[] = {
	{"IsFile", (PyCFunction)Haiku_Statable_IsFile, METH_VARARGS, ""},
	{"IsDirectory", (PyCFunction)Haiku_Statable_IsDirectory, METH_VARARGS, ""},
	{"IsSymLink", (PyCFunction)Haiku_Statable_IsSymLink, METH_VARARGS, ""},
	{"GetNodeRef", (PyCFunction)Haiku_Statable_GetNodeRef, METH_VARARGS, ""},
	{"GetOwner", (PyCFunction)Haiku_Statable_GetOwner, METH_VARARGS, ""},
	{"SetOwner", (PyCFunction)Haiku_Statable_SetOwner, METH_VARARGS, ""},
	{"GetGroup", (PyCFunction)Haiku_Statable_GetGroup, METH_VARARGS, ""},
	{"SetGroup", (PyCFunction)Haiku_Statable_SetGroup, METH_VARARGS, ""},
	{"GetPermissions", (PyCFunction)Haiku_Statable_GetPermissions, METH_VARARGS, ""},
	{"SetPermissions", (PyCFunction)Haiku_Statable_SetPermissions, METH_VARARGS, ""},
	{"GetSize", (PyCFunction)Haiku_Statable_GetSize, METH_VARARGS, ""},
	{"GetModificationTime", (PyCFunction)Haiku_Statable_GetModificationTime, METH_VARARGS, ""},
	{"SetModificationTime", (PyCFunction)Haiku_Statable_SetModificationTime, METH_VARARGS, ""},
	{"GetCreationTime", (PyCFunction)Haiku_Statable_GetCreationTime, METH_VARARGS, ""},
	{"SetCreationTime", (PyCFunction)Haiku_Statable_SetCreationTime, METH_VARARGS, ""},
	{"GetAccessTime", (PyCFunction)Haiku_Statable_GetAccessTime, METH_VARARGS, ""},
	{"SetAccessTime", (PyCFunction)Haiku_Statable_SetAccessTime, METH_VARARGS, ""},
	{"GetVolume", (PyCFunction)Haiku_Statable_GetVolume, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Statable_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Statable";
	type->tp_basicsize   = sizeof(Haiku_Statable_Object);
	type->tp_dealloc     = (destructor)0;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Statable_RichCompare;
	type->tp_methods     = Haiku_Statable_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)0;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

