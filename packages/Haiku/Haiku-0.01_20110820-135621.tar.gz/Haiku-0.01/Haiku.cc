/*
 * Automatically generated file
 */

extern "C" {
#include <Python.h>
}

#include "Haiku.h"
#include "HaikuUtils.cpp"
#include "ext/Haiku/Handler.cc"
#include "ext/Haiku/Looper.cc"
#include "ext/Haiku/Application.cc"
#include "ext/Haiku/CustomApplication.cpp"
#include "ext/Haiku/CustomApplication.cc"
#include "ext/Haiku/Clipboard.cc"
#include "ext/Haiku/Cursor.cc"
#include "ext/Haiku/Invoker.cc"
#include "ext/Haiku/Message.cc"
#include "ext/Haiku/Messenger.cc"
#include "ext/Haiku/Window.cc"
#include "ext/Haiku/CustomWindow.cpp"
#include "ext/Haiku/CustomWindow.cc"
#include "ext/Haiku/Alert.cc"
#include "ext/Haiku/View.cc"
#include "ext/Haiku/Box.cc"
#include "ext/Haiku/Control.cc"
#include "ext/Haiku/Button.cc"
#include "ext/Haiku/CheckBox.cc"
#include "ext/Haiku/ColorControl.cc"
#include "ext/Haiku/PictureButton.cc"
#include "ext/Haiku/RadioButton.cc"
#include "ext/Haiku/Slider.cc"
#include "ext/Haiku/TextControl.cc"
#include "ext/Haiku/ListView.cc"
#include "ext/Haiku/OutlineListView.cc"
#include "ext/Haiku/Menu.cc"
#include "ext/Haiku/menu_info.cc"
#include "ext/Haiku/MenuBar.cc"
#include "ext/Haiku/PopUpMenu.cc"
#include "ext/Haiku/MenuField.cc"
#include "ext/Haiku/ScrollBar.cc"
#include "ext/Haiku/ScrollView.cc"
#include "ext/Haiku/StatusBar.cc"
#include "ext/Haiku/StringView.cc"
#include "ext/Haiku/TabView.cc"
#include "ext/Haiku/Tab.cc"
#include "ext/Haiku/TextView.cc"
#include "ext/Haiku/CustomTextView.cpp"
#include "ext/Haiku/CustomTextView.cc"
#include "ext/Haiku/text_run.cc"
#include "ext/Haiku/text_run_array.cc"
#include "ext/Haiku/MenuItem.cc"
#include "ext/Haiku/SeparatorItem.cc"
#include "ext/Haiku/ListItem.cc"
#include "ext/Haiku/StringItem.cc"
#include "ext/Haiku/Font.cc"
#include "ext/Haiku/unicode_block.cc"
#include "ext/Haiku/edge_info.cc"
#include "ext/Haiku/font_height.cc"
#include "ext/Haiku/escapement_delta.cc"
#include "ext/Haiku/font_cache_info.cc"
#include "ext/Haiku/tuned_font_info.cc"
#include "ext/Haiku/Picture.cc"
#include "ext/Haiku/Point.cc"
#include "ext/Haiku/Polygon.cc"
#include "ext/Haiku/Rect.cc"
#include "ext/Haiku/Screen.cc"
#include "ext/Haiku/Shape.cc"
#include "ext/Haiku/ShapeIterator.cc"
#include "ext/Haiku/key_info.cc"
#include "ext/Haiku/key_map.cc"
#include "ext/Haiku/mouse_map.cc"
#include "ext/Haiku/scroll_bar_info.cc"
#include "ext/Haiku/pattern.cc"
#include "ext/Haiku/rgb_color.cc"
#include "ext/Haiku/color_map.cc"
#include "ext/Haiku/overlay_rect_limits.cc"
#include "ext/Haiku/overlay_restrictions.cc"
#include "ext/Haiku/screen_id.cc"
#include "ext/Haiku/EntryList.cc"
#include "ext/Haiku/Query.cc"
#include "ext/Haiku/MimeType.cc"
#include "ext/Haiku/NodeInfo.cc"
#include "ext/Haiku/Path.cc"
#include "ext/Haiku/Statable.cc"
#include "ext/Haiku/Entry.cc"
#include "ext/Haiku/entry_ref.cc"
#include "ext/Haiku/Node.cc"
#include "ext/Haiku/node_ref.cc"
#include "ext/Haiku/Volume.cc"
#include "ext/Haiku/VolumeRoster.cc"
#include "ext/Haiku/dirent.cc"
#include "ext/Haiku/stat_beos.cc"
#include "ext/Haiku/stat_beos_time.cc"
#include "ext/Haiku/stat.cc"
#include "ext/Haiku/timespec.cc"
#include "ext/Haiku/attr_info.cc"
#include "ext/Haiku/Archivable.cc"
#include "ext/Haiku/Archiver.cc"
#include "ext/Haiku/Unarchiver.cc"

static PyMethodDef Haiku_methods[] = {
	{NULL} /* Sentinel */
};

PyMODINIT_FUNC
initHaiku()
{
	PyObject* Haiku_module;
	PyObject* Haiku_HandlerConstants_module;
	PyObject* Haiku_LooperConstants_module;
	PyObject* Haiku_ClipboardConstants_module;
	PyObject* Haiku_CursorConstants_module;
	PyObject* Haiku_MessageConstants_module;
	PyObject* Haiku_WindowConstants_module;
	PyObject* Haiku_AlertConstants_module;
	PyObject* Haiku_ViewConstants_module;
	PyObject* Haiku_ControlConstants_module;
	PyObject* Haiku_ColorControlConstants_module;
	PyObject* Haiku_PictureButtonConstants_module;
	PyObject* Haiku_SliderConstants_module;
	PyObject* Haiku_ListViewConstants_module;
	PyObject* Haiku_MenuConstants_module;
	PyObject* Haiku_MenuBarConstants_module;
	PyObject* Haiku_ScrollBarConstants_module;
	PyObject* Haiku_TabViewConstants_module;
	PyObject* Haiku_TextViewConstants_module;
	PyObject* Haiku_FontConstants_module;
	PyObject* Haiku_PointConstants_module;
	PyObject* Haiku_QueryConstants_module;
	PyObject* Haiku_MimeTypeConstants_module;
	PyObject* Haiku_UnarchiverConstants_module;
	
	python_main = PyImport_AddModule("__main__");
	main_dict = PyModule_GetDict(python_main);

	// Haiku: package module
	Haiku_module = Py_InitModule("Haiku", Haiku_methods);
	if (Haiku_module == NULL)
		return;
	
	// add us immediately (ordinarily we're not added until this
	// function returns, but we need it before then
//	Py_INCREF(Haiku_module);
//	PyModule_AddObject(python_main, "Haiku", Haiku_module);

	// Haiku.Handler: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Handler_PyType(&Haiku_Handler_PyType);
	if (PyType_Ready(&Haiku_Handler_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Handler_PyType);
	PyModule_AddObject(Haiku_module, "Handler", (PyObject*)&Haiku_Handler_PyType);
	
	// Haiku.Looper: class
	//Py_INCREF(&Haiku_Handler_PyType);	// base class
	init_Haiku_Looper_PyType(&Haiku_Looper_PyType);
	if (PyType_Ready(&Haiku_Looper_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Looper_PyType);
	PyModule_AddObject(Haiku_module, "Looper", (PyObject*)&Haiku_Looper_PyType);
	
	// Haiku.Application: class
	//Py_INCREF(&Haiku_Looper_PyType);	// base class
	init_Haiku_Application_PyType(&Haiku_Application_PyType);
	if (PyType_Ready(&Haiku_Application_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Application_PyType);
	PyModule_AddObject(Haiku_module, "Application", (PyObject*)&Haiku_Application_PyType);
	
	// Haiku.CustomApplication: class
	//Py_INCREF(&Haiku_Application_PyType);	// base class
	init_Haiku_CustomApplication_PyType(&Haiku_CustomApplication_PyType);
	if (PyType_Ready(&Haiku_CustomApplication_PyType) < 0)
		return;
	Py_INCREF(&Haiku_CustomApplication_PyType);
	PyModule_AddObject(Haiku_module, "CustomApplication", (PyObject*)&Haiku_CustomApplication_PyType);
	
	// Haiku.Clipboard: class
	init_Haiku_Clipboard_PyType(&Haiku_Clipboard_PyType);
	if (PyType_Ready(&Haiku_Clipboard_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Clipboard_PyType);
	PyModule_AddObject(Haiku_module, "Clipboard", (PyObject*)&Haiku_Clipboard_PyType);
	
	// Haiku.Cursor: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Cursor_PyType(&Haiku_Cursor_PyType);
	if (PyType_Ready(&Haiku_Cursor_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Cursor_PyType);
	PyModule_AddObject(Haiku_module, "Cursor", (PyObject*)&Haiku_Cursor_PyType);
	
	// Haiku.Invoker: class
	init_Haiku_Invoker_PyType(&Haiku_Invoker_PyType);
	if (PyType_Ready(&Haiku_Invoker_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Invoker_PyType);
	PyModule_AddObject(Haiku_module, "Invoker", (PyObject*)&Haiku_Invoker_PyType);
	
	// Haiku.Message: class
	init_Haiku_Message_PyType(&Haiku_Message_PyType);
	if (PyType_Ready(&Haiku_Message_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Message_PyType);
	PyModule_AddObject(Haiku_module, "Message", (PyObject*)&Haiku_Message_PyType);
	
	// Haiku.Messenger: class
	init_Haiku_Messenger_PyType(&Haiku_Messenger_PyType);
	if (PyType_Ready(&Haiku_Messenger_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Messenger_PyType);
	PyModule_AddObject(Haiku_module, "Messenger", (PyObject*)&Haiku_Messenger_PyType);
	
	// Haiku.Window: class
	//Py_INCREF(&Haiku_Looper_PyType);	// base class
	init_Haiku_Window_PyType(&Haiku_Window_PyType);
	if (PyType_Ready(&Haiku_Window_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Window_PyType);
	PyModule_AddObject(Haiku_module, "Window", (PyObject*)&Haiku_Window_PyType);
	
	// Haiku.CustomWindow: class
	//Py_INCREF(&Haiku_Window_PyType);	// base class
	init_Haiku_CustomWindow_PyType(&Haiku_CustomWindow_PyType);
	if (PyType_Ready(&Haiku_CustomWindow_PyType) < 0)
		return;
	Py_INCREF(&Haiku_CustomWindow_PyType);
	PyModule_AddObject(Haiku_module, "CustomWindow", (PyObject*)&Haiku_CustomWindow_PyType);
	
	// Haiku.Alert: class
	//Py_INCREF(&Haiku_Window_PyType);	// base class
	init_Haiku_Alert_PyType(&Haiku_Alert_PyType);
	if (PyType_Ready(&Haiku_Alert_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Alert_PyType);
	PyModule_AddObject(Haiku_module, "Alert", (PyObject*)&Haiku_Alert_PyType);
	
	// Haiku.View: class
	//Py_INCREF(&Haiku_Handler_PyType);	// base class
	init_Haiku_View_PyType(&Haiku_View_PyType);
	if (PyType_Ready(&Haiku_View_PyType) < 0)
		return;
	Py_INCREF(&Haiku_View_PyType);
	PyModule_AddObject(Haiku_module, "View", (PyObject*)&Haiku_View_PyType);
	
	// Haiku.Box: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_Box_PyType(&Haiku_Box_PyType);
	if (PyType_Ready(&Haiku_Box_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Box_PyType);
	PyModule_AddObject(Haiku_module, "Box", (PyObject*)&Haiku_Box_PyType);
	
	// Haiku.Control: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	//Py_INCREF(&Haiku_Invoker_PyType);	// base class
	init_Haiku_Control_PyType(&Haiku_Control_PyType);
	if (PyType_Ready(&Haiku_Control_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Control_PyType);
	PyModule_AddObject(Haiku_module, "Control", (PyObject*)&Haiku_Control_PyType);
	
	// Haiku.Button: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_Button_PyType(&Haiku_Button_PyType);
	if (PyType_Ready(&Haiku_Button_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Button_PyType);
	PyModule_AddObject(Haiku_module, "Button", (PyObject*)&Haiku_Button_PyType);
	
	// Haiku.CheckBox: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_CheckBox_PyType(&Haiku_CheckBox_PyType);
	if (PyType_Ready(&Haiku_CheckBox_PyType) < 0)
		return;
	Py_INCREF(&Haiku_CheckBox_PyType);
	PyModule_AddObject(Haiku_module, "CheckBox", (PyObject*)&Haiku_CheckBox_PyType);
	
	// Haiku.ColorControl: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_ColorControl_PyType(&Haiku_ColorControl_PyType);
	if (PyType_Ready(&Haiku_ColorControl_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ColorControl_PyType);
	PyModule_AddObject(Haiku_module, "ColorControl", (PyObject*)&Haiku_ColorControl_PyType);
	
	// Haiku.PictureButton: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_PictureButton_PyType(&Haiku_PictureButton_PyType);
	if (PyType_Ready(&Haiku_PictureButton_PyType) < 0)
		return;
	Py_INCREF(&Haiku_PictureButton_PyType);
	PyModule_AddObject(Haiku_module, "PictureButton", (PyObject*)&Haiku_PictureButton_PyType);
	
	// Haiku.RadioButton: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_RadioButton_PyType(&Haiku_RadioButton_PyType);
	if (PyType_Ready(&Haiku_RadioButton_PyType) < 0)
		return;
	Py_INCREF(&Haiku_RadioButton_PyType);
	PyModule_AddObject(Haiku_module, "RadioButton", (PyObject*)&Haiku_RadioButton_PyType);
	
	// Haiku.Slider: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_Slider_PyType(&Haiku_Slider_PyType);
	if (PyType_Ready(&Haiku_Slider_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Slider_PyType);
	PyModule_AddObject(Haiku_module, "Slider", (PyObject*)&Haiku_Slider_PyType);
	
	// Haiku.TextControl: class
	//Py_INCREF(&Haiku_Control_PyType);	// base class
	init_Haiku_TextControl_PyType(&Haiku_TextControl_PyType);
	if (PyType_Ready(&Haiku_TextControl_PyType) < 0)
		return;
	Py_INCREF(&Haiku_TextControl_PyType);
	PyModule_AddObject(Haiku_module, "TextControl", (PyObject*)&Haiku_TextControl_PyType);
	
	// Haiku.ListView: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	//Py_INCREF(&Haiku_Invoker_PyType);	// base class
	init_Haiku_ListView_PyType(&Haiku_ListView_PyType);
	if (PyType_Ready(&Haiku_ListView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ListView_PyType);
	PyModule_AddObject(Haiku_module, "ListView", (PyObject*)&Haiku_ListView_PyType);
	
	// Haiku.OutlineListView: class
	//Py_INCREF(&Haiku_ListView_PyType);	// base class
	init_Haiku_OutlineListView_PyType(&Haiku_OutlineListView_PyType);
	if (PyType_Ready(&Haiku_OutlineListView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_OutlineListView_PyType);
	PyModule_AddObject(Haiku_module, "OutlineListView", (PyObject*)&Haiku_OutlineListView_PyType);
	
	// Haiku.Menu: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_Menu_PyType(&Haiku_Menu_PyType);
	if (PyType_Ready(&Haiku_Menu_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Menu_PyType);
	PyModule_AddObject(Haiku_module, "Menu", (PyObject*)&Haiku_Menu_PyType);
	
	// Haiku.menu_info: class
	init_Haiku_menu_info_PyType(&Haiku_menu_info_PyType);
	if (PyType_Ready(&Haiku_menu_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_menu_info_PyType);
	PyModule_AddObject(Haiku_module, "menu_info", (PyObject*)&Haiku_menu_info_PyType);
	
	// Haiku.MenuBar: class
	//Py_INCREF(&Haiku_Menu_PyType);	// base class
	init_Haiku_MenuBar_PyType(&Haiku_MenuBar_PyType);
	if (PyType_Ready(&Haiku_MenuBar_PyType) < 0)
		return;
	Py_INCREF(&Haiku_MenuBar_PyType);
	PyModule_AddObject(Haiku_module, "MenuBar", (PyObject*)&Haiku_MenuBar_PyType);
	
	// Haiku.PopUpMenu: class
	//Py_INCREF(&Haiku_Menu_PyType);	// base class
	init_Haiku_PopUpMenu_PyType(&Haiku_PopUpMenu_PyType);
	if (PyType_Ready(&Haiku_PopUpMenu_PyType) < 0)
		return;
	Py_INCREF(&Haiku_PopUpMenu_PyType);
	PyModule_AddObject(Haiku_module, "PopUpMenu", (PyObject*)&Haiku_PopUpMenu_PyType);
	
	// Haiku.MenuField: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_MenuField_PyType(&Haiku_MenuField_PyType);
	if (PyType_Ready(&Haiku_MenuField_PyType) < 0)
		return;
	Py_INCREF(&Haiku_MenuField_PyType);
	PyModule_AddObject(Haiku_module, "MenuField", (PyObject*)&Haiku_MenuField_PyType);
	
	// Haiku.ScrollBar: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_ScrollBar_PyType(&Haiku_ScrollBar_PyType);
	if (PyType_Ready(&Haiku_ScrollBar_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ScrollBar_PyType);
	PyModule_AddObject(Haiku_module, "ScrollBar", (PyObject*)&Haiku_ScrollBar_PyType);
	
	// Haiku.ScrollView: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_ScrollView_PyType(&Haiku_ScrollView_PyType);
	if (PyType_Ready(&Haiku_ScrollView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ScrollView_PyType);
	PyModule_AddObject(Haiku_module, "ScrollView", (PyObject*)&Haiku_ScrollView_PyType);
	
	// Haiku.StatusBar: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_StatusBar_PyType(&Haiku_StatusBar_PyType);
	if (PyType_Ready(&Haiku_StatusBar_PyType) < 0)
		return;
	Py_INCREF(&Haiku_StatusBar_PyType);
	PyModule_AddObject(Haiku_module, "StatusBar", (PyObject*)&Haiku_StatusBar_PyType);
	
	// Haiku.StringView: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_StringView_PyType(&Haiku_StringView_PyType);
	if (PyType_Ready(&Haiku_StringView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_StringView_PyType);
	PyModule_AddObject(Haiku_module, "StringView", (PyObject*)&Haiku_StringView_PyType);
	
	// Haiku.TabView: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_TabView_PyType(&Haiku_TabView_PyType);
	if (PyType_Ready(&Haiku_TabView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_TabView_PyType);
	PyModule_AddObject(Haiku_module, "TabView", (PyObject*)&Haiku_TabView_PyType);
	
	// Haiku.Tab: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Tab_PyType(&Haiku_Tab_PyType);
	if (PyType_Ready(&Haiku_Tab_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Tab_PyType);
	PyModule_AddObject(Haiku_module, "Tab", (PyObject*)&Haiku_Tab_PyType);
	
	// Haiku.TextView: class
	//Py_INCREF(&Haiku_View_PyType);	// base class
	init_Haiku_TextView_PyType(&Haiku_TextView_PyType);
	if (PyType_Ready(&Haiku_TextView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_TextView_PyType);
	PyModule_AddObject(Haiku_module, "TextView", (PyObject*)&Haiku_TextView_PyType);
	
	// Haiku.CustomTextView: class
	//Py_INCREF(&Haiku_TextView_PyType);	// base class
	init_Haiku_CustomTextView_PyType(&Haiku_CustomTextView_PyType);
	if (PyType_Ready(&Haiku_CustomTextView_PyType) < 0)
		return;
	Py_INCREF(&Haiku_CustomTextView_PyType);
	PyModule_AddObject(Haiku_module, "CustomTextView", (PyObject*)&Haiku_CustomTextView_PyType);
	
	// Haiku.text_run: class
	init_Haiku_text_run_PyType(&Haiku_text_run_PyType);
	if (PyType_Ready(&Haiku_text_run_PyType) < 0)
		return;
	Py_INCREF(&Haiku_text_run_PyType);
	PyModule_AddObject(Haiku_module, "text_run", (PyObject*)&Haiku_text_run_PyType);
	
	// Haiku.text_run_array: class
	init_Haiku_text_run_array_PyType(&Haiku_text_run_array_PyType);
	if (PyType_Ready(&Haiku_text_run_array_PyType) < 0)
		return;
	Py_INCREF(&Haiku_text_run_array_PyType);
	PyModule_AddObject(Haiku_module, "text_run_array", (PyObject*)&Haiku_text_run_array_PyType);
	
	// Haiku.MenuItem: class
	//Py_INCREF(&Haiku_Invoker_PyType);	// base class
	init_Haiku_MenuItem_PyType(&Haiku_MenuItem_PyType);
	if (PyType_Ready(&Haiku_MenuItem_PyType) < 0)
		return;
	Py_INCREF(&Haiku_MenuItem_PyType);
	PyModule_AddObject(Haiku_module, "MenuItem", (PyObject*)&Haiku_MenuItem_PyType);
	
	// Haiku.SeparatorItem: class
	//Py_INCREF(&Haiku_MenuItem_PyType);	// base class
	init_Haiku_SeparatorItem_PyType(&Haiku_SeparatorItem_PyType);
	if (PyType_Ready(&Haiku_SeparatorItem_PyType) < 0)
		return;
	Py_INCREF(&Haiku_SeparatorItem_PyType);
	PyModule_AddObject(Haiku_module, "SeparatorItem", (PyObject*)&Haiku_SeparatorItem_PyType);
	
	// Haiku.ListItem: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_ListItem_PyType(&Haiku_ListItem_PyType);
	if (PyType_Ready(&Haiku_ListItem_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ListItem_PyType);
	PyModule_AddObject(Haiku_module, "ListItem", (PyObject*)&Haiku_ListItem_PyType);
	
	// Haiku.StringItem: class
	//Py_INCREF(&Haiku_ListItem_PyType);	// base class
	init_Haiku_StringItem_PyType(&Haiku_StringItem_PyType);
	if (PyType_Ready(&Haiku_StringItem_PyType) < 0)
		return;
	Py_INCREF(&Haiku_StringItem_PyType);
	PyModule_AddObject(Haiku_module, "StringItem", (PyObject*)&Haiku_StringItem_PyType);
	
	// Haiku.Font: class
	init_Haiku_Font_PyType(&Haiku_Font_PyType);
	if (PyType_Ready(&Haiku_Font_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Font_PyType);
	PyModule_AddObject(Haiku_module, "Font", (PyObject*)&Haiku_Font_PyType);
	
	// Haiku.unicode_block: class
	init_Haiku_unicode_block_PyType(&Haiku_unicode_block_PyType);
	if (PyType_Ready(&Haiku_unicode_block_PyType) < 0)
		return;
	Py_INCREF(&Haiku_unicode_block_PyType);
	PyModule_AddObject(Haiku_module, "unicode_block", (PyObject*)&Haiku_unicode_block_PyType);
	
	// Haiku.edge_info: class
	init_Haiku_edge_info_PyType(&Haiku_edge_info_PyType);
	if (PyType_Ready(&Haiku_edge_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_edge_info_PyType);
	PyModule_AddObject(Haiku_module, "edge_info", (PyObject*)&Haiku_edge_info_PyType);
	
	// Haiku.font_height: class
	init_Haiku_font_height_PyType(&Haiku_font_height_PyType);
	if (PyType_Ready(&Haiku_font_height_PyType) < 0)
		return;
	Py_INCREF(&Haiku_font_height_PyType);
	PyModule_AddObject(Haiku_module, "font_height", (PyObject*)&Haiku_font_height_PyType);
	
	// Haiku.escapement_delta: class
	init_Haiku_escapement_delta_PyType(&Haiku_escapement_delta_PyType);
	if (PyType_Ready(&Haiku_escapement_delta_PyType) < 0)
		return;
	Py_INCREF(&Haiku_escapement_delta_PyType);
	PyModule_AddObject(Haiku_module, "escapement_delta", (PyObject*)&Haiku_escapement_delta_PyType);
	
	// Haiku.font_cache_info: class
	init_Haiku_font_cache_info_PyType(&Haiku_font_cache_info_PyType);
	if (PyType_Ready(&Haiku_font_cache_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_font_cache_info_PyType);
	PyModule_AddObject(Haiku_module, "font_cache_info", (PyObject*)&Haiku_font_cache_info_PyType);
	
	// Haiku.tuned_font_info: class
	init_Haiku_tuned_font_info_PyType(&Haiku_tuned_font_info_PyType);
	if (PyType_Ready(&Haiku_tuned_font_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_tuned_font_info_PyType);
	PyModule_AddObject(Haiku_module, "tuned_font_info", (PyObject*)&Haiku_tuned_font_info_PyType);
	
	// Haiku.Picture: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Picture_PyType(&Haiku_Picture_PyType);
	if (PyType_Ready(&Haiku_Picture_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Picture_PyType);
	PyModule_AddObject(Haiku_module, "Picture", (PyObject*)&Haiku_Picture_PyType);
	
	// Haiku.Point: class
	init_Haiku_Point_PyType(&Haiku_Point_PyType);
	if (PyType_Ready(&Haiku_Point_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Point_PyType);
	PyModule_AddObject(Haiku_module, "Point", (PyObject*)&Haiku_Point_PyType);
	
	// Haiku.Polygon: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Polygon_PyType(&Haiku_Polygon_PyType);
	if (PyType_Ready(&Haiku_Polygon_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Polygon_PyType);
	PyModule_AddObject(Haiku_module, "Polygon", (PyObject*)&Haiku_Polygon_PyType);
	
	// Haiku.Rect: class
	init_Haiku_Rect_PyType(&Haiku_Rect_PyType);
	if (PyType_Ready(&Haiku_Rect_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Rect_PyType);
	PyModule_AddObject(Haiku_module, "Rect", (PyObject*)&Haiku_Rect_PyType);
	
	// Haiku.Screen: class
	init_Haiku_Screen_PyType(&Haiku_Screen_PyType);
	if (PyType_Ready(&Haiku_Screen_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Screen_PyType);
	PyModule_AddObject(Haiku_module, "Screen", (PyObject*)&Haiku_Screen_PyType);
	
	// Haiku.Shape: class
	//Py_INCREF(&Haiku_Archivable_PyType);	// base class
	init_Haiku_Shape_PyType(&Haiku_Shape_PyType);
	if (PyType_Ready(&Haiku_Shape_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Shape_PyType);
	PyModule_AddObject(Haiku_module, "Shape", (PyObject*)&Haiku_Shape_PyType);
	
	// Haiku.ShapeIterator: class
	init_Haiku_ShapeIterator_PyType(&Haiku_ShapeIterator_PyType);
	if (PyType_Ready(&Haiku_ShapeIterator_PyType) < 0)
		return;
	Py_INCREF(&Haiku_ShapeIterator_PyType);
	PyModule_AddObject(Haiku_module, "ShapeIterator", (PyObject*)&Haiku_ShapeIterator_PyType);
	
	// Haiku.key_info: class
	init_Haiku_key_info_PyType(&Haiku_key_info_PyType);
	if (PyType_Ready(&Haiku_key_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_key_info_PyType);
	PyModule_AddObject(Haiku_module, "key_info", (PyObject*)&Haiku_key_info_PyType);
	
	// Haiku.key_map: class
	init_Haiku_key_map_PyType(&Haiku_key_map_PyType);
	if (PyType_Ready(&Haiku_key_map_PyType) < 0)
		return;
	Py_INCREF(&Haiku_key_map_PyType);
	PyModule_AddObject(Haiku_module, "key_map", (PyObject*)&Haiku_key_map_PyType);
	
	// Haiku.mouse_map: class
	init_Haiku_mouse_map_PyType(&Haiku_mouse_map_PyType);
	if (PyType_Ready(&Haiku_mouse_map_PyType) < 0)
		return;
	Py_INCREF(&Haiku_mouse_map_PyType);
	PyModule_AddObject(Haiku_module, "mouse_map", (PyObject*)&Haiku_mouse_map_PyType);
	
	// Haiku.scroll_bar_info: class
	init_Haiku_scroll_bar_info_PyType(&Haiku_scroll_bar_info_PyType);
	if (PyType_Ready(&Haiku_scroll_bar_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_scroll_bar_info_PyType);
	PyModule_AddObject(Haiku_module, "scroll_bar_info", (PyObject*)&Haiku_scroll_bar_info_PyType);
	
	// Haiku.pattern: class
	init_Haiku_pattern_PyType(&Haiku_pattern_PyType);
	if (PyType_Ready(&Haiku_pattern_PyType) < 0)
		return;
	Py_INCREF(&Haiku_pattern_PyType);
	PyModule_AddObject(Haiku_module, "pattern", (PyObject*)&Haiku_pattern_PyType);
	
	// Haiku.rgb_color: class
	init_Haiku_rgb_color_PyType(&Haiku_rgb_color_PyType);
	if (PyType_Ready(&Haiku_rgb_color_PyType) < 0)
		return;
	Py_INCREF(&Haiku_rgb_color_PyType);
	PyModule_AddObject(Haiku_module, "rgb_color", (PyObject*)&Haiku_rgb_color_PyType);
	
	// Haiku.color_map: class
	init_Haiku_color_map_PyType(&Haiku_color_map_PyType);
	if (PyType_Ready(&Haiku_color_map_PyType) < 0)
		return;
	Py_INCREF(&Haiku_color_map_PyType);
	PyModule_AddObject(Haiku_module, "color_map", (PyObject*)&Haiku_color_map_PyType);
	
	// Haiku.overlay_rect_limits: class
	init_Haiku_overlay_rect_limits_PyType(&Haiku_overlay_rect_limits_PyType);
	if (PyType_Ready(&Haiku_overlay_rect_limits_PyType) < 0)
		return;
	Py_INCREF(&Haiku_overlay_rect_limits_PyType);
	PyModule_AddObject(Haiku_module, "overlay_rect_limits", (PyObject*)&Haiku_overlay_rect_limits_PyType);
	
	// Haiku.overlay_restrictions: class
	init_Haiku_overlay_restrictions_PyType(&Haiku_overlay_restrictions_PyType);
	if (PyType_Ready(&Haiku_overlay_restrictions_PyType) < 0)
		return;
	Py_INCREF(&Haiku_overlay_restrictions_PyType);
	PyModule_AddObject(Haiku_module, "overlay_restrictions", (PyObject*)&Haiku_overlay_restrictions_PyType);
	
	// Haiku.screen_id: class
	init_Haiku_screen_id_PyType(&Haiku_screen_id_PyType);
	if (PyType_Ready(&Haiku_screen_id_PyType) < 0)
		return;
	Py_INCREF(&Haiku_screen_id_PyType);
	PyModule_AddObject(Haiku_module, "screen_id", (PyObject*)&Haiku_screen_id_PyType);
	
	// Haiku.EntryList: class
	init_Haiku_EntryList_PyType(&Haiku_EntryList_PyType);
	if (PyType_Ready(&Haiku_EntryList_PyType) < 0)
		return;
	Py_INCREF(&Haiku_EntryList_PyType);
	PyModule_AddObject(Haiku_module, "EntryList", (PyObject*)&Haiku_EntryList_PyType);
	
	// Haiku.Query: class
	//Py_INCREF(&Haiku_EntryList_PyType);	// base class
	init_Haiku_Query_PyType(&Haiku_Query_PyType);
	if (PyType_Ready(&Haiku_Query_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Query_PyType);
	PyModule_AddObject(Haiku_module, "Query", (PyObject*)&Haiku_Query_PyType);
	
	// Haiku.MimeType: class
	init_Haiku_MimeType_PyType(&Haiku_MimeType_PyType);
	if (PyType_Ready(&Haiku_MimeType_PyType) < 0)
		return;
	Py_INCREF(&Haiku_MimeType_PyType);
	PyModule_AddObject(Haiku_module, "MimeType", (PyObject*)&Haiku_MimeType_PyType);
	
	// Haiku.NodeInfo: class
	init_Haiku_NodeInfo_PyType(&Haiku_NodeInfo_PyType);
	if (PyType_Ready(&Haiku_NodeInfo_PyType) < 0)
		return;
	Py_INCREF(&Haiku_NodeInfo_PyType);
	PyModule_AddObject(Haiku_module, "NodeInfo", (PyObject*)&Haiku_NodeInfo_PyType);
	
	// Haiku.Path: class
	init_Haiku_Path_PyType(&Haiku_Path_PyType);
	if (PyType_Ready(&Haiku_Path_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Path_PyType);
	PyModule_AddObject(Haiku_module, "Path", (PyObject*)&Haiku_Path_PyType);
	
	// Haiku.Statable: class
	init_Haiku_Statable_PyType(&Haiku_Statable_PyType);
	if (PyType_Ready(&Haiku_Statable_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Statable_PyType);
	PyModule_AddObject(Haiku_module, "Statable", (PyObject*)&Haiku_Statable_PyType);
	
	// Haiku.Entry: class
	//Py_INCREF(&Haiku_Statable_PyType);	// base class
	init_Haiku_Entry_PyType(&Haiku_Entry_PyType);
	if (PyType_Ready(&Haiku_Entry_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Entry_PyType);
	PyModule_AddObject(Haiku_module, "Entry", (PyObject*)&Haiku_Entry_PyType);
	
	// Haiku.entry_ref: class
	init_Haiku_entry_ref_PyType(&Haiku_entry_ref_PyType);
	if (PyType_Ready(&Haiku_entry_ref_PyType) < 0)
		return;
	Py_INCREF(&Haiku_entry_ref_PyType);
	PyModule_AddObject(Haiku_module, "entry_ref", (PyObject*)&Haiku_entry_ref_PyType);
	
	// Haiku.Node: class
	//Py_INCREF(&Haiku_Statable_PyType);	// base class
	init_Haiku_Node_PyType(&Haiku_Node_PyType);
	if (PyType_Ready(&Haiku_Node_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Node_PyType);
	PyModule_AddObject(Haiku_module, "Node", (PyObject*)&Haiku_Node_PyType);
	
	// Haiku.node_ref: class
	init_Haiku_node_ref_PyType(&Haiku_node_ref_PyType);
	if (PyType_Ready(&Haiku_node_ref_PyType) < 0)
		return;
	Py_INCREF(&Haiku_node_ref_PyType);
	PyModule_AddObject(Haiku_module, "node_ref", (PyObject*)&Haiku_node_ref_PyType);
	
	// Haiku.Volume: class
	init_Haiku_Volume_PyType(&Haiku_Volume_PyType);
	if (PyType_Ready(&Haiku_Volume_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Volume_PyType);
	PyModule_AddObject(Haiku_module, "Volume", (PyObject*)&Haiku_Volume_PyType);
	
	// Haiku.VolumeRoster: class
	init_Haiku_VolumeRoster_PyType(&Haiku_VolumeRoster_PyType);
	if (PyType_Ready(&Haiku_VolumeRoster_PyType) < 0)
		return;
	Py_INCREF(&Haiku_VolumeRoster_PyType);
	PyModule_AddObject(Haiku_module, "VolumeRoster", (PyObject*)&Haiku_VolumeRoster_PyType);
	
	// Haiku.dirent: class
	init_Haiku_dirent_PyType(&Haiku_dirent_PyType);
	if (PyType_Ready(&Haiku_dirent_PyType) < 0)
		return;
	Py_INCREF(&Haiku_dirent_PyType);
	PyModule_AddObject(Haiku_module, "dirent", (PyObject*)&Haiku_dirent_PyType);
	
	// Haiku.stat_beos: class
	init_Haiku_stat_beos_PyType(&Haiku_stat_beos_PyType);
	if (PyType_Ready(&Haiku_stat_beos_PyType) < 0)
		return;
	Py_INCREF(&Haiku_stat_beos_PyType);
	PyModule_AddObject(Haiku_module, "stat_beos", (PyObject*)&Haiku_stat_beos_PyType);
	
	// Haiku.stat_beos_time: class
	init_Haiku_stat_beos_time_PyType(&Haiku_stat_beos_time_PyType);
	if (PyType_Ready(&Haiku_stat_beos_time_PyType) < 0)
		return;
	Py_INCREF(&Haiku_stat_beos_time_PyType);
	PyModule_AddObject(Haiku_module, "stat_beos_time", (PyObject*)&Haiku_stat_beos_time_PyType);
	
	// Haiku.stat: class
	init_Haiku_stat_PyType(&Haiku_stat_PyType);
	if (PyType_Ready(&Haiku_stat_PyType) < 0)
		return;
	Py_INCREF(&Haiku_stat_PyType);
	PyModule_AddObject(Haiku_module, "stat", (PyObject*)&Haiku_stat_PyType);
	
	// Haiku.timespec: class
	init_Haiku_timespec_PyType(&Haiku_timespec_PyType);
	if (PyType_Ready(&Haiku_timespec_PyType) < 0)
		return;
	Py_INCREF(&Haiku_timespec_PyType);
	PyModule_AddObject(Haiku_module, "timespec", (PyObject*)&Haiku_timespec_PyType);
	
	// Haiku.attr_info: class
	init_Haiku_attr_info_PyType(&Haiku_attr_info_PyType);
	if (PyType_Ready(&Haiku_attr_info_PyType) < 0)
		return;
	Py_INCREF(&Haiku_attr_info_PyType);
	PyModule_AddObject(Haiku_module, "attr_info", (PyObject*)&Haiku_attr_info_PyType);
	
	// Haiku.Archivable: class
	init_Haiku_Archivable_PyType(&Haiku_Archivable_PyType);
	if (PyType_Ready(&Haiku_Archivable_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Archivable_PyType);
	PyModule_AddObject(Haiku_module, "Archivable", (PyObject*)&Haiku_Archivable_PyType);
	
	// Haiku.Archiver: class
	init_Haiku_Archiver_PyType(&Haiku_Archiver_PyType);
	if (PyType_Ready(&Haiku_Archiver_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Archiver_PyType);
	PyModule_AddObject(Haiku_module, "Archiver", (PyObject*)&Haiku_Archiver_PyType);
	
	// Haiku.Unarchiver: class
	init_Haiku_Unarchiver_PyType(&Haiku_Unarchiver_PyType);
	if (PyType_Ready(&Haiku_Unarchiver_PyType) < 0)
		return;
	Py_INCREF(&Haiku_Unarchiver_PyType);
	PyModule_AddObject(Haiku_module, "Unarchiver", (PyObject*)&Haiku_Unarchiver_PyType);
	
	// Handler: constants (in their own module)
	Haiku_HandlerConstants_module = Py_InitModule("Haiku.HandlerConstants", Haiku_HandlerConstants_PyMethods);
	if (Haiku_HandlerConstants_module == NULL)
		return;
	Py_INCREF(Haiku_HandlerConstants_module);
	PyModule_AddObject(Haiku_module, "HandlerConstants", Haiku_HandlerConstants_module);
	
	PyObject* Haiku_Handler_B_OBSERVE_WHAT_CHANGE;
	PyObject* Haiku_Handler_B_OBSERVE_ORIGINAL_WHAT;
	PyObject* Haiku_Handler_B_OBSERVER_OBSERVE_ALL;

	Haiku_Handler_B_OBSERVE_WHAT_CHANGE = Py_BuildValue("i", B_OBSERVE_WHAT_CHANGE);
	Py_INCREF(Haiku_Handler_B_OBSERVE_WHAT_CHANGE);
	PyModule_AddObject(Haiku_HandlerConstants_module, "B_OBSERVE_WHAT_CHANGE", Haiku_Handler_B_OBSERVE_WHAT_CHANGE);
	
	Haiku_Handler_B_OBSERVE_ORIGINAL_WHAT = Py_BuildValue("i", B_OBSERVE_ORIGINAL_WHAT);
	Py_INCREF(Haiku_Handler_B_OBSERVE_ORIGINAL_WHAT);
	PyModule_AddObject(Haiku_HandlerConstants_module, "B_OBSERVE_ORIGINAL_WHAT", Haiku_Handler_B_OBSERVE_ORIGINAL_WHAT);
	
	Haiku_Handler_B_OBSERVER_OBSERVE_ALL = Py_BuildValue("k", B_OBSERVER_OBSERVE_ALL);
	Py_INCREF(Haiku_Handler_B_OBSERVER_OBSERVE_ALL);
	PyModule_AddObject(Haiku_HandlerConstants_module, "B_OBSERVER_OBSERVE_ALL", Haiku_Handler_B_OBSERVER_OBSERVE_ALL);
	
	// Looper: constants (in their own module)
	Haiku_LooperConstants_module = Py_InitModule("Haiku.LooperConstants", Haiku_LooperConstants_PyMethods);
	if (Haiku_LooperConstants_module == NULL)
		return;
	Py_INCREF(Haiku_LooperConstants_module);
	PyModule_AddObject(Haiku_module, "LooperConstants", Haiku_LooperConstants_module);
	
	PyObject* Haiku_Looper_B_LOOPER_PORT_DEFAULT_CAPACITY;

	Haiku_Looper_B_LOOPER_PORT_DEFAULT_CAPACITY = Py_BuildValue("i", B_LOOPER_PORT_DEFAULT_CAPACITY);
	Py_INCREF(Haiku_Looper_B_LOOPER_PORT_DEFAULT_CAPACITY);
	PyModule_AddObject(Haiku_LooperConstants_module, "B_LOOPER_PORT_DEFAULT_CAPACITY", Haiku_Looper_B_LOOPER_PORT_DEFAULT_CAPACITY);
	
	// Clipboard: constants (in their own module)
	Haiku_ClipboardConstants_module = Py_InitModule("Haiku.ClipboardConstants", Haiku_ClipboardConstants_PyMethods);
	if (Haiku_ClipboardConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ClipboardConstants_module);
	PyModule_AddObject(Haiku_module, "ClipboardConstants", Haiku_ClipboardConstants_module);
	
	PyObject* Haiku_Clipboard_B_CLIPBOARD_CHANGED;

	Haiku_Clipboard_B_CLIPBOARD_CHANGED = Py_BuildValue("i", B_CLIPBOARD_CHANGED);
	Py_INCREF(Haiku_Clipboard_B_CLIPBOARD_CHANGED);
	PyModule_AddObject(Haiku_ClipboardConstants_module, "B_CLIPBOARD_CHANGED", Haiku_Clipboard_B_CLIPBOARD_CHANGED);
	
	// Cursor: constants (in their own module)
	Haiku_CursorConstants_module = Py_InitModule("Haiku.CursorConstants", Haiku_CursorConstants_PyMethods);
	if (Haiku_CursorConstants_module == NULL)
		return;
	Py_INCREF(Haiku_CursorConstants_module);
	PyModule_AddObject(Haiku_module, "CursorConstants", Haiku_CursorConstants_module);
	
	PyObject* Haiku_Cursor_B_CURSOR_ID_SYSTEM_DEFAULT;
	PyObject* Haiku_Cursor_B_CURSOR_ID_CONTEXT_MENU;
	PyObject* Haiku_Cursor_B_CURSOR_ID_COPY;
	PyObject* Haiku_Cursor_B_CURSOR_ID_CREATE_LINK;
	PyObject* Haiku_Cursor_B_CURSOR_ID_CROSS_HAIR;
	PyObject* Haiku_Cursor_B_CURSOR_ID_FOLLOW_LINK;
	PyObject* Haiku_Cursor_B_CURSOR_ID_GRAB;
	PyObject* Haiku_Cursor_B_CURSOR_ID_GRABBING;
	PyObject* Haiku_Cursor_B_CURSOR_ID_HELP;
	PyObject* Haiku_Cursor_B_CURSOR_ID_I_BEAM;
	PyObject* Haiku_Cursor_B_CURSOR_ID_I_BEAM_HORIZONTAL;
	PyObject* Haiku_Cursor_B_CURSOR_ID_MOVE;
	PyObject* Haiku_Cursor_B_CURSOR_ID_NO_CURSOR;
	PyObject* Haiku_Cursor_B_CURSOR_ID_NOT_ALLOWED;
	PyObject* Haiku_Cursor_B_CURSOR_ID_PROGRESS;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_WEST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_EAST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_WEST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_SOUTH;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST_WEST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST;
	PyObject* Haiku_Cursor_B_CURSOR_ID_ZOOM_IN;
	PyObject* Haiku_Cursor_B_CURSOR_ID_ZOOM_OUT;

	Haiku_Cursor_B_CURSOR_ID_SYSTEM_DEFAULT = Py_BuildValue("i", B_CURSOR_ID_SYSTEM_DEFAULT);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_SYSTEM_DEFAULT);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_SYSTEM_DEFAULT", Haiku_Cursor_B_CURSOR_ID_SYSTEM_DEFAULT);
	
	Haiku_Cursor_B_CURSOR_ID_CONTEXT_MENU = Py_BuildValue("i", B_CURSOR_ID_CONTEXT_MENU);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_CONTEXT_MENU);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_CONTEXT_MENU", Haiku_Cursor_B_CURSOR_ID_CONTEXT_MENU);
	
	Haiku_Cursor_B_CURSOR_ID_COPY = Py_BuildValue("i", B_CURSOR_ID_COPY);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_COPY);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_COPY", Haiku_Cursor_B_CURSOR_ID_COPY);
	
	Haiku_Cursor_B_CURSOR_ID_CREATE_LINK = Py_BuildValue("i", B_CURSOR_ID_CREATE_LINK);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_CREATE_LINK);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_CREATE_LINK", Haiku_Cursor_B_CURSOR_ID_CREATE_LINK);
	
	Haiku_Cursor_B_CURSOR_ID_CROSS_HAIR = Py_BuildValue("i", B_CURSOR_ID_CROSS_HAIR);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_CROSS_HAIR);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_CROSS_HAIR", Haiku_Cursor_B_CURSOR_ID_CROSS_HAIR);
	
	Haiku_Cursor_B_CURSOR_ID_FOLLOW_LINK = Py_BuildValue("i", B_CURSOR_ID_FOLLOW_LINK);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_FOLLOW_LINK);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_FOLLOW_LINK", Haiku_Cursor_B_CURSOR_ID_FOLLOW_LINK);
	
	Haiku_Cursor_B_CURSOR_ID_GRAB = Py_BuildValue("i", B_CURSOR_ID_GRAB);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_GRAB);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_GRAB", Haiku_Cursor_B_CURSOR_ID_GRAB);
	
	Haiku_Cursor_B_CURSOR_ID_GRABBING = Py_BuildValue("i", B_CURSOR_ID_GRABBING);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_GRABBING);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_GRABBING", Haiku_Cursor_B_CURSOR_ID_GRABBING);
	
	Haiku_Cursor_B_CURSOR_ID_HELP = Py_BuildValue("i", B_CURSOR_ID_HELP);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_HELP);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_HELP", Haiku_Cursor_B_CURSOR_ID_HELP);
	
	Haiku_Cursor_B_CURSOR_ID_I_BEAM = Py_BuildValue("i", B_CURSOR_ID_I_BEAM);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_I_BEAM);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_I_BEAM", Haiku_Cursor_B_CURSOR_ID_I_BEAM);
	
	Haiku_Cursor_B_CURSOR_ID_I_BEAM_HORIZONTAL = Py_BuildValue("i", B_CURSOR_ID_I_BEAM_HORIZONTAL);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_I_BEAM_HORIZONTAL);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_I_BEAM_HORIZONTAL", Haiku_Cursor_B_CURSOR_ID_I_BEAM_HORIZONTAL);
	
	Haiku_Cursor_B_CURSOR_ID_MOVE = Py_BuildValue("i", B_CURSOR_ID_MOVE);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_MOVE);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_MOVE", Haiku_Cursor_B_CURSOR_ID_MOVE);
	
	Haiku_Cursor_B_CURSOR_ID_NO_CURSOR = Py_BuildValue("i", B_CURSOR_ID_NO_CURSOR);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_NO_CURSOR);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_NO_CURSOR", Haiku_Cursor_B_CURSOR_ID_NO_CURSOR);
	
	Haiku_Cursor_B_CURSOR_ID_NOT_ALLOWED = Py_BuildValue("i", B_CURSOR_ID_NOT_ALLOWED);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_NOT_ALLOWED);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_NOT_ALLOWED", Haiku_Cursor_B_CURSOR_ID_NOT_ALLOWED);
	
	Haiku_Cursor_B_CURSOR_ID_PROGRESS = Py_BuildValue("i", B_CURSOR_ID_PROGRESS);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_PROGRESS);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_PROGRESS", Haiku_Cursor_B_CURSOR_ID_PROGRESS);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_EAST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_EAST", Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH = Py_BuildValue("i", B_CURSOR_ID_RESIZE_SOUTH);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_SOUTH", Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_WEST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_WEST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_WEST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_WEST", Haiku_Cursor_B_CURSOR_ID_RESIZE_WEST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH_EAST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH_EAST", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH_WEST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH_WEST", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_EAST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_SOUTH_EAST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_EAST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_SOUTH_EAST", Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_EAST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_WEST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_SOUTH_WEST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_WEST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_SOUTH_WEST", Haiku_Cursor_B_CURSOR_ID_RESIZE_SOUTH_WEST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_SOUTH = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH_SOUTH);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_SOUTH);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH_SOUTH", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_SOUTH);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST_WEST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_EAST_WEST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST_WEST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_EAST_WEST", Haiku_Cursor_B_CURSOR_ID_RESIZE_EAST_WEST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_EAST_SOUTH_WEST);
	
	Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST = Py_BuildValue("i", B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST", Haiku_Cursor_B_CURSOR_ID_RESIZE_NORTH_WEST_SOUTH_EAST);
	
	Haiku_Cursor_B_CURSOR_ID_ZOOM_IN = Py_BuildValue("i", B_CURSOR_ID_ZOOM_IN);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_ZOOM_IN);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_ZOOM_IN", Haiku_Cursor_B_CURSOR_ID_ZOOM_IN);
	
	Haiku_Cursor_B_CURSOR_ID_ZOOM_OUT = Py_BuildValue("i", B_CURSOR_ID_ZOOM_OUT);
	Py_INCREF(Haiku_Cursor_B_CURSOR_ID_ZOOM_OUT);
	PyModule_AddObject(Haiku_CursorConstants_module, "B_CURSOR_ID_ZOOM_OUT", Haiku_Cursor_B_CURSOR_ID_ZOOM_OUT);
	
	// Message: constants (in their own module)
	Haiku_MessageConstants_module = Py_InitModule("Haiku.MessageConstants", Haiku_MessageConstants_PyMethods);
	if (Haiku_MessageConstants_module == NULL)
		return;
	Py_INCREF(Haiku_MessageConstants_module);
	PyModule_AddObject(Haiku_module, "MessageConstants", Haiku_MessageConstants_module);
	
	PyObject* Haiku_Message_B_FIELD_NAME_LENGTH;
	PyObject* Haiku_Message_B_PROPERTY_NAME_LENGTH;
	PyObject* Haiku_Message_B_NO_SPECIFIER;
	PyObject* Haiku_Message_B_DIRECT_SPECIFIER;
	PyObject* Haiku_Message_B_INDEX_SPECIFIER;
	PyObject* Haiku_Message_B_REVERSE_INDEX_SPECIFIER;
	PyObject* Haiku_Message_B_RANGE_SPECIFIER;
	PyObject* Haiku_Message_B_REVERSE_RANGE_SPECIFIER;
	PyObject* Haiku_Message_B_NAME_SPECIFIER;
	PyObject* Haiku_Message_B_ID_SPECIFIER;
	PyObject* Haiku_Message_B_SPECIFIERS_END;

	Haiku_Message_B_FIELD_NAME_LENGTH = Py_BuildValue("i", B_FIELD_NAME_LENGTH);
	Py_INCREF(Haiku_Message_B_FIELD_NAME_LENGTH);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_FIELD_NAME_LENGTH", Haiku_Message_B_FIELD_NAME_LENGTH);
	
	Haiku_Message_B_PROPERTY_NAME_LENGTH = Py_BuildValue("i", B_PROPERTY_NAME_LENGTH);
	Py_INCREF(Haiku_Message_B_PROPERTY_NAME_LENGTH);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_PROPERTY_NAME_LENGTH", Haiku_Message_B_PROPERTY_NAME_LENGTH);
	
	Haiku_Message_B_NO_SPECIFIER = Py_BuildValue("i", B_NO_SPECIFIER);
	Py_INCREF(Haiku_Message_B_NO_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_NO_SPECIFIER", Haiku_Message_B_NO_SPECIFIER);
	
	Haiku_Message_B_DIRECT_SPECIFIER = Py_BuildValue("i", B_DIRECT_SPECIFIER);
	Py_INCREF(Haiku_Message_B_DIRECT_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_DIRECT_SPECIFIER", Haiku_Message_B_DIRECT_SPECIFIER);
	
	Haiku_Message_B_INDEX_SPECIFIER = Py_BuildValue("i", B_INDEX_SPECIFIER);
	Py_INCREF(Haiku_Message_B_INDEX_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_INDEX_SPECIFIER", Haiku_Message_B_INDEX_SPECIFIER);
	
	Haiku_Message_B_REVERSE_INDEX_SPECIFIER = Py_BuildValue("i", B_REVERSE_INDEX_SPECIFIER);
	Py_INCREF(Haiku_Message_B_REVERSE_INDEX_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_REVERSE_INDEX_SPECIFIER", Haiku_Message_B_REVERSE_INDEX_SPECIFIER);
	
	Haiku_Message_B_RANGE_SPECIFIER = Py_BuildValue("i", B_RANGE_SPECIFIER);
	Py_INCREF(Haiku_Message_B_RANGE_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_RANGE_SPECIFIER", Haiku_Message_B_RANGE_SPECIFIER);
	
	Haiku_Message_B_REVERSE_RANGE_SPECIFIER = Py_BuildValue("i", B_REVERSE_RANGE_SPECIFIER);
	Py_INCREF(Haiku_Message_B_REVERSE_RANGE_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_REVERSE_RANGE_SPECIFIER", Haiku_Message_B_REVERSE_RANGE_SPECIFIER);
	
	Haiku_Message_B_NAME_SPECIFIER = Py_BuildValue("i", B_NAME_SPECIFIER);
	Py_INCREF(Haiku_Message_B_NAME_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_NAME_SPECIFIER", Haiku_Message_B_NAME_SPECIFIER);
	
	Haiku_Message_B_ID_SPECIFIER = Py_BuildValue("i", B_ID_SPECIFIER);
	Py_INCREF(Haiku_Message_B_ID_SPECIFIER);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_ID_SPECIFIER", Haiku_Message_B_ID_SPECIFIER);
	
	Haiku_Message_B_SPECIFIERS_END = Py_BuildValue("i", B_SPECIFIERS_END);
	Py_INCREF(Haiku_Message_B_SPECIFIERS_END);
	PyModule_AddObject(Haiku_MessageConstants_module, "B_SPECIFIERS_END", Haiku_Message_B_SPECIFIERS_END);
	
	// Window: constants (in their own module)
	Haiku_WindowConstants_module = Py_InitModule("Haiku.WindowConstants", Haiku_WindowConstants_PyMethods);
	if (Haiku_WindowConstants_module == NULL)
		return;
	Py_INCREF(Haiku_WindowConstants_module);
	PyModule_AddObject(Haiku_module, "WindowConstants", Haiku_WindowConstants_module);
	
	PyObject* Haiku_Window_B_UNTYPED_WINDOW;
	PyObject* Haiku_Window_B_TITLED_WINDOW;
	PyObject* Haiku_Window_B_MODAL_WINDOW;
	PyObject* Haiku_Window_B_DOCUMENT_WINDOW;
	PyObject* Haiku_Window_B_BORDERED_WINDOW;
	PyObject* Haiku_Window_B_FLOATING_WINDOW;
	PyObject* Haiku_Window_B_BORDERED_WINDOW_LOOK;
	PyObject* Haiku_Window_B_NO_BORDER_WINDOW_LOOK;
	PyObject* Haiku_Window_B_TITLED_WINDOW_LOOK;
	PyObject* Haiku_Window_B_DOCUMENT_WINDOW_LOOK;
	PyObject* Haiku_Window_B_MODAL_WINDOW_LOOK;
	PyObject* Haiku_Window_B_FLOATING_WINDOW_LOOK;
	PyObject* Haiku_Window_B_NORMAL_WINDOW_FEEL;
	PyObject* Haiku_Window_B_MODAL_SUBSET_WINDOW_FEEL;
	PyObject* Haiku_Window_B_MODAL_APP_WINDOW_FEEL;
	PyObject* Haiku_Window_B_MODAL_ALL_WINDOW_FEEL;
	PyObject* Haiku_Window_B_FLOATING_SUBSET_WINDOW_FEEL;
	PyObject* Haiku_Window_B_FLOATING_APP_WINDOW_FEEL;
	PyObject* Haiku_Window_B_FLOATING_ALL_WINDOW_FEEL;
	PyObject* Haiku_Window_B_BYTE_ALIGNMENT;
	PyObject* Haiku_Window_B_PIXEL_ALIGNMENT;
	PyObject* Haiku_Window_B_NOT_MOVABLE;
	PyObject* Haiku_Window_B_NOT_CLOSABLE;
	PyObject* Haiku_Window_B_NOT_ZOOMABLE;
	PyObject* Haiku_Window_B_NOT_MINIMIZABLE;
	PyObject* Haiku_Window_B_NOT_RESIZABLE;
	PyObject* Haiku_Window_B_NOT_H_RESIZABLE;
	PyObject* Haiku_Window_B_NOT_V_RESIZABLE;
	PyObject* Haiku_Window_B_AVOID_FRONT;
	PyObject* Haiku_Window_B_AVOID_FOCUS;
	PyObject* Haiku_Window_B_WILL_ACCEPT_FIRST_CLICK;
	PyObject* Haiku_Window_B_OUTLINE_RESIZE;
	PyObject* Haiku_Window_B_NO_WORKSPACE_ACTIVATION;
	PyObject* Haiku_Window_B_NOT_ANCHORED_ON_ACTIVATE;
	PyObject* Haiku_Window_B_ASYNCHRONOUS_CONTROLS;
	PyObject* Haiku_Window_B_QUIT_ON_WINDOW_CLOSE;
	PyObject* Haiku_Window_B_SAME_POSITION_IN_ALL_WORKSPACES;
	PyObject* Haiku_Window_B_AUTO_UPDATE_SIZE_LIMITS;
	PyObject* Haiku_Window_B_CLOSE_ON_ESCAPE;
	PyObject* Haiku_Window_B_NO_SERVER_SIDE_WINDOW_MODIFIERS;
	PyObject* Haiku_Window_B_CURRENT_WORKSPACE;
	PyObject* Haiku_Window_B_ALL_WORKSPACES;

	Haiku_Window_B_UNTYPED_WINDOW = Py_BuildValue("i", B_UNTYPED_WINDOW);
	Py_INCREF(Haiku_Window_B_UNTYPED_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_UNTYPED_WINDOW", Haiku_Window_B_UNTYPED_WINDOW);
	
	Haiku_Window_B_TITLED_WINDOW = Py_BuildValue("i", B_TITLED_WINDOW);
	Py_INCREF(Haiku_Window_B_TITLED_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_TITLED_WINDOW", Haiku_Window_B_TITLED_WINDOW);
	
	Haiku_Window_B_MODAL_WINDOW = Py_BuildValue("i", B_MODAL_WINDOW);
	Py_INCREF(Haiku_Window_B_MODAL_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_MODAL_WINDOW", Haiku_Window_B_MODAL_WINDOW);
	
	Haiku_Window_B_DOCUMENT_WINDOW = Py_BuildValue("i", B_DOCUMENT_WINDOW);
	Py_INCREF(Haiku_Window_B_DOCUMENT_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_DOCUMENT_WINDOW", Haiku_Window_B_DOCUMENT_WINDOW);
	
	Haiku_Window_B_BORDERED_WINDOW = Py_BuildValue("i", B_BORDERED_WINDOW);
	Py_INCREF(Haiku_Window_B_BORDERED_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_BORDERED_WINDOW", Haiku_Window_B_BORDERED_WINDOW);
	
	Haiku_Window_B_FLOATING_WINDOW = Py_BuildValue("i", B_FLOATING_WINDOW);
	Py_INCREF(Haiku_Window_B_FLOATING_WINDOW);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_FLOATING_WINDOW", Haiku_Window_B_FLOATING_WINDOW);
	
	Haiku_Window_B_BORDERED_WINDOW_LOOK = Py_BuildValue("i", B_BORDERED_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_BORDERED_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_BORDERED_WINDOW_LOOK", Haiku_Window_B_BORDERED_WINDOW_LOOK);
	
	Haiku_Window_B_NO_BORDER_WINDOW_LOOK = Py_BuildValue("i", B_NO_BORDER_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_NO_BORDER_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NO_BORDER_WINDOW_LOOK", Haiku_Window_B_NO_BORDER_WINDOW_LOOK);
	
	Haiku_Window_B_TITLED_WINDOW_LOOK = Py_BuildValue("i", B_TITLED_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_TITLED_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_TITLED_WINDOW_LOOK", Haiku_Window_B_TITLED_WINDOW_LOOK);
	
	Haiku_Window_B_DOCUMENT_WINDOW_LOOK = Py_BuildValue("i", B_DOCUMENT_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_DOCUMENT_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_DOCUMENT_WINDOW_LOOK", Haiku_Window_B_DOCUMENT_WINDOW_LOOK);
	
	Haiku_Window_B_MODAL_WINDOW_LOOK = Py_BuildValue("i", B_MODAL_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_MODAL_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_MODAL_WINDOW_LOOK", Haiku_Window_B_MODAL_WINDOW_LOOK);
	
	Haiku_Window_B_FLOATING_WINDOW_LOOK = Py_BuildValue("i", B_FLOATING_WINDOW_LOOK);
	Py_INCREF(Haiku_Window_B_FLOATING_WINDOW_LOOK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_FLOATING_WINDOW_LOOK", Haiku_Window_B_FLOATING_WINDOW_LOOK);
	
	Haiku_Window_B_NORMAL_WINDOW_FEEL = Py_BuildValue("i", B_NORMAL_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_NORMAL_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NORMAL_WINDOW_FEEL", Haiku_Window_B_NORMAL_WINDOW_FEEL);
	
	Haiku_Window_B_MODAL_SUBSET_WINDOW_FEEL = Py_BuildValue("i", B_MODAL_SUBSET_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_MODAL_SUBSET_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_MODAL_SUBSET_WINDOW_FEEL", Haiku_Window_B_MODAL_SUBSET_WINDOW_FEEL);
	
	Haiku_Window_B_MODAL_APP_WINDOW_FEEL = Py_BuildValue("i", B_MODAL_APP_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_MODAL_APP_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_MODAL_APP_WINDOW_FEEL", Haiku_Window_B_MODAL_APP_WINDOW_FEEL);
	
	Haiku_Window_B_MODAL_ALL_WINDOW_FEEL = Py_BuildValue("i", B_MODAL_ALL_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_MODAL_ALL_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_MODAL_ALL_WINDOW_FEEL", Haiku_Window_B_MODAL_ALL_WINDOW_FEEL);
	
	Haiku_Window_B_FLOATING_SUBSET_WINDOW_FEEL = Py_BuildValue("i", B_FLOATING_SUBSET_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_FLOATING_SUBSET_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_FLOATING_SUBSET_WINDOW_FEEL", Haiku_Window_B_FLOATING_SUBSET_WINDOW_FEEL);
	
	Haiku_Window_B_FLOATING_APP_WINDOW_FEEL = Py_BuildValue("i", B_FLOATING_APP_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_FLOATING_APP_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_FLOATING_APP_WINDOW_FEEL", Haiku_Window_B_FLOATING_APP_WINDOW_FEEL);
	
	Haiku_Window_B_FLOATING_ALL_WINDOW_FEEL = Py_BuildValue("i", B_FLOATING_ALL_WINDOW_FEEL);
	Py_INCREF(Haiku_Window_B_FLOATING_ALL_WINDOW_FEEL);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_FLOATING_ALL_WINDOW_FEEL", Haiku_Window_B_FLOATING_ALL_WINDOW_FEEL);
	
	Haiku_Window_B_BYTE_ALIGNMENT = Py_BuildValue("i", B_BYTE_ALIGNMENT);
	Py_INCREF(Haiku_Window_B_BYTE_ALIGNMENT);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_BYTE_ALIGNMENT", Haiku_Window_B_BYTE_ALIGNMENT);
	
	Haiku_Window_B_PIXEL_ALIGNMENT = Py_BuildValue("i", B_PIXEL_ALIGNMENT);
	Py_INCREF(Haiku_Window_B_PIXEL_ALIGNMENT);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_PIXEL_ALIGNMENT", Haiku_Window_B_PIXEL_ALIGNMENT);
	
	Haiku_Window_B_NOT_MOVABLE = Py_BuildValue("i", B_NOT_MOVABLE);
	Py_INCREF(Haiku_Window_B_NOT_MOVABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_MOVABLE", Haiku_Window_B_NOT_MOVABLE);
	
	Haiku_Window_B_NOT_CLOSABLE = Py_BuildValue("i", B_NOT_CLOSABLE);
	Py_INCREF(Haiku_Window_B_NOT_CLOSABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_CLOSABLE", Haiku_Window_B_NOT_CLOSABLE);
	
	Haiku_Window_B_NOT_ZOOMABLE = Py_BuildValue("i", B_NOT_ZOOMABLE);
	Py_INCREF(Haiku_Window_B_NOT_ZOOMABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_ZOOMABLE", Haiku_Window_B_NOT_ZOOMABLE);
	
	Haiku_Window_B_NOT_MINIMIZABLE = Py_BuildValue("i", B_NOT_MINIMIZABLE);
	Py_INCREF(Haiku_Window_B_NOT_MINIMIZABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_MINIMIZABLE", Haiku_Window_B_NOT_MINIMIZABLE);
	
	Haiku_Window_B_NOT_RESIZABLE = Py_BuildValue("i", B_NOT_RESIZABLE);
	Py_INCREF(Haiku_Window_B_NOT_RESIZABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_RESIZABLE", Haiku_Window_B_NOT_RESIZABLE);
	
	Haiku_Window_B_NOT_H_RESIZABLE = Py_BuildValue("i", B_NOT_H_RESIZABLE);
	Py_INCREF(Haiku_Window_B_NOT_H_RESIZABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_H_RESIZABLE", Haiku_Window_B_NOT_H_RESIZABLE);
	
	Haiku_Window_B_NOT_V_RESIZABLE = Py_BuildValue("i", B_NOT_V_RESIZABLE);
	Py_INCREF(Haiku_Window_B_NOT_V_RESIZABLE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_V_RESIZABLE", Haiku_Window_B_NOT_V_RESIZABLE);
	
	Haiku_Window_B_AVOID_FRONT = Py_BuildValue("i", B_AVOID_FRONT);
	Py_INCREF(Haiku_Window_B_AVOID_FRONT);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_AVOID_FRONT", Haiku_Window_B_AVOID_FRONT);
	
	Haiku_Window_B_AVOID_FOCUS = Py_BuildValue("i", B_AVOID_FOCUS);
	Py_INCREF(Haiku_Window_B_AVOID_FOCUS);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_AVOID_FOCUS", Haiku_Window_B_AVOID_FOCUS);
	
	Haiku_Window_B_WILL_ACCEPT_FIRST_CLICK = Py_BuildValue("i", B_WILL_ACCEPT_FIRST_CLICK);
	Py_INCREF(Haiku_Window_B_WILL_ACCEPT_FIRST_CLICK);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_WILL_ACCEPT_FIRST_CLICK", Haiku_Window_B_WILL_ACCEPT_FIRST_CLICK);
	
	Haiku_Window_B_OUTLINE_RESIZE = Py_BuildValue("i", B_OUTLINE_RESIZE);
	Py_INCREF(Haiku_Window_B_OUTLINE_RESIZE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_OUTLINE_RESIZE", Haiku_Window_B_OUTLINE_RESIZE);
	
	Haiku_Window_B_NO_WORKSPACE_ACTIVATION = Py_BuildValue("i", B_NO_WORKSPACE_ACTIVATION);
	Py_INCREF(Haiku_Window_B_NO_WORKSPACE_ACTIVATION);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NO_WORKSPACE_ACTIVATION", Haiku_Window_B_NO_WORKSPACE_ACTIVATION);
	
	Haiku_Window_B_NOT_ANCHORED_ON_ACTIVATE = Py_BuildValue("i", B_NOT_ANCHORED_ON_ACTIVATE);
	Py_INCREF(Haiku_Window_B_NOT_ANCHORED_ON_ACTIVATE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NOT_ANCHORED_ON_ACTIVATE", Haiku_Window_B_NOT_ANCHORED_ON_ACTIVATE);
	
	Haiku_Window_B_ASYNCHRONOUS_CONTROLS = Py_BuildValue("i", B_ASYNCHRONOUS_CONTROLS);
	Py_INCREF(Haiku_Window_B_ASYNCHRONOUS_CONTROLS);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_ASYNCHRONOUS_CONTROLS", Haiku_Window_B_ASYNCHRONOUS_CONTROLS);
	
	Haiku_Window_B_QUIT_ON_WINDOW_CLOSE = Py_BuildValue("i", B_QUIT_ON_WINDOW_CLOSE);
	Py_INCREF(Haiku_Window_B_QUIT_ON_WINDOW_CLOSE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_QUIT_ON_WINDOW_CLOSE", Haiku_Window_B_QUIT_ON_WINDOW_CLOSE);
	
	Haiku_Window_B_SAME_POSITION_IN_ALL_WORKSPACES = Py_BuildValue("i", B_SAME_POSITION_IN_ALL_WORKSPACES);
	Py_INCREF(Haiku_Window_B_SAME_POSITION_IN_ALL_WORKSPACES);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_SAME_POSITION_IN_ALL_WORKSPACES", Haiku_Window_B_SAME_POSITION_IN_ALL_WORKSPACES);
	
	Haiku_Window_B_AUTO_UPDATE_SIZE_LIMITS = Py_BuildValue("i", B_AUTO_UPDATE_SIZE_LIMITS);
	Py_INCREF(Haiku_Window_B_AUTO_UPDATE_SIZE_LIMITS);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_AUTO_UPDATE_SIZE_LIMITS", Haiku_Window_B_AUTO_UPDATE_SIZE_LIMITS);
	
	Haiku_Window_B_CLOSE_ON_ESCAPE = Py_BuildValue("i", B_CLOSE_ON_ESCAPE);
	Py_INCREF(Haiku_Window_B_CLOSE_ON_ESCAPE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_CLOSE_ON_ESCAPE", Haiku_Window_B_CLOSE_ON_ESCAPE);
	
	Haiku_Window_B_NO_SERVER_SIDE_WINDOW_MODIFIERS = Py_BuildValue("i", B_NO_SERVER_SIDE_WINDOW_MODIFIERS);
	Py_INCREF(Haiku_Window_B_NO_SERVER_SIDE_WINDOW_MODIFIERS);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_NO_SERVER_SIDE_WINDOW_MODIFIERS", Haiku_Window_B_NO_SERVER_SIDE_WINDOW_MODIFIERS);
	
	Haiku_Window_B_CURRENT_WORKSPACE = Py_BuildValue("i", B_CURRENT_WORKSPACE);
	Py_INCREF(Haiku_Window_B_CURRENT_WORKSPACE);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_CURRENT_WORKSPACE", Haiku_Window_B_CURRENT_WORKSPACE);
	
	Haiku_Window_B_ALL_WORKSPACES = Py_BuildValue("i", B_ALL_WORKSPACES);
	Py_INCREF(Haiku_Window_B_ALL_WORKSPACES);
	PyModule_AddObject(Haiku_WindowConstants_module, "B_ALL_WORKSPACES", Haiku_Window_B_ALL_WORKSPACES);
	
	// Alert: constants (in their own module)
	Haiku_AlertConstants_module = Py_InitModule("Haiku.AlertConstants", Haiku_AlertConstants_PyMethods);
	if (Haiku_AlertConstants_module == NULL)
		return;
	Py_INCREF(Haiku_AlertConstants_module);
	PyModule_AddObject(Haiku_module, "AlertConstants", Haiku_AlertConstants_module);
	
	PyObject* Haiku_Alert_B_EMPTY_ALERT;
	PyObject* Haiku_Alert_B_INFO_ALERT;
	PyObject* Haiku_Alert_B_IDEA_ALERT;
	PyObject* Haiku_Alert_B_WARNING_ALERT;
	PyObject* Haiku_Alert_B_STOP_ALERT;
	PyObject* Haiku_Alert_B_EVEN_SPACING;
	PyObject* Haiku_Alert_B_OFFSET_SPACING;

	Haiku_Alert_B_EMPTY_ALERT = Py_BuildValue("i", B_EMPTY_ALERT);
	Py_INCREF(Haiku_Alert_B_EMPTY_ALERT);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_EMPTY_ALERT", Haiku_Alert_B_EMPTY_ALERT);
	
	Haiku_Alert_B_INFO_ALERT = Py_BuildValue("i", B_INFO_ALERT);
	Py_INCREF(Haiku_Alert_B_INFO_ALERT);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_INFO_ALERT", Haiku_Alert_B_INFO_ALERT);
	
	Haiku_Alert_B_IDEA_ALERT = Py_BuildValue("i", B_IDEA_ALERT);
	Py_INCREF(Haiku_Alert_B_IDEA_ALERT);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_IDEA_ALERT", Haiku_Alert_B_IDEA_ALERT);
	
	Haiku_Alert_B_WARNING_ALERT = Py_BuildValue("i", B_WARNING_ALERT);
	Py_INCREF(Haiku_Alert_B_WARNING_ALERT);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_WARNING_ALERT", Haiku_Alert_B_WARNING_ALERT);
	
	Haiku_Alert_B_STOP_ALERT = Py_BuildValue("i", B_STOP_ALERT);
	Py_INCREF(Haiku_Alert_B_STOP_ALERT);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_STOP_ALERT", Haiku_Alert_B_STOP_ALERT);
	
	Haiku_Alert_B_EVEN_SPACING = Py_BuildValue("i", B_EVEN_SPACING);
	Py_INCREF(Haiku_Alert_B_EVEN_SPACING);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_EVEN_SPACING", Haiku_Alert_B_EVEN_SPACING);
	
	Haiku_Alert_B_OFFSET_SPACING = Py_BuildValue("i", B_OFFSET_SPACING);
	Py_INCREF(Haiku_Alert_B_OFFSET_SPACING);
	PyModule_AddObject(Haiku_AlertConstants_module, "B_OFFSET_SPACING", Haiku_Alert_B_OFFSET_SPACING);
	
	// View: constants (in their own module)
	Haiku_ViewConstants_module = Py_InitModule("Haiku.ViewConstants", Haiku_ViewConstants_PyMethods);
	if (Haiku_ViewConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ViewConstants_module);
	PyModule_AddObject(Haiku_module, "ViewConstants", Haiku_ViewConstants_module);
	
	PyObject* Haiku_View_B_PRIMARY_MOUSE_BUTTON;
	PyObject* Haiku_View_B_SECONDARY_MOUSE_BUTTON;
	PyObject* Haiku_View_B_TERTIARY_MOUSE_BUTTON;
	PyObject* Haiku_View_B_ENTERED_VIEW;
	PyObject* Haiku_View_B_INSIDE_VIEW;
	PyObject* Haiku_View_B_EXITED_VIEW;
	PyObject* Haiku_View_B_OUTSIDE_VIEW;
	PyObject* Haiku_View_B_POINTER_EVENTS;
	PyObject* Haiku_View_B_KEYBOARD_EVENTS;
	PyObject* Haiku_View_B_LOCK_WINDOW_FOCUS;
	PyObject* Haiku_View_B_SUSPEND_VIEW_FOCUS;
	PyObject* Haiku_View_B_NO_POINTER_HISTORY;
	PyObject* Haiku_View_B_FULL_POINTER_HISTORY;
	PyObject* Haiku_View_B_TRACK_WHOLE_RECT;
	PyObject* Haiku_View_B_TRACK_RECT_CORNER;
	PyObject* Haiku_View_B_FONT_FAMILY_AND_STYLE;
	PyObject* Haiku_View_B_FONT_SIZE;
	PyObject* Haiku_View_B_FONT_SHEAR;
	PyObject* Haiku_View_B_FONT_ROTATION;
	PyObject* Haiku_View_B_FONT_SPACING;
	PyObject* Haiku_View_B_FONT_ENCODING;
	PyObject* Haiku_View_B_FONT_FACE;
	PyObject* Haiku_View_B_FONT_FLAGS;
	PyObject* Haiku_View_B_FONT_FALSE_BOLD_WIDTH;
	PyObject* Haiku_View_B_FONT_ALL;
	PyObject* Haiku_View_B_FULL_UPDATE_ON_RESIZE;
	PyObject* Haiku_View_B_WILL_DRAW;
	PyObject* Haiku_View_B_PULSE_NEEDED;
	PyObject* Haiku_View_B_NAVIGABLE_JUMP;
	PyObject* Haiku_View_B_FRAME_EVENTS;
	PyObject* Haiku_View_B_NAVIGABLE;
	PyObject* Haiku_View_B_SUBPIXEL_PRECISE;
	PyObject* Haiku_View_B_DRAW_ON_CHILDREN;
	PyObject* Haiku_View_B_INPUT_METHOD_AWARE;
	PyObject* Haiku_View_B_SUPPORTS_LAYOUT;
	PyObject* Haiku_View_B_INVALIDATE_AFTER_LAYOUT;
	PyObject* Haiku_View_B_FOLLOW_NONE;
	PyObject* Haiku_View_B_FOLLOW_ALL_SIDES;
	PyObject* Haiku_View_B_FOLLOW_ALL;
	PyObject* Haiku_View_B_FOLLOW_LEFT;
	PyObject* Haiku_View_B_FOLLOW_RIGHT;
	PyObject* Haiku_View_B_FOLLOW_LEFT_RIGHT;
	PyObject* Haiku_View_B_FOLLOW_H_CENTER;
	PyObject* Haiku_View_B_FOLLOW_TOP;
	PyObject* Haiku_View_B_FOLLOW_BOTTOM;
	PyObject* Haiku_View_B_FOLLOW_TOP_BOTTOM;
	PyObject* Haiku_View_B_FOLLOW_V_CENTER;

	Haiku_View_B_PRIMARY_MOUSE_BUTTON = Py_BuildValue("i", B_PRIMARY_MOUSE_BUTTON);
	Py_INCREF(Haiku_View_B_PRIMARY_MOUSE_BUTTON);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_PRIMARY_MOUSE_BUTTON", Haiku_View_B_PRIMARY_MOUSE_BUTTON);
	
	Haiku_View_B_SECONDARY_MOUSE_BUTTON = Py_BuildValue("i", B_SECONDARY_MOUSE_BUTTON);
	Py_INCREF(Haiku_View_B_SECONDARY_MOUSE_BUTTON);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_SECONDARY_MOUSE_BUTTON", Haiku_View_B_SECONDARY_MOUSE_BUTTON);
	
	Haiku_View_B_TERTIARY_MOUSE_BUTTON = Py_BuildValue("i", B_TERTIARY_MOUSE_BUTTON);
	Py_INCREF(Haiku_View_B_TERTIARY_MOUSE_BUTTON);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_TERTIARY_MOUSE_BUTTON", Haiku_View_B_TERTIARY_MOUSE_BUTTON);
	
	Haiku_View_B_ENTERED_VIEW = Py_BuildValue("i", B_ENTERED_VIEW);
	Py_INCREF(Haiku_View_B_ENTERED_VIEW);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_ENTERED_VIEW", Haiku_View_B_ENTERED_VIEW);
	
	Haiku_View_B_INSIDE_VIEW = Py_BuildValue("i", B_INSIDE_VIEW);
	Py_INCREF(Haiku_View_B_INSIDE_VIEW);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_INSIDE_VIEW", Haiku_View_B_INSIDE_VIEW);
	
	Haiku_View_B_EXITED_VIEW = Py_BuildValue("i", B_EXITED_VIEW);
	Py_INCREF(Haiku_View_B_EXITED_VIEW);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_EXITED_VIEW", Haiku_View_B_EXITED_VIEW);
	
	Haiku_View_B_OUTSIDE_VIEW = Py_BuildValue("i", B_OUTSIDE_VIEW);
	Py_INCREF(Haiku_View_B_OUTSIDE_VIEW);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_OUTSIDE_VIEW", Haiku_View_B_OUTSIDE_VIEW);
	
	Haiku_View_B_POINTER_EVENTS = Py_BuildValue("i", B_POINTER_EVENTS);
	Py_INCREF(Haiku_View_B_POINTER_EVENTS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_POINTER_EVENTS", Haiku_View_B_POINTER_EVENTS);
	
	Haiku_View_B_KEYBOARD_EVENTS = Py_BuildValue("i", B_KEYBOARD_EVENTS);
	Py_INCREF(Haiku_View_B_KEYBOARD_EVENTS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_KEYBOARD_EVENTS", Haiku_View_B_KEYBOARD_EVENTS);
	
	Haiku_View_B_LOCK_WINDOW_FOCUS = Py_BuildValue("i", B_LOCK_WINDOW_FOCUS);
	Py_INCREF(Haiku_View_B_LOCK_WINDOW_FOCUS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_LOCK_WINDOW_FOCUS", Haiku_View_B_LOCK_WINDOW_FOCUS);
	
	Haiku_View_B_SUSPEND_VIEW_FOCUS = Py_BuildValue("i", B_SUSPEND_VIEW_FOCUS);
	Py_INCREF(Haiku_View_B_SUSPEND_VIEW_FOCUS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_SUSPEND_VIEW_FOCUS", Haiku_View_B_SUSPEND_VIEW_FOCUS);
	
	Haiku_View_B_NO_POINTER_HISTORY = Py_BuildValue("i", B_NO_POINTER_HISTORY);
	Py_INCREF(Haiku_View_B_NO_POINTER_HISTORY);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_NO_POINTER_HISTORY", Haiku_View_B_NO_POINTER_HISTORY);
	
	Haiku_View_B_FULL_POINTER_HISTORY = Py_BuildValue("i", B_FULL_POINTER_HISTORY);
	Py_INCREF(Haiku_View_B_FULL_POINTER_HISTORY);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FULL_POINTER_HISTORY", Haiku_View_B_FULL_POINTER_HISTORY);
	
	Haiku_View_B_TRACK_WHOLE_RECT = Py_BuildValue("i", B_TRACK_WHOLE_RECT);
	Py_INCREF(Haiku_View_B_TRACK_WHOLE_RECT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_TRACK_WHOLE_RECT", Haiku_View_B_TRACK_WHOLE_RECT);
	
	Haiku_View_B_TRACK_RECT_CORNER = Py_BuildValue("i", B_TRACK_RECT_CORNER);
	Py_INCREF(Haiku_View_B_TRACK_RECT_CORNER);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_TRACK_RECT_CORNER", Haiku_View_B_TRACK_RECT_CORNER);
	
	Haiku_View_B_FONT_FAMILY_AND_STYLE = Py_BuildValue("i", B_FONT_FAMILY_AND_STYLE);
	Py_INCREF(Haiku_View_B_FONT_FAMILY_AND_STYLE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_FAMILY_AND_STYLE", Haiku_View_B_FONT_FAMILY_AND_STYLE);
	
	Haiku_View_B_FONT_SIZE = Py_BuildValue("i", B_FONT_SIZE);
	Py_INCREF(Haiku_View_B_FONT_SIZE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_SIZE", Haiku_View_B_FONT_SIZE);
	
	Haiku_View_B_FONT_SHEAR = Py_BuildValue("i", B_FONT_SHEAR);
	Py_INCREF(Haiku_View_B_FONT_SHEAR);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_SHEAR", Haiku_View_B_FONT_SHEAR);
	
	Haiku_View_B_FONT_ROTATION = Py_BuildValue("i", B_FONT_ROTATION);
	Py_INCREF(Haiku_View_B_FONT_ROTATION);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_ROTATION", Haiku_View_B_FONT_ROTATION);
	
	Haiku_View_B_FONT_SPACING = Py_BuildValue("i", B_FONT_SPACING);
	Py_INCREF(Haiku_View_B_FONT_SPACING);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_SPACING", Haiku_View_B_FONT_SPACING);
	
	Haiku_View_B_FONT_ENCODING = Py_BuildValue("i", B_FONT_ENCODING);
	Py_INCREF(Haiku_View_B_FONT_ENCODING);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_ENCODING", Haiku_View_B_FONT_ENCODING);
	
	Haiku_View_B_FONT_FACE = Py_BuildValue("i", B_FONT_FACE);
	Py_INCREF(Haiku_View_B_FONT_FACE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_FACE", Haiku_View_B_FONT_FACE);
	
	Haiku_View_B_FONT_FLAGS = Py_BuildValue("i", B_FONT_FLAGS);
	Py_INCREF(Haiku_View_B_FONT_FLAGS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_FLAGS", Haiku_View_B_FONT_FLAGS);
	
	Haiku_View_B_FONT_FALSE_BOLD_WIDTH = Py_BuildValue("i", B_FONT_FALSE_BOLD_WIDTH);
	Py_INCREF(Haiku_View_B_FONT_FALSE_BOLD_WIDTH);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_FALSE_BOLD_WIDTH", Haiku_View_B_FONT_FALSE_BOLD_WIDTH);
	
	Haiku_View_B_FONT_ALL = Py_BuildValue("i", B_FONT_ALL);
	Py_INCREF(Haiku_View_B_FONT_ALL);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FONT_ALL", Haiku_View_B_FONT_ALL);
	
	Haiku_View_B_FULL_UPDATE_ON_RESIZE = Py_BuildValue("i", B_FULL_UPDATE_ON_RESIZE);
	Py_INCREF(Haiku_View_B_FULL_UPDATE_ON_RESIZE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FULL_UPDATE_ON_RESIZE", Haiku_View_B_FULL_UPDATE_ON_RESIZE);
	
	Haiku_View_B_WILL_DRAW = Py_BuildValue("i", B_WILL_DRAW);
	Py_INCREF(Haiku_View_B_WILL_DRAW);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_WILL_DRAW", Haiku_View_B_WILL_DRAW);
	
	Haiku_View_B_PULSE_NEEDED = Py_BuildValue("i", B_PULSE_NEEDED);
	Py_INCREF(Haiku_View_B_PULSE_NEEDED);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_PULSE_NEEDED", Haiku_View_B_PULSE_NEEDED);
	
	Haiku_View_B_NAVIGABLE_JUMP = Py_BuildValue("i", B_NAVIGABLE_JUMP);
	Py_INCREF(Haiku_View_B_NAVIGABLE_JUMP);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_NAVIGABLE_JUMP", Haiku_View_B_NAVIGABLE_JUMP);
	
	Haiku_View_B_FRAME_EVENTS = Py_BuildValue("i", B_FRAME_EVENTS);
	Py_INCREF(Haiku_View_B_FRAME_EVENTS);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FRAME_EVENTS", Haiku_View_B_FRAME_EVENTS);
	
	Haiku_View_B_NAVIGABLE = Py_BuildValue("i", B_NAVIGABLE);
	Py_INCREF(Haiku_View_B_NAVIGABLE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_NAVIGABLE", Haiku_View_B_NAVIGABLE);
	
	Haiku_View_B_SUBPIXEL_PRECISE = Py_BuildValue("i", B_SUBPIXEL_PRECISE);
	Py_INCREF(Haiku_View_B_SUBPIXEL_PRECISE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_SUBPIXEL_PRECISE", Haiku_View_B_SUBPIXEL_PRECISE);
	
	Haiku_View_B_DRAW_ON_CHILDREN = Py_BuildValue("k", B_DRAW_ON_CHILDREN);
	Py_INCREF(Haiku_View_B_DRAW_ON_CHILDREN);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_DRAW_ON_CHILDREN", Haiku_View_B_DRAW_ON_CHILDREN);
	
	Haiku_View_B_INPUT_METHOD_AWARE = Py_BuildValue("k", B_INPUT_METHOD_AWARE);
	Py_INCREF(Haiku_View_B_INPUT_METHOD_AWARE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_INPUT_METHOD_AWARE", Haiku_View_B_INPUT_METHOD_AWARE);
	
	Haiku_View_B_SUPPORTS_LAYOUT = Py_BuildValue("k", B_SUPPORTS_LAYOUT);
	Py_INCREF(Haiku_View_B_SUPPORTS_LAYOUT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_SUPPORTS_LAYOUT", Haiku_View_B_SUPPORTS_LAYOUT);
	
	Haiku_View_B_INVALIDATE_AFTER_LAYOUT = Py_BuildValue("k", B_INVALIDATE_AFTER_LAYOUT);
	Py_INCREF(Haiku_View_B_INVALIDATE_AFTER_LAYOUT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_INVALIDATE_AFTER_LAYOUT", Haiku_View_B_INVALIDATE_AFTER_LAYOUT);
	
	Haiku_View_B_FOLLOW_NONE = Py_BuildValue("i", B_FOLLOW_NONE);
	Py_INCREF(Haiku_View_B_FOLLOW_NONE);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_NONE", Haiku_View_B_FOLLOW_NONE);
	
	Haiku_View_B_FOLLOW_ALL_SIDES = Py_BuildValue("i", B_FOLLOW_ALL_SIDES);
	Py_INCREF(Haiku_View_B_FOLLOW_ALL_SIDES);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_ALL_SIDES", Haiku_View_B_FOLLOW_ALL_SIDES);
	
	Haiku_View_B_FOLLOW_ALL = Py_BuildValue("i", B_FOLLOW_ALL);
	Py_INCREF(Haiku_View_B_FOLLOW_ALL);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_ALL", Haiku_View_B_FOLLOW_ALL);
	
	Haiku_View_B_FOLLOW_LEFT = Py_BuildValue("i", B_FOLLOW_LEFT);
	Py_INCREF(Haiku_View_B_FOLLOW_LEFT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_LEFT", Haiku_View_B_FOLLOW_LEFT);
	
	Haiku_View_B_FOLLOW_RIGHT = Py_BuildValue("i", B_FOLLOW_RIGHT);
	Py_INCREF(Haiku_View_B_FOLLOW_RIGHT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_RIGHT", Haiku_View_B_FOLLOW_RIGHT);
	
	Haiku_View_B_FOLLOW_LEFT_RIGHT = Py_BuildValue("i", B_FOLLOW_LEFT_RIGHT);
	Py_INCREF(Haiku_View_B_FOLLOW_LEFT_RIGHT);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_LEFT_RIGHT", Haiku_View_B_FOLLOW_LEFT_RIGHT);
	
	Haiku_View_B_FOLLOW_H_CENTER = Py_BuildValue("i", B_FOLLOW_H_CENTER);
	Py_INCREF(Haiku_View_B_FOLLOW_H_CENTER);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_H_CENTER", Haiku_View_B_FOLLOW_H_CENTER);
	
	Haiku_View_B_FOLLOW_TOP = Py_BuildValue("i", B_FOLLOW_TOP);
	Py_INCREF(Haiku_View_B_FOLLOW_TOP);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_TOP", Haiku_View_B_FOLLOW_TOP);
	
	Haiku_View_B_FOLLOW_BOTTOM = Py_BuildValue("i", B_FOLLOW_BOTTOM);
	Py_INCREF(Haiku_View_B_FOLLOW_BOTTOM);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_BOTTOM", Haiku_View_B_FOLLOW_BOTTOM);
	
	Haiku_View_B_FOLLOW_TOP_BOTTOM = Py_BuildValue("i", B_FOLLOW_TOP_BOTTOM);
	Py_INCREF(Haiku_View_B_FOLLOW_TOP_BOTTOM);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_TOP_BOTTOM", Haiku_View_B_FOLLOW_TOP_BOTTOM);
	
	Haiku_View_B_FOLLOW_V_CENTER = Py_BuildValue("i", B_FOLLOW_V_CENTER);
	Py_INCREF(Haiku_View_B_FOLLOW_V_CENTER);
	PyModule_AddObject(Haiku_ViewConstants_module, "B_FOLLOW_V_CENTER", Haiku_View_B_FOLLOW_V_CENTER);
	
	// Control: constants (in their own module)
	Haiku_ControlConstants_module = Py_InitModule("Haiku.ControlConstants", Haiku_ControlConstants_PyMethods);
	if (Haiku_ControlConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ControlConstants_module);
	PyModule_AddObject(Haiku_module, "ControlConstants", Haiku_ControlConstants_module);
	
	PyObject* Haiku_Control_B_CONTROL_ON;
	PyObject* Haiku_Control_B_CONTROL_OFF;

	Haiku_Control_B_CONTROL_ON = Py_BuildValue("i", B_CONTROL_ON);
	Py_INCREF(Haiku_Control_B_CONTROL_ON);
	PyModule_AddObject(Haiku_ControlConstants_module, "B_CONTROL_ON", Haiku_Control_B_CONTROL_ON);
	
	Haiku_Control_B_CONTROL_OFF = Py_BuildValue("i", B_CONTROL_OFF);
	Py_INCREF(Haiku_Control_B_CONTROL_OFF);
	PyModule_AddObject(Haiku_ControlConstants_module, "B_CONTROL_OFF", Haiku_Control_B_CONTROL_OFF);
	
	// ColorControl: constants (in their own module)
	Haiku_ColorControlConstants_module = Py_InitModule("Haiku.ColorControlConstants", Haiku_ColorControlConstants_PyMethods);
	if (Haiku_ColorControlConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ColorControlConstants_module);
	PyModule_AddObject(Haiku_module, "ColorControlConstants", Haiku_ColorControlConstants_module);
	
	PyObject* Haiku_ColorControl_B_CELLS_4x64;
	PyObject* Haiku_ColorControl_B_CELLS_8x32;
	PyObject* Haiku_ColorControl_B_CELLS_16x16;
	PyObject* Haiku_ColorControl_B_CELLS_32x8;
	PyObject* Haiku_ColorControl_B_CELLS_64x4;

	Haiku_ColorControl_B_CELLS_4x64 = Py_BuildValue("i", B_CELLS_4x64);
	Py_INCREF(Haiku_ColorControl_B_CELLS_4x64);
	PyModule_AddObject(Haiku_ColorControlConstants_module, "B_CELLS_4x64", Haiku_ColorControl_B_CELLS_4x64);
	
	Haiku_ColorControl_B_CELLS_8x32 = Py_BuildValue("i", B_CELLS_8x32);
	Py_INCREF(Haiku_ColorControl_B_CELLS_8x32);
	PyModule_AddObject(Haiku_ColorControlConstants_module, "B_CELLS_8x32", Haiku_ColorControl_B_CELLS_8x32);
	
	Haiku_ColorControl_B_CELLS_16x16 = Py_BuildValue("i", B_CELLS_16x16);
	Py_INCREF(Haiku_ColorControl_B_CELLS_16x16);
	PyModule_AddObject(Haiku_ColorControlConstants_module, "B_CELLS_16x16", Haiku_ColorControl_B_CELLS_16x16);
	
	Haiku_ColorControl_B_CELLS_32x8 = Py_BuildValue("i", B_CELLS_32x8);
	Py_INCREF(Haiku_ColorControl_B_CELLS_32x8);
	PyModule_AddObject(Haiku_ColorControlConstants_module, "B_CELLS_32x8", Haiku_ColorControl_B_CELLS_32x8);
	
	Haiku_ColorControl_B_CELLS_64x4 = Py_BuildValue("i", B_CELLS_64x4);
	Py_INCREF(Haiku_ColorControl_B_CELLS_64x4);
	PyModule_AddObject(Haiku_ColorControlConstants_module, "B_CELLS_64x4", Haiku_ColorControl_B_CELLS_64x4);
	
	// PictureButton: constants (in their own module)
	Haiku_PictureButtonConstants_module = Py_InitModule("Haiku.PictureButtonConstants", Haiku_PictureButtonConstants_PyMethods);
	if (Haiku_PictureButtonConstants_module == NULL)
		return;
	Py_INCREF(Haiku_PictureButtonConstants_module);
	PyModule_AddObject(Haiku_module, "PictureButtonConstants", Haiku_PictureButtonConstants_module);
	
	PyObject* Haiku_PictureButton_B_ONE_STATE_BUTTON;
	PyObject* Haiku_PictureButton_B_TWO_STATE_BUTTON;

	Haiku_PictureButton_B_ONE_STATE_BUTTON = Py_BuildValue("i", B_ONE_STATE_BUTTON);
	Py_INCREF(Haiku_PictureButton_B_ONE_STATE_BUTTON);
	PyModule_AddObject(Haiku_PictureButtonConstants_module, "B_ONE_STATE_BUTTON", Haiku_PictureButton_B_ONE_STATE_BUTTON);
	
	Haiku_PictureButton_B_TWO_STATE_BUTTON = Py_BuildValue("i", B_TWO_STATE_BUTTON);
	Py_INCREF(Haiku_PictureButton_B_TWO_STATE_BUTTON);
	PyModule_AddObject(Haiku_PictureButtonConstants_module, "B_TWO_STATE_BUTTON", Haiku_PictureButton_B_TWO_STATE_BUTTON);
	
	// Slider: constants (in their own module)
	Haiku_SliderConstants_module = Py_InitModule("Haiku.SliderConstants", Haiku_SliderConstants_PyMethods);
	if (Haiku_SliderConstants_module == NULL)
		return;
	Py_INCREF(Haiku_SliderConstants_module);
	PyModule_AddObject(Haiku_module, "SliderConstants", Haiku_SliderConstants_module);
	
	PyObject* Haiku_Slider_B_HASH_MARKS_NONE;
	PyObject* Haiku_Slider_B_HASH_MARKS_TOP;
	PyObject* Haiku_Slider_B_HASH_MARKS_LEFT;
	PyObject* Haiku_Slider_B_HASH_MARKS_BOTTOM;
	PyObject* Haiku_Slider_B_HASH_MARKS_RIGHT;
	PyObject* Haiku_Slider_B_HASH_MARKS_BOTH;
	PyObject* Haiku_Slider_B_BLOCK_THUMB;
	PyObject* Haiku_Slider_B_TRIANGLE_THUMB;

	Haiku_Slider_B_HASH_MARKS_NONE = Py_BuildValue("i", B_HASH_MARKS_NONE);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_NONE);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_NONE", Haiku_Slider_B_HASH_MARKS_NONE);
	
	Haiku_Slider_B_HASH_MARKS_TOP = Py_BuildValue("i", B_HASH_MARKS_TOP);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_TOP);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_TOP", Haiku_Slider_B_HASH_MARKS_TOP);
	
	Haiku_Slider_B_HASH_MARKS_LEFT = Py_BuildValue("i", B_HASH_MARKS_LEFT);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_LEFT);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_LEFT", Haiku_Slider_B_HASH_MARKS_LEFT);
	
	Haiku_Slider_B_HASH_MARKS_BOTTOM = Py_BuildValue("i", B_HASH_MARKS_BOTTOM);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_BOTTOM);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_BOTTOM", Haiku_Slider_B_HASH_MARKS_BOTTOM);
	
	Haiku_Slider_B_HASH_MARKS_RIGHT = Py_BuildValue("i", B_HASH_MARKS_RIGHT);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_RIGHT);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_RIGHT", Haiku_Slider_B_HASH_MARKS_RIGHT);
	
	Haiku_Slider_B_HASH_MARKS_BOTH = Py_BuildValue("i", B_HASH_MARKS_BOTH);
	Py_INCREF(Haiku_Slider_B_HASH_MARKS_BOTH);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_HASH_MARKS_BOTH", Haiku_Slider_B_HASH_MARKS_BOTH);
	
	Haiku_Slider_B_BLOCK_THUMB = Py_BuildValue("i", B_BLOCK_THUMB);
	Py_INCREF(Haiku_Slider_B_BLOCK_THUMB);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_BLOCK_THUMB", Haiku_Slider_B_BLOCK_THUMB);
	
	Haiku_Slider_B_TRIANGLE_THUMB = Py_BuildValue("i", B_TRIANGLE_THUMB);
	Py_INCREF(Haiku_Slider_B_TRIANGLE_THUMB);
	PyModule_AddObject(Haiku_SliderConstants_module, "B_TRIANGLE_THUMB", Haiku_Slider_B_TRIANGLE_THUMB);
	
	// ListView: constants (in their own module)
	Haiku_ListViewConstants_module = Py_InitModule("Haiku.ListViewConstants", Haiku_ListViewConstants_PyMethods);
	if (Haiku_ListViewConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ListViewConstants_module);
	PyModule_AddObject(Haiku_module, "ListViewConstants", Haiku_ListViewConstants_module);
	
	PyObject* Haiku_ListView_B_SINGLE_SELECTION_LIST;
	PyObject* Haiku_ListView_B_MULTIPLE_SELECTION_LIST;

	Haiku_ListView_B_SINGLE_SELECTION_LIST = Py_BuildValue("i", B_SINGLE_SELECTION_LIST);
	Py_INCREF(Haiku_ListView_B_SINGLE_SELECTION_LIST);
	PyModule_AddObject(Haiku_ListViewConstants_module, "B_SINGLE_SELECTION_LIST", Haiku_ListView_B_SINGLE_SELECTION_LIST);
	
	Haiku_ListView_B_MULTIPLE_SELECTION_LIST = Py_BuildValue("i", B_MULTIPLE_SELECTION_LIST);
	Py_INCREF(Haiku_ListView_B_MULTIPLE_SELECTION_LIST);
	PyModule_AddObject(Haiku_ListViewConstants_module, "B_MULTIPLE_SELECTION_LIST", Haiku_ListView_B_MULTIPLE_SELECTION_LIST);
	
	// Menu: constants (in their own module)
	Haiku_MenuConstants_module = Py_InitModule("Haiku.MenuConstants", Haiku_MenuConstants_PyMethods);
	if (Haiku_MenuConstants_module == NULL)
		return;
	Py_INCREF(Haiku_MenuConstants_module);
	PyModule_AddObject(Haiku_module, "MenuConstants", Haiku_MenuConstants_module);
	
	PyObject* Haiku_Menu_B_ITEMS_IN_ROW;
	PyObject* Haiku_Menu_B_ITEMS_IN_COLUMN;
	PyObject* Haiku_Menu_B_ITEMS_IN_MATRIX;
	PyObject* Haiku_Menu_B_INITIAL_ADD;
	PyObject* Haiku_Menu_B_PROCESSING;
	PyObject* Haiku_Menu_B_ABORT;

	Haiku_Menu_B_ITEMS_IN_ROW = Py_BuildValue("i", B_ITEMS_IN_ROW);
	Py_INCREF(Haiku_Menu_B_ITEMS_IN_ROW);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_ITEMS_IN_ROW", Haiku_Menu_B_ITEMS_IN_ROW);
	
	Haiku_Menu_B_ITEMS_IN_COLUMN = Py_BuildValue("i", B_ITEMS_IN_COLUMN);
	Py_INCREF(Haiku_Menu_B_ITEMS_IN_COLUMN);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_ITEMS_IN_COLUMN", Haiku_Menu_B_ITEMS_IN_COLUMN);
	
	Haiku_Menu_B_ITEMS_IN_MATRIX = Py_BuildValue("i", B_ITEMS_IN_MATRIX);
	Py_INCREF(Haiku_Menu_B_ITEMS_IN_MATRIX);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_ITEMS_IN_MATRIX", Haiku_Menu_B_ITEMS_IN_MATRIX);
	
	Haiku_Menu_B_INITIAL_ADD = Py_BuildValue("i", BMenu::B_INITIAL_ADD);
	Py_INCREF(Haiku_Menu_B_INITIAL_ADD);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_INITIAL_ADD", Haiku_Menu_B_INITIAL_ADD);
	
	Haiku_Menu_B_PROCESSING = Py_BuildValue("i", BMenu::B_PROCESSING);
	Py_INCREF(Haiku_Menu_B_PROCESSING);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_PROCESSING", Haiku_Menu_B_PROCESSING);
	
	Haiku_Menu_B_ABORT = Py_BuildValue("i", BMenu::B_ABORT);
	Py_INCREF(Haiku_Menu_B_ABORT);
	PyModule_AddObject(Haiku_MenuConstants_module, "B_ABORT", Haiku_Menu_B_ABORT);
	
	// MenuBar: constants (in their own module)
	Haiku_MenuBarConstants_module = Py_InitModule("Haiku.MenuBarConstants", Haiku_MenuBarConstants_PyMethods);
	if (Haiku_MenuBarConstants_module == NULL)
		return;
	Py_INCREF(Haiku_MenuBarConstants_module);
	PyModule_AddObject(Haiku_module, "MenuBarConstants", Haiku_MenuBarConstants_module);
	
	PyObject* Haiku_MenuBar_B_BORDER_FRAME;
	PyObject* Haiku_MenuBar_B_BORDER_CONTENTS;
	PyObject* Haiku_MenuBar_B_BORDER_EACH_ITEM;

	Haiku_MenuBar_B_BORDER_FRAME = Py_BuildValue("i", B_BORDER_FRAME);
	Py_INCREF(Haiku_MenuBar_B_BORDER_FRAME);
	PyModule_AddObject(Haiku_MenuBarConstants_module, "B_BORDER_FRAME", Haiku_MenuBar_B_BORDER_FRAME);
	
	Haiku_MenuBar_B_BORDER_CONTENTS = Py_BuildValue("i", B_BORDER_CONTENTS);
	Py_INCREF(Haiku_MenuBar_B_BORDER_CONTENTS);
	PyModule_AddObject(Haiku_MenuBarConstants_module, "B_BORDER_CONTENTS", Haiku_MenuBar_B_BORDER_CONTENTS);
	
	Haiku_MenuBar_B_BORDER_EACH_ITEM = Py_BuildValue("i", B_BORDER_EACH_ITEM);
	Py_INCREF(Haiku_MenuBar_B_BORDER_EACH_ITEM);
	PyModule_AddObject(Haiku_MenuBarConstants_module, "B_BORDER_EACH_ITEM", Haiku_MenuBar_B_BORDER_EACH_ITEM);
	
	// ScrollBar: constants (in their own module)
	Haiku_ScrollBarConstants_module = Py_InitModule("Haiku.ScrollBarConstants", Haiku_ScrollBarConstants_PyMethods);
	if (Haiku_ScrollBarConstants_module == NULL)
		return;
	Py_INCREF(Haiku_ScrollBarConstants_module);
	PyModule_AddObject(Haiku_module, "ScrollBarConstants", Haiku_ScrollBarConstants_module);
	
	PyObject* Haiku_ScrollBar_B_V_SCROLL_BAR_WIDTH;
	PyObject* Haiku_ScrollBar_B_H_SCROLL_BAR_HEIGHT;
	PyObject* Haiku_ScrollBar_SCROLL_BAR_MAXIMUM_KNOB_SIZE;
	PyObject* Haiku_ScrollBar_SCROLL_BAR_MINIMUM_KNOB_SIZE;
	PyObject* Haiku_ScrollBar_DISABLES_ON_WINDOW_DEACTIVATION;

	Haiku_ScrollBar_B_V_SCROLL_BAR_WIDTH = Py_BuildValue("i", B_V_SCROLL_BAR_WIDTH);
	Py_INCREF(Haiku_ScrollBar_B_V_SCROLL_BAR_WIDTH);
	PyModule_AddObject(Haiku_ScrollBarConstants_module, "B_V_SCROLL_BAR_WIDTH", Haiku_ScrollBar_B_V_SCROLL_BAR_WIDTH);
	
	Haiku_ScrollBar_B_H_SCROLL_BAR_HEIGHT = Py_BuildValue("i", B_H_SCROLL_BAR_HEIGHT);
	Py_INCREF(Haiku_ScrollBar_B_H_SCROLL_BAR_HEIGHT);
	PyModule_AddObject(Haiku_ScrollBarConstants_module, "B_H_SCROLL_BAR_HEIGHT", Haiku_ScrollBar_B_H_SCROLL_BAR_HEIGHT);
	
	Haiku_ScrollBar_SCROLL_BAR_MAXIMUM_KNOB_SIZE = Py_BuildValue("i", SCROLL_BAR_MAXIMUM_KNOB_SIZE);
	Py_INCREF(Haiku_ScrollBar_SCROLL_BAR_MAXIMUM_KNOB_SIZE);
	PyModule_AddObject(Haiku_ScrollBarConstants_module, "SCROLL_BAR_MAXIMUM_KNOB_SIZE", Haiku_ScrollBar_SCROLL_BAR_MAXIMUM_KNOB_SIZE);
	
	Haiku_ScrollBar_SCROLL_BAR_MINIMUM_KNOB_SIZE = Py_BuildValue("i", SCROLL_BAR_MINIMUM_KNOB_SIZE);
	Py_INCREF(Haiku_ScrollBar_SCROLL_BAR_MINIMUM_KNOB_SIZE);
	PyModule_AddObject(Haiku_ScrollBarConstants_module, "SCROLL_BAR_MINIMUM_KNOB_SIZE", Haiku_ScrollBar_SCROLL_BAR_MINIMUM_KNOB_SIZE);
	
	Haiku_ScrollBar_DISABLES_ON_WINDOW_DEACTIVATION = Py_BuildValue("i", DISABLES_ON_WINDOW_DEACTIVATION);
	Py_INCREF(Haiku_ScrollBar_DISABLES_ON_WINDOW_DEACTIVATION);
	PyModule_AddObject(Haiku_ScrollBarConstants_module, "DISABLES_ON_WINDOW_DEACTIVATION", Haiku_ScrollBar_DISABLES_ON_WINDOW_DEACTIVATION);
	
	// TabView: constants (in their own module)
	Haiku_TabViewConstants_module = Py_InitModule("Haiku.TabViewConstants", Haiku_TabViewConstants_PyMethods);
	if (Haiku_TabViewConstants_module == NULL)
		return;
	Py_INCREF(Haiku_TabViewConstants_module);
	PyModule_AddObject(Haiku_module, "TabViewConstants", Haiku_TabViewConstants_module);
	
	PyObject* Haiku_TabView_B_TAB_FIRST;
	PyObject* Haiku_TabView_B_TAB_FRONT;
	PyObject* Haiku_TabView_B_TAB_ANY;

	Haiku_TabView_B_TAB_FIRST = Py_BuildValue("i", B_TAB_FIRST);
	Py_INCREF(Haiku_TabView_B_TAB_FIRST);
	PyModule_AddObject(Haiku_TabViewConstants_module, "B_TAB_FIRST", Haiku_TabView_B_TAB_FIRST);
	
	Haiku_TabView_B_TAB_FRONT = Py_BuildValue("i", B_TAB_FRONT);
	Py_INCREF(Haiku_TabView_B_TAB_FRONT);
	PyModule_AddObject(Haiku_TabViewConstants_module, "B_TAB_FRONT", Haiku_TabView_B_TAB_FRONT);
	
	Haiku_TabView_B_TAB_ANY = Py_BuildValue("i", B_TAB_ANY);
	Py_INCREF(Haiku_TabView_B_TAB_ANY);
	PyModule_AddObject(Haiku_TabViewConstants_module, "B_TAB_ANY", Haiku_TabView_B_TAB_ANY);
	
	// TextView: constants (in their own module)
	Haiku_TextViewConstants_module = Py_InitModule("Haiku.TextViewConstants", Haiku_TextViewConstants_PyMethods);
	if (Haiku_TextViewConstants_module == NULL)
		return;
	Py_INCREF(Haiku_TextViewConstants_module);
	PyModule_AddObject(Haiku_module, "TextViewConstants", Haiku_TextViewConstants_module);
	
	PyObject* Haiku_TextView_B_UNDO_UNAVAILABLE;
	PyObject* Haiku_TextView_B_UNDO_TYPING;
	PyObject* Haiku_TextView_B_UNDO_CUT;
	PyObject* Haiku_TextView_B_UNDO_PASTE;
	PyObject* Haiku_TextView_B_UNDO_CLEAR;
	PyObject* Haiku_TextView_B_UNDO_DROP;

	Haiku_TextView_B_UNDO_UNAVAILABLE = Py_BuildValue("i", B_UNDO_UNAVAILABLE);
	Py_INCREF(Haiku_TextView_B_UNDO_UNAVAILABLE);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_UNAVAILABLE", Haiku_TextView_B_UNDO_UNAVAILABLE);
	
	Haiku_TextView_B_UNDO_TYPING = Py_BuildValue("i", B_UNDO_TYPING);
	Py_INCREF(Haiku_TextView_B_UNDO_TYPING);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_TYPING", Haiku_TextView_B_UNDO_TYPING);
	
	Haiku_TextView_B_UNDO_CUT = Py_BuildValue("i", B_UNDO_CUT);
	Py_INCREF(Haiku_TextView_B_UNDO_CUT);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_CUT", Haiku_TextView_B_UNDO_CUT);
	
	Haiku_TextView_B_UNDO_PASTE = Py_BuildValue("i", B_UNDO_PASTE);
	Py_INCREF(Haiku_TextView_B_UNDO_PASTE);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_PASTE", Haiku_TextView_B_UNDO_PASTE);
	
	Haiku_TextView_B_UNDO_CLEAR = Py_BuildValue("i", B_UNDO_CLEAR);
	Py_INCREF(Haiku_TextView_B_UNDO_CLEAR);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_CLEAR", Haiku_TextView_B_UNDO_CLEAR);
	
	Haiku_TextView_B_UNDO_DROP = Py_BuildValue("i", B_UNDO_DROP);
	Py_INCREF(Haiku_TextView_B_UNDO_DROP);
	PyModule_AddObject(Haiku_TextViewConstants_module, "B_UNDO_DROP", Haiku_TextView_B_UNDO_DROP);
	
	// Font: constants (in their own module)
	Haiku_FontConstants_module = Py_InitModule("Haiku.FontConstants", Haiku_FontConstants_PyMethods);
	if (Haiku_FontConstants_module == NULL)
		return;
	Py_INCREF(Haiku_FontConstants_module);
	PyModule_AddObject(Haiku_module, "FontConstants", Haiku_FontConstants_module);
	
	PyObject* Haiku_Font_B_FONT_FAMILY_LENGTH;
	PyObject* Haiku_Font_B_FONT_STYLE_LENGTH;
	PyObject* Haiku_Font_B_CHAR_SPACING;
	PyObject* Haiku_Font_B_STRING_SPACING;
	PyObject* Haiku_Font_B_BITMAP_SPACING;
	PyObject* Haiku_Font_B_FIXED_SPACING;
	PyObject* Haiku_Font_B_FONT_LEFT_TO_RIGHT;
	PyObject* Haiku_Font_B_FONT_RIGHT_TO_LEFT;
	PyObject* Haiku_Font_B_DISABLE_ANTIALIASING;
	PyObject* Haiku_Font_B_FORCE_ANTIALIASING;
	PyObject* Haiku_Font_B_TRUNCATE_END;
	PyObject* Haiku_Font_B_TRUNCATE_BEGINNING;
	PyObject* Haiku_Font_B_TRUNCATE_MIDDLE;
	PyObject* Haiku_Font_B_TRUNCATE_SMART;
	PyObject* Haiku_Font_B_UNICODE_UTF8;
	PyObject* Haiku_Font_B_ISO_8859_1;
	PyObject* Haiku_Font_B_ISO_8859_2;
	PyObject* Haiku_Font_B_ISO_8859_3;
	PyObject* Haiku_Font_B_ISO_8859_4;
	PyObject* Haiku_Font_B_ISO_8859_5;
	PyObject* Haiku_Font_B_ISO_8859_6;
	PyObject* Haiku_Font_B_ISO_8859_7;
	PyObject* Haiku_Font_B_ISO_8859_8;
	PyObject* Haiku_Font_B_ISO_8859_9;
	PyObject* Haiku_Font_B_ISO_8859_10;
	PyObject* Haiku_Font_B_MACINTOSH_ROMAN;
	PyObject* Haiku_Font_B_HAS_TUNED_FONT;
	PyObject* Haiku_Font_B_IS_FIXED;
	PyObject* Haiku_Font_B_ITALIC_FACE;
	PyObject* Haiku_Font_B_UNDERSCORE_FACE;
	PyObject* Haiku_Font_B_NEGATIVE_FACE;
	PyObject* Haiku_Font_B_OUTLINED_FACE;
	PyObject* Haiku_Font_B_STRIKEOUT_FACE;
	PyObject* Haiku_Font_B_BOLD_FACE;
	PyObject* Haiku_Font_B_REGULAR_FACE;
	PyObject* Haiku_Font_B_CONDENSED_FACE;
	PyObject* Haiku_Font_B_LIGHT_FACE;
	PyObject* Haiku_Font_B_HEAVY_FACE;
	PyObject* Haiku_Font_B_SCREEN_METRIC;
	PyObject* Haiku_Font_B_PRINTING_METRIC;
	PyObject* Haiku_Font_B_TRUETYPE_WINDOWS;
	PyObject* Haiku_Font_B_POSTSCRIPT_TYPE1_WINDOWS;
	Haiku_unicode_block_Object* Haiku_Font_B_BASIC_LATIN_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LATIN_EXTENDED_A_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LATIN_EXTENDED_B_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_IPA_EXTENSIONS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BASIC_GREEK_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CYRILLIC_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ARMENIAN_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BASIC_HEBREW_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HEBREW_EXTENDED_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BASIC_ARABIC_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ARABIC_EXTENDED_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_DEVANAGARI_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BENGALI_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GURMUKHI_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GUJARATI_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ORIYA_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_TAMIL_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_TELUGU_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_KANNADA_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_MALAYALAM_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_THAI_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LAO_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BASIC_GEORGIAN_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HANGUL_JAMO_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GREEK_EXTENDED_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_NUMBER_FORMS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ARROWS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CONTROL_PICTURES_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BOX_DRAWING_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BLOCK_ELEMENTS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_DINGBATS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HIRAGANA_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_KATAKANA_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_BOPOMOFO_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_COMPATIBILITY_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HANGUL_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HIGH_SURROGATES_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_LOW_SURROGATES_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_PRIVATE_USE_AREA_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_SPECIALS_BLOCK;
	Haiku_unicode_block_Object* Haiku_Font_B_TIBETAN_BLOCK;

	Haiku_Font_B_FONT_FAMILY_LENGTH = Py_BuildValue("i", B_FONT_FAMILY_LENGTH);
	Py_INCREF(Haiku_Font_B_FONT_FAMILY_LENGTH);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FONT_FAMILY_LENGTH", Haiku_Font_B_FONT_FAMILY_LENGTH);
	
	Haiku_Font_B_FONT_STYLE_LENGTH = Py_BuildValue("i", B_FONT_STYLE_LENGTH);
	Py_INCREF(Haiku_Font_B_FONT_STYLE_LENGTH);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FONT_STYLE_LENGTH", Haiku_Font_B_FONT_STYLE_LENGTH);
	
	Haiku_Font_B_CHAR_SPACING = Py_BuildValue("i", B_CHAR_SPACING);
	Py_INCREF(Haiku_Font_B_CHAR_SPACING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CHAR_SPACING", Haiku_Font_B_CHAR_SPACING);
	
	Haiku_Font_B_STRING_SPACING = Py_BuildValue("i", B_STRING_SPACING);
	Py_INCREF(Haiku_Font_B_STRING_SPACING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_STRING_SPACING", Haiku_Font_B_STRING_SPACING);
	
	Haiku_Font_B_BITMAP_SPACING = Py_BuildValue("i", B_BITMAP_SPACING);
	Py_INCREF(Haiku_Font_B_BITMAP_SPACING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BITMAP_SPACING", Haiku_Font_B_BITMAP_SPACING);
	
	Haiku_Font_B_FIXED_SPACING = Py_BuildValue("i", B_FIXED_SPACING);
	Py_INCREF(Haiku_Font_B_FIXED_SPACING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FIXED_SPACING", Haiku_Font_B_FIXED_SPACING);
	
	Haiku_Font_B_FONT_LEFT_TO_RIGHT = Py_BuildValue("i", B_FONT_LEFT_TO_RIGHT);
	Py_INCREF(Haiku_Font_B_FONT_LEFT_TO_RIGHT);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FONT_LEFT_TO_RIGHT", Haiku_Font_B_FONT_LEFT_TO_RIGHT);
	
	Haiku_Font_B_FONT_RIGHT_TO_LEFT = Py_BuildValue("i", B_FONT_RIGHT_TO_LEFT);
	Py_INCREF(Haiku_Font_B_FONT_RIGHT_TO_LEFT);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FONT_RIGHT_TO_LEFT", Haiku_Font_B_FONT_RIGHT_TO_LEFT);
	
	Haiku_Font_B_DISABLE_ANTIALIASING = Py_BuildValue("i", B_DISABLE_ANTIALIASING);
	Py_INCREF(Haiku_Font_B_DISABLE_ANTIALIASING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_DISABLE_ANTIALIASING", Haiku_Font_B_DISABLE_ANTIALIASING);
	
	Haiku_Font_B_FORCE_ANTIALIASING = Py_BuildValue("i", B_FORCE_ANTIALIASING);
	Py_INCREF(Haiku_Font_B_FORCE_ANTIALIASING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_FORCE_ANTIALIASING", Haiku_Font_B_FORCE_ANTIALIASING);
	
	Haiku_Font_B_TRUNCATE_END = Py_BuildValue("i", B_TRUNCATE_END);
	Py_INCREF(Haiku_Font_B_TRUNCATE_END);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TRUNCATE_END", Haiku_Font_B_TRUNCATE_END);
	
	Haiku_Font_B_TRUNCATE_BEGINNING = Py_BuildValue("i", B_TRUNCATE_BEGINNING);
	Py_INCREF(Haiku_Font_B_TRUNCATE_BEGINNING);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TRUNCATE_BEGINNING", Haiku_Font_B_TRUNCATE_BEGINNING);
	
	Haiku_Font_B_TRUNCATE_MIDDLE = Py_BuildValue("i", B_TRUNCATE_MIDDLE);
	Py_INCREF(Haiku_Font_B_TRUNCATE_MIDDLE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TRUNCATE_MIDDLE", Haiku_Font_B_TRUNCATE_MIDDLE);
	
	Haiku_Font_B_TRUNCATE_SMART = Py_BuildValue("i", B_TRUNCATE_SMART);
	Py_INCREF(Haiku_Font_B_TRUNCATE_SMART);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TRUNCATE_SMART", Haiku_Font_B_TRUNCATE_SMART);
	
	Haiku_Font_B_UNICODE_UTF8 = Py_BuildValue("i", B_UNICODE_UTF8);
	Py_INCREF(Haiku_Font_B_UNICODE_UTF8);
	PyModule_AddObject(Haiku_FontConstants_module, "B_UNICODE_UTF8", Haiku_Font_B_UNICODE_UTF8);
	
	Haiku_Font_B_ISO_8859_1 = Py_BuildValue("i", B_ISO_8859_1);
	Py_INCREF(Haiku_Font_B_ISO_8859_1);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_1", Haiku_Font_B_ISO_8859_1);
	
	Haiku_Font_B_ISO_8859_2 = Py_BuildValue("i", B_ISO_8859_2);
	Py_INCREF(Haiku_Font_B_ISO_8859_2);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_2", Haiku_Font_B_ISO_8859_2);
	
	Haiku_Font_B_ISO_8859_3 = Py_BuildValue("i", B_ISO_8859_3);
	Py_INCREF(Haiku_Font_B_ISO_8859_3);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_3", Haiku_Font_B_ISO_8859_3);
	
	Haiku_Font_B_ISO_8859_4 = Py_BuildValue("i", B_ISO_8859_4);
	Py_INCREF(Haiku_Font_B_ISO_8859_4);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_4", Haiku_Font_B_ISO_8859_4);
	
	Haiku_Font_B_ISO_8859_5 = Py_BuildValue("i", B_ISO_8859_5);
	Py_INCREF(Haiku_Font_B_ISO_8859_5);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_5", Haiku_Font_B_ISO_8859_5);
	
	Haiku_Font_B_ISO_8859_6 = Py_BuildValue("i", B_ISO_8859_6);
	Py_INCREF(Haiku_Font_B_ISO_8859_6);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_6", Haiku_Font_B_ISO_8859_6);
	
	Haiku_Font_B_ISO_8859_7 = Py_BuildValue("i", B_ISO_8859_7);
	Py_INCREF(Haiku_Font_B_ISO_8859_7);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_7", Haiku_Font_B_ISO_8859_7);
	
	Haiku_Font_B_ISO_8859_8 = Py_BuildValue("i", B_ISO_8859_8);
	Py_INCREF(Haiku_Font_B_ISO_8859_8);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_8", Haiku_Font_B_ISO_8859_8);
	
	Haiku_Font_B_ISO_8859_9 = Py_BuildValue("i", B_ISO_8859_9);
	Py_INCREF(Haiku_Font_B_ISO_8859_9);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_9", Haiku_Font_B_ISO_8859_9);
	
	Haiku_Font_B_ISO_8859_10 = Py_BuildValue("i", B_ISO_8859_10);
	Py_INCREF(Haiku_Font_B_ISO_8859_10);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ISO_8859_10", Haiku_Font_B_ISO_8859_10);
	
	Haiku_Font_B_MACINTOSH_ROMAN = Py_BuildValue("i", B_MACINTOSH_ROMAN);
	Py_INCREF(Haiku_Font_B_MACINTOSH_ROMAN);
	PyModule_AddObject(Haiku_FontConstants_module, "B_MACINTOSH_ROMAN", Haiku_Font_B_MACINTOSH_ROMAN);
	
	Haiku_Font_B_HAS_TUNED_FONT = Py_BuildValue("i", B_HAS_TUNED_FONT);
	Py_INCREF(Haiku_Font_B_HAS_TUNED_FONT);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HAS_TUNED_FONT", Haiku_Font_B_HAS_TUNED_FONT);
	
	Haiku_Font_B_IS_FIXED = Py_BuildValue("i", B_IS_FIXED);
	Py_INCREF(Haiku_Font_B_IS_FIXED);
	PyModule_AddObject(Haiku_FontConstants_module, "B_IS_FIXED", Haiku_Font_B_IS_FIXED);
	
	Haiku_Font_B_ITALIC_FACE = Py_BuildValue("i", B_ITALIC_FACE);
	Py_INCREF(Haiku_Font_B_ITALIC_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ITALIC_FACE", Haiku_Font_B_ITALIC_FACE);
	
	Haiku_Font_B_UNDERSCORE_FACE = Py_BuildValue("i", B_UNDERSCORE_FACE);
	Py_INCREF(Haiku_Font_B_UNDERSCORE_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_UNDERSCORE_FACE", Haiku_Font_B_UNDERSCORE_FACE);
	
	Haiku_Font_B_NEGATIVE_FACE = Py_BuildValue("i", B_NEGATIVE_FACE);
	Py_INCREF(Haiku_Font_B_NEGATIVE_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_NEGATIVE_FACE", Haiku_Font_B_NEGATIVE_FACE);
	
	Haiku_Font_B_OUTLINED_FACE = Py_BuildValue("i", B_OUTLINED_FACE);
	Py_INCREF(Haiku_Font_B_OUTLINED_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_OUTLINED_FACE", Haiku_Font_B_OUTLINED_FACE);
	
	Haiku_Font_B_STRIKEOUT_FACE = Py_BuildValue("i", B_STRIKEOUT_FACE);
	Py_INCREF(Haiku_Font_B_STRIKEOUT_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_STRIKEOUT_FACE", Haiku_Font_B_STRIKEOUT_FACE);
	
	Haiku_Font_B_BOLD_FACE = Py_BuildValue("i", B_BOLD_FACE);
	Py_INCREF(Haiku_Font_B_BOLD_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BOLD_FACE", Haiku_Font_B_BOLD_FACE);
	
	Haiku_Font_B_REGULAR_FACE = Py_BuildValue("i", B_REGULAR_FACE);
	Py_INCREF(Haiku_Font_B_REGULAR_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_REGULAR_FACE", Haiku_Font_B_REGULAR_FACE);
	
	Haiku_Font_B_CONDENSED_FACE = Py_BuildValue("i", B_CONDENSED_FACE);
	Py_INCREF(Haiku_Font_B_CONDENSED_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CONDENSED_FACE", Haiku_Font_B_CONDENSED_FACE);
	
	Haiku_Font_B_LIGHT_FACE = Py_BuildValue("i", B_LIGHT_FACE);
	Py_INCREF(Haiku_Font_B_LIGHT_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LIGHT_FACE", Haiku_Font_B_LIGHT_FACE);
	
	Haiku_Font_B_HEAVY_FACE = Py_BuildValue("i", B_HEAVY_FACE);
	Py_INCREF(Haiku_Font_B_HEAVY_FACE);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HEAVY_FACE", Haiku_Font_B_HEAVY_FACE);
	
	Haiku_Font_B_SCREEN_METRIC = Py_BuildValue("i", B_SCREEN_METRIC);
	Py_INCREF(Haiku_Font_B_SCREEN_METRIC);
	PyModule_AddObject(Haiku_FontConstants_module, "B_SCREEN_METRIC", Haiku_Font_B_SCREEN_METRIC);
	
	Haiku_Font_B_PRINTING_METRIC = Py_BuildValue("i", B_PRINTING_METRIC);
	Py_INCREF(Haiku_Font_B_PRINTING_METRIC);
	PyModule_AddObject(Haiku_FontConstants_module, "B_PRINTING_METRIC", Haiku_Font_B_PRINTING_METRIC);
	
	Haiku_Font_B_TRUETYPE_WINDOWS = Py_BuildValue("i", B_TRUETYPE_WINDOWS);
	Py_INCREF(Haiku_Font_B_TRUETYPE_WINDOWS);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TRUETYPE_WINDOWS", Haiku_Font_B_TRUETYPE_WINDOWS);
	
	Haiku_Font_B_POSTSCRIPT_TYPE1_WINDOWS = Py_BuildValue("i", B_POSTSCRIPT_TYPE1_WINDOWS);
	Py_INCREF(Haiku_Font_B_POSTSCRIPT_TYPE1_WINDOWS);
	PyModule_AddObject(Haiku_FontConstants_module, "B_POSTSCRIPT_TYPE1_WINDOWS", Haiku_Font_B_POSTSCRIPT_TYPE1_WINDOWS);
	
	Haiku_Font_B_BASIC_LATIN_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BASIC_LATIN_BLOCK->cpp_object = (unicode_block*)&B_BASIC_LATIN_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BASIC_LATIN_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BASIC_LATIN_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BASIC_LATIN_BLOCK", (PyObject*)Haiku_Font_B_BASIC_LATIN_BLOCK);
	
	Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK->cpp_object = (unicode_block*)&B_LATIN1_SUPPLEMENT_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LATIN1_SUPPLEMENT_BLOCK", (PyObject*)Haiku_Font_B_LATIN1_SUPPLEMENT_BLOCK);
	
	Haiku_Font_B_LATIN_EXTENDED_A_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LATIN_EXTENDED_A_BLOCK->cpp_object = (unicode_block*)&B_LATIN_EXTENDED_A_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LATIN_EXTENDED_A_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LATIN_EXTENDED_A_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LATIN_EXTENDED_A_BLOCK", (PyObject*)Haiku_Font_B_LATIN_EXTENDED_A_BLOCK);
	
	Haiku_Font_B_LATIN_EXTENDED_B_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LATIN_EXTENDED_B_BLOCK->cpp_object = (unicode_block*)&B_LATIN_EXTENDED_B_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LATIN_EXTENDED_B_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LATIN_EXTENDED_B_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LATIN_EXTENDED_B_BLOCK", (PyObject*)Haiku_Font_B_LATIN_EXTENDED_B_BLOCK);
	
	Haiku_Font_B_IPA_EXTENSIONS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_IPA_EXTENSIONS_BLOCK->cpp_object = (unicode_block*)&B_IPA_EXTENSIONS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_IPA_EXTENSIONS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_IPA_EXTENSIONS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_IPA_EXTENSIONS_BLOCK", (PyObject*)Haiku_Font_B_IPA_EXTENSIONS_BLOCK);
	
	Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK->cpp_object = (unicode_block*)&B_SPACING_MODIFIER_LETTERS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_SPACING_MODIFIER_LETTERS_BLOCK", (PyObject*)Haiku_Font_B_SPACING_MODIFIER_LETTERS_BLOCK);
	
	Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK->cpp_object = (unicode_block*)&B_COMBINING_DIACRITICAL_MARKS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_COMBINING_DIACRITICAL_MARKS_BLOCK", (PyObject*)Haiku_Font_B_COMBINING_DIACRITICAL_MARKS_BLOCK);
	
	Haiku_Font_B_BASIC_GREEK_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BASIC_GREEK_BLOCK->cpp_object = (unicode_block*)&B_BASIC_GREEK_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BASIC_GREEK_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BASIC_GREEK_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BASIC_GREEK_BLOCK", (PyObject*)Haiku_Font_B_BASIC_GREEK_BLOCK);
	
	Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK->cpp_object = (unicode_block*)&B_GREEK_SYMBOLS_AND_COPTIC_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GREEK_SYMBOLS_AND_COPTIC_BLOCK", (PyObject*)Haiku_Font_B_GREEK_SYMBOLS_AND_COPTIC_BLOCK);
	
	Haiku_Font_B_CYRILLIC_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CYRILLIC_BLOCK->cpp_object = (unicode_block*)&B_CYRILLIC_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CYRILLIC_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CYRILLIC_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CYRILLIC_BLOCK", (PyObject*)Haiku_Font_B_CYRILLIC_BLOCK);
	
	Haiku_Font_B_ARMENIAN_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ARMENIAN_BLOCK->cpp_object = (unicode_block*)&B_ARMENIAN_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ARMENIAN_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ARMENIAN_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ARMENIAN_BLOCK", (PyObject*)Haiku_Font_B_ARMENIAN_BLOCK);
	
	Haiku_Font_B_BASIC_HEBREW_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BASIC_HEBREW_BLOCK->cpp_object = (unicode_block*)&B_BASIC_HEBREW_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BASIC_HEBREW_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BASIC_HEBREW_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BASIC_HEBREW_BLOCK", (PyObject*)Haiku_Font_B_BASIC_HEBREW_BLOCK);
	
	Haiku_Font_B_HEBREW_EXTENDED_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HEBREW_EXTENDED_BLOCK->cpp_object = (unicode_block*)&B_HEBREW_EXTENDED_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HEBREW_EXTENDED_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HEBREW_EXTENDED_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HEBREW_EXTENDED_BLOCK", (PyObject*)Haiku_Font_B_HEBREW_EXTENDED_BLOCK);
	
	Haiku_Font_B_BASIC_ARABIC_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BASIC_ARABIC_BLOCK->cpp_object = (unicode_block*)&B_BASIC_ARABIC_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BASIC_ARABIC_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BASIC_ARABIC_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BASIC_ARABIC_BLOCK", (PyObject*)Haiku_Font_B_BASIC_ARABIC_BLOCK);
	
	Haiku_Font_B_ARABIC_EXTENDED_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ARABIC_EXTENDED_BLOCK->cpp_object = (unicode_block*)&B_ARABIC_EXTENDED_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ARABIC_EXTENDED_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ARABIC_EXTENDED_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ARABIC_EXTENDED_BLOCK", (PyObject*)Haiku_Font_B_ARABIC_EXTENDED_BLOCK);
	
	Haiku_Font_B_DEVANAGARI_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_DEVANAGARI_BLOCK->cpp_object = (unicode_block*)&B_DEVANAGARI_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_DEVANAGARI_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_DEVANAGARI_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_DEVANAGARI_BLOCK", (PyObject*)Haiku_Font_B_DEVANAGARI_BLOCK);
	
	Haiku_Font_B_BENGALI_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BENGALI_BLOCK->cpp_object = (unicode_block*)&B_BENGALI_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BENGALI_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BENGALI_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BENGALI_BLOCK", (PyObject*)Haiku_Font_B_BENGALI_BLOCK);
	
	Haiku_Font_B_GURMUKHI_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GURMUKHI_BLOCK->cpp_object = (unicode_block*)&B_GURMUKHI_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GURMUKHI_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GURMUKHI_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GURMUKHI_BLOCK", (PyObject*)Haiku_Font_B_GURMUKHI_BLOCK);
	
	Haiku_Font_B_GUJARATI_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GUJARATI_BLOCK->cpp_object = (unicode_block*)&B_GUJARATI_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GUJARATI_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GUJARATI_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GUJARATI_BLOCK", (PyObject*)Haiku_Font_B_GUJARATI_BLOCK);
	
	Haiku_Font_B_ORIYA_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ORIYA_BLOCK->cpp_object = (unicode_block*)&B_ORIYA_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ORIYA_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ORIYA_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ORIYA_BLOCK", (PyObject*)Haiku_Font_B_ORIYA_BLOCK);
	
	Haiku_Font_B_TAMIL_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_TAMIL_BLOCK->cpp_object = (unicode_block*)&B_TAMIL_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_TAMIL_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_TAMIL_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TAMIL_BLOCK", (PyObject*)Haiku_Font_B_TAMIL_BLOCK);
	
	Haiku_Font_B_TELUGU_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_TELUGU_BLOCK->cpp_object = (unicode_block*)&B_TELUGU_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_TELUGU_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_TELUGU_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TELUGU_BLOCK", (PyObject*)Haiku_Font_B_TELUGU_BLOCK);
	
	Haiku_Font_B_KANNADA_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_KANNADA_BLOCK->cpp_object = (unicode_block*)&B_KANNADA_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_KANNADA_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_KANNADA_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_KANNADA_BLOCK", (PyObject*)Haiku_Font_B_KANNADA_BLOCK);
	
	Haiku_Font_B_MALAYALAM_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_MALAYALAM_BLOCK->cpp_object = (unicode_block*)&B_MALAYALAM_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_MALAYALAM_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_MALAYALAM_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_MALAYALAM_BLOCK", (PyObject*)Haiku_Font_B_MALAYALAM_BLOCK);
	
	Haiku_Font_B_THAI_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_THAI_BLOCK->cpp_object = (unicode_block*)&B_THAI_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_THAI_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_THAI_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_THAI_BLOCK", (PyObject*)Haiku_Font_B_THAI_BLOCK);
	
	Haiku_Font_B_LAO_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LAO_BLOCK->cpp_object = (unicode_block*)&B_LAO_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LAO_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LAO_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LAO_BLOCK", (PyObject*)Haiku_Font_B_LAO_BLOCK);
	
	Haiku_Font_B_BASIC_GEORGIAN_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BASIC_GEORGIAN_BLOCK->cpp_object = (unicode_block*)&B_BASIC_GEORGIAN_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BASIC_GEORGIAN_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BASIC_GEORGIAN_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BASIC_GEORGIAN_BLOCK", (PyObject*)Haiku_Font_B_BASIC_GEORGIAN_BLOCK);
	
	Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK->cpp_object = (unicode_block*)&B_GEORGIAN_EXTENDED_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GEORGIAN_EXTENDED_BLOCK", (PyObject*)Haiku_Font_B_GEORGIAN_EXTENDED_BLOCK);
	
	Haiku_Font_B_HANGUL_JAMO_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HANGUL_JAMO_BLOCK->cpp_object = (unicode_block*)&B_HANGUL_JAMO_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HANGUL_JAMO_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HANGUL_JAMO_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HANGUL_JAMO_BLOCK", (PyObject*)Haiku_Font_B_HANGUL_JAMO_BLOCK);
	
	Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK->cpp_object = (unicode_block*)&B_LATIN_EXTENDED_ADDITIONAL_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LATIN_EXTENDED_ADDITIONAL_BLOCK", (PyObject*)Haiku_Font_B_LATIN_EXTENDED_ADDITIONAL_BLOCK);
	
	Haiku_Font_B_GREEK_EXTENDED_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GREEK_EXTENDED_BLOCK->cpp_object = (unicode_block*)&B_GREEK_EXTENDED_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GREEK_EXTENDED_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GREEK_EXTENDED_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GREEK_EXTENDED_BLOCK", (PyObject*)Haiku_Font_B_GREEK_EXTENDED_BLOCK);
	
	Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK->cpp_object = (unicode_block*)&B_GENERAL_PUNCTUATION_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GENERAL_PUNCTUATION_BLOCK", (PyObject*)Haiku_Font_B_GENERAL_PUNCTUATION_BLOCK);
	
	Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK->cpp_object = (unicode_block*)&B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK", (PyObject*)Haiku_Font_B_SUPERSCRIPTS_AND_SUBSCRIPTS_BLOCK);
	
	Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK->cpp_object = (unicode_block*)&B_CURRENCY_SYMBOLS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CURRENCY_SYMBOLS_BLOCK", (PyObject*)Haiku_Font_B_CURRENCY_SYMBOLS_BLOCK);
	
	Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK->cpp_object = (unicode_block*)&B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK", (PyObject*)Haiku_Font_B_COMBINING_MARKS_FOR_SYMBOLS_BLOCK);
	
	Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK->cpp_object = (unicode_block*)&B_LETTERLIKE_SYMBOLS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LETTERLIKE_SYMBOLS_BLOCK", (PyObject*)Haiku_Font_B_LETTERLIKE_SYMBOLS_BLOCK);
	
	Haiku_Font_B_NUMBER_FORMS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_NUMBER_FORMS_BLOCK->cpp_object = (unicode_block*)&B_NUMBER_FORMS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_NUMBER_FORMS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_NUMBER_FORMS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_NUMBER_FORMS_BLOCK", (PyObject*)Haiku_Font_B_NUMBER_FORMS_BLOCK);
	
	Haiku_Font_B_ARROWS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ARROWS_BLOCK->cpp_object = (unicode_block*)&B_ARROWS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ARROWS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ARROWS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ARROWS_BLOCK", (PyObject*)Haiku_Font_B_ARROWS_BLOCK);
	
	Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK->cpp_object = (unicode_block*)&B_MATHEMATICAL_OPERATORS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_MATHEMATICAL_OPERATORS_BLOCK", (PyObject*)Haiku_Font_B_MATHEMATICAL_OPERATORS_BLOCK);
	
	Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK->cpp_object = (unicode_block*)&B_MISCELLANEOUS_TECHNICAL_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_MISCELLANEOUS_TECHNICAL_BLOCK", (PyObject*)Haiku_Font_B_MISCELLANEOUS_TECHNICAL_BLOCK);
	
	Haiku_Font_B_CONTROL_PICTURES_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CONTROL_PICTURES_BLOCK->cpp_object = (unicode_block*)&B_CONTROL_PICTURES_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CONTROL_PICTURES_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CONTROL_PICTURES_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CONTROL_PICTURES_BLOCK", (PyObject*)Haiku_Font_B_CONTROL_PICTURES_BLOCK);
	
	Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK->cpp_object = (unicode_block*)&B_OPTICAL_CHARACTER_RECOGNITION_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_OPTICAL_CHARACTER_RECOGNITION_BLOCK", (PyObject*)Haiku_Font_B_OPTICAL_CHARACTER_RECOGNITION_BLOCK);
	
	Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK->cpp_object = (unicode_block*)&B_ENCLOSED_ALPHANUMERICS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ENCLOSED_ALPHANUMERICS_BLOCK", (PyObject*)Haiku_Font_B_ENCLOSED_ALPHANUMERICS_BLOCK);
	
	Haiku_Font_B_BOX_DRAWING_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BOX_DRAWING_BLOCK->cpp_object = (unicode_block*)&B_BOX_DRAWING_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BOX_DRAWING_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BOX_DRAWING_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BOX_DRAWING_BLOCK", (PyObject*)Haiku_Font_B_BOX_DRAWING_BLOCK);
	
	Haiku_Font_B_BLOCK_ELEMENTS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BLOCK_ELEMENTS_BLOCK->cpp_object = (unicode_block*)&B_BLOCK_ELEMENTS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BLOCK_ELEMENTS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BLOCK_ELEMENTS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BLOCK_ELEMENTS_BLOCK", (PyObject*)Haiku_Font_B_BLOCK_ELEMENTS_BLOCK);
	
	Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK->cpp_object = (unicode_block*)&B_GEOMETRIC_SHAPES_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_GEOMETRIC_SHAPES_BLOCK", (PyObject*)Haiku_Font_B_GEOMETRIC_SHAPES_BLOCK);
	
	Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK->cpp_object = (unicode_block*)&B_MISCELLANEOUS_SYMBOLS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_MISCELLANEOUS_SYMBOLS_BLOCK", (PyObject*)Haiku_Font_B_MISCELLANEOUS_SYMBOLS_BLOCK);
	
	Haiku_Font_B_DINGBATS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_DINGBATS_BLOCK->cpp_object = (unicode_block*)&B_DINGBATS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_DINGBATS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_DINGBATS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_DINGBATS_BLOCK", (PyObject*)Haiku_Font_B_DINGBATS_BLOCK);
	
	Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK->cpp_object = (unicode_block*)&B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK", (PyObject*)Haiku_Font_B_CJK_SYMBOLS_AND_PUNCTUATION_BLOCK);
	
	Haiku_Font_B_HIRAGANA_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HIRAGANA_BLOCK->cpp_object = (unicode_block*)&B_HIRAGANA_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HIRAGANA_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HIRAGANA_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HIRAGANA_BLOCK", (PyObject*)Haiku_Font_B_HIRAGANA_BLOCK);
	
	Haiku_Font_B_KATAKANA_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_KATAKANA_BLOCK->cpp_object = (unicode_block*)&B_KATAKANA_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_KATAKANA_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_KATAKANA_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_KATAKANA_BLOCK", (PyObject*)Haiku_Font_B_KATAKANA_BLOCK);
	
	Haiku_Font_B_BOPOMOFO_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_BOPOMOFO_BLOCK->cpp_object = (unicode_block*)&B_BOPOMOFO_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_BOPOMOFO_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_BOPOMOFO_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_BOPOMOFO_BLOCK", (PyObject*)Haiku_Font_B_BOPOMOFO_BLOCK);
	
	Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK->cpp_object = (unicode_block*)&B_HANGUL_COMPATIBILITY_JAMO_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HANGUL_COMPATIBILITY_JAMO_BLOCK", (PyObject*)Haiku_Font_B_HANGUL_COMPATIBILITY_JAMO_BLOCK);
	
	Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK->cpp_object = (unicode_block*)&B_CJK_MISCELLANEOUS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_MISCELLANEOUS_BLOCK", (PyObject*)Haiku_Font_B_CJK_MISCELLANEOUS_BLOCK);
	
	Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK->cpp_object = (unicode_block*)&B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK", (PyObject*)Haiku_Font_B_ENCLOSED_CJK_LETTERS_AND_MONTHS_BLOCK);
	
	Haiku_Font_B_CJK_COMPATIBILITY_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_COMPATIBILITY_BLOCK->cpp_object = (unicode_block*)&B_CJK_COMPATIBILITY_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_COMPATIBILITY_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_COMPATIBILITY_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_COMPATIBILITY_BLOCK", (PyObject*)Haiku_Font_B_CJK_COMPATIBILITY_BLOCK);
	
	Haiku_Font_B_HANGUL_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HANGUL_BLOCK->cpp_object = (unicode_block*)&B_HANGUL_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HANGUL_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HANGUL_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HANGUL_BLOCK", (PyObject*)Haiku_Font_B_HANGUL_BLOCK);
	
	Haiku_Font_B_HIGH_SURROGATES_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HIGH_SURROGATES_BLOCK->cpp_object = (unicode_block*)&B_HIGH_SURROGATES_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HIGH_SURROGATES_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HIGH_SURROGATES_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HIGH_SURROGATES_BLOCK", (PyObject*)Haiku_Font_B_HIGH_SURROGATES_BLOCK);
	
	Haiku_Font_B_LOW_SURROGATES_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_LOW_SURROGATES_BLOCK->cpp_object = (unicode_block*)&B_LOW_SURROGATES_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_LOW_SURROGATES_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_LOW_SURROGATES_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_LOW_SURROGATES_BLOCK", (PyObject*)Haiku_Font_B_LOW_SURROGATES_BLOCK);
	
	Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK->cpp_object = (unicode_block*)&B_CJK_UNIFIED_IDEOGRAPHS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_UNIFIED_IDEOGRAPHS_BLOCK", (PyObject*)Haiku_Font_B_CJK_UNIFIED_IDEOGRAPHS_BLOCK);
	
	Haiku_Font_B_PRIVATE_USE_AREA_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_PRIVATE_USE_AREA_BLOCK->cpp_object = (unicode_block*)&B_PRIVATE_USE_AREA_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_PRIVATE_USE_AREA_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_PRIVATE_USE_AREA_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_PRIVATE_USE_AREA_BLOCK", (PyObject*)Haiku_Font_B_PRIVATE_USE_AREA_BLOCK);
	
	Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK->cpp_object = (unicode_block*)&B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK", (PyObject*)Haiku_Font_B_CJK_COMPATIBILITY_IDEOGRAPHS_BLOCK);
	
	Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK->cpp_object = (unicode_block*)&B_ALPHABETIC_PRESENTATION_FORMS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ALPHABETIC_PRESENTATION_FORMS_BLOCK", (PyObject*)Haiku_Font_B_ALPHABETIC_PRESENTATION_FORMS_BLOCK);
	
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK->cpp_object = (unicode_block*)&B_ARABIC_PRESENTATION_FORMS_A_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ARABIC_PRESENTATION_FORMS_A_BLOCK", (PyObject*)Haiku_Font_B_ARABIC_PRESENTATION_FORMS_A_BLOCK);
	
	Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK->cpp_object = (unicode_block*)&B_COMBINING_HALF_MARKS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_COMBINING_HALF_MARKS_BLOCK", (PyObject*)Haiku_Font_B_COMBINING_HALF_MARKS_BLOCK);
	
	Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK->cpp_object = (unicode_block*)&B_CJK_COMPATIBILITY_FORMS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_CJK_COMPATIBILITY_FORMS_BLOCK", (PyObject*)Haiku_Font_B_CJK_COMPATIBILITY_FORMS_BLOCK);
	
	Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK->cpp_object = (unicode_block*)&B_SMALL_FORM_VARIANTS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_SMALL_FORM_VARIANTS_BLOCK", (PyObject*)Haiku_Font_B_SMALL_FORM_VARIANTS_BLOCK);
	
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK->cpp_object = (unicode_block*)&B_ARABIC_PRESENTATION_FORMS_B_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_ARABIC_PRESENTATION_FORMS_B_BLOCK", (PyObject*)Haiku_Font_B_ARABIC_PRESENTATION_FORMS_B_BLOCK);
	
	Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK->cpp_object = (unicode_block*)&B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK", (PyObject*)Haiku_Font_B_HALFWIDTH_AND_FULLWIDTH_FORMS_BLOCK);
	
	Haiku_Font_B_SPECIALS_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_SPECIALS_BLOCK->cpp_object = (unicode_block*)&B_SPECIALS_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_SPECIALS_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_SPECIALS_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_SPECIALS_BLOCK", (PyObject*)Haiku_Font_B_SPECIALS_BLOCK);
	
	Haiku_Font_B_TIBETAN_BLOCK = (Haiku_unicode_block_Object*)Haiku_unicode_block_PyType.tp_alloc(&Haiku_unicode_block_PyType, 0);
	Haiku_Font_B_TIBETAN_BLOCK->cpp_object = (unicode_block*)&B_TIBETAN_BLOCK;
	// cannot delete this object; we do not own it
	Haiku_Font_B_TIBETAN_BLOCK->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Font_B_TIBETAN_BLOCK);
	PyModule_AddObject(Haiku_FontConstants_module, "B_TIBETAN_BLOCK", (PyObject*)Haiku_Font_B_TIBETAN_BLOCK);
	
	// Point: constants (in their own module)
	Haiku_PointConstants_module = Py_InitModule("Haiku.PointConstants", Haiku_PointConstants_PyMethods);
	if (Haiku_PointConstants_module == NULL)
		return;
	Py_INCREF(Haiku_PointConstants_module);
	PyModule_AddObject(Haiku_module, "PointConstants", Haiku_PointConstants_module);
	
	Haiku_Point_Object* Haiku_Point_B_ORIGIN;

	Haiku_Point_B_ORIGIN = (Haiku_Point_Object*)Haiku_Point_PyType.tp_alloc(&Haiku_Point_PyType, 0);
	Haiku_Point_B_ORIGIN->cpp_object = (BPoint*)&B_ORIGIN;
	// cannot delete this object; we do not own it
	Haiku_Point_B_ORIGIN->can_delete_cpp_object = false;
	Py_INCREF(Haiku_Point_B_ORIGIN);
	PyModule_AddObject(Haiku_PointConstants_module, "B_ORIGIN", (PyObject*)Haiku_Point_B_ORIGIN);
	
	// Query: constants (in their own module)
	Haiku_QueryConstants_module = Py_InitModule("Haiku.QueryConstants", Haiku_QueryConstants_PyMethods);
	if (Haiku_QueryConstants_module == NULL)
		return;
	Py_INCREF(Haiku_QueryConstants_module);
	PyModule_AddObject(Haiku_module, "QueryConstants", Haiku_QueryConstants_module);
	
	PyObject* Haiku_Query_B_INVALID_OP;
	PyObject* Haiku_Query_B_EQ;
	PyObject* Haiku_Query_B_GT;
	PyObject* Haiku_Query_B_GE;
	PyObject* Haiku_Query_B_LT;
	PyObject* Haiku_Query_B_LE;
	PyObject* Haiku_Query_B_NE;
	PyObject* Haiku_Query_B_CONTAINS;
	PyObject* Haiku_Query_B_BEGINS_WITH;
	PyObject* Haiku_Query_B_ENDS_WITH;
	PyObject* Haiku_Query_B_AND;
	PyObject* Haiku_Query_B_OR;
	PyObject* Haiku_Query_B_NOT;

	Haiku_Query_B_INVALID_OP = Py_BuildValue("i", B_INVALID_OP);
	Py_INCREF(Haiku_Query_B_INVALID_OP);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_INVALID_OP", Haiku_Query_B_INVALID_OP);
	
	Haiku_Query_B_EQ = Py_BuildValue("i", B_EQ);
	Py_INCREF(Haiku_Query_B_EQ);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_EQ", Haiku_Query_B_EQ);
	
	Haiku_Query_B_GT = Py_BuildValue("i", B_GT);
	Py_INCREF(Haiku_Query_B_GT);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_GT", Haiku_Query_B_GT);
	
	Haiku_Query_B_GE = Py_BuildValue("i", B_GE);
	Py_INCREF(Haiku_Query_B_GE);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_GE", Haiku_Query_B_GE);
	
	Haiku_Query_B_LT = Py_BuildValue("i", B_LT);
	Py_INCREF(Haiku_Query_B_LT);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_LT", Haiku_Query_B_LT);
	
	Haiku_Query_B_LE = Py_BuildValue("i", B_LE);
	Py_INCREF(Haiku_Query_B_LE);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_LE", Haiku_Query_B_LE);
	
	Haiku_Query_B_NE = Py_BuildValue("i", B_NE);
	Py_INCREF(Haiku_Query_B_NE);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_NE", Haiku_Query_B_NE);
	
	Haiku_Query_B_CONTAINS = Py_BuildValue("i", B_CONTAINS);
	Py_INCREF(Haiku_Query_B_CONTAINS);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_CONTAINS", Haiku_Query_B_CONTAINS);
	
	Haiku_Query_B_BEGINS_WITH = Py_BuildValue("i", B_BEGINS_WITH);
	Py_INCREF(Haiku_Query_B_BEGINS_WITH);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_BEGINS_WITH", Haiku_Query_B_BEGINS_WITH);
	
	Haiku_Query_B_ENDS_WITH = Py_BuildValue("i", B_ENDS_WITH);
	Py_INCREF(Haiku_Query_B_ENDS_WITH);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_ENDS_WITH", Haiku_Query_B_ENDS_WITH);
	
	Haiku_Query_B_AND = Py_BuildValue("i", B_AND);
	Py_INCREF(Haiku_Query_B_AND);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_AND", Haiku_Query_B_AND);
	
	Haiku_Query_B_OR = Py_BuildValue("i", B_OR);
	Py_INCREF(Haiku_Query_B_OR);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_OR", Haiku_Query_B_OR);
	
	Haiku_Query_B_NOT = Py_BuildValue("i", B_NOT);
	Py_INCREF(Haiku_Query_B_NOT);
	PyModule_AddObject(Haiku_QueryConstants_module, "B_NOT", Haiku_Query_B_NOT);
	
	// MimeType: constants (in their own module)
	Haiku_MimeTypeConstants_module = Py_InitModule("Haiku.MimeTypeConstants", Haiku_MimeTypeConstants_PyMethods);
	if (Haiku_MimeTypeConstants_module == NULL)
		return;
	Py_INCREF(Haiku_MimeTypeConstants_module);
	PyModule_AddObject(Haiku_module, "MimeTypeConstants", Haiku_MimeTypeConstants_module);
	
	PyObject* Haiku_MimeType_B_OPEN;
	PyObject* Haiku_MimeType_B_APP_MIME_TYPE;
	PyObject* Haiku_MimeType_B_PEF_APP_MIME_TYPE;
	PyObject* Haiku_MimeType_B_PE_APP_MIME_TYPE;
	PyObject* Haiku_MimeType_B_ELF_APP_MIME_TYPE;
	PyObject* Haiku_MimeType_B_RESOURCE_MIME_TYPE;
	PyObject* Haiku_MimeType_B_FILE_MIME_TYPE;
	PyObject* Haiku_MimeType_B_META_MIME_CHANGED;
	PyObject* Haiku_MimeType_B_ICON_CHANGED;
	PyObject* Haiku_MimeType_B_PREFERRED_APP_CHANGED;
	PyObject* Haiku_MimeType_B_ATTR_INFO_CHANGED;
	PyObject* Haiku_MimeType_B_FILE_EXTENSIONS_CHANGED;
	PyObject* Haiku_MimeType_B_SHORT_DESCRIPTION_CHANGED;
	PyObject* Haiku_MimeType_B_LONG_DESCRIPTION_CHANGED;
	PyObject* Haiku_MimeType_B_ICON_FOR_TYPE_CHANGED;
	PyObject* Haiku_MimeType_B_APP_HINT_CHANGED;
	PyObject* Haiku_MimeType_B_MIME_TYPE_CREATED;
	PyObject* Haiku_MimeType_B_MIME_TYPE_DELETED;
	PyObject* Haiku_MimeType_B_SNIFFER_RULE_CHANGED;
	PyObject* Haiku_MimeType_B_SUPPORTED_TYPES_CHANGED;
	PyObject* Haiku_MimeType_B_EVERYTHING_CHANGED;
	PyObject* Haiku_MimeType_B_META_MIME_MODIFIED;
	PyObject* Haiku_MimeType_B_META_MIME_DELETED;

	Haiku_MimeType_B_OPEN = Py_BuildValue("i", B_OPEN);
	Py_INCREF(Haiku_MimeType_B_OPEN);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_OPEN", Haiku_MimeType_B_OPEN);
	
	Haiku_MimeType_B_APP_MIME_TYPE = Py_BuildValue("s", B_APP_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_APP_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_APP_MIME_TYPE", Haiku_MimeType_B_APP_MIME_TYPE);
	
	Haiku_MimeType_B_PEF_APP_MIME_TYPE = Py_BuildValue("s", B_PEF_APP_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_PEF_APP_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_PEF_APP_MIME_TYPE", Haiku_MimeType_B_PEF_APP_MIME_TYPE);
	
	Haiku_MimeType_B_PE_APP_MIME_TYPE = Py_BuildValue("s", B_PE_APP_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_PE_APP_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_PE_APP_MIME_TYPE", Haiku_MimeType_B_PE_APP_MIME_TYPE);
	
	Haiku_MimeType_B_ELF_APP_MIME_TYPE = Py_BuildValue("s", B_ELF_APP_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_ELF_APP_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_ELF_APP_MIME_TYPE", Haiku_MimeType_B_ELF_APP_MIME_TYPE);
	
	Haiku_MimeType_B_RESOURCE_MIME_TYPE = Py_BuildValue("s", B_RESOURCE_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_RESOURCE_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_RESOURCE_MIME_TYPE", Haiku_MimeType_B_RESOURCE_MIME_TYPE);
	
	Haiku_MimeType_B_FILE_MIME_TYPE = Py_BuildValue("s", B_FILE_MIME_TYPE);
	Py_INCREF(Haiku_MimeType_B_FILE_MIME_TYPE);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_FILE_MIME_TYPE", Haiku_MimeType_B_FILE_MIME_TYPE);
	
	Haiku_MimeType_B_META_MIME_CHANGED = Py_BuildValue("i", B_META_MIME_CHANGED);
	Py_INCREF(Haiku_MimeType_B_META_MIME_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_META_MIME_CHANGED", Haiku_MimeType_B_META_MIME_CHANGED);
	
	Haiku_MimeType_B_ICON_CHANGED = Py_BuildValue("i", B_ICON_CHANGED);
	Py_INCREF(Haiku_MimeType_B_ICON_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_ICON_CHANGED", Haiku_MimeType_B_ICON_CHANGED);
	
	Haiku_MimeType_B_PREFERRED_APP_CHANGED = Py_BuildValue("i", B_PREFERRED_APP_CHANGED);
	Py_INCREF(Haiku_MimeType_B_PREFERRED_APP_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_PREFERRED_APP_CHANGED", Haiku_MimeType_B_PREFERRED_APP_CHANGED);
	
	Haiku_MimeType_B_ATTR_INFO_CHANGED = Py_BuildValue("i", B_ATTR_INFO_CHANGED);
	Py_INCREF(Haiku_MimeType_B_ATTR_INFO_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_ATTR_INFO_CHANGED", Haiku_MimeType_B_ATTR_INFO_CHANGED);
	
	Haiku_MimeType_B_FILE_EXTENSIONS_CHANGED = Py_BuildValue("i", B_FILE_EXTENSIONS_CHANGED);
	Py_INCREF(Haiku_MimeType_B_FILE_EXTENSIONS_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_FILE_EXTENSIONS_CHANGED", Haiku_MimeType_B_FILE_EXTENSIONS_CHANGED);
	
	Haiku_MimeType_B_SHORT_DESCRIPTION_CHANGED = Py_BuildValue("i", B_SHORT_DESCRIPTION_CHANGED);
	Py_INCREF(Haiku_MimeType_B_SHORT_DESCRIPTION_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_SHORT_DESCRIPTION_CHANGED", Haiku_MimeType_B_SHORT_DESCRIPTION_CHANGED);
	
	Haiku_MimeType_B_LONG_DESCRIPTION_CHANGED = Py_BuildValue("i", B_LONG_DESCRIPTION_CHANGED);
	Py_INCREF(Haiku_MimeType_B_LONG_DESCRIPTION_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_LONG_DESCRIPTION_CHANGED", Haiku_MimeType_B_LONG_DESCRIPTION_CHANGED);
	
	Haiku_MimeType_B_ICON_FOR_TYPE_CHANGED = Py_BuildValue("i", B_ICON_FOR_TYPE_CHANGED);
	Py_INCREF(Haiku_MimeType_B_ICON_FOR_TYPE_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_ICON_FOR_TYPE_CHANGED", Haiku_MimeType_B_ICON_FOR_TYPE_CHANGED);
	
	Haiku_MimeType_B_APP_HINT_CHANGED = Py_BuildValue("i", B_APP_HINT_CHANGED);
	Py_INCREF(Haiku_MimeType_B_APP_HINT_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_APP_HINT_CHANGED", Haiku_MimeType_B_APP_HINT_CHANGED);
	
	Haiku_MimeType_B_MIME_TYPE_CREATED = Py_BuildValue("i", B_MIME_TYPE_CREATED);
	Py_INCREF(Haiku_MimeType_B_MIME_TYPE_CREATED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_MIME_TYPE_CREATED", Haiku_MimeType_B_MIME_TYPE_CREATED);
	
	Haiku_MimeType_B_MIME_TYPE_DELETED = Py_BuildValue("i", B_MIME_TYPE_DELETED);
	Py_INCREF(Haiku_MimeType_B_MIME_TYPE_DELETED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_MIME_TYPE_DELETED", Haiku_MimeType_B_MIME_TYPE_DELETED);
	
	Haiku_MimeType_B_SNIFFER_RULE_CHANGED = Py_BuildValue("i", B_SNIFFER_RULE_CHANGED);
	Py_INCREF(Haiku_MimeType_B_SNIFFER_RULE_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_SNIFFER_RULE_CHANGED", Haiku_MimeType_B_SNIFFER_RULE_CHANGED);
	
	Haiku_MimeType_B_SUPPORTED_TYPES_CHANGED = Py_BuildValue("i", B_SUPPORTED_TYPES_CHANGED);
	Py_INCREF(Haiku_MimeType_B_SUPPORTED_TYPES_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_SUPPORTED_TYPES_CHANGED", Haiku_MimeType_B_SUPPORTED_TYPES_CHANGED);
	
	Haiku_MimeType_B_EVERYTHING_CHANGED = Py_BuildValue("i", B_EVERYTHING_CHANGED);
	Py_INCREF(Haiku_MimeType_B_EVERYTHING_CHANGED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_EVERYTHING_CHANGED", Haiku_MimeType_B_EVERYTHING_CHANGED);
	
	Haiku_MimeType_B_META_MIME_MODIFIED = Py_BuildValue("i", B_META_MIME_MODIFIED);
	Py_INCREF(Haiku_MimeType_B_META_MIME_MODIFIED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_META_MIME_MODIFIED", Haiku_MimeType_B_META_MIME_MODIFIED);
	
	Haiku_MimeType_B_META_MIME_DELETED = Py_BuildValue("i", B_META_MIME_DELETED);
	Py_INCREF(Haiku_MimeType_B_META_MIME_DELETED);
	PyModule_AddObject(Haiku_MimeTypeConstants_module, "B_META_MIME_DELETED", Haiku_MimeType_B_META_MIME_DELETED);
	
	// Unarchiver: constants (in their own module)
	Haiku_UnarchiverConstants_module = Py_InitModule("Haiku.UnarchiverConstants", Haiku_UnarchiverConstants_PyMethods);
	if (Haiku_UnarchiverConstants_module == NULL)
		return;
	Py_INCREF(Haiku_UnarchiverConstants_module);
	PyModule_AddObject(Haiku_module, "UnarchiverConstants", Haiku_UnarchiverConstants_module);
	
	PyObject* Haiku_Unarchiver_B_ASSUME_OWNERSHIP;
	PyObject* Haiku_Unarchiver_B_DONT_ASSUME_OWNERSHIP;

	Haiku_Unarchiver_B_ASSUME_OWNERSHIP = Py_BuildValue("i", BUnarchiver::B_ASSUME_OWNERSHIP);
	Py_INCREF(Haiku_Unarchiver_B_ASSUME_OWNERSHIP);
	PyModule_AddObject(Haiku_UnarchiverConstants_module, "B_ASSUME_OWNERSHIP", Haiku_Unarchiver_B_ASSUME_OWNERSHIP);
	
	Haiku_Unarchiver_B_DONT_ASSUME_OWNERSHIP = Py_BuildValue("i", BUnarchiver::B_DONT_ASSUME_OWNERSHIP);
	Py_INCREF(Haiku_Unarchiver_B_DONT_ASSUME_OWNERSHIP);
	PyModule_AddObject(Haiku_UnarchiverConstants_module, "B_DONT_ASSUME_OWNERSHIP", Haiku_Unarchiver_B_DONT_ASSUME_OWNERSHIP);
	
	// exception object
	HaikuError = PyErr_NewException((char*)"Haiku.error", NULL, NULL);
    Py_INCREF(HaikuError);
    PyModule_AddObject(Haiku_module, "error", HaikuError);
} //initHaiku

