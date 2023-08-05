/*
 * Consistent Overhead Byte Stuffing (COBS)
 *
 * Python C extension for COBS encoding and decoding functions.
 *
 * Copyright (c) 2010 Craig McQueen
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */


/*****************************************************************************
 * Includes
 ****************************************************************************/

// Force Py_ssize_t to be used for s# conversions.
#define PY_SSIZE_T_CLEAN
#include <Python.h>


/*****************************************************************************
 * Defines
 ****************************************************************************/

// Make compatible with previous Python versions
#if PY_VERSION_HEX < 0x02050000
typedef int Py_ssize_t;
#define PY_SSIZE_T_MAX INT_MAX
#define PY_SSIZE_T_MIN INT_MIN
#endif


#ifndef FALSE
#define FALSE       (0)
#endif

#ifndef TRUE
#define TRUE        (!FALSE)
#endif


#define COBS_ENCODE_DST_BUF_LEN_MAX(SRC_LEN)            ((SRC_LEN) + ((SRC_LEN)/254u) + 1)
#define COBS_DECODE_DST_BUF_LEN_MAX(SRC_LEN)            (((SRC_LEN) <= 1) ? 1 : ((SRC_LEN) - 1))


/*****************************************************************************
 * Variables
 ****************************************************************************/

/*
 * cobs.DecodeError exception class.
 */
static PyObject *CobsDecodeError;


/*****************************************************************************
 * Functions
 ****************************************************************************/

/*
 * Encode
 */
PyDoc_STRVAR(cobsencode__doc__,
"Encode a string using Consistent Overhead Byte Stuffing (COBS).\n"
"\n"
"Input is any byte string. Output is also a byte string.\n"
"\n"
"Encoding guarantees no zero bytes in the output. The output\n"
"string will be expanded slightly, by a predictable amount.\n"
"\n"
"An empty string is encoded to '\\x01'.");

static PyObject*
cobsencode(PyObject* self, PyObject* args)
{
    const char *    src_ptr;
    Py_ssize_t      src_len;
    const char *    src_end_ptr;
    char *          dst_buf_ptr;
    char *          dst_code_write_ptr;
    char *          dst_write_ptr;
    char            src_byte;
    unsigned char   search_len;
    char            final_zero;
    PyObject *      dst_py_obj_ptr;


    if (!PyArg_ParseTuple(args, "s#:in_bytes", &src_ptr, &src_len))
    {
        return NULL;
    }
    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyString_FromStringAndSize(NULL, COBS_ENCODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyString_AsString(dst_py_obj_ptr);

    /* Encode */
    dst_code_write_ptr  = dst_buf_ptr;
    dst_write_ptr = dst_code_write_ptr + 1;
    search_len = 1;
    final_zero = TRUE;

    /* Iterate over the source bytes */
    while (src_ptr < src_end_ptr)
    {
        src_byte = *src_ptr++;
        if (src_byte == 0)
        {
            /* We found a zero byte */
            *dst_code_write_ptr = (char) search_len;
            dst_code_write_ptr = dst_write_ptr++;
            search_len = 1;
            final_zero = TRUE;
        }
        else
        {
            /* Copy the non-zero byte to the destination buffer */
            *dst_write_ptr++ = src_byte;
            search_len++;
            if (search_len == 0xFF)
            {
                /* We have a long string of non-zero bytes */
                *dst_code_write_ptr = (char) search_len;
                dst_code_write_ptr = dst_write_ptr++;
                search_len = 1;
                final_zero = FALSE;
            }
        }
    }

    /* We've reached the end of the source data (or possibly run out of output buffer)
     * Finalise the remaining output. In particular, write the code (length) byte.
     * Update the pointer to calculate the final output length.
     */
    if ((search_len > 1) || (final_zero != FALSE))
    {
        *dst_code_write_ptr = (char) search_len;
        dst_code_write_ptr = dst_write_ptr;
    }

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyString_Resize(&dst_py_obj_ptr, dst_code_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*
 * Decode
 */
PyDoc_STRVAR(cobsdecode__doc__,
"Decode a string using Consistent Overhead Byte Stuffing (COBS).\n"
"\n"
"Input should be a byte string that has been COBS encoded. Output\n"
"is also a byte string.\n"
"\n"
"A cobs.DecodeError exception may be raised if the encoded data\n"
"is invalid.");

static PyObject*
cobsdecode(PyObject* self, PyObject* args)
{
    const char *            src_ptr;
    Py_ssize_t              src_len;
    const char *            src_end_ptr;
    char *                  dst_buf_ptr;
    char *                  dst_write_ptr;
    Py_ssize_t              remaining_bytes;
    unsigned char           len_code;
    unsigned char           src_byte;
    unsigned char           i;
    PyObject *              dst_py_obj_ptr;


    if (!PyArg_ParseTuple(args, "s#:in_bytes", &src_ptr, &src_len))
    {
        return NULL;
    }
    src_end_ptr = src_ptr + src_len;

    /* Make an output string */
    dst_py_obj_ptr = PyString_FromStringAndSize(NULL, COBS_DECODE_DST_BUF_LEN_MAX(src_len));
    if (dst_py_obj_ptr == NULL)
    {
        return NULL;
    }
    dst_buf_ptr = PyString_AsString(dst_py_obj_ptr);

    /* Decode */
    dst_write_ptr = dst_buf_ptr;

    if (src_len != 0)
    {
        for (;;)
        {
            len_code = (unsigned char) *src_ptr++;
            if (len_code == 0)
            {
                Py_DECREF(dst_py_obj_ptr);
                PyErr_SetString(CobsDecodeError, "zero byte found in input");
                return NULL;
            }
            len_code--;

            remaining_bytes = src_end_ptr - src_ptr;
            if (len_code > remaining_bytes)
            {
                Py_DECREF(dst_py_obj_ptr);
                PyErr_SetString(CobsDecodeError, "not enough input bytes for length code");
                return NULL;
            }

            for (i = len_code; i != 0; i--)
            {
                src_byte = *src_ptr++;
                if (src_byte == 0)
                {
                    Py_DECREF(dst_py_obj_ptr);
                    PyErr_SetString(CobsDecodeError, "zero byte found in input");
                    return NULL;
                }
                *dst_write_ptr++ = src_byte;
            }

            if (src_ptr >= src_end_ptr)
            {
                break;
            }

            /* Add a zero to the end */
            if (len_code != 0xFE)
            {
                *dst_write_ptr++ = 0;
            }
        }
    }

    /* Calculate the output length, from the value of dst_code_write_ptr */
    _PyString_Resize(&dst_py_obj_ptr, dst_write_ptr - dst_buf_ptr);

    return dst_py_obj_ptr;
}


/*****************************************************************************
 * Module definitions
 ****************************************************************************/

PyDoc_STRVAR(module__doc__,
"Consistent Overhead Byte Stuffing (COBS)"
);

static PyMethodDef methodTable[] =
{
    { "encode", cobsencode, METH_VARARGS, cobsencode__doc__ },
    { "decode", cobsdecode, METH_VARARGS, cobsdecode__doc__ },
    { NULL, NULL, 0, NULL }
};


/*****************************************************************************
 * Module initialisation
 ****************************************************************************/

PyMODINIT_FUNC
init_cobsext(void)
{
    PyObject *m;

    /* Initialise cobs module C extension cobs._cobsext */
    m = Py_InitModule3("_cobsext", methodTable, module__doc__);
    if (m == NULL)
        return;

    /* Initialise cobs.DecodeError exception class. */
    CobsDecodeError = PyErr_NewException("cobs.DecodeError", NULL, NULL);
    Py_INCREF(CobsDecodeError);
    PyModule_AddObject(m, "DecodeError", CobsDecodeError);
}

