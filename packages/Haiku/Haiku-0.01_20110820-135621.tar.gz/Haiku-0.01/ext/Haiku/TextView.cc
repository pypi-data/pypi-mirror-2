/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_TextViewConstants_PyMethods[] = {
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
//static int Haiku_TextView_init(Haiku_TextView_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_TextView_init(Haiku_TextView_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
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
	
	python_self->cpp_object = new BTextView(frame, name, textRect, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_TextView_newWithFontAndColor(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextView_newWithFontAndColor(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextView_Object* python_self;
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
	
	python_self = (Haiku_TextView_Object*)python_type->tp_alloc(python_type, 0);
	
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
	
	python_self->cpp_object = new BTextView(frame, name, textRect, font, color, resizingMode, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TextView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextView_newWithoutFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextView_Object* python_self;
	const char* name;
	uint32 flags;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sk", &name, &flags);
	
	python_self->cpp_object = new BTextView(name, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TextView_newWithFontAndColorAndNoFrame(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextView_newWithFontAndColorAndNoFrame(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextView_Object* python_self;
	const char* name;
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	rgb_color* color;
	Haiku_rgb_color_Object* py_color; // from generate_py()
	uint32 flags;
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "sOOk", &name, &py_font, &py_color, &flags);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	if (py_color != NULL) {
		color = ((Haiku_rgb_color_Object*)py_color)->cpp_object;
	}
	
	python_self->cpp_object = new BTextView(name, font, color, flags);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static PyObject* Haiku_TextView_newFromArchive(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_TextView_newFromArchive(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_TextView_Object* python_self;
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_TextView_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	python_self->cpp_object = new BTextView(archive);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_TextView_DESTROY(Haiku_TextView_Object* python_self);
static void Haiku_TextView_DESTROY(Haiku_TextView_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_TextView_Instantiate(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Instantiate(Haiku_TextView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextView_Archive(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Archive(Haiku_TextView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextView_MakeFocus(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MakeFocus(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool focused = true;
	PyObject* py_focused; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_focused);
	focused = (bool)(PyObject_IsTrue(py_focused));
	
	python_self->cpp_object->MakeFocus(focused);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_ResolveSpecifier(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ResolveSpecifier(Haiku_TextView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextView_GetSupportedSuites(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetSupportedSuites(Haiku_TextView_Object* python_self, PyObject* python_args) {
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

//static PyObject* Haiku_TextView_SetText(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetText(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* inText;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s|O", &inText, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->SetText(inText, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_SetTextWithLength(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetTextWithLength(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* inText;
	int32 inLength;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl|O", &inText, &inLength, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->SetText(inText, inLength, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Insert(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Insert(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* inText;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s|O", &inText, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->Insert(inText, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_InsertWithLength(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_InsertWithLength(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* inText;
	int32 inLength;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "sl|O", &inText, &inLength, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->Insert(inText, inLength, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_InsertWithOffset(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_InsertWithOffset(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	const char* inText;
	int32 inLength;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "lsl|O", &startOffset, &inText, &inLength, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->Insert(startOffset, inText, inLength, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Delete(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Delete(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Delete();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_DeleteWithOffset(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DeleteWithOffset(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	
	PyArg_ParseTuple(python_args, "ll", &startOffset, &endOffset);
	
	python_self->cpp_object->Delete(startOffset, endOffset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Text(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Text(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Text();
	
	py_retval = Py_BuildValue("s", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_TextLength(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_TextLength(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TextLength();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_GetText(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetText(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	int32 length;
	char* buffer;
	PyObject* py_buffer; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll", &offset, &length);
	
	python_self->cpp_object->GetText(offset, length, buffer);
	
	py_buffer = Py_BuildValue("s", buffer);
	return py_buffer;
}

//static PyObject* Haiku_TextView_ByteAt(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ByteAt(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &offset);
	
	retval = python_self->cpp_object->ByteAt(offset);
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_CountLines(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_CountLines(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountLines();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_CurrentLine(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_CurrentLine(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CurrentLine();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_GoToLine(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GoToLine(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 lineIndex;
	
	PyArg_ParseTuple(python_args, "l", &lineIndex);
	
	python_self->cpp_object->GoToLine(lineIndex);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Cut(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Cut(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BClipboard* clipboard;
	Haiku_Clipboard_Object* py_clipboard; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_clipboard);
	if (py_clipboard != NULL) {
		clipboard = ((Haiku_Clipboard_Object*)py_clipboard)->cpp_object;
	}
	
	python_self->cpp_object->Cut(clipboard);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Copy(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Copy(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BClipboard* clipboard;
	Haiku_Clipboard_Object* py_clipboard; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_clipboard);
	if (py_clipboard != NULL) {
		clipboard = ((Haiku_Clipboard_Object*)py_clipboard)->cpp_object;
	}
	
	python_self->cpp_object->Copy(clipboard);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Paste(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Paste(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BClipboard* clipboard;
	Haiku_Clipboard_Object* py_clipboard; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_clipboard);
	if (py_clipboard != NULL) {
		clipboard = ((Haiku_Clipboard_Object*)py_clipboard)->cpp_object;
	}
	
	python_self->cpp_object->Paste(clipboard);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Clear(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Clear(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->Clear();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_AcceptsPaste(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AcceptsPaste(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BClipboard* clipboard;
	Haiku_Clipboard_Object* py_clipboard; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_clipboard);
	if (py_clipboard != NULL) {
		clipboard = ((Haiku_Clipboard_Object*)py_clipboard)->cpp_object;
	}
	
	retval = python_self->cpp_object->AcceptsPaste(clipboard);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_AcceptsDrop(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AcceptsDrop(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BMessage* archive;
	Haiku_Message_Object* py_archive; // from generate_py()
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_archive);
	if (py_archive != NULL) {
		archive = ((Haiku_Message_Object*)py_archive)->cpp_object;
	}
	
	retval = python_self->cpp_object->AcceptsDrop(archive);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_Select(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Select(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	
	PyArg_ParseTuple(python_args, "ll", &startOffset, &endOffset);
	
	python_self->cpp_object->Select(startOffset, endOffset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_SelectAll(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SelectAll(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->SelectAll();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_GetSelection(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetSelection(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 outStart;
	int32 outEnd;
	
	python_self->cpp_object->GetSelection(&outStart, &outEnd);
	
	return Py_BuildValue("ll", outStart, outEnd);
}

//static PyObject* Haiku_TextView_SetFontAndColor(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetFontAndColor(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BFont* inFont;
	Haiku_Font_Object* py_inFont; // from generate_py()
	uint32 inMode = B_FONT_ALL;
	rgb_color* inColor = NULL;
	Haiku_rgb_color_Object* py_inColor; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|kO", &py_inFont, &inMode, &py_inColor);
	if (py_inFont != NULL) {
		inFont = ((Haiku_Font_Object*)py_inFont)->cpp_object;
	}
	if (py_inColor != NULL) {
		inColor = ((Haiku_rgb_color_Object*)py_inColor)->cpp_object;
	}
	
	python_self->cpp_object->SetFontAndColor(inFont, inMode, inColor);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_SetFontAndColorBetweenOffsets(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetFontAndColorBetweenOffsets(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	BFont* inFont;
	Haiku_Font_Object* py_inFont; // from generate_py()
	uint32 inMode = B_FONT_ALL;
	rgb_color* inColor = NULL;
	Haiku_rgb_color_Object* py_inColor; // from generate_py()
	
	PyArg_ParseTuple(python_args, "llO|kO", &startOffset, &endOffset, &py_inFont, &inMode, &py_inColor);
	if (py_inFont != NULL) {
		inFont = ((Haiku_Font_Object*)py_inFont)->cpp_object;
	}
	if (py_inColor != NULL) {
		inColor = ((Haiku_rgb_color_Object*)py_inColor)->cpp_object;
	}
	
	python_self->cpp_object->SetFontAndColor(startOffset, endOffset, inFont, inMode, inColor);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_GetFontAndColor(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetFontAndColor(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 inOffset;
	BFont* outFont;
	rgb_color* outColor = NULL;
	Haiku_rgb_color_Object* py_outColor; // from generate_py()
	Haiku_Font_Object* py_outFont; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l|O", &inOffset, &py_outColor);
	if (py_outColor != NULL) {
		outColor = ((Haiku_rgb_color_Object*)py_outColor)->cpp_object;
	}
	
	python_self->cpp_object->GetFontAndColor(inOffset, outFont, outColor);
	
	py_outFont = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_outFont->cpp_object = (BFont*)outFont;
	// we own this object, so we can delete it
	py_outFont->can_delete_cpp_object = true;
	return (PyObject*)py_outFont;
}

//static PyObject* Haiku_TextView_GetFontAndColorAtSelection(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetFontAndColorAtSelection(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BFont* outFont;
	uint32 sameProperties;
	rgb_color* outColor = NULL;
	bool sameColor;
	Haiku_Font_Object* py_outFont; // from generate_py()
	Haiku_rgb_color_Object* py_outColor; // from generate_py()
	PyObject* py_sameColor; // from generate_py()
	
	python_self->cpp_object->GetFontAndColor(outFont, &sameProperties, outColor, &sameColor);
	
	py_outFont = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_outFont->cpp_object = (BFont*)outFont;
	// we own this object, so we can delete it
	py_outFont->can_delete_cpp_object = true;
	py_outColor = (Haiku_rgb_color_Object*)Haiku_rgb_color_PyType.tp_alloc(&Haiku_rgb_color_PyType, 0);
	py_outColor->cpp_object = (rgb_color*)outColor;
	// we own this object, so we can delete it
	py_outColor->can_delete_cpp_object = true;
	py_sameColor = Py_BuildValue("b", (sameColor ? 1 : 0));
	
	return Py_BuildValue("OkOO", py_outFont, sameProperties, py_outColor, py_sameColor);
}

//static PyObject* Haiku_TextView_SetRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	text_run_array* inRuns = NULL;
	Haiku_text_run_array_Object* py_inRuns; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll|O", &startOffset, &endOffset, &py_inRuns);
	if (py_inRuns != NULL) {
		inRuns = ((Haiku_text_run_array_Object*)py_inRuns)->cpp_object;
	}
	
	python_self->cpp_object->SetRunArray(startOffset, endOffset, inRuns);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_RunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_RunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	int32 outSize;
	text_run_array* retval;
	Haiku_text_run_array_Object* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "ll", &startOffset, &endOffset);
	
	retval = python_self->cpp_object->RunArray(startOffset, endOffset, &outSize);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_text_run_array_Object*)Haiku_text_run_array_PyType.tp_alloc(&Haiku_text_run_array_PyType, 0);
	py_retval->cpp_object = (text_run_array*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	
	return Py_BuildValue("Ol", py_retval, outSize);
}

//static PyObject* Haiku_TextView_LineAt(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_LineAt(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &offset);
	
	retval = python_self->cpp_object->LineAt(offset);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_LineAtPoint(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_LineAtPoint(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->LineAt(point);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_PointAt(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_PointAt(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	float outHeight;
	BPoint retval;
	Haiku_Point_Object* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &offset);
	
	retval = python_self->cpp_object->PointAt(offset, &outHeight);
	
	py_retval = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	py_retval->cpp_object = (BPoint*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	
	return Py_BuildValue("Of", py_retval, outHeight);
}

//static PyObject* Haiku_TextView_OffsetAt(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_OffsetAt(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 line;
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &line);
	
	retval = python_self->cpp_object->OffsetAt(line);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_OffsetAtPoint(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_OffsetAtPoint(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	retval = python_self->cpp_object->OffsetAt(point);
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_FindWord(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_FindWord(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 inOffset;
	int32 outFromOffset;
	int32 outToOffset;
	
	PyArg_ParseTuple(python_args, "l", &inOffset);
	
	python_self->cpp_object->FindWord(inOffset, &outFromOffset, &outToOffset);
	
	return Py_BuildValue("ll", outFromOffset, outToOffset);
}

//static PyObject* Haiku_TextView_CanEndLine(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_CanEndLine(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &offset);
	
	retval = python_self->cpp_object->CanEndLine(offset);
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_LineWidth(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_LineWidth(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 lineIndex = 0;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|l", &lineIndex);
	
	retval = python_self->cpp_object->LineWidth(lineIndex);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_LineHeight(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_LineHeight(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 lineIndex = 0;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|l", &lineIndex);
	
	retval = python_self->cpp_object->LineHeight(lineIndex);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_TextHeight(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_TextHeight(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startLine = 0;
	int32 endLine = 0;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "|ll", &startLine, &endLine);
	
	retval = python_self->cpp_object->TextHeight(startLine, endLine);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_ScrollToOffset(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ScrollToOffset(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 offset;
	
	PyArg_ParseTuple(python_args, "l", &offset);
	
	python_self->cpp_object->ScrollToOffset(offset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_ScrollToSelection(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ScrollToSelection(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ScrollToSelection();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Highlight(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Highlight(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 startOffset;
	int32 endOffset;
	
	PyArg_ParseTuple(python_args, "ll", &startOffset, &endOffset);
	
	python_self->cpp_object->Highlight(startOffset, endOffset);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_SetTextRect(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetTextRect(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BRect rect;
	Haiku_Rect_Object* py_rect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_rect);
	if (py_rect != NULL) {
		memcpy((void*)&rect, (void*)((Haiku_Rect_Object*)py_rect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->SetTextRect(rect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_TextRect(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_TextRect(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->TextRect();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TextView_SetInsets(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetInsets(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float left;
	float top;
	float right;
	float bottom;
	
	PyArg_ParseTuple(python_args, "ffff", &left, &top, &right, &bottom);
	
	python_self->cpp_object->SetInsets(left, top, right, bottom);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_GetInsets(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetInsets(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float left;
	float top;
	float right;
	float bottom;
	
	python_self->cpp_object->GetInsets(&left, &top, &right, &bottom);
	
	return Py_BuildValue("ffff", left, top, right, bottom);
}

//static PyObject* Haiku_TextView_SetStylable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetStylable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool stylable;
	PyObject* py_stylable; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_stylable);
	stylable = (bool)(PyObject_IsTrue(py_stylable));
	
	python_self->cpp_object->SetStylable(stylable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_IsStylable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_IsStylable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsStylable();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_SetTabWidth(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetTabWidth(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float width;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->SetTabWidth(width);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_TabWidth(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_TabWidth(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->TabWidth();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_MakeSelectable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MakeSelectable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool selectable;
	PyObject* py_selectable; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_selectable);
	selectable = (bool)(PyObject_IsTrue(py_selectable));
	
	python_self->cpp_object->MakeSelectable(selectable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_IsSelectable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_IsSelectable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsSelectable();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_MakeEditable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MakeEditable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool editable;
	PyObject* py_editable; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_editable);
	editable = (bool)(PyObject_IsTrue(py_editable));
	
	python_self->cpp_object->MakeEditable(editable);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_IsEditable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_IsEditable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsEditable();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_SetWordWrap(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetWordWrap(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool wrap;
	PyObject* py_wrap; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_wrap);
	wrap = (bool)(PyObject_IsTrue(py_wrap));
	
	python_self->cpp_object->SetWordWrap(wrap);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_DoesWordWrap(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DoesWordWrap(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DoesWordWrap();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_SetMaxBytes(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetMaxBytes(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 max;
	
	PyArg_ParseTuple(python_args, "l", &max);
	
	python_self->cpp_object->SetMaxBytes(max);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_MaxBytes(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MaxBytes(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->MaxBytes();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_DisallowChar(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DisallowChar(Haiku_TextView_Object* python_self, PyObject* python_args) {
	uint32 aChar;
	
	PyArg_ParseTuple(python_args, "k", &aChar);
	
	python_self->cpp_object->DisallowChar(aChar);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_AllowChar(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AllowChar(Haiku_TextView_Object* python_self, PyObject* python_args) {
	uint32 aChar;
	
	PyArg_ParseTuple(python_args, "k", &aChar);
	
	python_self->cpp_object->AllowChar(aChar);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_SetAlignment(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetAlignment(Haiku_TextView_Object* python_self, PyObject* python_args) {
	alignment flag;
	
	PyArg_ParseTuple(python_args, "i", &flag);
	
	python_self->cpp_object->SetAlignment(flag);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Alignment(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Alignment(Haiku_TextView_Object* python_self, PyObject* python_args) {
	alignment retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Alignment();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_SetAutoindent(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetAutoindent(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->SetAutoindent(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_DoesAutoindent(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DoesAutoindent(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DoesAutoindent();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_SetColorSpace(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetColorSpace(Haiku_TextView_Object* python_self, PyObject* python_args) {
	color_space colors;
	
	PyArg_ParseTuple(python_args, "i", &colors);
	
	python_self->cpp_object->SetColorSpace(colors);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_ColorSpace(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ColorSpace(Haiku_TextView_Object* python_self, PyObject* python_args) {
	color_space retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->ColorSpace();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_TextView_MakeResizable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MakeResizable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool resize;
	PyObject* py_resize; // from generate_py ()
	BView* resizeView = NULL;
	Haiku_View_Object* py_resizeView; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O|O", &py_resize, &py_resizeView);
	resize = (bool)(PyObject_IsTrue(py_resize));
	if (py_resizeView != NULL) {
		resizeView = ((Haiku_View_Object*)py_resizeView)->cpp_object;
	}
	
	python_self->cpp_object->MakeResizable(resize, resizeView);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_IsResizable(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_IsResizable(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsResizable();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_SetDoesUndo(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_SetDoesUndo(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool undo;
	PyObject* py_undo; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_undo);
	undo = (bool)(PyObject_IsTrue(py_undo));
	
	python_self->cpp_object->SetDoesUndo(undo);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_DoesUndo(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DoesUndo(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->DoesUndo();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_HideTyping(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_HideTyping(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool enabled;
	PyObject* py_enabled; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_enabled);
	enabled = (bool)(PyObject_IsTrue(py_enabled));
	
	python_self->cpp_object->HideTyping(enabled);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_IsTypingHidden(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_IsTypingHidden(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsTypingHidden();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_ResizeToPreferred(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_ResizeToPreferred(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->ResizeToPreferred();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_GetPreferredSize(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetPreferredSize(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float width;
	float height;
	
	python_self->cpp_object->GetPreferredSize(&width, &height);
	
	return Py_BuildValue("ff", width, height);
}

//static PyObject* Haiku_TextView_HasHeightForWidth(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_HasHeightForWidth(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->HasHeightForWidth();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_TextView_GetHeightForWidth(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_GetHeightForWidth(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float width;
	float min;
	float max;
	float preferred;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->GetHeightForWidth(width, &min, &max, &preferred);
	
	return Py_BuildValue("fff", min, max, preferred);
}

//static PyObject* Haiku_TextView_InvalidateLayout(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_InvalidateLayout(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool descendants = false;
	PyObject* py_descendants; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "|O", &py_descendants);
	descendants = (bool)(PyObject_IsTrue(py_descendants));
	
	python_self->cpp_object->InvalidateLayout(descendants);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_AllocRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AllocRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	int32 entryCount;
	int32 outSize;
	text_run_array* retval;
	Haiku_text_run_array_Object* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "l", &entryCount);
	
	retval = python_self->cpp_object->AllocRunArray(entryCount, &outSize);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_text_run_array_Object*)Haiku_text_run_array_PyType.tp_alloc(&Haiku_text_run_array_PyType, 0);
	py_retval->cpp_object = (text_run_array*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	
	return Py_BuildValue("Ol", py_retval, outSize);
}

//static PyObject* Haiku_TextView_CopyRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_CopyRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	text_run_array* orig;
	Haiku_text_run_array_Object* py_orig; // from generate_py()
	int32 countDelta;
	text_run_array* retval;
	Haiku_text_run_array_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "Ol", &py_orig, &countDelta);
	if (py_orig != NULL) {
		orig = ((Haiku_text_run_array_Object*)py_orig)->cpp_object;
	}
	
	retval = python_self->cpp_object->CopyRunArray(orig, countDelta);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_text_run_array_Object*)Haiku_text_run_array_PyType.tp_alloc(&Haiku_text_run_array_PyType, 0);
	py_retval->cpp_object = (text_run_array*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TextView_FreeRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_FreeRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	text_run_array* array;
	Haiku_text_run_array_Object* py_array; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_array);
	if (py_array != NULL) {
		array = ((Haiku_text_run_array_Object*)py_array)->cpp_object;
	}
	
	python_self->cpp_object->FreeRunArray(array);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_FlattenRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_FlattenRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const text_run_array* inArray;
	Haiku_text_run_array_Object* py_inArray; // from generate_py()
	int32 outSize;
	void* retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_inArray);
	if (py_inArray != NULL) {
		inArray = ((Haiku_text_run_array_Object*)py_inArray)->cpp_object;
	}
	
	retval = python_self->cpp_object->FlattenRunArray(inArray, &outSize);
	
	py_retval = Py_BuildValue("s#", retval, outSize);
	return py_retval;
}

//static PyObject* Haiku_TextView_UnflattenRunArray(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_UnflattenRunArray(Haiku_TextView_Object* python_self, PyObject* python_args) {
	void* data;
	PyObject* py_data; // from generate_py ()
	int32 outSize;
	text_run_array* retval;
	Haiku_text_run_array_Object* py_retval; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "O", &py_data);
	PyString_AsStringAndSize(py_data, (char**)&data, (Py_ssize_t*)&outSize);
	
	retval = python_self->cpp_object->UnflattenRunArray(data, &outSize);
	if (retval == NULL)
		Py_RETURN_NONE;	
	
	py_retval = (Haiku_text_run_array_Object*)Haiku_text_run_array_PyType.tp_alloc(&Haiku_text_run_array_PyType, 0);
	py_retval->cpp_object = (text_run_array*)retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_TextView_Undo(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Undo(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BClipboard* clipoard;
	Haiku_Clipboard_Object* py_clipoard; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_clipoard);
	if (py_clipoard != NULL) {
		clipoard = ((Haiku_Clipboard_Object*)py_clipoard)->cpp_object;
	}
	
	python_self->cpp_object->Undo(clipoard);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_UndoState(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_UndoState(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool isRedo;
	undo_state retval;
	PyObject* py_isRedo; // from generate_py()
	
	retval = python_self->cpp_object->UndoState(&isRedo);
	
	py_isRedo = Py_BuildValue("b", (isRedo ? 1 : 0));
	
	return Py_BuildValue("iO", retval, py_isRedo);
}

//static PyObject* Haiku_TextView_AttachedToWindow(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AttachedToWindow(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BTextView::AttachedToWindow();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_DetachedFromWindow(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_DetachedFromWindow(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BTextView::DetachedFromWindow();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Draw(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Draw(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BRect updateRect;
	Haiku_Rect_Object* py_updateRect; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_updateRect);
	if (py_updateRect != NULL) {
		memcpy((void*)&updateRect, (void*)((Haiku_Rect_Object*)py_updateRect)->cpp_object, sizeof(BRect));
	}
	
	python_self->cpp_object->BTextView::Draw(updateRect);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_MouseDown(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MouseDown(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->BTextView::MouseDown(point);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_MouseUp(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MouseUp(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_point);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	
	python_self->cpp_object->BTextView::MouseUp(point);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_MouseMoved(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MouseMoved(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BPoint point;
	Haiku_Point_Object* py_point; // from generate_py()
	uint32 transit;
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "OkO", &py_point, &transit, &py_message);
	if (py_point != NULL) {
		memcpy((void*)&point, (void*)((Haiku_Point_Object*)py_point)->cpp_object, sizeof(BPoint));
	}
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
	}
	
	python_self->cpp_object->BTextView::MouseMoved(point, transit, message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_WindowActivated(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_WindowActivated(Haiku_TextView_Object* python_self, PyObject* python_args) {
	bool state;
	PyObject* py_state; // from generate_py ()
	
	PyArg_ParseTuple(python_args, "O", &py_state);
	state = (bool)(PyObject_IsTrue(py_state));
	
	python_self->cpp_object->BTextView::WindowActivated(state);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_KeyDown(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_KeyDown(Haiku_TextView_Object* python_self, PyObject* python_args) {
	const char* bytes;
	PyObject* py_bytes; // from generate_py ()
	int32 numBytes;
	
	PyArg_ParseTuple(python_args, "O", &py_bytes);
	PyString_AsStringAndSize(py_bytes, (char**)&bytes, (Py_ssize_t*)&numBytes);
	
	python_self->cpp_object->BTextView::KeyDown(bytes, numBytes);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_Pulse(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_Pulse(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BTextView::Pulse();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_FrameResized(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_FrameResized(Haiku_TextView_Object* python_self, PyObject* python_args) {
	float newWidth;
	float newHeight;
	
	PyArg_ParseTuple(python_args, "ff", &newWidth, &newHeight);
	
	python_self->cpp_object->BTextView::FrameResized(newWidth, newHeight);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_MessageReceived(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_MessageReceived(Haiku_TextView_Object* python_self, PyObject* python_args) {
	BMessage* message;
	Haiku_Message_Object* py_message; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_message);
	if (py_message != NULL) {
		message = ((Haiku_Message_Object*)py_message)->cpp_object;
		((Haiku_Message_Object*)py_message)->can_delete_cpp_object = false;
	}
	
	python_self->cpp_object->BTextView::MessageReceived(message);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_AllAttached(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AllAttached(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BTextView::AllAttached();
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_TextView_AllDetached(Haiku_TextView_Object* python_self, PyObject* python_args);
static PyObject* Haiku_TextView_AllDetached(Haiku_TextView_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->BTextView::AllDetached();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_TextView_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_TextView_Object*)a)->cpp_object == ((Haiku_TextView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_TextView_Object*)a)->cpp_object != ((Haiku_TextView_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_TextView_PyMethods[] = {
	{"WithFontAndColor", (PyCFunction)Haiku_TextView_newWithFontAndColor, METH_VARARGS|METH_CLASS, ""},
	{"WithoutFrame", (PyCFunction)Haiku_TextView_newWithoutFrame, METH_VARARGS|METH_CLASS, ""},
	{"WithFontAndColorAndNoFrame", (PyCFunction)Haiku_TextView_newWithFontAndColorAndNoFrame, METH_VARARGS|METH_CLASS, ""},
	{"FromArchive", (PyCFunction)Haiku_TextView_newFromArchive, METH_VARARGS|METH_CLASS, ""},
	{"Instantiate", (PyCFunction)Haiku_TextView_Instantiate, METH_VARARGS, ""},
	{"Archive", (PyCFunction)Haiku_TextView_Archive, METH_VARARGS, ""},
	{"MakeFocus", (PyCFunction)Haiku_TextView_MakeFocus, METH_VARARGS, ""},
	{"ResolveSpecifier", (PyCFunction)Haiku_TextView_ResolveSpecifier, METH_VARARGS, ""},
	{"GetSupportedSuites", (PyCFunction)Haiku_TextView_GetSupportedSuites, METH_VARARGS, ""},
	{"SetText", (PyCFunction)Haiku_TextView_SetText, METH_VARARGS, ""},
	{"SetTextWithLength", (PyCFunction)Haiku_TextView_SetTextWithLength, METH_VARARGS, ""},
	{"Insert", (PyCFunction)Haiku_TextView_Insert, METH_VARARGS, ""},
	{"InsertWithLength", (PyCFunction)Haiku_TextView_InsertWithLength, METH_VARARGS, ""},
	{"InsertWithOffset", (PyCFunction)Haiku_TextView_InsertWithOffset, METH_VARARGS, ""},
	{"Delete", (PyCFunction)Haiku_TextView_Delete, METH_VARARGS, ""},
	{"DeleteWithOffset", (PyCFunction)Haiku_TextView_DeleteWithOffset, METH_VARARGS, ""},
	{"Text", (PyCFunction)Haiku_TextView_Text, METH_VARARGS, ""},
	{"TextLength", (PyCFunction)Haiku_TextView_TextLength, METH_VARARGS, ""},
	{"GetText", (PyCFunction)Haiku_TextView_GetText, METH_VARARGS, ""},
	{"ByteAt", (PyCFunction)Haiku_TextView_ByteAt, METH_VARARGS, ""},
	{"CountLines", (PyCFunction)Haiku_TextView_CountLines, METH_VARARGS, ""},
	{"CurrentLine", (PyCFunction)Haiku_TextView_CurrentLine, METH_VARARGS, ""},
	{"GoToLine", (PyCFunction)Haiku_TextView_GoToLine, METH_VARARGS, ""},
	{"Cut", (PyCFunction)Haiku_TextView_Cut, METH_VARARGS, ""},
	{"Copy", (PyCFunction)Haiku_TextView_Copy, METH_VARARGS, ""},
	{"Paste", (PyCFunction)Haiku_TextView_Paste, METH_VARARGS, ""},
	{"Clear", (PyCFunction)Haiku_TextView_Clear, METH_VARARGS, ""},
	{"AcceptsPaste", (PyCFunction)Haiku_TextView_AcceptsPaste, METH_VARARGS, ""},
	{"AcceptsDrop", (PyCFunction)Haiku_TextView_AcceptsDrop, METH_VARARGS, ""},
	{"Select", (PyCFunction)Haiku_TextView_Select, METH_VARARGS, ""},
	{"SelectAll", (PyCFunction)Haiku_TextView_SelectAll, METH_VARARGS, ""},
	{"GetSelection", (PyCFunction)Haiku_TextView_GetSelection, METH_VARARGS, ""},
	{"SetFontAndColor", (PyCFunction)Haiku_TextView_SetFontAndColor, METH_VARARGS, ""},
	{"SetFontAndColorBetweenOffsets", (PyCFunction)Haiku_TextView_SetFontAndColorBetweenOffsets, METH_VARARGS, ""},
	{"GetFontAndColor", (PyCFunction)Haiku_TextView_GetFontAndColor, METH_VARARGS, ""},
	{"GetFontAndColorAtSelection", (PyCFunction)Haiku_TextView_GetFontAndColorAtSelection, METH_VARARGS, ""},
	{"SetRunArray", (PyCFunction)Haiku_TextView_SetRunArray, METH_VARARGS, ""},
	{"RunArray", (PyCFunction)Haiku_TextView_RunArray, METH_VARARGS, ""},
	{"LineAt", (PyCFunction)Haiku_TextView_LineAt, METH_VARARGS, ""},
	{"LineAtPoint", (PyCFunction)Haiku_TextView_LineAtPoint, METH_VARARGS, ""},
	{"PointAt", (PyCFunction)Haiku_TextView_PointAt, METH_VARARGS, ""},
	{"OffsetAt", (PyCFunction)Haiku_TextView_OffsetAt, METH_VARARGS, ""},
	{"OffsetAtPoint", (PyCFunction)Haiku_TextView_OffsetAtPoint, METH_VARARGS, ""},
	{"FindWord", (PyCFunction)Haiku_TextView_FindWord, METH_VARARGS, ""},
	{"CanEndLine", (PyCFunction)Haiku_TextView_CanEndLine, METH_VARARGS, ""},
	{"LineWidth", (PyCFunction)Haiku_TextView_LineWidth, METH_VARARGS, ""},
	{"LineHeight", (PyCFunction)Haiku_TextView_LineHeight, METH_VARARGS, ""},
	{"TextHeight", (PyCFunction)Haiku_TextView_TextHeight, METH_VARARGS, ""},
	{"ScrollToOffset", (PyCFunction)Haiku_TextView_ScrollToOffset, METH_VARARGS, ""},
	{"ScrollToSelection", (PyCFunction)Haiku_TextView_ScrollToSelection, METH_VARARGS, ""},
	{"Highlight", (PyCFunction)Haiku_TextView_Highlight, METH_VARARGS, ""},
	{"SetTextRect", (PyCFunction)Haiku_TextView_SetTextRect, METH_VARARGS, ""},
	{"TextRect", (PyCFunction)Haiku_TextView_TextRect, METH_VARARGS, ""},
	{"SetInsets", (PyCFunction)Haiku_TextView_SetInsets, METH_VARARGS, ""},
	{"GetInsets", (PyCFunction)Haiku_TextView_GetInsets, METH_VARARGS, ""},
	{"SetStylable", (PyCFunction)Haiku_TextView_SetStylable, METH_VARARGS, ""},
	{"IsStylable", (PyCFunction)Haiku_TextView_IsStylable, METH_VARARGS, ""},
	{"SetTabWidth", (PyCFunction)Haiku_TextView_SetTabWidth, METH_VARARGS, ""},
	{"TabWidth", (PyCFunction)Haiku_TextView_TabWidth, METH_VARARGS, ""},
	{"MakeSelectable", (PyCFunction)Haiku_TextView_MakeSelectable, METH_VARARGS, ""},
	{"IsSelectable", (PyCFunction)Haiku_TextView_IsSelectable, METH_VARARGS, ""},
	{"MakeEditable", (PyCFunction)Haiku_TextView_MakeEditable, METH_VARARGS, ""},
	{"IsEditable", (PyCFunction)Haiku_TextView_IsEditable, METH_VARARGS, ""},
	{"SetWordWrap", (PyCFunction)Haiku_TextView_SetWordWrap, METH_VARARGS, ""},
	{"DoesWordWrap", (PyCFunction)Haiku_TextView_DoesWordWrap, METH_VARARGS, ""},
	{"SetMaxBytes", (PyCFunction)Haiku_TextView_SetMaxBytes, METH_VARARGS, ""},
	{"MaxBytes", (PyCFunction)Haiku_TextView_MaxBytes, METH_VARARGS, ""},
	{"DisallowChar", (PyCFunction)Haiku_TextView_DisallowChar, METH_VARARGS, ""},
	{"AllowChar", (PyCFunction)Haiku_TextView_AllowChar, METH_VARARGS, ""},
	{"SetAlignment", (PyCFunction)Haiku_TextView_SetAlignment, METH_VARARGS, ""},
	{"Alignment", (PyCFunction)Haiku_TextView_Alignment, METH_VARARGS, ""},
	{"SetAutoindent", (PyCFunction)Haiku_TextView_SetAutoindent, METH_VARARGS, ""},
	{"DoesAutoindent", (PyCFunction)Haiku_TextView_DoesAutoindent, METH_VARARGS, ""},
	{"SetColorSpace", (PyCFunction)Haiku_TextView_SetColorSpace, METH_VARARGS, ""},
	{"ColorSpace", (PyCFunction)Haiku_TextView_ColorSpace, METH_VARARGS, ""},
	{"MakeResizable", (PyCFunction)Haiku_TextView_MakeResizable, METH_VARARGS, ""},
	{"IsResizable", (PyCFunction)Haiku_TextView_IsResizable, METH_VARARGS, ""},
	{"SetDoesUndo", (PyCFunction)Haiku_TextView_SetDoesUndo, METH_VARARGS, ""},
	{"DoesUndo", (PyCFunction)Haiku_TextView_DoesUndo, METH_VARARGS, ""},
	{"HideTyping", (PyCFunction)Haiku_TextView_HideTyping, METH_VARARGS, ""},
	{"IsTypingHidden", (PyCFunction)Haiku_TextView_IsTypingHidden, METH_VARARGS, ""},
	{"ResizeToPreferred", (PyCFunction)Haiku_TextView_ResizeToPreferred, METH_VARARGS, ""},
	{"GetPreferredSize", (PyCFunction)Haiku_TextView_GetPreferredSize, METH_VARARGS, ""},
	{"HasHeightForWidth", (PyCFunction)Haiku_TextView_HasHeightForWidth, METH_VARARGS, ""},
	{"GetHeightForWidth", (PyCFunction)Haiku_TextView_GetHeightForWidth, METH_VARARGS, ""},
	{"InvalidateLayout", (PyCFunction)Haiku_TextView_InvalidateLayout, METH_VARARGS, ""},
	{"AllocRunArray", (PyCFunction)Haiku_TextView_AllocRunArray, METH_VARARGS, ""},
	{"CopyRunArray", (PyCFunction)Haiku_TextView_CopyRunArray, METH_VARARGS, ""},
	{"FreeRunArray", (PyCFunction)Haiku_TextView_FreeRunArray, METH_VARARGS, ""},
	{"FlattenRunArray", (PyCFunction)Haiku_TextView_FlattenRunArray, METH_VARARGS, ""},
	{"UnflattenRunArray", (PyCFunction)Haiku_TextView_UnflattenRunArray, METH_VARARGS, ""},
	{"Undo", (PyCFunction)Haiku_TextView_Undo, METH_VARARGS, ""},
	{"UndoState", (PyCFunction)Haiku_TextView_UndoState, METH_VARARGS, ""},
	{"AttachedToWindow", (PyCFunction)Haiku_TextView_AttachedToWindow, METH_VARARGS, ""},
	{"DetachedFromWindow", (PyCFunction)Haiku_TextView_DetachedFromWindow, METH_VARARGS, ""},
	{"Draw", (PyCFunction)Haiku_TextView_Draw, METH_VARARGS, ""},
	{"MouseDown", (PyCFunction)Haiku_TextView_MouseDown, METH_VARARGS, ""},
	{"MouseUp", (PyCFunction)Haiku_TextView_MouseUp, METH_VARARGS, ""},
	{"MouseMoved", (PyCFunction)Haiku_TextView_MouseMoved, METH_VARARGS, ""},
	{"WindowActivated", (PyCFunction)Haiku_TextView_WindowActivated, METH_VARARGS, ""},
	{"KeyDown", (PyCFunction)Haiku_TextView_KeyDown, METH_VARARGS, ""},
	{"Pulse", (PyCFunction)Haiku_TextView_Pulse, METH_VARARGS, ""},
	{"FrameResized", (PyCFunction)Haiku_TextView_FrameResized, METH_VARARGS, ""},
	{"MessageReceived", (PyCFunction)Haiku_TextView_MessageReceived, METH_VARARGS, ""},
	{"AllAttached", (PyCFunction)Haiku_TextView_AllAttached, METH_VARARGS, ""},
	{"AllDetached", (PyCFunction)Haiku_TextView_AllDetached, METH_VARARGS, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_TextView_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.TextView";
	type->tp_basicsize   = sizeof(Haiku_TextView_Object);
	type->tp_dealloc     = (destructor)Haiku_TextView_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_TextView_RichCompare;
	type->tp_methods     = Haiku_TextView_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = &Haiku_View_PyType;
	type->tp_init        = (initproc)Haiku_TextView_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

