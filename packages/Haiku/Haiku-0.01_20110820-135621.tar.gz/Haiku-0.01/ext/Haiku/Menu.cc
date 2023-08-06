/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_MenuConstants_PyMethods[] = {
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
//static int Haiku_Menu_init(Haiku_Menu_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Menu_init(Haiku_Menu_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	const char* name;
	menu_layout layout = B_ITEMS_IN_COLUMN;
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	PyArg_ParseTuple(python_args, "s|i", &name, &layout);
	
	python_self->cpp_object = new BMenu(name, layout);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Menu_newMatrixMenu(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Menu_newMatrixMenu(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Menu_Object* python_self;
	const char* name;
	float width;
	float height;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Menu_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sff", &name, &width, &height);
	
	python_self->cpp_object = new BMenu(name, width, height);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_Menu_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Menu_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Menu_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Menu_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BMenu(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Menu_DESTROY(Haiku_Menu_Object* python_self);
static void Haiku_Menu_DESTROY(Haiku_Menu_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Menu_Instantiate(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_Instantiate(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	BArchivable* retval;
	Haiku_Archivable_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->Instantiate(data);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Archivable_Object*)Haiku_Archivable_PyType.tp_alloc(&Haiku_Archivable_PyType, 0);
	py_retval->cpp_object = (BArchivable*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_Archive(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_Archive(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMessage* data;
	bool deep = true;
	PyObject* py_deep; // from generate_py ()
	status_t retval;
	Haiku_Message_Object* py_data; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "|O", &py_deep);
	deep = (bool)(PyObject_IsTrue(py_deep));
	
	retval = python_self->cpp_object->Archive(data, deep);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	py_data = (Haiku_Message_Object*)Haiku_Message_PyType.tp_alloc(&Haiku_Message_PyType, 0);
	py_data->cpp_object = (BMessage*)data;
	// we own this object, so we can delete it
	py_data->can_delete_cpp_object = true;
	return (PyObject*)py_data;
}

//static PyObject* Haiku_Menu_GetPreferredSize(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_GetPreferredSize(Haiku_Menu_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_Menu_ResizeToPreferred(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_ResizeToPreferred(Haiku_Menu_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_DoLayout(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_DoLayout(Haiku_Menu_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->DoLayout();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_InvalidateLayout(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_InvalidateLayout(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_MakeFocus(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_MakeFocus(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_AddItem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddItem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
		((Haiku_MenuItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	retval = python_self->cpp_object->AddItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AddItemAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddItemAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	int32 index;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Ol", &py_item, &index);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
		((Haiku_MenuItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	retval = python_self->cpp_object->AddItem(item, index);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_ToMatrix(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_ToMatrix(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_item, &py_frame);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
		((Haiku_MenuItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->AddItem(item, frame);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AddSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
		((Haiku_MenuItem_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	retval = python_self->cpp_object->AddItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AddSubmenuAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddSubmenuAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu* item;
	Haiku_Menu_Object* py_item; // from generate_py()
	int32 index;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "Ol", &py_item, &index);
	if (py_item != NULL) {
		item = ((Haiku_Menu_Object*)py_item)->cpp_object;
		((Haiku_Menu_Object*)py_item)->can_delete_cpp_object = false;
	}
	
	retval = python_self->cpp_object->AddItem(item, index);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AddSubmenuToMatrix(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddSubmenuToMatrix(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu* item;
	Haiku_Menu_Object* py_item; // from generate_py()
	BRect frame;
	Haiku_Rect_Object* py_frame; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OO", &py_item, &py_frame);
	if (py_item != NULL) {
		item = ((Haiku_Menu_Object*)py_item)->cpp_object;
		((Haiku_Menu_Object*)py_item)->can_delete_cpp_object = false;
	}
	if (py_frame != NULL) {
		memcpy((void*)&frame, (void*)((Haiku_Rect_Object*)py_frame)->cpp_object, sizeof(BRect));
	}
	
	retval = python_self->cpp_object->AddItem(item, frame);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AddSeparatorItem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddSeparatorItem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->AddSeparatorItem();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_RemoveItem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_RemoveItem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->RemoveItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_RemoveSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_RemoveSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu* item;
	Haiku_Menu_Object* py_item; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_Menu_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->RemoveItem(item);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_RemoveItemAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_RemoveItemAtIndex(Haiku_Menu_Object* python_self, PyObject* python_args) {
	int32 index;
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->RemoveItem(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_RemoveItems(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_RemoveItems(Haiku_Menu_Object* python_self, PyObject* python_args) {
	int32 index;
	int32 count;
	bool deleteItems = false;
	PyObject* py_deleteItems; // from generate_py ()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll|O", &index, &count, &py_deleteItems);
	deleteItems = (bool)(PyObject_IsTrue(py_deleteItems));
	
	retval = python_self->cpp_object->RemoveItems(index, count, deleteItems);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_ItemAt(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_ItemAt(Haiku_Menu_Object* python_self, PyObject* python_args) {
	int32 index;
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->ItemAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_SubmenuAt(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SubmenuAt(Haiku_Menu_Object* python_self, PyObject* python_args) {
	int32 index;
	BMenu* retval;
	Haiku_Menu_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	retval = python_self->cpp_object->SubmenuAt(index);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Menu_Object*)Haiku_Menu_PyType.tp_alloc(&Haiku_Menu_PyType, 0);
	py_retval->cpp_object = (BMenu*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_CountItems(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_CountItems(Haiku_Menu_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountItems();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Menu_IndexOf(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IndexOf(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* item;
	Haiku_MenuItem_Object* py_item; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_MenuItem_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->IndexOf(item);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Menu_IndexOfSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IndexOfSubmenu(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu* item;
	Haiku_Menu_Object* py_item; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_item);
	if (py_item != NULL) {
		item = ((Haiku_Menu_Object*)py_item)->cpp_object;
	}
	
	retval = python_self->cpp_object->IndexOf(item);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Menu_FindItem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_FindItem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	const char* label;
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "s", &label);
	
	retval = python_self->cpp_object->FindItem(label);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_FindItemByCommand(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_FindItemByCommand(Haiku_Menu_Object* python_self, PyObject* python_args) {
	uint32 command;
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "k", &command);
	
	retval = python_self->cpp_object->FindItem(command);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// cannot delete this object; we do not own it
	py_retval->can_delete_cpp_object = false;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_SetTargetForItems(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetTargetForItems(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BHandler* handler;
	Haiku_Handler_Object* py_handler; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_handler);
	if (py_handler != NULL) {
		handler = ((Haiku_Handler_Object*)py_handler)->cpp_object;
	}
	
	retval = python_self->cpp_object->SetTargetForItems(handler);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetMessengerTargetForItems(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetMessengerTargetForItems(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMessenger messenger;
	Haiku_Messenger_Object* py_messenger; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_messenger);
	if (py_messenger != NULL) {
		memcpy((void*)&messenger, (void*)((Haiku_Messenger_Object*)py_messenger)->cpp_object, sizeof(BMessenger));
	}
	
	retval = python_self->cpp_object->SetTargetForItems(messenger);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetEnabled(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetEnabled(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->SetEnabled(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetRadioMode(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetRadioMode(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool flag;
	PyObject* py_flag; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_flag);
	flag = (bool)(PyObject_IsTrue(py_flag));
	
	python_self->cpp_object->SetRadioMode(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetTriggersEnabled(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetTriggersEnabled(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool flag;
	PyObject* py_flag; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_flag);
	flag = (bool)(PyObject_IsTrue(py_flag));
	
	python_self->cpp_object->SetTriggersEnabled(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetMaxContentWidth(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetMaxContentWidth(Haiku_Menu_Object* python_self, PyObject* python_args) {
	float width;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->SetMaxContentWidth(width);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_SetLabelFromMarked(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_SetLabelFromMarked(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetLabelFromMarked(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_IsLabelFromMarked(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IsLabelFromMarked(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsLabelFromMarked();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_IsEnabled(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IsEnabled(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_IsRadioMode(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IsRadioMode(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsRadioMode();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_AreTriggersEnabled(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AreTriggersEnabled(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->AreTriggersEnabled();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_IsRedrawAfterSticky(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_IsRedrawAfterSticky(Haiku_Menu_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsRedrawAfterSticky();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_MaxContentWidth(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_MaxContentWidth(Haiku_Menu_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MaxContentWidth();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Menu_FindMarked(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_FindMarked(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->FindMarked();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_Supermenu(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_Supermenu(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu* retval;
	Haiku_Menu_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Supermenu();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Menu_Object*)Haiku_Menu_PyType.tp_alloc(&Haiku_Menu_PyType, 0);
	py_retval->cpp_object = (BMenu*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_Superitem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_Superitem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenuItem* retval;
	Haiku_MenuItem_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Superitem();
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_MenuItem_Object*)Haiku_MenuItem_PyType.tp_alloc(&Haiku_MenuItem_PyType, 0);
	py_retval->cpp_object = (BMenuItem*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_ResolveSpecifier(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_ResolveSpecifier(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	int32 index;
	BMessage* specifier;
	Haiku_Message_Object* py_specifier; // from generate_py()
	int32 form;
	const char* property;
	BHandler* retval;
	Haiku_Handler_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "OlOls", &py_message, &index, &py_specifier, &form, &property);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	if (py_specifier != NULL) {
		specifier = ((Haiku_Message_Object*)py_specifier)->cpp_object;
	}
	
	retval = python_self->cpp_object->ResolveSpecifier(message, index, specifier, form, property);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_Handler_Object*)Haiku_Handler_PyType.tp_alloc(&Haiku_Handler_PyType, 0);
	py_retval->cpp_object = (BHandler*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Menu_GetSupportedSuites(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_GetSupportedSuites(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMessage* data;
	Haiku_Message_Object* py_data; // from generate_py()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	if (py_data != NULL) {
		data = ((Haiku_Message_Object*)py_data)->cpp_object;
	}
	
	retval = python_self->cpp_object->GetSupportedSuites(data);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Menu_AddDynamicItem(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_AddDynamicItem(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BMenu::add_state state;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "i", &state);
	
	retval = python_self->cpp_object->AddDynamicItem(state);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Menu_DrawBackground(Haiku_Menu_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Menu_DrawBackground(Haiku_Menu_Object* python_self, PyObject* python_args) {
	BRect update;
	Haiku_Rect_Object* py_update; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_update);
	if (py_update != NULL) {
		memcpy((void*)&update, (void*)((Haiku_Rect_Object*)py_update)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->DrawBackground(update);
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Menu_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_Menu_Object*)a)->cpp_object == ((Haiku_Menu_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_Menu_Object*)a)->cpp_object != ((Haiku_Menu_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Menu_PyMethods[] = {
	{"MatrixMenu", (PyCFunction)Haiku_Menu_newMatrixMenu, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_Menu_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_Menu_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_Menu_Archive, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_Menu_GetPreferredSize, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_Menu_ResizeToPreferred, METH_VARARGS, ""},
	{"DoLayout", (PyCFunction)Haiku_Menu_DoLayout, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_Menu_InvalidateLayout, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_Menu_MakeFocus, METH_VARARGS, ""},
	{"AddItem", (PyCFunction)Haiku_Menu_AddItem, METH_VARARGS, ""},
	{"AddItemAtIndex", (PyCFunction)Haiku_Menu_AddItemAtIndex, METH_VARARGS, ""},
	{"ToMatrix", (PyCFunction)Haiku_Menu_ToMatrix, METH_VARARGS, ""},
	{"AddSubmenu", (PyCFunction)Haiku_Menu_AddSubmenu, METH_VARARGS, ""},
	{"AddSubmenuAtIndex", (PyCFunction)Haiku_Menu_AddSubmenuAtIndex, METH_VARARGS, ""},
	{"AddSubmenuToMatrix", (PyCFunction)Haiku_Menu_AddSubmenuToMatrix, METH_VARARGS, ""},
	{"AddSeparatorItem", (PyCFunction)Haiku_Menu_AddSeparatorItem, METH_VARARGS, ""},
	{"RemoveItem", (PyCFunction)Haiku_Menu_RemoveItem, METH_VARARGS, ""},
	{"RemoveSubmenu", (PyCFunction)Haiku_Menu_RemoveSubmenu, METH_VARARGS, ""},
	{"RemoveItemAtIndex", (PyCFunction)Haiku_Menu_RemoveItemAtIndex, METH_VARARGS, ""},
	{"RemoveItems", (PyCFunction)Haiku_Menu_RemoveItems, METH_VARARGS, ""},
	{"ItemAt", (PyCFunction)Haiku_Menu_ItemAt, METH_VARARGS, ""},
	{"SubmenuAt", (PyCFunction)Haiku_Menu_SubmenuAt, METH_VARARGS, ""},
	{"CountItems", (PyCFunction)Haiku_Menu_CountItems, METH_VARARGS, ""},
	{"IndexOf", (PyCFunction)Haiku_Menu_IndexOf, METH_VARARGS, ""},
	{"IndexOfSubmenu", (PyCFunction)Haiku_Menu_IndexOfSubmenu, METH_VARARGS, ""},
	{"FindItem", (PyCFunction)Haiku_Menu_FindItem, METH_VARARGS, ""},
	{"FindItemByCommand", (PyCFunction)Haiku_Menu_FindItemByCommand, METH_VARARGS, ""},
	{"SetTargetForItems", (PyCFunction)Haiku_Menu_SetTargetForItems, METH_VARARGS, ""},
	{"SetMessengerTargetForItems", (PyCFunction)Haiku_Menu_SetMessengerTargetForItems, METH_VARARGS, ""},
	{"SetEnabled", (PyCFunction)Haiku_Menu_SetEnabled, METH_VARARGS, ""},
	{"SetRadioMode", (PyCFunction)Haiku_Menu_SetRadioMode, METH_VARARGS, ""},
	{"SetTriggersEnabled", (PyCFunction)Haiku_Menu_SetTriggersEnabled, METH_VARARGS, ""},
	{"SetMaxContentWidth", (PyCFunction)Haiku_Menu_SetMaxContentWidth, METH_VARARGS, ""},
	{"SetLabelFromMarked", (PyCFunction)Haiku_Menu_SetLabelFromMarked, METH_VARARGS, ""},
	{"IsLabelFromMarked", (PyCFunction)Haiku_Menu_IsLabelFromMarked, METH_VARARGS, ""},
	{"IsEnabled", (PyCFunction)Haiku_Menu_IsEnabled, METH_VARARGS, ""},
	{"IsRadioMode", (PyCFunction)Haiku_Menu_IsRadioMode, METH_VARARGS, ""},
	{"AreTriggersEnabled", (PyCFunction)Haiku_Menu_AreTriggersEnabled, METH_VARARGS, ""},
	{"IsRedrawAfterSticky", (PyCFunction)Haiku_Menu_IsRedrawAfterSticky, METH_VARARGS, ""},
	{"MaxContentWidth", (PyCFunction)Haiku_Menu_MaxContentWidth, METH_VARARGS, ""},
	{"FindMarked", (PyCFunction)Haiku_Menu_FindMarked, METH_VARARGS, ""},
	{"Supermenu", (PyCFunction)Haiku_Menu_Supermenu, METH_VARARGS, ""},
	{"Superitem", (PyCFunction)Haiku_Menu_Superitem, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_Menu_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_Menu_GetSupportedSuites, METH_VARARGS, ""},
	{"AddDynamicItem", (PyCFunction)Haiku_Menu_AddDynamicItem, METH_VARARGS, ""},
	{"DrawBackground", (PyCFunction)Haiku_Menu_DrawBackground, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Menu_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Menu";
	type->tp_basicsize   = sizeof(Haiku_Menu_Object);
	type->tp_dealloc     = (destructor)Haiku_Menu_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Menu_RichCompare;
	type->tp_methods     = Haiku_Menu_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_Menu_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

