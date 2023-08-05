/*
 * C extention module for escape_html(), encode_url(), and decode_url()
 *
 * Requirements: Python source code, C99 compiler.
 *
 * $Release: 0.0.1 $
 * $Copyright: Copyright(c) 2009-2010 kuwata-lab.com all rights reserved. $
 * $License: MIT License $
 */

#include <Python.h>


static char *
webext_encoding_cstr;

static PyObject *
webext_encoding;

static PyObject *
webext_get_encoding(PyObject *self, PyObject *args) {
    Py_INCREF(webext_encoding);
    return webext_encoding;
}

static PyObject *
webext_set_encoding(PyObject *self, PyObject *args) {
    /// check argument
    PyObject *arg;
    if (! PyArg_ParseTuple(args, "S", &arg)) {
        return NULL;
    }
    /// set encoding
    Py_DECREF(webext_encoding);
    Py_INCREF(arg);
    webext_encoding = arg;
    webext_encoding_cstr = PyString_AsString(arg);
    /// return None
    Py_RETURN_NONE;
}



static PyObject *
webext_empty_str;     // initialized in webextinit()


static PyObject *
webext_to_str(PyObject *self, PyObject *args) {
    /// check argument
    PyObject *arg;
    if (! PyArg_ParseTuple(args, "O", &arg)) {
        return NULL;
    }
    /// return empty string if None
    if (arg == Py_None) {
        Py_INCREF(webext_empty_str);
        return webext_empty_str;
    }
    /// return arg as is when str
    if (arg->ob_type == &PyString_Type) {
        Py_INCREF(arg);   // IMPORTANT!
        return arg;
    }
    /// convert into str when unicode
    if (arg->ob_type == &PyUnicode_Type) {
        return PyUnicode_AsEncodedString(arg, webext_encoding_cstr, NULL);
    }
    /// return str(arg)
    return PyObject_Str(arg);
}


static PyObject *
webext_escape_html(PyObject *self, PyObject *args) {
    /// check argument
    PyObject *arg;
    if (! PyArg_ParseTuple(args, "O", &arg)) {
        return NULL;
    }
    /// return empty string if None
    if (arg == Py_None) {
        Py_INCREF(webext_empty_str);
        return webext_empty_str;
    }
    /// convert into str
    PyObject *str_obj;
    PyTypeObject *type = arg->ob_type;
    if (type == &PyString_Type) {
        str_obj = arg;
        Py_INCREF(str_obj);    // IMPORTANT!
    }
    else if (type == &PyUnicode_Type) {
        str_obj = PyUnicode_AsEncodedString(arg, webext_encoding_cstr, NULL);
        if (str_obj == NULL) return NULL;
    }
    else if (type == &PyInt_Type || type == &PyFloat_Type) {
        return PyObject_Str(arg);
    }
    else {
        str_obj = PyObject_Str(arg);
        if (str_obj == NULL) return NULL;
    }
    assert(str_obj != NULL);
    assert(str_obj->ob_type == &PyString_Type);
    /// get C string and length
    char *str;
    int len;
    //PyString_AsStringAndSize(str, &s, &len);    // abort. why?
    str = PyString_AS_STRING(str_obj);   // or PyString_AsString(str_obj)
    len = PyString_GET_SIZE(str_obj);    // or PyString_Size(str_obj)
    /// calculate delta size
    char *end = str + len;
    char *s = str;
    int  delta = 0;
    while (s < end) {
        switch (*s++) {
        case '&':  delta += 4;  break;  // len("&amp;")  - 1 == 4
        case '<':  delta += 3;  break;  // len("&lt;")   - 1 == 3
        case '>':  delta += 3;  break;  // len("&gt;")   - 1 == 3
        case '"':  delta += 5;  break;  // len("&quot;") - 1 == 5
#ifdef ENT_QUOTES
        case '\'': delta += 5;  break;  // len("&#039;") - 1 == 5
#endif
        default:  break;
        }
    }
    /// if no html special chars found, return 1st argument
    if (delta == 0) {
        //return PySequence_GetItem(args, 0);
        return str_obj;
    }
    /// copy string
    char *str2 = (char *)alloca(len + delta + 1);
    s = str;
    char *t = str2;
    while (s < end) {
        int c = *s++;
        switch (c) {
        case '&':  *t++='&'; *t++='a'; *t++='m'; *t++='p'; *t++=';';  break;
        case '<':  *t++='&'; *t++='l'; *t++='t'; *t++=';';            break;
        case '>':  *t++='&'; *t++='g'; *t++='t'; *t++=';';            break;
        case '"':  *t++='&'; *t++='q'; *t++='u'; *t++='o'; *t++='t'; *t++=';'; break;
#ifdef ENT_QUOTES
        case '\'': *t++='&'; *t++='#'; *t++='0'; *t++='3'; *t++='9'; *t++=';'; break;
#endif
        default :  *t++ = c;  break;
        }
    }
    assert(*s == '\0');
    *s = '\0';
    /// return new str object
    Py_DECREF(str_obj);
    //return Py_BuildValue("s", str2);
    return PyString_FromStringAndSize(str2, len + delta);
}


static char *
webext_doc = "C extention module for escape_html()\n";


static PyMethodDef
webext_methods[] = {
    { "to_str",
      webext_to_str,
      METH_VARARGS,
      "cnvert to str\n" },
    { "escape_html",
      webext_escape_html,
      METH_VARARGS,
      "escape html special chars.\n" },
    { "escape",
      webext_escape_html,
      METH_VARARGS,
      "alias to escape_html().\n" },
    { "get_encoding",
      webext_get_encoding,
      METH_VARARGS,
      "get encoding for escape_html() and to_st().\n" },
    { "set_encoding",
      webext_set_encoding,
      METH_VARARGS,
      "set encoding for escape_html() and to_st().\n" },
    { NULL, NULL, 0, NULL },
};


PyMODINIT_FUNC
initwebext(void) {   // 'init' + module-name
    /// initialize module
    PyObject *mod = Py_InitModule3("webext", webext_methods, webext_doc);
    /// empty string
    webext_empty_str = PyString_FromString("");  // or Py_BuildValue("s", "") ?
    //PyObject_SetAttrString(mod, "empty_str", webext_empty_str);
    ///
    webext_encoding_cstr = "utf8";
    webext_encoding = PyString_FromString(webext_encoding_cstr);
}
