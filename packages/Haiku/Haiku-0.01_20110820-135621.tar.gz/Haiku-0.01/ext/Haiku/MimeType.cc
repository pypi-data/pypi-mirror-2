/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_MimeTypeConstants_PyMethods[] = {
	{NULL} /* Sentinel */
};
//static PyObject* Haiku_MimeType_newEmpty(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_newEmpty(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_MimeType_Object* python_self;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_MimeType_Object*)python_type->tp_alloc(python_type, 0);
	
	python_self->cpp_object = new BMimeType();
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

/*
 * The main constructor is implemented in terms of __init__(). This allows
 * __new__() to return an empty object, so when we pass to Python an object
 * from the system (rather than one we created ourselves), we can use
 * __new__() and assign the already existing C++ object to the Python object.
 *
 * This does somewhat expose us to the danger of Python code calling
 * __init__() a second time, so we need to check for that.
 */
//static int Haiku_MimeType_init(Haiku_MimeType_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_MimeType_init(Haiku_MimeType_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* mimeType;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s", &mimeType);
	
	python_self->cpp_object = new BMimeType(mimeType);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_MimeType_DESTROY(Haiku_MimeType_Object* python_self);
static void Haiku_MimeType_DESTROY(Haiku_MimeType_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_MimeType_SetTo(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetTo(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	const char* mimeType;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &mimeType);
	
	retval = python_self->cpp_object->SetTo(mimeType);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_Unset(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_Unset(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Unset();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_InitCheck(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_InitCheck(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	status_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->InitCheck();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_MimeType_Type(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_Type(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	const char* retval;
	
	retval = python_self->cpp_object->Type();
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("s", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_IsValid(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_IsValid(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsValid();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MimeType_IsSupertypeOnly(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_IsSupertypeOnly(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSupertypeOnly();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MimeType_GetSupertype(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetSupertype(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMimeType* superType;
	status_t retval;
	Haiku_MimeType_Object* py_superType; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetSupertype(superType);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_superType = (Haiku_MimeType_Object*)Haiku_MimeType_PyType.tp_alloc(&Haiku_MimeType_PyType, 0);
	py_superType->cpp_object = (BMimeType*)superType;
	// we own this object, so we can delete it
	py_superType->can_delete_cpp_object = true;
	return (PyObject*)py_superType;
}

//static PyObject* Haiku_MimeType_Install(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_Install(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	status_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Install();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_MimeType_Delete(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_Delete(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	status_t retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Delete();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_MimeType_IsInstalled(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_IsInstalled(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsInstalled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MimeType_GetIconData(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetIconData(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	uint8** data;
	size_t size;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	retval = python_self->cpp_object->GetIcon(data, &size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, size);
	return py_data;
}

//static PyObject* Haiku_MimeType_GetPreferredApp(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetPreferredApp(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* signature;
	app_verb verb = B_OPEN;
	status_t retval;
	PyObject* py_signature; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|i", &verb);
	
	retval = python_self->cpp_object->GetPreferredApp(signature, verb);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_signature = Py_BuildValue("s", signature);
	return py_signature;
}

//static PyObject* Haiku_MimeType_GetAttrInfo(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetAttrInfo(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMessage* info;
	status_t retval;
	Haiku_Message_Object* py_info; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetAttrInfo(info);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_info = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_info->cpp_object = (BMessage*)info;
	// we own this object, so we can delete it
	py_info->can_delete_cpp_object = true;
	return (PyObject*)py_info;
}

//static PyObject* Haiku_MimeType_GetFileExtensions(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetFileExtensions(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMessage* extensions;
	status_t retval;
	Haiku_Message_Object* py_extensions; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetFileExtensions(extensions);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_extensions = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_extensions->cpp_object = (BMessage*)extensions;
	// we own this object, so we can delete it
	py_extensions->can_delete_cpp_object = true;
	return (PyObject*)py_extensions;
}

//static PyObject* Haiku_MimeType_GetShortDescription(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetShortDescription(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* description;
	status_t retval;
	PyObject* py_description; // from generate_py()
	
	retval = python_self->cpp_object->GetShortDescription(description);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_description = Py_BuildValue("s", description);
	return py_description;
}

//static PyObject* Haiku_MimeType_GetLongDescription(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetLongDescription(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* description;
	status_t retval;
	PyObject* py_description; // from generate_py()
	
	retval = python_self->cpp_object->GetLongDescription(description);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_description = Py_BuildValue("s", description);
	return py_description;
}

//static PyObject* Haiku_MimeType_GetSupportingApps(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetSupportingApps(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMessage* signatures;
	status_t retval;
	Haiku_Message_Object* py_signatures; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->GetSupportingApps(signatures);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_signatures = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_signatures->cpp_object = (BMessage*)signatures;
	// we own this object, so we can delete it
	py_signatures->can_delete_cpp_object = true;
	return (PyObject*)py_signatures;
}

//static PyObject* Haiku_MimeType_SetIconFromData(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetIconFromData(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	uint8* data;
	PyObject* py_data; // from generate_py ()
	size_t size;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	PyString_AsStringAndSize(py_data, (char**)&data, (Py_ssize_t*)&size);
	
	retval = python_self->cpp_object->SetIcon(data, size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_SetPreferredApp(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetPreferredApp(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* signature;
	app_verb verb = B_OPEN;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s|i", &signature, &verb);
	
	retval = python_self->cpp_object->SetPreferredApp(signature, verb);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_SetAttrInfo(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetAttrInfo(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMessage* info;
	Haiku_Message_Object* py_info; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_info);
	if (py_info != NULL) {
		info = ((Haiku_Message_Object*)py_info)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetAttrInfo(info);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_SetFileExtensions(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetFileExtensions(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	BMessage* extensions;
	Haiku_Message_Object* py_extensions; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_extensions);
	if (py_extensions != NULL) {
		extensions = ((Haiku_Message_Object*)py_extensions)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetFileExtensions(extensions);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_SetShortDescription(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetShortDescription(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* description;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "s", &description);
	
	retval = python_self->cpp_object->SetShortDescription(description);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_SetLongDescription(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetLongDescription(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	char* description;
	status_t retval;
	PyObject* py_description; // from generate_py()
	
	retval = python_self->cpp_object->SetLongDescription(description);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_description = Py_BuildValue("s", description);
	return py_description;
}

//static PyObject* Haiku_MimeType_SetAppHint(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetAppHint(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	entry_ref* ref;
	status_t retval;
	Haiku_entry_ref_Object* py_ref; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->SetAppHint(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_ref = (Haiku_entry_ref_Object*)Haiku_entry_ref_PyType.tp_alloc(&Haiku_entry_ref_PyType, 0);
	py_ref->cpp_object = (entry_ref*)ref;
	// we own this object, so we can delete it
	py_ref->can_delete_cpp_object = true;
	return (PyObject*)py_ref;
}

//static PyObject* Haiku_MimeType_GetAppHint(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetAppHint(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	entry_ref* ref;
	Haiku_entry_ref_Object* py_ref; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_ref);
	if (py_ref != NULL) {
		ref = ((Haiku_entry_ref_Object*)py_ref)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetAppHint(ref);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_GetIconDataForType(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_GetIconDataForType(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	const char* type;
	uint8** data;
	size_t size;
	status_t retval;
	PyObject* py_data; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &type);
	
	retval = python_self->cpp_object->GetIconForType(type, data, &size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = Py_BuildValue("s#", data, size);
	return py_data;
}

//static PyObject* Haiku_MimeType_SetIconFromDataForType(Haiku_MimeType_Object* python_self, PyObject* python_args);
static PyObject* Haiku_MimeType_SetIconFromDataForType(Haiku_MimeType_Object* python_self, PyObject* python_args) {
	const char* type;
	uint8* data;
	PyObject* py_data; // from generate_py ()
	char* buffer;
	size_t size;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "sO", &type, &py_data);
	buffer = (char*)malloc(0xffff);	// should be big enough for most purposes
	PyString_AsStringAndSize(py_data, &buffer, (Py_ssize_t*)&size);
	memcpy((void*)&data, (void*)buffer, size);
	free(buffer);
	
	retval = python_self->cpp_object->SetIconForType(type, data, size);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_GetInstalledSupertypes(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GetInstalledSupertypes(PyObject* python_type, PyObject* python_args) {
	BMessage* supertypes;
	status_t retval;
	Haiku_Message_Object* py_supertypes; // from generate_py() (for outputs)
	
	retval = BMimeType::GetInstalledSupertypes(supertypes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_supertypes = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_supertypes->cpp_object = (BMessage*)supertypes;
	// we own this object, so we can delete it
	py_supertypes->can_delete_cpp_object = true;
	return (PyObject*)py_supertypes;
}

//static PyObject* Haiku_MimeType_GetInstalledTypes(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GetInstalledTypes(PyObject* python_type, PyObject* python_args) {
	BMessage* types;
	status_t retval;
	Haiku_Message_Object* py_types; // from generate_py() (for outputs)
	
	retval = BMimeType::GetInstalledTypes(types);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_types = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_types->cpp_object = (BMessage*)types;
	// we own this object, so we can delete it
	py_types->can_delete_cpp_object = true;
	return (PyObject*)py_types;
}

//static PyObject* Haiku_MimeType_GetInstalledTypeForSupertype(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GetInstalledTypeForSupertype(PyObject* python_type, PyObject* python_args) {
	const char* supertype;
	BMessage* subtypes;
	status_t retval;
	Haiku_Message_Object* py_subtypes; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &supertype);
	
	retval = BMimeType::GetInstalledTypes(supertype, subtypes);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_subtypes = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_subtypes->cpp_object = (BMessage*)subtypes;
	// we own this object, so we can delete it
	py_subtypes->can_delete_cpp_object = true;
	return (PyObject*)py_subtypes;
}

//static PyObject* Haiku_MimeType_GetWildcardApps(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GetWildcardApps(PyObject* python_type, PyObject* python_args) {
	BMessage* wildcardApps;
	status_t retval;
	Haiku_Message_Object* py_wildcardApps; // from generate_py() (for outputs)
	
	retval = BMimeType::GetWildcardApps(wildcardApps);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_wildcardApps = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_wildcardApps->cpp_object = (BMessage*)wildcardApps;
	// we own this object, so we can delete it
	py_wildcardApps->can_delete_cpp_object = true;
	return (PyObject*)py_wildcardApps;
}

//static PyObject* Haiku_MimeType_IsMimeTypeValid(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_IsMimeTypeValid(PyObject* python_type, PyObject* python_args) {
	const char* mimeType;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &mimeType);
	
	retval = BMimeType::IsValid(mimeType);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_MimeType_GuessMimeTypeForEntryRef(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GuessMimeTypeForEntryRef(PyObject* python_type, PyObject* python_args) {
	const entry_ref* file;
	Haiku_entry_ref_Object* py_file; // from generate_py()
	BMimeType* type;
	status_t retval;
	Haiku_MimeType_Object* py_type; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_file);
	if (py_file != NULL) {
		file = ((Haiku_entry_ref_Object*)py_file)->cpp_object;
	}
	
	retval = BMimeType::GuessMimeType(file, type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_type = (Haiku_MimeType_Object*)Haiku_MimeType_PyType.tp_alloc(&Haiku_MimeType_PyType, 0);
	py_type->cpp_object = (BMimeType*)type;
	// we own this object, so we can delete it
	py_type->can_delete_cpp_object = true;
	return (PyObject*)py_type;
}

//static PyObject* Haiku_MimeType_GuessMimeTypeForString(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GuessMimeTypeForString(PyObject* python_type, PyObject* python_args) {
	void* buffer;
	PyObject* py_buffer; // from generate_py ()
	int32 length;
	BMimeType* type;
	status_t retval;
	Haiku_MimeType_Object* py_type; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_buffer);
	PyString_AsStringAndSize(py_buffer, (char**)&buffer, (Py_ssize_t*)&length);
	
	retval = BMimeType::GuessMimeType(buffer, length, type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_type = (Haiku_MimeType_Object*)Haiku_MimeType_PyType.tp_alloc(&Haiku_MimeType_PyType, 0);
	py_type->cpp_object = (BMimeType*)type;
	// we own this object, so we can delete it
	py_type->can_delete_cpp_object = true;
	return (PyObject*)py_type;
}

//static PyObject* Haiku_MimeType_GuessMimeType(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_GuessMimeType(PyObject* python_type, PyObject* python_args) {
	const char* filename;
	BMimeType* type;
	status_t retval;
	Haiku_MimeType_Object* py_type; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &filename);
	
	retval = BMimeType::GuessMimeType(filename, type);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_type = (Haiku_MimeType_Object*)Haiku_MimeType_PyType.tp_alloc(&Haiku_MimeType_PyType, 0);
	py_type->cpp_object = (BMimeType*)type;
	// we own this object, so we can delete it
	py_type->can_delete_cpp_object = true;
	return (PyObject*)py_type;
}

//static PyObject* Haiku_MimeType_StartWatching(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_StartWatching(PyObject* python_type, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = BMimeType::StartWatching(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_MimeType_StopWatching(PyObject* python_type, PyObject* python_args);
static PyObject* Haiku_MimeType_StopWatching(PyObject* python_type, PyObject* python_args) {
	BMessenger target;
	Haiku_Messenger_Object* py_target; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_target);
	if (py_target != NULL) {
		memcpy((void*)&target, (void*)((Haiku_Messenger_Object*)py_target)->cpp_object, sizeof(BMessenger));
	}
	
	retval = BMimeType::StopWatching(target);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

static PyObject* Haiku_MimeType_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_MimeType_Object*)a)->cpp_object == ((Haiku_MimeType_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_MimeType_Object*)a)->cpp_object != ((Haiku_MimeType_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_MimeType_PyMethods[] = {
	{"Empty", (PyCFunction)Haiku_MimeType_newEmpty, METH_VARARGS|METH_CLASS, ""},
	{"SetTo", (PyCFunction)Haiku_MimeType_SetTo, METH_VARARGS, ""},
	{"Unset", (PyCFunction)Haiku_MimeType_Unset, METH_VARARGS, ""},
	{"InitCheck", (PyCFunction)Haiku_MimeType_InitCheck, METH_VARARGS, ""},
	{"Type", (PyCFunction)Haiku_MimeType_Type, METH_VARARGS, ""},
	{"IsValid", (PyCFunction)Haiku_MimeType_IsValid, METH_VARARGS, ""},
	{"IsSupertypeOnly", (PyCFunction)Haiku_MimeType_IsSupertypeOnly, METH_VARARGS, ""},
	{"GetSupertype", (PyCFunction)Haiku_MimeType_GetSupertype, METH_VARARGS, ""},
	{"Install", (PyCFunction)Haiku_MimeType_Install, METH_VARARGS, ""},
	{"Delete", (PyCFunction)Haiku_MimeType_Delete, METH_VARARGS, ""},
	{"IsInstalled", (PyCFunction)Haiku_MimeType_IsInstalled, METH_VARARGS, ""},
	{"GetIconData", (PyCFunction)Haiku_MimeType_GetIconData, METH_VARARGS, ""},
	{"GetPreferredApp", (PyCFunction)Haiku_MimeType_GetPreferredApp, METH_VARARGS, ""},
	{"GetAttrInfo", (PyCFunction)Haiku_MimeType_GetAttrInfo, METH_VARARGS, ""},
	{"GetFileExtensions", (PyCFunction)Haiku_MimeType_GetFileExtensions, METH_VARARGS, ""},
	{"GetShortDescription", (PyCFunction)Haiku_MimeType_GetShortDescription, METH_VARARGS, ""},
	{"GetLongDescription", (PyCFunction)Haiku_MimeType_GetLongDescription, METH_VARARGS, ""},
	{"GetSupportingApps", (PyCFunction)Haiku_MimeType_GetSupportingApps, METH_VARARGS, ""},
	{"SetIconFromData", (PyCFunction)Haiku_MimeType_SetIconFromData, METH_VARARGS, ""},
	{"SetPreferredApp", (PyCFunction)Haiku_MimeType_SetPreferredApp, METH_VARARGS, ""},
	{"SetAttrInfo", (PyCFunction)Haiku_MimeType_SetAttrInfo, METH_VARARGS, ""},
	{"SetFileExtensions", (PyCFunction)Haiku_MimeType_SetFileExtensions, METH_VARARGS, ""},
	{"SetShortDescription", (PyCFunction)Haiku_MimeType_SetShortDescription, METH_VARARGS, ""},
	{"SetLongDescription", (PyCFunction)Haiku_MimeType_SetLongDescription, METH_VARARGS, ""},
	{"SetAppHint", (PyCFunction)Haiku_MimeType_SetAppHint, METH_VARARGS, ""},
	{"GetAppHint", (PyCFunction)Haiku_MimeType_GetAppHint, METH_VARARGS, ""},
	{"GetIconDataForType", (PyCFunction)Haiku_MimeType_GetIconDataForType, METH_VARARGS, ""},
	{"SetIconFromDataForType", (PyCFunction)Haiku_MimeType_SetIconFromDataForType, METH_VARARGS, ""},
	{"GetInstalledSupertypes", (PyCFunction)Haiku_MimeType_GetInstalledSupertypes, METH_VARARGS|METH_CLASS, ""},
	{"GetInstalledTypes", (PyCFunction)Haiku_MimeType_GetInstalledTypes, METH_VARARGS|METH_CLASS, ""},
	{"GetInstalledTypeForSupertype", (PyCFunction)Haiku_MimeType_GetInstalledTypeForSupertype, METH_VARARGS|METH_CLASS, ""},
	{"GetWildcardApps", (PyCFunction)Haiku_MimeType_GetWildcardApps, METH_VARARGS|METH_CLASS, ""},
	{"IsMimeTypeValid", (PyCFunction)Haiku_MimeType_IsMimeTypeValid, METH_VARARGS|METH_CLASS, ""},
	{"GuessMimeTypeForEntryRef", (PyCFunction)Haiku_MimeType_GuessMimeTypeForEntryRef, METH_VARARGS|METH_CLASS, ""},
	{"GuessMimeTypeForString", (PyCFunction)Haiku_MimeType_GuessMimeTypeForString, METH_VARARGS|METH_CLASS, ""},
	{"GuessMimeType", (PyCFunction)Haiku_MimeType_GuessMimeType, METH_VARARGS|METH_CLASS, ""},
	{"StartWatching", (PyCFunction)Haiku_MimeType_StartWatching, METH_VARARGS|METH_CLASS, ""},
	{"StopWatching", (PyCFunction)Haiku_MimeType_StopWatching, METH_VARARGS|METH_CLASS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_MimeType_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.MimeType";
	type->tp_basicsize   = sizeof(Haiku_MimeType_Object);
	type->tp_dealloc     = (destructor)Haiku_MimeType_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_MimeType_RichCompare;
	type->tp_methods     = Haiku_MimeType_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_MimeType_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

