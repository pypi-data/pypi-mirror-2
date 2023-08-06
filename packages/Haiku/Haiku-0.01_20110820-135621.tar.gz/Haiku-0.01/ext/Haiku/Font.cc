/*
 * Automatically generated file
 */

// we need a module to expose the constants, and every module needs
// a methoddef, even if it's empty
static PyMethodDef Haiku_FontConstants_PyMethods[] = {
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
//static int Haiku_Font_init(Haiku_Font_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_Font_init(Haiku_Font_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new BFont();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static PyObject* Haiku_Font_newFromFont(PyTypeObject* python_type, PyObject* python_args);
static PyObject* Haiku_Font_newFromFont(PyTypeObject* python_type, PyObject* python_args) {
	Haiku_Font_Object* python_self;
	BFont* font;
	Haiku_Font_Object* py_font; // from generate_py()
	// python_self->cpp_object already defined
	
	python_self = (Haiku_Font_Object*)python_type->tp_alloc(python_type, 0);
	
	PyArg_ParseTuple(python_args, "O", &py_font);
	if (py_font != NULL) {
		font = ((Haiku_Font_Object*)py_font)->cpp_object;
	}
	
	python_self->cpp_object = new BFont(font);
	if (python_self->cpp_object == NULL)
		Py_RETURN_NONE;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return (PyObject*)python_self;
}

//static void Haiku_Font_DESTROY(Haiku_Font_Object* python_self);
static void Haiku_Font_DESTROY(Haiku_Font_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

//static PyObject* Haiku_Font_SetFamilyAndStyle(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFamilyAndStyle(Haiku_Font_Object* python_self, PyObject* python_args) {
	const font_family family = "";
	PyObject* py_family; // from generate_py ()
	const font_style style = "";
	PyObject* py_style; // from generate_py ()
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|OO", &py_family, &py_style);
	memcpy((void*)&family, (void*)PyString_AsString(py_family), B_FONT_FAMILY_LENGTH + 1);
	memcpy((void*)&style, (void*)PyString_AsString(py_style), B_FONT_STYLE_LENGTH + 1);
	
	retval = python_self->cpp_object->SetFamilyAndStyle(family, style);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetFamilyAndStyleFromCode(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFamilyAndStyleFromCode(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint32 code;
	
	PyArg_ParseTuple(python_args, "k", &code);
	
	python_self->cpp_object->SetFamilyAndStyle(code);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetFamilyAndFace(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFamilyAndFace(Haiku_Font_Object* python_self, PyObject* python_args) {
	const font_family family = "";
	PyObject* py_family; // from generate_py ()
	uint16 face;
	status_t retval;
	
	PyArg_ParseTuple(python_args, "|OH", &py_family, &face);
	memcpy((void*)&family, (void*)PyString_AsString(py_family), B_FONT_FAMILY_LENGTH + 1);
	
	retval = python_self->cpp_object->SetFamilyAndFace(family, face);
	
	if (retval != B_OK) {
		PyObject* errval = Py_BuildValue("l", retval);
		PyErr_SetObject(HaikuError, errval);
		return NULL;
	}
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetSize(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetSize(Haiku_Font_Object* python_self, PyObject* python_args) {
	float size;
	
	PyArg_ParseTuple(python_args, "f", &size);
	
	python_self->cpp_object->SetSize(size);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetShear(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetShear(Haiku_Font_Object* python_self, PyObject* python_args) {
	float shear;
	
	PyArg_ParseTuple(python_args, "f", &shear);
	
	python_self->cpp_object->SetShear(shear);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetRotation(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetRotation(Haiku_Font_Object* python_self, PyObject* python_args) {
	float rotation;
	
	PyArg_ParseTuple(python_args, "f", &rotation);
	
	python_self->cpp_object->SetRotation(rotation);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetFalseBoldWidth(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFalseBoldWidth(Haiku_Font_Object* python_self, PyObject* python_args) {
	float width;
	
	PyArg_ParseTuple(python_args, "f", &width);
	
	python_self->cpp_object->SetFalseBoldWidth(width);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetSpacing(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetSpacing(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint8 spacing;
	
	PyArg_ParseTuple(python_args, "B", &spacing);
	
	python_self->cpp_object->SetSpacing(spacing);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetEncoding(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetEncoding(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint8 encoding;
	
	PyArg_ParseTuple(python_args, "B", &encoding);
	
	python_self->cpp_object->SetEncoding(encoding);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetFace(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFace(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint16 face;
	
	PyArg_ParseTuple(python_args, "H", &face);
	
	python_self->cpp_object->SetFace(face);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_SetFlags(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_SetFlags(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint32 flags;
	
	PyArg_ParseTuple(python_args, "k", &flags);
	
	python_self->cpp_object->SetFlags(flags);
	
	Py_RETURN_NONE;
}

//static PyObject* Haiku_Font_GetFamilyAndStyle(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetFamilyAndStyle(Haiku_Font_Object* python_self, PyObject* python_args) {
	font_family* family;
	font_style* style;
	PyObject* py_family; // from generate_py()
	Py_ssize_t py_family_length;
	PyObject* py_style; // from generate_py()
	Py_ssize_t py_style_length;
	
	python_self->cpp_object->GetFamilyAndStyle(family, style);
	
	py_family = Py_BuildValue("s", &family);	// 's' instead of 's#' lets Python calculate length
	
	py_family_length = PyString_Size(py_family);
	if (py_family_length > B_FONT_FAMILY_LENGTH + 1) {
		py_family_length = B_FONT_FAMILY_LENGTH + 1;
		_PyString_Resize(&py_family, py_family_length);
	}
	
	py_style = Py_BuildValue("s", &style);	// 's' instead of 's#' lets Python calculate length
	
	py_style_length = PyString_Size(py_style);
	if (py_style_length > B_FONT_STYLE_LENGTH + 1) {
		py_style_length = B_FONT_STYLE_LENGTH + 1;
		_PyString_Resize(&py_style, py_style_length);
	}
	
	
	return Py_BuildValue("OO", py_family, py_style);
}

//static PyObject* Haiku_Font_FamilyAndStyleAsCode(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_FamilyAndStyleAsCode(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FamilyAndStyle();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Size(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Size(Haiku_Font_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Size();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Shear(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Shear(Haiku_Font_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Shear();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Rotation(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Rotation(Haiku_Font_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Rotation();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_FalseBoldWidth(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_FalseBoldWidth(Haiku_Font_Object* python_self, PyObject* python_args) {
	float retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FalseBoldWidth();
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Spacing(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Spacing(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Spacing();
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Encoding(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Encoding(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint8 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Encoding();
	
	py_retval = Py_BuildValue("B", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Face(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Face(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint16 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Face();
	
	py_retval = Py_BuildValue("H", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Flags(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Flags(Haiku_Font_Object* python_self, PyObject* python_args) {
	uint32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Flags();
	
	py_retval = Py_BuildValue("k", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_Direction(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Direction(Haiku_Font_Object* python_self, PyObject* python_args) {
	font_direction retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->Direction();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_IsFixed(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_IsFixed(Haiku_Font_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFixed();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Font_IsFullAndHalfFixed(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_IsFullAndHalfFixed(Haiku_Font_Object* python_self, PyObject* python_args) {
	bool retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->IsFullAndHalfFixed();
	
	py_retval = Py_BuildValue("b", (retval ? 1 : 0));
	return py_retval;
}

//static PyObject* Haiku_Font_BoundingBox(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_BoundingBox(Haiku_Font_Object* python_self, PyObject* python_args) {
	BRect retval;
	Haiku_Rect_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->BoundingBox();
	
	py_retval = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
	py_retval->cpp_object = (BRect*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Font_Blocks(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_Blocks(Haiku_Font_Object* python_self, PyObject* python_args) {
	unicode_block retval;
	Haiku_unicode_block_Object* py_retval; // from generate_py() (for outputs)
	
	retval = python_self->cpp_object->Blocks();
	
	py_retval = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	py_retval->cpp_object = (unicode_block*)&retval;
	// we own this object, so we can delete it
	py_retval->can_delete_cpp_object = true;
	return (PyObject*)py_retval;
}

//static PyObject* Haiku_Font_FileFormat(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_FileFormat(Haiku_Font_Object* python_self, PyObject* python_args) {
	font_file_format retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->FileFormat();
	
	py_retval = Py_BuildValue("i", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_CountTuned(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_CountTuned(Haiku_Font_Object* python_self, PyObject* python_args) {
	int32 retval;
	PyObject* py_retval; // from generate_py()
	
	retval = python_self->cpp_object->CountTuned();
	
	py_retval = Py_BuildValue("l", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_GetTunedInfo(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetTunedInfo(Haiku_Font_Object* python_self, PyObject* python_args) {
	int32 index;
	tuned_font_info* info;
	Haiku_tuned_font_info_Object* py_info; // from generate_py() (for outputs)
	
	PyArg_ParseTuple(python_args, "l", &index);
	
	python_self->cpp_object->GetTunedInfo(index, info);
	
	py_info = (Haiku_tuned_font_info_Object*)Haiku_tuned_font_info_PyType.tp_alloc(&Haiku_tuned_font_info_PyType, 0);
	py_info->cpp_object = (tuned_font_info*)info;
	// we own this object, so we can delete it
	py_info->can_delete_cpp_object = true;
	return (PyObject*)py_info;
}

//static PyObject* Haiku_Font_GetTruncatedStrings(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetTruncatedStrings(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char** stringArray;
	PyObject* py_stringArray; // from generate_py ()
	PyObject* py_stringArray_element;	// from array_arg_parser()
	int32 numStrings;
	uint32 mode;
	float width;
	char** resultArray;
	PyObject* py_resultArray; // from generate_py()
	PyObject* py_resultArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "Okf", &py_stringArray, &mode, &width);
	numStrings = PyList_Size(py_stringArray);
	for (int i = 0; i < numStrings; i++) {
		py_stringArray_element = PyList_GetItem(py_stringArray, i);
		if (py_stringArray_element == NULL) {
			stringArray[i] = NULL;
			continue;
		}
		stringArray[i] = (const char*)PyString_AsString(py_stringArray_element); // element code
	}
	
	python_self->cpp_object->GetTruncatedStrings(stringArray, numStrings, mode, width, resultArray);
	
	py_resultArray = PyList_New(0);
	for (int i = 0; i < numStrings; i++) {
		py_resultArray_element = Py_BuildValue("s", resultArray[i]);
		PyList_Append(py_resultArray, py_resultArray_element);
	}
	return py_resultArray;
}

//static PyObject* Haiku_Font_StringWidth(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_StringWidth(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* string;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "s", &string);
	
	retval = python_self->cpp_object->StringWidth(string);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_StringWidthWithLength(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_StringWidthWithLength(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* string;
	PyObject* py_string; // from generate_py ()
	int32 length;
	float retval;
	PyObject* py_retval; // from generate_py()
	
	PyArg_ParseTuple(python_args, "O", &py_string);
	PyString_AsStringAndSize(py_string, (char**)&string, (Py_ssize_t*)&length);
	
	retval = python_self->cpp_object->StringWidth(string, length);
	
	py_retval = Py_BuildValue("f", retval);
	return py_retval;
}

//static PyObject* Haiku_Font_GetStringWidths(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetStringWidths(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char** stringArray;
	PyObject* py_stringArray; // from generate_py ()
	PyObject* py_stringArray_element;	// from array_arg_parser()
	int32* lengthArray;
	PyObject* py_lengthArray; // from generate_py ()
	PyObject* py_lengthArray_element;	// from array_arg_parser()
	int32 numStrings;
	float* widthArray;
	PyObject* py_widthArray; // from generate_py()
	PyObject* py_widthArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OO", &py_stringArray, &py_lengthArray);
	numStrings = PyList_Size(py_stringArray);
	for (int i = 0; i < numStrings; i++) {
		py_stringArray_element = PyList_GetItem(py_stringArray, i);
		if (py_stringArray_element == NULL) {
			stringArray[i] = NULL;
			continue;
		}
		stringArray[i] = (const char*)PyString_AsString(py_stringArray_element); // element code
	}
	for (int i = 0; i < numStrings; i++) {
		py_lengthArray_element = PyList_GetItem(py_lengthArray, i);
		if (py_lengthArray_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		lengthArray[i] = (int32)PyInt_AsLong(py_lengthArray_element); // element code
	}
	
	python_self->cpp_object->GetStringWidths(stringArray, lengthArray, numStrings, widthArray);
	
	py_widthArray = PyList_New(0);
	for (int i = 0; i < numStrings; i++) {
		py_widthArray_element = Py_BuildValue("f", widthArray[i]);
		PyList_Append(py_widthArray, py_widthArray_element);
	}
	return py_widthArray;
}

//static PyObject* Haiku_Font_GetEscapements(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetEscapements(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	float* ecapementArray;
	PyObject* py_ecapementArray; // from generate_py()
	PyObject* py_ecapementArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "O", &py_charArray);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	
	python_self->cpp_object->GetEscapements(charArray, numChars, ecapementArray);
	
	py_ecapementArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_ecapementArray_element = Py_BuildValue("f", ecapementArray[i]);
		PyList_Append(py_ecapementArray, py_ecapementArray_element);
	}
	return py_ecapementArray;
}

//static PyObject* Haiku_Font_GetEscapementsWithDelta(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetEscapementsWithDelta(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	escapement_delta* delta;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	float* ecapementArray;
	PyObject* py_ecapementArray; // from generate_py()
	PyObject* py_ecapementArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OO", &py_charArray, &py_delta);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->GetEscapements(charArray, numChars, delta, ecapementArray);
	
	py_ecapementArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_ecapementArray_element = Py_BuildValue("f", ecapementArray[i]);
		PyList_Append(py_ecapementArray, py_ecapementArray_element);
	}
	return py_ecapementArray;
}

//static PyObject* Haiku_Font_GetEscapementsAsPoints(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetEscapementsAsPoints(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	escapement_delta* delta;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	BPoint* ecapementArray;
	PyObject* py_ecapementArray; // from generate_py()
	Haiku_Point_Object* py_ecapementArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OO", &py_charArray, &py_delta);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->GetEscapements(charArray, numChars, delta, ecapementArray);
	
	py_ecapementArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_ecapementArray_element = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_ecapementArray_element->cpp_object = (BPoint*)&ecapementArray[i];
		// we own this object, so we can delete it
		py_ecapementArray_element->can_delete_cpp_object = true;
		PyList_Append(py_ecapementArray, (PyObject*)py_ecapementArray_element);
	}
	return py_ecapementArray;
}

//static PyObject* Haiku_Font_GetEscapementsAsPointsWithOffsets(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetEscapementsAsPointsWithOffsets(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	escapement_delta* delta;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	BPoint* ecapementArray;
	BPoint* offsetArray;
	PyObject* py_ecapementArray; // from generate_py()
	Haiku_Point_Object* py_ecapementArray_element;	// from array_arg_builder
	PyObject* py_offsetArray; // from generate_py()
	Haiku_Point_Object* py_offsetArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OO", &py_charArray, &py_delta);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->GetEscapements(charArray, numChars, delta, ecapementArray, offsetArray);
	
	py_ecapementArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_ecapementArray_element = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_ecapementArray_element->cpp_object = (BPoint*)&ecapementArray[i];
		// we own this object, so we can delete it
		py_ecapementArray_element->can_delete_cpp_object = true;
		PyList_Append(py_ecapementArray, (PyObject*)py_ecapementArray_element);
	}
	py_offsetArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_offsetArray_element = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
		py_offsetArray_element->cpp_object = (BPoint*)&offsetArray[i];
		// we own this object, so we can delete it
		py_offsetArray_element->can_delete_cpp_object = true;
		PyList_Append(py_offsetArray, (PyObject*)py_offsetArray_element);
	}
	
	return Py_BuildValue("OO", py_ecapementArray, py_offsetArray);
}

//static PyObject* Haiku_Font_GetEdges(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetEdges(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	edge_info* edgeArray;
	PyObject* py_edgeArray; // from generate_py()
	Haiku_edge_info_Object* py_edgeArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "O", &py_charArray);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	
	python_self->cpp_object->GetEdges(charArray, numChars, edgeArray);
	
	py_edgeArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_edgeArray_element = (Haiku_edge_info_Object*)Haiku_edge_info_PyType.tp_alloc(&Haiku_edge_info_PyType, 0);
		py_edgeArray_element->cpp_object = (edge_info*)&edgeArray[i];
		// we own this object, so we can delete it
		py_edgeArray_element->can_delete_cpp_object = true;
		PyList_Append(py_edgeArray, (PyObject*)py_edgeArray_element);
	}
	return py_edgeArray;
}

//static PyObject* Haiku_Font_GetHeight(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetHeight(Haiku_Font_Object* python_self, PyObject* python_args) {
	font_height* height;
	Haiku_font_height_Object* py_height; // from generate_py() (for outputs)
	
	python_self->cpp_object->GetHeight(height);
	
	py_height = (Haiku_font_height_Object*)Haiku_font_height_PyType.tp_alloc(&Haiku_font_height_PyType, 0);
	py_height->cpp_object = (font_height*)height;
	// we own this object, so we can delete it
	py_height->can_delete_cpp_object = true;
	return (PyObject*)py_height;
}

//static PyObject* Haiku_Font_GetBoundingBoxesAsGlyphs(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetBoundingBoxesAsGlyphs(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	font_metric_mode mode;
	BRect* boundingBoxArray;
	PyObject* py_boundingBoxArray; // from generate_py()
	Haiku_Rect_Object* py_boundingBoxArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "Oi", &py_charArray, &mode);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	
	python_self->cpp_object->GetBoundingBoxesAsGlyphs(charArray, numChars, mode, boundingBoxArray);
	
	py_boundingBoxArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_boundingBoxArray_element = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
		py_boundingBoxArray_element->cpp_object = (BRect*)&boundingBoxArray[i];
		// we own this object, so we can delete it
		py_boundingBoxArray_element->can_delete_cpp_object = true;
		PyList_Append(py_boundingBoxArray, (PyObject*)py_boundingBoxArray_element);
	}
	return py_boundingBoxArray;
}

//static PyObject* Haiku_Font_GetBoundingBoxesAsString(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetBoundingBoxesAsString(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	font_metric_mode mode;
	escapement_delta* delta;
	Haiku_escapement_delta_Object* py_delta; // from generate_py()
	BRect* boundingBoxArray;
	PyObject* py_boundingBoxArray; // from generate_py()
	Haiku_Rect_Object* py_boundingBoxArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OiO", &py_charArray, &mode, &py_delta);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	if (py_delta != NULL) {
		delta = ((Haiku_escapement_delta_Object*)py_delta)->cpp_object;
	}
	
	python_self->cpp_object->GetBoundingBoxesAsString(charArray, numChars, mode, delta, boundingBoxArray);
	
	py_boundingBoxArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_boundingBoxArray_element = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
		py_boundingBoxArray_element->cpp_object = (BRect*)&boundingBoxArray[i];
		// we own this object, so we can delete it
		py_boundingBoxArray_element->can_delete_cpp_object = true;
		PyList_Append(py_boundingBoxArray, (PyObject*)py_boundingBoxArray_element);
	}
	return py_boundingBoxArray;
}

//static PyObject* Haiku_Font_GetBoundingBoxesForStrings(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetBoundingBoxesForStrings(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char** stringArray;
	PyObject* py_stringArray; // from generate_py ()
	PyObject* py_stringArray_element;	// from array_arg_parser()
	int32 numStrings;
	font_metric_mode mode;
	escapement_delta* deltas;
	PyObject* py_deltas; // from generate_py ()
	PyObject* py_deltas_element;	// from array_arg_parser()
	BRect* boundingBoxArray;
	PyObject* py_boundingBoxArray; // from generate_py()
	Haiku_Rect_Object* py_boundingBoxArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "OiO", &py_stringArray, &mode, &py_deltas);
	numStrings = PyList_Size(py_stringArray);
	for (int i = 0; i < numStrings; i++) {
		py_stringArray_element = PyList_GetItem(py_stringArray, i);
		if (py_stringArray_element == NULL) {
			stringArray[i] = NULL;
			continue;
		}
		stringArray[i] = (const char*)PyString_AsString(py_stringArray_element); // element code
	}
	for (int i = 0; i < numStrings; i++) {
		py_deltas_element = PyList_GetItem(py_deltas, i);
		if (py_deltas_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		if (py_deltas_element != NULL) { // element code
			memcpy((void*)&deltas[i], (void*)((Haiku_escapement_delta_Object*)py_deltas_element)->cpp_object, sizeof(escapement_delta)); // element code
		} // element code
	}
	
	python_self->cpp_object->GetBoundingBoxesForStrings(stringArray, numStrings, mode, deltas, boundingBoxArray);
	
	py_boundingBoxArray = PyList_New(0);
	for (int i = 0; i < numStrings; i++) {
		py_boundingBoxArray_element = (Haiku_Rect_Object*)Haiku_Rect_PyType.tp_alloc(&Haiku_Rect_PyType, 0);
		py_boundingBoxArray_element->cpp_object = (BRect*)&boundingBoxArray[i];
		// we own this object, so we can delete it
		py_boundingBoxArray_element->can_delete_cpp_object = true;
		PyList_Append(py_boundingBoxArray, (PyObject*)py_boundingBoxArray_element);
	}
	return py_boundingBoxArray;
}

//static PyObject* Haiku_Font_GetGlyphShapes(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetGlyphShapes(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	BShape** glyphShapeArray;
	PyObject* py_glyphShapeArray; // from generate_py()
	Haiku_Shape_Object* py_glyphShapeArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "O", &py_charArray);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	
	python_self->cpp_object->GetGlyphShapes(charArray, numChars, glyphShapeArray);
	
	py_glyphShapeArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_glyphShapeArray_element = (Haiku_Shape_Object*)Haiku_Shape_PyType.tp_alloc(&Haiku_Shape_PyType, 0);
		py_glyphShapeArray_element->cpp_object = (BShape*)glyphShapeArray[i];
		// we own this object, so we can delete it
		py_glyphShapeArray_element->can_delete_cpp_object = true;
		PyList_Append(py_glyphShapeArray, (PyObject*)py_glyphShapeArray_element);
	}
	return py_glyphShapeArray;
}

//static PyObject* Haiku_Font_GetHasGlyphs(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_GetHasGlyphs(Haiku_Font_Object* python_self, PyObject* python_args) {
	const char* charArray;
	PyObject* py_charArray; // from generate_py ()
	int32 numChars;
	bool* hasArray;
	PyObject* py_hasArray; // from generate_py()
	PyObject* py_hasArray_element;	// from array_arg_builder
	
	PyArg_ParseTuple(python_args, "O", &py_charArray);
	PyString_AsStringAndSize(py_charArray, (char**)&charArray, (Py_ssize_t*)&numChars);
	
	python_self->cpp_object->GetHasGlyphs(charArray, numChars, hasArray);
	
	py_hasArray = PyList_New(0);
	for (int i = 0; i < numChars; i++) {
		py_hasArray_element = Py_BuildValue("b", (hasArray[i] ? 1 : 0));
		PyList_Append(py_hasArray, py_hasArray_element);
	}
	return py_hasArray;
}

//static PyObject* Haiku_Font_PrintToStream(Haiku_Font_Object* python_self, PyObject* python_args);
static PyObject* Haiku_Font_PrintToStream(Haiku_Font_Object* python_self, PyObject* python_args) {
	python_self->cpp_object->PrintToStream();
	
	Py_RETURN_NONE;
}

static PyObject* Haiku_Font_Object_be_plain_font(Haiku_Font_Object* python_dummy) {
	Haiku_Font_Object* py_be_plain_font;
	py_be_plain_font = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_be_plain_font->cpp_object = (BFont*)be_plain_font;
	// cannot delete this object; we do not own it
	py_be_plain_font->can_delete_cpp_object = false;
	return (PyObject*)py_be_plain_font;
}

static PyObject* Haiku_Font_Object_be_bold_font(Haiku_Font_Object* python_dummy) {
	Haiku_Font_Object* py_be_bold_font;
	py_be_bold_font = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_be_bold_font->cpp_object = (BFont*)be_bold_font;
	// cannot delete this object; we do not own it
	py_be_bold_font->can_delete_cpp_object = false;
	return (PyObject*)py_be_bold_font;
}

static PyObject* Haiku_Font_Object_be_fixed_font(Haiku_Font_Object* python_dummy) {
	Haiku_Font_Object* py_be_fixed_font;
	py_be_fixed_font = (Haiku_Font_Object*)Haiku_Font_PyType.tp_alloc(&Haiku_Font_PyType, 0);
	py_be_fixed_font->cpp_object = (BFont*)be_fixed_font;
	// cannot delete this object; we do not own it
	py_be_fixed_font->can_delete_cpp_object = false;
	return (PyObject*)py_be_fixed_font;
}

static PyObject* Haiku_Font_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = *((Haiku_Font_Object*)a)->cpp_object == *((Haiku_Font_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = *((Haiku_Font_Object*)a)->cpp_object != *((Haiku_Font_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyMethodDef Haiku_Font_PyMethods[] = {
	{"FromFont", (PyCFunction)Haiku_Font_newFromFont, METH_VARARGS|METH_CLASS, ""},
	{"SetFamilyAndStyle", (PyCFunction)Haiku_Font_SetFamilyAndStyle, METH_VARARGS, ""},
	{"SetFamilyAndStyleFromCode", (PyCFunction)Haiku_Font_SetFamilyAndStyleFromCode, METH_VARARGS, ""},
	{"SetFamilyAndFace", (PyCFunction)Haiku_Font_SetFamilyAndFace, METH_VARARGS, ""},
	{"SetSize", (PyCFunction)Haiku_Font_SetSize, METH_VARARGS, ""},
	{"SetShear", (PyCFunction)Haiku_Font_SetShear, METH_VARARGS, ""},
	{"SetRotation", (PyCFunction)Haiku_Font_SetRotation, METH_VARARGS, ""},
	{"SetFalseBoldWidth", (PyCFunction)Haiku_Font_SetFalseBoldWidth, METH_VARARGS, ""},
	{"SetSpacing", (PyCFunction)Haiku_Font_SetSpacing, METH_VARARGS, ""},
	{"SetEncoding", (PyCFunction)Haiku_Font_SetEncoding, METH_VARARGS, ""},
	{"SetFace", (PyCFunction)Haiku_Font_SetFace, METH_VARARGS, ""},
	{"SetFlags", (PyCFunction)Haiku_Font_SetFlags, METH_VARARGS, ""},
	{"GetFamilyAndStyle", (PyCFunction)Haiku_Font_GetFamilyAndStyle, METH_VARARGS, ""},
	{"FamilyAndStyleAsCode", (PyCFunction)Haiku_Font_FamilyAndStyleAsCode, METH_VARARGS, ""},
	{"Size", (PyCFunction)Haiku_Font_Size, METH_VARARGS, ""},
	{"Shear", (PyCFunction)Haiku_Font_Shear, METH_VARARGS, ""},
	{"Rotation", (PyCFunction)Haiku_Font_Rotation, METH_VARARGS, ""},
	{"FalseBoldWidth", (PyCFunction)Haiku_Font_FalseBoldWidth, METH_VARARGS, ""},
	{"Spacing", (PyCFunction)Haiku_Font_Spacing, METH_VARARGS, ""},
	{"Encoding", (PyCFunction)Haiku_Font_Encoding, METH_VARARGS, ""},
	{"Face", (PyCFunction)Haiku_Font_Face, METH_VARARGS, ""},
	{"Flags", (PyCFunction)Haiku_Font_Flags, METH_VARARGS, ""},
	{"Direction", (PyCFunction)Haiku_Font_Direction, METH_VARARGS, ""},
	{"IsFixed", (PyCFunction)Haiku_Font_IsFixed, METH_VARARGS, ""},
	{"IsFullAndHalfFixed", (PyCFunction)Haiku_Font_IsFullAndHalfFixed, METH_VARARGS, ""},
	{"BoundingBox", (PyCFunction)Haiku_Font_BoundingBox, METH_VARARGS, ""},
	{"Blocks", (PyCFunction)Haiku_Font_Blocks, METH_VARARGS, ""},
	{"FileFormat", (PyCFunction)Haiku_Font_FileFormat, METH_VARARGS, ""},
	{"CountTuned", (PyCFunction)Haiku_Font_CountTuned, METH_VARARGS, ""},
	{"GetTunedInfo", (PyCFunction)Haiku_Font_GetTunedInfo, METH_VARARGS, ""},
	{"GetTruncatedStrings", (PyCFunction)Haiku_Font_GetTruncatedStrings, METH_VARARGS, ""},
	{"StringWidth", (PyCFunction)Haiku_Font_StringWidth, METH_VARARGS, ""},
	{"StringWidthWithLength", (PyCFunction)Haiku_Font_StringWidthWithLength, METH_VARARGS, ""},
	{"GetStringWidths", (PyCFunction)Haiku_Font_GetStringWidths, METH_VARARGS, ""},
	{"GetEscapements", (PyCFunction)Haiku_Font_GetEscapements, METH_VARARGS, ""},
	{"GetEscapementsWithDelta", (PyCFunction)Haiku_Font_GetEscapementsWithDelta, METH_VARARGS, ""},
	{"GetEscapementsAsPoints", (PyCFunction)Haiku_Font_GetEscapementsAsPoints, METH_VARARGS, ""},
	{"GetEscapementsAsPointsWithOffsets", (PyCFunction)Haiku_Font_GetEscapementsAsPointsWithOffsets, METH_VARARGS, ""},
	{"GetEdges", (PyCFunction)Haiku_Font_GetEdges, METH_VARARGS, ""},
	{"GetHeight", (PyCFunction)Haiku_Font_GetHeight, METH_VARARGS, ""},
	{"GetBoundingBoxesAsGlyphs", (PyCFunction)Haiku_Font_GetBoundingBoxesAsGlyphs, METH_VARARGS, ""},
	{"GetBoundingBoxesAsString", (PyCFunction)Haiku_Font_GetBoundingBoxesAsString, METH_VARARGS, ""},
	{"GetBoundingBoxesForStrings", (PyCFunction)Haiku_Font_GetBoundingBoxesForStrings, METH_VARARGS, ""},
	{"GetGlyphShapes", (PyCFunction)Haiku_Font_GetGlyphShapes, METH_VARARGS, ""},
	{"GetHasGlyphs", (PyCFunction)Haiku_Font_GetHasGlyphs, METH_VARARGS, ""},
	{"PrintToStream", (PyCFunction)Haiku_Font_PrintToStream, METH_VARARGS, ""},
	{"be_plain_font", (PyCFunction)Haiku_Font_Object_be_plain_font, METH_NOARGS|METH_STATIC, ""},
	{"be_bold_font", (PyCFunction)Haiku_Font_Object_be_bold_font, METH_NOARGS|METH_STATIC, ""},
	{"be_fixed_font", (PyCFunction)Haiku_Font_Object_be_fixed_font, METH_NOARGS|METH_STATIC, ""},
	{NULL} /* Sentinel */
};

static void init_Haiku_Font_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.Font";
	type->tp_basicsize   = sizeof(Haiku_Font_Object);
	type->tp_dealloc     = (destructor)Haiku_Font_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_Font_RichCompare;
	type->tp_methods     = Haiku_Font_PyMethods;
	type->tp_getset      = 0;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_Font_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

