#define PY_SSIZE_T_CLEAN 1

#include <Python.h>
#include <string.h>

static PyObject* xor(PyObject* self, PyObject* args) {
  const char* source;
  const char* code;
  Py_ssize_t source_len;
  Py_ssize_t code_len;
  if (!PyArg_ParseTuple(args, "s#s#", &source, &source_len,
                        &code, &code_len)) {
    return NULL;
  }
  char* result = malloc(source_len);
  Py_ssize_t si = 0;
  Py_ssize_t ci = 0;
  for (; si < source_len; si ++, ci ++) {
    if (ci == code_len) {
      ci = 0;
    }
    result[si] = source[si] ^ code[ci];
  }
  PyObject* res = Py_BuildValue("s#", result, source_len);
  free(result);
  result = NULL;
  return res;
}

static PyMethodDef cxorMethods[] = {
  {"xor", xor, METH_VARARGS, "fast xor"},
  {NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC initcxor(void) {
  (void) Py_InitModule("cxor", cxorMethods);
}
