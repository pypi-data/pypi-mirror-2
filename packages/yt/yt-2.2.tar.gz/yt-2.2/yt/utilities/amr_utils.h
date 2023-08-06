#ifndef __PYX_HAVE__yt__utilities__amr_utils
#define __PYX_HAVE__yt__utilities__amr_utils
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif

/* "/home/mturk/yt/yt-dist/yt/utilities/_amr_utils/png_writer.pyx":223
 * # http://stackoverflow.com/questions/1821806/how-to-encode-png-to-buffer-using-libpng
 * 
 * cdef public struct mem_encode:             # <<<<<<<<<<<<<<
 *     char *buffer
 *     size_t size
 */

struct mem_encode {
  char *buffer;
  size_t size;
};

#ifndef __PYX_HAVE_API__yt__utilities__amr_utils

__PYX_EXTERN_C DL_IMPORT(void) my_png_write_data(png_structp, png_bytep, size_t);
__PYX_EXTERN_C DL_IMPORT(void) my_png_flush(png_structp);

#endif

PyMODINIT_FUNC initamr_utils(void);

#endif
