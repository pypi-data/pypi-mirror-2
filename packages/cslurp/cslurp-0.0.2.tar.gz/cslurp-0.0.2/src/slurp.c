#include "slurp.h"

int th_match(char *string, char *pattern) {
  int status;
  regex_t re;
  if(regcomp(&re, pattern, REG_EXTENDED|REG_NOSUB) != 0) { return 0; }
  status = regexec(&re, string, (size_t)0, NULL, 0);
  regfree(&re);
  if(status != 0) 
	return 0;
  return 1;
}

/* Lets keep this around until we're sure we won't need it */
/*
static PyObject *
matches(PyObject *self, PyObject *args) {
	const char *string, *pattern;

	if (!PyArg_ParseTuple(args, "ss", &string, &pattern))
		return NULL;

	return Py_BuildValue("i", match(string, pattern));
}

static PyMethodDef cslurpMethods[] = {
    {"matches",  matches, METH_VARARGS,
     "Determine if string matches pattern."},
    {NULL, NULL, 0, NULL} 
};

PyMODINIT_FUNC
initcslurp(void)
{
    (void) Py_InitModule("thci.ext.cslurp", cslurpMethods);
}

int main(int argc, char *argv[]) {
	if (argc < 3) {
		printf("%s <STRING> <PATTERN>\n", argv[0]);
		exit(-1);
	}
	if (match(argv[1], argv[2]) == 1) {
		printf("Match found\n");
	} else {
		printf("No match found\n");
	}
	return 0;
}  */
