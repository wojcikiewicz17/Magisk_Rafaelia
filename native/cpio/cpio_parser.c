#define _GNU_SOURCE
/*
 * native/cpio/cpio_parser.c
 * Minimal robust parser for newc (070701) - streaming and defensive (MVP)
 */
#include "cpio_parser.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <stdint.h>

#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>

/* Minimal robust parser for newc (070701) - streaming and defensive (MVP) */
static int parse_hex8(const char *s, uint32_t *out) {
    char tmp[9]; memcpy(tmp, s, 8); tmp[8]=0;
    char *end; unsigned long v = strtoul(tmp, &end, 16);
    if (end == tmp) return -1;
    *out = (uint32_t)v; return 0;
}

int cpio_parse_fd(int fd, uint64_t max_bytes, cpio_feed_cb_t feed, void *userdata) {
    if (fd < 0 || !feed) return -1;
    char header_magic[7];
    while (1) {
        ssize_t r = read(fd, header_magic, 6);
        if (r == 0) return 0; /* EOF */
        if (r < 6) return -1;
        header_magic[6]=0;
        if (memcmp(header_magic, "070701", 6) != 0) return -1;
        char fields[13][9];
        char buf[13*8];
        r = read(fd, buf, 13*8);
        if (r != 13*8) return -1;
        for (int i=0;i<13;i++){ memcpy(fields[i], buf + i*8, 8); fields[i][8]=0; }
        uint32_t namesize=0, filesize=0;
        if (parse_hex8(fields[11], &namesize) != 0) return -1;
        if (parse_hex8(fields[6], &filesize) != 0) return -1;
        if (namesize == 0 || namesize > (1024*1024)) return -1;
        size_t name_padded = (namesize + 3) & ~3;
        char *name = malloc(name_padded);
        if (!name) return -1;
        r = read(fd, name, name_padded);
        if (r != (ssize_t)name_padded) { free(name); return -1; }
        if (memcmp(name, "TRAILER!!!", 10) == 0) { free(name); return 0; }
        free(name);
        uint64_t remain = filesize;
        unsigned char *bufdata = malloc(65536);
        if (!bufdata) return -1;
        while (remain) {
            size_t toread = (remain > 65536) ? 65536 : (size_t)remain;
            ssize_t rr = read(fd, bufdata, toread);
            if (rr <= 0) { free(bufdata); return -1; }
            if (feed(bufdata, (size_t)rr, userdata) != 0) { free(bufdata); return -1; }
            remain -= (size_t)rr;
            if (max_bytes && max_bytes < (uint64_t)rr) { free(bufdata); return -1; }
            if (max_bytes) max_bytes -= (uint64_t)rr;
        }
        free(bufdata);
        off_t cur = lseek(fd, 0, SEEK_CUR);
        off_t aligned = ((cur + 3) & ~3);
        if (aligned > cur) lseek(fd, aligned, SEEK_SET);
    }
    return 0;
}