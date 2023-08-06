/*
    NodeTree - Python XML stream parsing
    Copyright (C) 2010 Arc Riley

    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program; if not, see http://www.gnu.org/licenses
*/

#include "nodetree.h"

static char
nodetree_doc[] = "NodeTree - Python XML stream parsing\n"
"\n"
"    Most XML libraries fit into one of two categories; they either parse XML\n"
"    streams with callbacks for each event encountered but leave it to the user\n"
"    to store and organize these events (such as expat or SAX), or they parse\n"
"    the entire XML document into memory in one batch and return a handle to\n"
"    the document's root element only after its finished (DOM and ElementTree).\n"
"\n"
"    While the latter is much easier to work with, it also requires that the\n"
"    entire XML stream be available before any of it can be processed and must\n"
"    load the entire stream into memory, even when only a piece of it needs to\n"
"    be evaluated at a time.\n"
"\n"
"    With NodeTree we seek a hybrid of these two techniques.  Callbacks can be\n"
"    set for virtually every stage of processing, but what is returned is the\n"
"    (possibly incomplete) object being processed.  Nodes which have been fully\n"
"    processed can be removed from the tree in processing to save memory and\n"
"    the user can even specify an alternative class to create child nodes of an\n"
"    element.  The goal is a clean, Pythonic API usable for the most basic\n"
"    to the most advanced XML processing.\n"
"\n"
"    NodeTree is similar to the familiar ElementTree API with a few notable\n"
"    differences:\n"
"\n"
"      * Element.tag has been renamed to Element.name\n"
"\n"
"      * Element attributes are a dictionary at Element.attributes\n"
"\n"
"      * Elements are sequences of their children\n"
"\n"
"      * Text inside an element is a child node, not Element.text property,\n"
"        so the order of text and child elements is preserved and available.\n"
"        Text nodes are strings, so you can just Element.append('text').\n"
"\n"
"      * Nodes work by duck typing and can be freely mixed from other XML\n"
"        libraries including (with very little work) ElementTree or DOM\n"
"\n"
"      * All nodes can be converted to XML strings with their __str__ method\n"
"\n";

static char
nodetree_credits[] = "Copyright (C) 2010 Arc Riley\n"
"\n"
"    This program is free software; you can redistribute it and/or modify\n"
"    it under the terms of the GNU Lesser General Public License as published\n"
"    by the Free Software Foundation, either version 3 of the License, or\n"
"    (at your option) any later version.\n"
"\n"
"    This program is distributed in the hope that it will be useful,\n"
"    but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
"    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n"
"    GNU Affero General Public License for more details.\n"
"\n"
"    You should have received a copy of the GNU Lesser General Public License\n"
"    along with this program; if not, see http://www.gnu.org/licenses\n"
"\n";


static PyMethodDef nodetree_methods[] = {
    {NULL, NULL}
};

#if PY_MAJOR_VERSION == 3
static struct PyModuleDef nodetree_module = {
    PyModuleDef_HEAD_INIT,
    "nodetree",                        /*m_name*/
    nodetree_doc,                      /*m_doc*/
    0,                                 /*m_size*/
    nodetree_methods,                  /*m_methods*/
    NULL,                              /*m_reload*/
    NULL,                              /*m_traverse*/
    NULL,                              /*m_clear*/
    NULL                               /*m_free*/
};

PyMODINIT_FUNC
PyInit_nodetree(void) {

# else // Python 2.x
void
initnodetree(void)
{
#endif

    PyObject *module, *dict, *Py_module_info;

#if PY_MAJOR_VERSION == 3
    module = PyModule_Create(&nodetree_module);
    dict = PyModule_GetDict(module);
    
#else // Python 2.x init module, must also set __doc__ manually
    module = Py_InitModule3("nodetree", nodetree_methods, nodetree_doc);
    dict = PyModule_GetDict(module);
#endif

    PyModule_AddStringConstant(module, "__credits__", nodetree_credits);
    PyModule_AddStringConstant(module, "__version__", NODETREE_VERSION);

    if (PyErr_Occurred())
        PyErr_SetString(PyExc_ImportError, "nodetree: init failed");

#if PY_MAJOR_VERSION == 3
    else
        return module;
#endif
}

