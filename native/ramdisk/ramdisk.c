#define _GNU_SOURCE
/*
 * native/ramdisk/ramdisk.c
 * Implementation of Ramdisk Engine (Camada 2 MVP)
 *
 * gzip decompression implemented using zlib's gzdopen/gzread streaming.
 * For other formats (xz/lz4/zstd) placeholders are provided; add libs and implement stubs
 * guarded by HAVE_LZMA / HAVE_LZ4 / HAVE_ZSTD.
 *
 * Security: enforces max_uncompressed limit and robust error handling.
 */

#include "ramdisk.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <zlib.h>
#include <errno.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <inttypes.h>

/* include cpio parser header (assumes path native/cpio/cpio_parser.h) */
#include "../cpio/cpio_parser.h"

/* logging helper (simple) */
static void raf_log(const char *level, const char *fmt, ...) {
    va_list ap;
    va_start(ap, fmt);
    fprintf(stderr, "[%s] ", level);
    vfprintf(stderr, fmt, ap);
    fprintf(stderr, "\n");
    va_end(ap);
}

/* detect by magic (first bytes) */
rd_comp_t detect_compression_magic(const uint8_t *buf, size_t len) {
    if (!buf || len < 4) return RD_COMP_UNKNOWN;
    uint32_t h = (uint32_t)buf[0] | ((uint32_t)buf[1] << 8) | ((uint32_t)buf[2] << 16) | ((uint32_t)buf[3] << 24);
    /* gzip magic 1f 8b */
    if (buf[0] == 0x1f && buf[1] == 0x8b) return RD_COMP_GZIP;
    /* xz: FD 37 7A 58 5A 00 (0xFD377A58) */
    if ((uint8_t)buf[0] == 0xFD && (uint8_t)buf[1] == 0x37 && (uint8_t)buf[2] == 0x7A && (uint8_t)buf[3] == 0x58) return RD_COMP_XZ;
    /* lz4 frame magic prefix 0x184D2204 little endian */
    if (h == 0x04224d18) return RD_COMP_LZ4;
    /* zstd magic 0x28B52FFD little endian */
    if (h == 0xFFD2B528 || h == 0x28B52FFD) return RD_COMP_ZSTD;
    return RD_COMP_UNKNOWN;
}

/* Helper: create a named temporary file (returns fd and path via out_path_buffer if provided) */
static int create_tempfile(char *out_path, size_t out_path_len) {
    char tmpl[] = "/tmp/raf_ramdisk_XXXXXX";
    int fd = mkstemp(tmpl);
    if (fd < 0) return -1;
    /* optionally copy path */
    if (out_path && out_path_len > strlen(tmpl)) strcpy(out_path, tmpl);
    /* unlink immediately so it will be cleaned up on close */
    unlink(tmpl);
    return fd;
}

/* gzip decompression into tempfile */
static int decompress_gzip_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd) {
    if (fd < 0 || !out_fd) return -1;
    int dupfd = dup(fd);
    if (dupfd < 0) { raf_log("ERROR", "dup failed: %s", strerror(errno)); return -1; }
    gzFile gzf = gzdopen(dupfd, "rb");
    if (!gzf) { close(dupfd); raf_log("ERROR", "gzdopen failed"); return -1; }

    int tmpfd = create_tempfile(NULL, 0);
    if (tmpfd < 0) { gzclose(gzf); raf_log("ERROR","mkstemp failed"); return -1; }

    unsigned char buf[64*1024];
    int r;
    uint64_t total = 0;
    while ((r = gzread(gzf, buf, sizeof(buf))) > 0) {
        total += (uint64_t)r;
        if (max_uncompressed && total > max_uncompressed) {
            raf_log("ERROR","decompress exceeded max_uncompressed=%" PRIu64, max_uncompressed);
            close(tmpfd); gzclose(gzf); return -2;
        }
        if (write(tmpfd, buf, r) != r) {
            raf_log("ERROR","write tmp failed: %s", strerror(errno));
            close(tmpfd); gzclose(gzf); return -1;
        }
    }
    if (r < 0) {
        raf_log("ERROR","gzread failed");
        close(tmpfd); gzclose(gzf); return -1;
    }
    /* sync and seek back */
    fsync(tmpfd);
    lseek(tmpfd, 0, SEEK_SET);
    gzclose(gzf);
    *out_fd = tmpfd;
    raf_log("INFO","decompress_gzip: wrote %" PRIu64 " bytes to tempfile", total);
    return 0;
}

/* Placeholders for other decompressors (to be implemented when libs are available) */
#ifdef HAVE_LZMA
static int decompress_xz_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd) {
    /* Implement using liblzma streaming */
    (void)fd; (void)max_uncompressed; (void)out_fd;
    raf_log("WARN","decompress_xz: not implemented in this build");
    return -1;
}
#endif

#ifdef HAVE_LZ4
static int decompress_lz4_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd) {
    (void)fd; (void)max_uncompressed; (void)out_fd;
    raf_log("WARN","decompress_lz4: not implemented in this build");
    return -1;
}
#endif

#ifdef HAVE_ZSTD
static int decompress_zstd_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd) {
    (void)fd; (void)max_uncompressed; (void)out_fd;
    raf_log("WARN","decompress_zstd: not implemented in this build");
    return -1;
}
#endif

int decompress_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd) {
    if (fd < 0 || !out_fd) return -1;

    /* read first up to 8 bytes from fd to inspect magic, then seek back */
    unsigned char magic[8] = {0};
    off_t cur = lseek(fd, 0, SEEK_CUR);
    if (cur == (off_t)-1) cur = 0;
    ssize_t got = pread(fd, magic, sizeof(magic), cur);
    if (got <= 0) {
        raf_log("ERROR","peek magic failed: %s", strerror(errno));
        return -1;
    }
    rd_comp_t comp = detect_compression_magic(magic, (size_t)got);
    if (comp == RD_COMP_GZIP) {
        return decompress_gzip_fd_to_tempfile(fd, max_uncompressed, out_fd);
    } else if (comp == RD_COMP_XZ) {
#ifdef HAVE_LZMA
        return decompress_xz_fd_to_tempfile(fd, max_uncompressed, out_fd);
#else
        raf_log("ERROR","xz detected but not supported in this build");
        return -1;
#endif
    } else if (comp == RD_COMP_LZ4) {
#ifdef HAVE_LZ4
        return decompress_lz4_fd_to_tempfile(fd, max_uncompressed, out_fd);
#else
        raf_log("ERROR","lz4 detected but not supported in this build");
        return -1;
#endif
    } else if (comp == RD_COMP_ZSTD) {
#ifdef HAVE_ZSTD
        return decompress_zstd_fd_to_tempfile(fd, max_uncompressed, out_fd);
#else
        raf_log("ERROR","zstd detected but not supported in this build");
        return -1;
#endif
    } else {
        raf_log("ERROR","unknown compression magic (not gzip/xz/lz4/zstd)");
        return -1;
    }
}

/* Compute sha256 of fd content (restore original pos) */
#include <openssl/sha.h>
int rd_sha256_fd(int fd, unsigned char out[32]) {
    if (fd < 0 || !out) return -1;
    off_t orig = lseek(fd, 0, SEEK_CUR);
    if (orig == (off_t)-1) orig = 0;
    lseek(fd, 0, SEEK_SET);
    SHA256_CTX ctx;
    SHA256_Init(&ctx);
    unsigned char buf[64*1024];
    ssize_t r;
    while ((r = read(fd, buf, sizeof(buf))) > 0) {
        SHA256_Update(&ctx, buf, (size_t)r);
    }
    if (r < 0) {
        raf_log("ERROR","sha256 read failed: %s", strerror(errno));
        if (orig != (off_t)-1) lseek(fd, orig, SEEK_SET);
        return -1;
    }
    SHA256_Final(out, &ctx);
    if (orig != (off_t)-1) lseek(fd, orig, SEEK_SET);
    return 0;
}

/*
 * High-level helper that decompresses fd -> tempfile and calls cpio_parse_fd on that tempfile.
 * feed_cb is the cpio feed callback (per-file payload).
 */
int ramdisk_extract_and_parse_fd(int fd, uint64_t max_uncompressed, rd_feed_cb_t feed_cb, void *userdata) {
    if (fd < 0 || !feed_cb) return -1;
    int tmpfd = -1;
    int rc = decompress_fd_to_tempfile(fd, max_uncompressed, &tmpfd);
    if (rc != 0) {
        raf_log("ERROR","decompress_fd_to_tempfile failed rc=%d", rc);
        return rc;
    }
    /* Use cpio parser on tmpfd */
    /* Seek to start */
    if (lseek(tmpfd, 0, SEEK_SET) == (off_t)-1) {
        raf_log("ERROR","lseek tmpfd failed: %s", strerror(errno));
        close(tmpfd);
        return -1;
    }
    int parse_rc = cpio_parse_fd(tmpfd, 0 /*no max*/, (cpio_feed_cb_t)feed_cb, userdata);
    close(tmpfd);
    return parse_rc;
}