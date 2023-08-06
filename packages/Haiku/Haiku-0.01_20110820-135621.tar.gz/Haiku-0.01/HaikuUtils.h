/*
 * Automatically generated file
 */
 
// comment this out to disallow debugging
#define DEBUGOK

#ifdef DEBUGOK
#define DEBUGME(LEVEL, PATTERN, ...) debug_me(LEVEL, __FILE__, __LINE__, PATTERN, ##__VA_ARGS__)
#else
#define DEBUGME(LEVEL, PATTERN, ...)
#endif

int debug_level = 0;

void debug_me(int level, const char* file, int line, const char* pattern, ...);

char** PyList2CharArray(PyObject* arg, int* count);
PyObject* CharArray2PyList(char** var, int count);
void PyString2Char(PyObject* arg, void* var, int num_chars, int size);
PyObject* Char2PyString(const void* var, int num_chars, int size);
