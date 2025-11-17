#ifndef RAF_UTILS_H
#define RAF_UTILS_H

#include <stddef.h>

void raf_info(const char *fmt, ...);
void raf_fatal(const char *fmt, ...);
int raf_read_file(const char *path, void **out_buf, size_t *out_sz);
int raf_write_on_diff(const char *path, const void *buf, size_t sz);

#endif
