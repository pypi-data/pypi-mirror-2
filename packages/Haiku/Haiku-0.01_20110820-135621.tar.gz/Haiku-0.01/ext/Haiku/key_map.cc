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
//static int Haiku_key_map_init(Haiku_key_map_Object* python_self, PyObject* python_args, PyObject* python_kwds);
static int Haiku_key_map_init(Haiku_key_map_Object* python_self, PyObject* python_args, PyObject* python_kwds) {
	// python_self->cpp_object already defined
	
	// don't let python code call us a second time
	if (python_self->cpp_object != NULL)
		return -1;
	
	python_self->cpp_object = new key_map();
	if (python_self->cpp_object == NULL)
		return -1;	
	
	// we own this object, so we can delete it
	python_self->can_delete_cpp_object = true;
	return 0;
}

//static void Haiku_key_map_DESTROY(Haiku_key_map_Object* python_self);
static void Haiku_key_map_DESTROY(Haiku_key_map_Object* python_self) {
	if (python_self->cpp_object != NULL) {
		if (python_self->can_delete_cpp_object) {
			delete python_self->cpp_object;
		}
	}
}

static PyObject* Haiku_key_map_Object_getversion(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_version; // from generate()
	py_version = Py_BuildValue("k", python_self->cpp_object->version);
	return py_version;
}

static int Haiku_key_map_Object_setversion(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->version = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getcaps_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_caps_key; // from generate()
	py_caps_key = Py_BuildValue("k", python_self->cpp_object->caps_key);
	return py_caps_key;
}

static int Haiku_key_map_Object_setcaps_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->caps_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getscroll_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_scroll_key; // from generate()
	py_scroll_key = Py_BuildValue("k", python_self->cpp_object->scroll_key);
	return py_scroll_key;
}

static int Haiku_key_map_Object_setscroll_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->scroll_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getnum_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_num_key; // from generate()
	py_num_key = Py_BuildValue("k", python_self->cpp_object->num_key);
	return py_num_key;
}

static int Haiku_key_map_Object_setnum_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->num_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getleft_shift_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_left_shift_key; // from generate()
	py_left_shift_key = Py_BuildValue("k", python_self->cpp_object->left_shift_key);
	return py_left_shift_key;
}

static int Haiku_key_map_Object_setleft_shift_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left_shift_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getright_shift_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_right_shift_key; // from generate()
	py_right_shift_key = Py_BuildValue("k", python_self->cpp_object->right_shift_key);
	return py_right_shift_key;
}

static int Haiku_key_map_Object_setright_shift_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right_shift_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getleft_command_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_left_command_key; // from generate()
	py_left_command_key = Py_BuildValue("k", python_self->cpp_object->left_command_key);
	return py_left_command_key;
}

static int Haiku_key_map_Object_setleft_command_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left_command_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getright_command_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_right_command_key; // from generate()
	py_right_command_key = Py_BuildValue("k", python_self->cpp_object->right_command_key);
	return py_right_command_key;
}

static int Haiku_key_map_Object_setright_command_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right_command_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getleft_control_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_left_control_key; // from generate()
	py_left_control_key = Py_BuildValue("k", python_self->cpp_object->left_control_key);
	return py_left_control_key;
}

static int Haiku_key_map_Object_setleft_control_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left_control_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getright_control_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_right_control_key; // from generate()
	py_right_control_key = Py_BuildValue("k", python_self->cpp_object->right_control_key);
	return py_right_control_key;
}

static int Haiku_key_map_Object_setright_control_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right_control_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getleft_option_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_left_option_key; // from generate()
	py_left_option_key = Py_BuildValue("k", python_self->cpp_object->left_option_key);
	return py_left_option_key;
}

static int Haiku_key_map_Object_setleft_option_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->left_option_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getright_option_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_right_option_key; // from generate()
	py_right_option_key = Py_BuildValue("k", python_self->cpp_object->right_option_key);
	return py_right_option_key;
}

static int Haiku_key_map_Object_setright_option_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->right_option_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getmenu_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_menu_key; // from generate()
	py_menu_key = Py_BuildValue("k", python_self->cpp_object->menu_key);
	return py_menu_key;
}

static int Haiku_key_map_Object_setmenu_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->menu_key = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getlock_settings(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_lock_settings; // from generate()
	py_lock_settings = Py_BuildValue("k", python_self->cpp_object->lock_settings);
	return py_lock_settings;
}

static int Haiku_key_map_Object_setlock_settings(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->lock_settings = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getcontrol_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_control_map; // from generate()
	PyObject* py_control_map_element;	// from array_arg_builder
	py_control_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_control_map_element = Py_BuildValue("l", python_self->cpp_object->control_map[i]);
		PyList_Append(py_control_map, py_control_map_element);
	}
	return py_control_map;
}

static int Haiku_key_map_Object_setcontrol_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->control_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getoption_caps_shift_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_option_caps_shift_map; // from generate()
	PyObject* py_option_caps_shift_map_element;	// from array_arg_builder
	py_option_caps_shift_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_option_caps_shift_map_element = Py_BuildValue("l", python_self->cpp_object->option_caps_shift_map[i]);
		PyList_Append(py_option_caps_shift_map, py_option_caps_shift_map_element);
	}
	return py_option_caps_shift_map;
}

static int Haiku_key_map_Object_setoption_caps_shift_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->option_caps_shift_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getoption_caps_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_option_caps_map; // from generate()
	PyObject* py_option_caps_map_element;	// from array_arg_builder
	py_option_caps_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_option_caps_map_element = Py_BuildValue("l", python_self->cpp_object->option_caps_map[i]);
		PyList_Append(py_option_caps_map, py_option_caps_map_element);
	}
	return py_option_caps_map;
}

static int Haiku_key_map_Object_setoption_caps_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->option_caps_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getoption_shift_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_option_shift_map; // from generate()
	PyObject* py_option_shift_map_element;	// from array_arg_builder
	py_option_shift_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_option_shift_map_element = Py_BuildValue("l", python_self->cpp_object->option_shift_map[i]);
		PyList_Append(py_option_shift_map, py_option_shift_map_element);
	}
	return py_option_shift_map;
}

static int Haiku_key_map_Object_setoption_shift_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->option_shift_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getoption_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_option_map; // from generate()
	PyObject* py_option_map_element;	// from array_arg_builder
	py_option_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_option_map_element = Py_BuildValue("l", python_self->cpp_object->option_map[i]);
		PyList_Append(py_option_map, py_option_map_element);
	}
	return py_option_map;
}

static int Haiku_key_map_Object_setoption_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->option_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getcaps_shift_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_caps_shift_map; // from generate()
	PyObject* py_caps_shift_map_element;	// from array_arg_builder
	py_caps_shift_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_caps_shift_map_element = Py_BuildValue("l", python_self->cpp_object->caps_shift_map[i]);
		PyList_Append(py_caps_shift_map, py_caps_shift_map_element);
	}
	return py_caps_shift_map;
}

static int Haiku_key_map_Object_setcaps_shift_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->caps_shift_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getcaps_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_caps_map; // from generate()
	PyObject* py_caps_map_element;	// from array_arg_builder
	py_caps_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_caps_map_element = Py_BuildValue("l", python_self->cpp_object->caps_map[i]);
		PyList_Append(py_caps_map, py_caps_map_element);
	}
	return py_caps_map;
}

static int Haiku_key_map_Object_setcaps_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->caps_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getshift_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_shift_map; // from generate()
	PyObject* py_shift_map_element;	// from array_arg_builder
	py_shift_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_shift_map_element = Py_BuildValue("l", python_self->cpp_object->shift_map[i]);
		PyList_Append(py_shift_map, py_shift_map_element);
	}
	return py_shift_map;
}

static int Haiku_key_map_Object_setshift_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->shift_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getnormal_map(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_normal_map; // from generate()
	PyObject* py_normal_map_element;	// from array_arg_builder
	py_normal_map = PyList_New(0);
	for (int i = 0; i < 128; i++) {
		py_normal_map_element = Py_BuildValue("l", python_self->cpp_object->normal_map[i]);
		PyList_Append(py_normal_map, py_normal_map_element);
	}
	return py_normal_map;
}

static int Haiku_key_map_Object_setnormal_map(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 128; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->normal_map[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getacute_dead_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_acute_dead_key; // from generate()
	PyObject* py_acute_dead_key_element;	// from array_arg_builder
	py_acute_dead_key = PyList_New(0);
	for (int i = 0; i < 32; i++) {
		py_acute_dead_key_element = Py_BuildValue("l", python_self->cpp_object->acute_dead_key[i]);
		PyList_Append(py_acute_dead_key, py_acute_dead_key_element);
	}
	return py_acute_dead_key;
}

static int Haiku_key_map_Object_setacute_dead_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->acute_dead_key[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getgrave_dead_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_grave_dead_key; // from generate()
	PyObject* py_grave_dead_key_element;	// from array_arg_builder
	py_grave_dead_key = PyList_New(0);
	for (int i = 0; i < 32; i++) {
		py_grave_dead_key_element = Py_BuildValue("l", python_self->cpp_object->grave_dead_key[i]);
		PyList_Append(py_grave_dead_key, py_grave_dead_key_element);
	}
	return py_grave_dead_key;
}

static int Haiku_key_map_Object_setgrave_dead_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->grave_dead_key[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getcircumflex_dead_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_circumflex_dead_key; // from generate()
	PyObject* py_circumflex_dead_key_element;	// from array_arg_builder
	py_circumflex_dead_key = PyList_New(0);
	for (int i = 0; i < 32; i++) {
		py_circumflex_dead_key_element = Py_BuildValue("l", python_self->cpp_object->circumflex_dead_key[i]);
		PyList_Append(py_circumflex_dead_key, py_circumflex_dead_key_element);
	}
	return py_circumflex_dead_key;
}

static int Haiku_key_map_Object_setcircumflex_dead_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->circumflex_dead_key[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getdieresis_dead_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_dieresis_dead_key; // from generate()
	PyObject* py_dieresis_dead_key_element;	// from array_arg_builder
	py_dieresis_dead_key = PyList_New(0);
	for (int i = 0; i < 32; i++) {
		py_dieresis_dead_key_element = Py_BuildValue("l", python_self->cpp_object->dieresis_dead_key[i]);
		PyList_Append(py_dieresis_dead_key, py_dieresis_dead_key_element);
	}
	return py_dieresis_dead_key;
}

static int Haiku_key_map_Object_setdieresis_dead_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->dieresis_dead_key[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_gettilde_dead_key(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_tilde_dead_key; // from generate()
	PyObject* py_tilde_dead_key_element;	// from array_arg_builder
	py_tilde_dead_key = PyList_New(0);
	for (int i = 0; i < 32; i++) {
		py_tilde_dead_key_element = Py_BuildValue("l", python_self->cpp_object->tilde_dead_key[i]);
		PyList_Append(py_tilde_dead_key, py_tilde_dead_key_element);
	}
	return py_tilde_dead_key;
}

static int Haiku_key_map_Object_settilde_dead_key(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	PyObject* value_element;	// from array_arg_parser()
	for (int i = 0; i < 32; i++) {
		value_element = PyList_GetItem(value, i);
		if (value_element == NULL) {
			// should be setting this to some default
			// but neither 0 nor NULL is right
			continue;
		}
		python_self->cpp_object->tilde_dead_key[i] = (int32)PyInt_AsLong(value_element); // element code
	}
	return 0;
}

static PyObject* Haiku_key_map_Object_getacute_tables(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_acute_tables; // from generate()
	py_acute_tables = Py_BuildValue("k", python_self->cpp_object->acute_tables);
	return py_acute_tables;
}

static int Haiku_key_map_Object_setacute_tables(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->acute_tables = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getgrave_tables(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_grave_tables; // from generate()
	py_grave_tables = Py_BuildValue("k", python_self->cpp_object->grave_tables);
	return py_grave_tables;
}

static int Haiku_key_map_Object_setgrave_tables(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->grave_tables = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getcircumflex_tables(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_circumflex_tables; // from generate()
	py_circumflex_tables = Py_BuildValue("k", python_self->cpp_object->circumflex_tables);
	return py_circumflex_tables;
}

static int Haiku_key_map_Object_setcircumflex_tables(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->circumflex_tables = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_getdieresis_tables(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_dieresis_tables; // from generate()
	py_dieresis_tables = Py_BuildValue("k", python_self->cpp_object->dieresis_tables);
	return py_dieresis_tables;
}

static int Haiku_key_map_Object_setdieresis_tables(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->dieresis_tables = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_Object_gettilde_tables(Haiku_key_map_Object* python_self, void* python_closure) {
	PyObject* py_tilde_tables; // from generate()
	py_tilde_tables = Py_BuildValue("k", python_self->cpp_object->tilde_tables);
	return py_tilde_tables;
}

static int Haiku_key_map_Object_settilde_tables(Haiku_key_map_Object* python_self, PyObject* value, void* closure) {
	python_self->cpp_object->tilde_tables = (uint32)PyLong_AsLong(value);
	return 0;
}

static PyObject* Haiku_key_map_RichCompare(PyObject* a, PyObject* b, int op) {
	bool retval;
	
	switch (op) {
		case Py_EQ:
			retval = ((Haiku_key_map_Object*)a)->cpp_object == ((Haiku_key_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		case Py_NE:
			retval = ((Haiku_key_map_Object*)a)->cpp_object != ((Haiku_key_map_Object*)b)->cpp_object;
			return Py_BuildValue("b", retval ? 1 : 0);
			break;
			
		default:
			return Py_NotImplemented;
	}
}

static PyGetSetDef Haiku_key_map_PyProperties[] = {
	{ (char*)"version", (getter)Haiku_key_map_Object_getversion, (setter)Haiku_key_map_Object_setversion, (char*)"<DOC>", NULL},
	{ (char*)"caps_key", (getter)Haiku_key_map_Object_getcaps_key, (setter)Haiku_key_map_Object_setcaps_key, (char*)"<DOC>", NULL},
	{ (char*)"scroll_key", (getter)Haiku_key_map_Object_getscroll_key, (setter)Haiku_key_map_Object_setscroll_key, (char*)"<DOC>", NULL},
	{ (char*)"num_key", (getter)Haiku_key_map_Object_getnum_key, (setter)Haiku_key_map_Object_setnum_key, (char*)"<DOC>", NULL},
	{ (char*)"left_shift_key", (getter)Haiku_key_map_Object_getleft_shift_key, (setter)Haiku_key_map_Object_setleft_shift_key, (char*)"<DOC>", NULL},
	{ (char*)"right_shift_key", (getter)Haiku_key_map_Object_getright_shift_key, (setter)Haiku_key_map_Object_setright_shift_key, (char*)"<DOC>", NULL},
	{ (char*)"left_command_key", (getter)Haiku_key_map_Object_getleft_command_key, (setter)Haiku_key_map_Object_setleft_command_key, (char*)"<DOC>", NULL},
	{ (char*)"right_command_key", (getter)Haiku_key_map_Object_getright_command_key, (setter)Haiku_key_map_Object_setright_command_key, (char*)"<DOC>", NULL},
	{ (char*)"left_control_key", (getter)Haiku_key_map_Object_getleft_control_key, (setter)Haiku_key_map_Object_setleft_control_key, (char*)"<DOC>", NULL},
	{ (char*)"right_control_key", (getter)Haiku_key_map_Object_getright_control_key, (setter)Haiku_key_map_Object_setright_control_key, (char*)"<DOC>", NULL},
	{ (char*)"left_option_key", (getter)Haiku_key_map_Object_getleft_option_key, (setter)Haiku_key_map_Object_setleft_option_key, (char*)"<DOC>", NULL},
	{ (char*)"right_option_key", (getter)Haiku_key_map_Object_getright_option_key, (setter)Haiku_key_map_Object_setright_option_key, (char*)"<DOC>", NULL},
	{ (char*)"menu_key", (getter)Haiku_key_map_Object_getmenu_key, (setter)Haiku_key_map_Object_setmenu_key, (char*)"<DOC>", NULL},
	{ (char*)"lock_settings", (getter)Haiku_key_map_Object_getlock_settings, (setter)Haiku_key_map_Object_setlock_settings, (char*)"<DOC>", NULL},
	{ (char*)"control_map", (getter)Haiku_key_map_Object_getcontrol_map, (setter)Haiku_key_map_Object_setcontrol_map, (char*)"<DOC>", NULL},
	{ (char*)"option_caps_shift_map", (getter)Haiku_key_map_Object_getoption_caps_shift_map, (setter)Haiku_key_map_Object_setoption_caps_shift_map, (char*)"<DOC>", NULL},
	{ (char*)"option_caps_map", (getter)Haiku_key_map_Object_getoption_caps_map, (setter)Haiku_key_map_Object_setoption_caps_map, (char*)"<DOC>", NULL},
	{ (char*)"option_shift_map", (getter)Haiku_key_map_Object_getoption_shift_map, (setter)Haiku_key_map_Object_setoption_shift_map, (char*)"<DOC>", NULL},
	{ (char*)"option_map", (getter)Haiku_key_map_Object_getoption_map, (setter)Haiku_key_map_Object_setoption_map, (char*)"<DOC>", NULL},
	{ (char*)"caps_shift_map", (getter)Haiku_key_map_Object_getcaps_shift_map, (setter)Haiku_key_map_Object_setcaps_shift_map, (char*)"<DOC>", NULL},
	{ (char*)"caps_map", (getter)Haiku_key_map_Object_getcaps_map, (setter)Haiku_key_map_Object_setcaps_map, (char*)"<DOC>", NULL},
	{ (char*)"shift_map", (getter)Haiku_key_map_Object_getshift_map, (setter)Haiku_key_map_Object_setshift_map, (char*)"<DOC>", NULL},
	{ (char*)"normal_map", (getter)Haiku_key_map_Object_getnormal_map, (setter)Haiku_key_map_Object_setnormal_map, (char*)"<DOC>", NULL},
	{ (char*)"acute_dead_key", (getter)Haiku_key_map_Object_getacute_dead_key, (setter)Haiku_key_map_Object_setacute_dead_key, (char*)"<DOC>", NULL},
	{ (char*)"grave_dead_key", (getter)Haiku_key_map_Object_getgrave_dead_key, (setter)Haiku_key_map_Object_setgrave_dead_key, (char*)"<DOC>", NULL},
	{ (char*)"circumflex_dead_key", (getter)Haiku_key_map_Object_getcircumflex_dead_key, (setter)Haiku_key_map_Object_setcircumflex_dead_key, (char*)"<DOC>", NULL},
	{ (char*)"dieresis_dead_key", (getter)Haiku_key_map_Object_getdieresis_dead_key, (setter)Haiku_key_map_Object_setdieresis_dead_key, (char*)"<DOC>", NULL},
	{ (char*)"tilde_dead_key", (getter)Haiku_key_map_Object_gettilde_dead_key, (setter)Haiku_key_map_Object_settilde_dead_key, (char*)"<DOC>", NULL},
	{ (char*)"acute_tables", (getter)Haiku_key_map_Object_getacute_tables, (setter)Haiku_key_map_Object_setacute_tables, (char*)"<DOC>", NULL},
	{ (char*)"grave_tables", (getter)Haiku_key_map_Object_getgrave_tables, (setter)Haiku_key_map_Object_setgrave_tables, (char*)"<DOC>", NULL},
	{ (char*)"circumflex_tables", (getter)Haiku_key_map_Object_getcircumflex_tables, (setter)Haiku_key_map_Object_setcircumflex_tables, (char*)"<DOC>", NULL},
	{ (char*)"dieresis_tables", (getter)Haiku_key_map_Object_getdieresis_tables, (setter)Haiku_key_map_Object_setdieresis_tables, (char*)"<DOC>", NULL},
	{ (char*)"tilde_tables", (getter)Haiku_key_map_Object_gettilde_tables, (setter)Haiku_key_map_Object_settilde_tables, (char*)"<DOC>", NULL},
	{NULL} /* Sentinel */
};

static void init_Haiku_key_map_PyType(PyTypeObject* type) {
	type->tp_name        = "Haiku.key_map";
	type->tp_basicsize   = sizeof(Haiku_key_map_Object);
	type->tp_dealloc     = (destructor)Haiku_key_map_DESTROY;
	type->tp_as_number   = 0;
	type->tp_flags       = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE;
	type->tp_doc         = "...";
	type->tp_richcompare = Haiku_key_map_RichCompare;
	type->tp_methods     = 0;
	type->tp_getset      = Haiku_key_map_PyProperties;
	type->tp_base        = 0;
	type->tp_init        = (initproc)Haiku_key_map_init;
	type->tp_alloc       = PyType_GenericAlloc;
	type->tp_new         = PyType_GenericNew;
	type->tp_bases       = 0;
}

