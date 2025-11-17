#define _GNU_SOURCE
#include "raf_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <string.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

void raf_info(const char *fmt, ...) {
    va_list ap; va_start(ap, fmt);
    fprintf(stderr, "[RAF INFO] "); vfprintf(stderr, fmt, ap); fprintf(stderr, "\n");
    va_end(ap);
}

void raf_fatal(const char *fmt, ...) {
    va_list ap; va_start(ap, fmt);
    fprintf(stderr, "[RAF FATAL] "); vfprintf(stderr, fmt, ap); fprintf(stderr, "\n");
    va_end(ap);
    exit(1);
}

int raf_read_file(const char *path, void **out_buf, size_t *out_sz) {
    if (!path || !out_buf || !out_sz) return -1;
    int fd = open(path, O_RDONLY);
    if (fd < 0) return -1;
    struct stat st; if (fstat(fd,&st)!=0){close(fd);return -1;}
    void *buf = malloc(st.st_size);
    if (!buf){close(fd);return -1;}
    ssize_t r = read(fd, buf, st.st_size);
    close(fd);
    if (r != (ssize_t)st.st_size){free(buf);return -1;}
    *out_buf = buf; *out_sz = st.st_size; return 0;
}

int raf_write_on_diff(const char *path, const void *buf, size_t sz) {
    /* if file exists and identical, skip write, else atomic write */
    void *old = NULL; size_t oldsz = 0;
    if (raf_read_file(path, &old, &oldsz) == 0) {
        if (oldsz == sz && memcmp(old, buf, sz) == 0) { free(old); raf_info("No changes for %s", path); return 0; }
        free(old);
    }
    /* write to tmp and rename */
    char tmp[4096]; snprintf(tmp, sizeof(tmp), "%s.rafaelia.tmp", path);
    int fd = open(tmp, O_CREAT|O_WRONLY|O_TRUNC, 0644);
    if (fd < 0) return -1;
    ssize_t w = write(fd, buf, sz);
    fsync(fd); close(fd);
    if ((size_t)w != sz) { unlink(tmp); return -1; }
    if (rename(tmp, path) != 0) { unlink(tmp); return -1; }
    raf_info("Wrote %s (sz=%zu)", path, sz);
    return 1;
}
