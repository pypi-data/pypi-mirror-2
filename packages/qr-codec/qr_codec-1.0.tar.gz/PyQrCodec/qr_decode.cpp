#include <Python.h>

#include <stdio.h>
#include <highgui.h>
#include "decodeqr.h"

static PyObject *qr_decode(PyObject *self, PyObject *args)
{
    char *filename;
    int temp;
    char *buffer;
    FILE *imagefile;

    if (!PyArg_ParseTuple(args, "s", &filename))
        return NULL;
    if ((imagefile = fopen(filename,"r")) == NULL)
        return NULL;
    fclose(imagefile);

    //cvNamedWindow("src",1);
    // load image
    //printf("Loading image..\n");
    //return Py_BuildValue("s", filename);
    IplImage *src = cvLoadImage(filename,1);
    //printf("image loaded\n");
    //cvShowImage("src",src);
    // show version info
    //printf("libdecodeqr version %s\n",qr_decoder_version());
    // initialize
    //printf("Initializing decoder..\n");
    QrDecoderHandle decoder=qr_decoder_open();
    //printf("decoder initialized\n");
    // do decode using default parameter
    //printf("Decoding image..\n");
    int stat = qr_decoder_decode_image(decoder,src);
    //printf("STATUS=%d\n",stat);
    //printf("image decoded\n");
    //printf("Getting QR code header..\n");
    // get QR code header
    QrCodeHeader header;
    //printf("QR header instance created\n");
    temp = qr_decoder_get_header(decoder,&header);
    if(temp)
    {
        // get QR code text
        // To null terminate, a buffer size is larger than body size.
        char *buf = new char[header.byte_size+1];
        //printf("got QR header\n");
        //printf("Getting QR body..\n");
        qr_decoder_get_body(decoder,(unsigned char *)buf,header.byte_size+1);
        //printf("got QR body\n");
        //printf("%s\n",buf);
        buffer = buf;
    }
    else
    {
        char *buf = new char[header.byte_size+1];
        buf = "";
        //printf("%s\n",buf);
        buffer = buf;
    }

    // finalize
    //printf("Destroying decoder..\n");
    qr_decoder_close(decoder);

    //printf("Destroying all open windows..\n");
    cvDestroyAllWindows();
    //printf("Releasing image..\n");
    cvReleaseImage(&src);

    //printf("Returning..\n");
    return Py_BuildValue("(is)", stat,buffer);
};

static PyMethodDef Qr_decodeMethods[] =
{
    {"decode",  qr_decode, METH_VARARGS,
     "Spots and decodes QR code from given image. Input is a string representing the image filename."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initqr_decode(void)
{
    (void) Py_InitModule("qr_decode", Qr_decodeMethods);
}


