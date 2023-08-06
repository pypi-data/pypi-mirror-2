/*
 * Automatically generated file
 */

#include <Application.h>
#include <Clipboard.h>
#include <Cursor.h>
#include <Handler.h>
#include <Invoker.h>
#include <Looper.h>
#include <Message.h>
#include <Messenger.h>
#include <Application.h>
#include <Alert.h>
#include <Bitmap.h>
#include <Box.h>
#include <Button.h>
#include <ChannelControl.h>
#include <ChannelSlider.h>
#include <CheckBox.h>
#include <ColorControl.h>
#include <Control.h>
#include <Font.h>
#include <Gradient.h>
#include <GradientConic.h>
#include <GradientDiamond.h>
#include <GradientLinear.h>
#include <GradientRadial.h>
#include <GradientRadialFocus.h>
#include <GraphicsDefs.h>
#include <IconUtils.h>
#include <InterfaceDefs.h>
#include <Menu.h>
#include <ListItem.h>
#include <ListView.h>
#include <MenuBar.h>
#include <MenuField.h>
#include <MenuItem.h>
#include <OptionControl.h>
#include <OptionPopUp.h>
#include <OutlineListView.h>
#include <Picture.h>
#include <PictureButton.h>
#include <Point.h>
#include <Polygon.h>
#include <PopUpMenu.h>
#include <RadioButton.h>
#include <Rect.h>
#include <Screen.h>
#include <ScrollBar.h>
#include <ScrollView.h>
#include <SeparatorItem.h>
#include <Shape.h>
#include <Slider.h>
#include <StatusBar.h>
#include <StringItem.h>
#include <StringView.h>
#include <TabView.h>
#include <TextControl.h>
#include <TextView.h>
#include <UnicodeBlockObjects.h>
#include <View.h>
#include <Window.h>
#include <Entry.h>
#include <EntryList.h>
#include <FilePanel.h>
#include <FindDirectory.h>
#include <Mime.h>
#include <MimeType.h>
#include <Node.h>
#include <NodeInfo.h>
#include <NodeMonitor.h>
#include <MimeType.h>
#include <Path.h>
#include <Query.h>
#include <Statable.h>
#include <StorageDefs.h>
#include <Volume.h>
#include <VolumeRoster.h>
#include <fs_attr.h>
#include <compat/sys/stat.h>
#include <Beep.h>
#include <Archivable.h>
#include <Errors.h>
#include <TypeConstants.h>

static PyObject* python_main;
static PyObject* main_dict;
static PyObject* HaikuError;

class Custom_BApplication;
class Custom_BWindow;
class Custom_BTextView;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Archivable_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BArchivable* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Archivable_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Point_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPoint* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Point_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Rect_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BRect* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Rect_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Window_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BWindow* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Window_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_entry_ref_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    entry_ref* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_entry_ref_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Clipboard_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BClipboard* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Clipboard_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Cursor_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BCursor* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Cursor_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Handler_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BHandler* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Handler_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Invoker_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BInvoker* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Invoker_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Message_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMessage* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Message_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Messenger_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMessenger* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Messenger_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Node_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BNode* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Node_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Menu_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMenu* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Menu_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Looper_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BLooper* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Looper_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Application_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BApplication* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Application_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_CustomApplication_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    Custom_BApplication* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_CustomApplication_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_CustomWindow_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    Custom_BWindow* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_CustomWindow_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Alert_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BAlert* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Alert_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_View_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_View_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Box_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BBox* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Box_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Control_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BControl* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Control_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Button_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BButton* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Button_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_CheckBox_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BCheckBox* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_CheckBox_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ColorControl_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BColorControl* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ColorControl_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_PictureButton_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPictureButton* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_PictureButton_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_RadioButton_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BRadioButton* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_RadioButton_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Slider_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BSlider* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Slider_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_TextControl_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BTextControl* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_TextControl_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ListView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BListView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ListView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_OutlineListView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BOutlineListView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_OutlineListView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_menu_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    menu_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_menu_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_MenuBar_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMenuBar* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_MenuBar_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_PopUpMenu_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPopUpMenu* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_PopUpMenu_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_MenuField_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMenuField* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_MenuField_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ScrollBar_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BScrollBar* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ScrollBar_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ScrollView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BScrollView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ScrollView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_StatusBar_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BStatusBar* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_StatusBar_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_StringView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BStringView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_StringView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_TabView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BTabView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_TabView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Tab_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BTab* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Tab_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_TextView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BTextView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_TextView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_CustomTextView_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    Custom_BTextView* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_CustomTextView_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_text_run_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    text_run* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_text_run_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_text_run_array_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    text_run_array* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_text_run_array_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_MenuItem_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMenuItem* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_MenuItem_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_SeparatorItem_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BSeparatorItem* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_SeparatorItem_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ListItem_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BListItem* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ListItem_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_StringItem_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BStringItem* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_StringItem_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Font_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BFont* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Font_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_unicode_block_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    unicode_block* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_unicode_block_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_edge_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    edge_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_edge_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_font_height_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    font_height* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_font_height_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_escapement_delta_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    escapement_delta* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_escapement_delta_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_font_cache_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    font_cache_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_font_cache_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_tuned_font_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    tuned_font_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_tuned_font_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Picture_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPicture* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Picture_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Polygon_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPolygon* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Polygon_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Screen_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BScreen* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Screen_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Shape_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BShape* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Shape_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_ShapeIterator_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BShapeIterator* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_ShapeIterator_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_key_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    key_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_key_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_key_map_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    key_map* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_key_map_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_mouse_map_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    mouse_map* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_mouse_map_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_scroll_bar_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    scroll_bar_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_scroll_bar_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_pattern_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    pattern* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_pattern_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_rgb_color_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    rgb_color* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_rgb_color_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_color_map_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    color_map* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_color_map_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_overlay_rect_limits_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    overlay_rect_limits* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_overlay_rect_limits_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_overlay_restrictions_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    overlay_restrictions* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_overlay_restrictions_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_screen_id_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    screen_id* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_screen_id_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_EntryList_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BEntryList* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_EntryList_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Query_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BQuery* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Query_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_MimeType_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BMimeType* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_MimeType_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_NodeInfo_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BNodeInfo* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_NodeInfo_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Path_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BPath* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Path_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Statable_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BStatable* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Statable_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Entry_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BEntry* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Entry_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_node_ref_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    node_ref* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_node_ref_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Volume_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BVolume* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Volume_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_VolumeRoster_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BVolumeRoster* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_VolumeRoster_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_dirent_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    dirent* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_dirent_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_stat_beos_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    stat_beos* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_stat_beos_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_stat_beos_time_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    stat_beos_time* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_stat_beos_time_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_stat_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    struct stat* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_stat_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_timespec_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    timespec* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_timespec_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_attr_info_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    attr_info* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_attr_info_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Archiver_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BArchiver* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Archiver_Object;

// make a default version here so it's available early
// we'll fill in the values in another file
static PyTypeObject Haiku_Unarchiver_PyType = { PyObject_HEAD_INIT(NULL) };
typedef struct {
    PyObject_HEAD
    BUnarchiver* cpp_object;
	bool  can_delete_cpp_object;
} Haiku_Unarchiver_Object;

