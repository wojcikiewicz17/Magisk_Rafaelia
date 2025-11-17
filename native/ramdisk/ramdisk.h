/*
 * native/ramdisk/ramdisk.h
 * RAFAELIA — Ramdisk Engine (Camada 2) MVP
 *
 * API:
 *   - detect_compression_magic(buf, len) -> comp_t
 *   - decompress_fd_to_tempfile(fd, max_uncompressed, &out_fd) -> 0 on success
 *   - ramdisk_extract_and_parse_fd(fd, max_uncompressed, feed_cb, userdata) -> calls cpio_parse_fd on decompressed tempfile
 *
 * Notes:
 *  - gzip implemented via zlib (gzdopen/gzread).
 *  - xz/lz4/zstd support compiled under HAVE_LZMA / HAVE_LZ4 / HAVE_ZSTD.
 *  - This module aims for safety (caps on uncompressed size) and simplicity (uses tempfile bridging to cpio parser).
 */

#ifndef RAFAELIA_RAMDISK_H
#define RAFAELIA_RAMDISK_H

#include <stdint.h>
#include <stddef.h>

#ifdef __cplusplus
extern "C" {
#endif

/* compression types detected by magic */
typedef enum {
    RD_COMP_NONE = 0,
    RD_COMP_GZIP,
    RD_COMP_XZ,
    RD_COMP_LZ4,
    RD_COMP_ZSTD,
    RD_COMP_UNKNOWN
} rd_comp_t;

/* feed callback - called for each chunk of decompressed data (only used for streaming APIs) */
typedef int (*rd_feed_cb_t)(const unsigned char *buf, size_t len, void *userdata);

/* detect compression type by magic bytes in buffer (len should be >= 4) */
rd_comp_t detect_compression_magic(const uint8_t *buf, size_t len);

/*
 * Decompress the compressed stream starting at current fd position into a temporary file.
 * The returned out_fd is a seekable fd positioned at beginning (caller must close it).
 * max_uncompressed: 0 = unlimited; otherwise cap on decompressed bytes.
 *
 * Returns 0 on success, negative on error.
 */
int decompress_fd_to_tempfile(int fd, uint64_t max_uncompressed, int *out_fd);

/*
 * High-level helper:
 *  - from an fd positioned at compressed ramdisk start, decompress to tempfile (with limit)
 *  - then parse the decompressed tempfile via cpio_parse_fd (from native/cpio)
 *
 * feed_cb is forwarded to cpio_parse_fd consumer expectation (the cpio parser will call it per file payload).
 *
 * Returns 0 on success, negative otherwise.
 */
int ramdisk_extract_and_parse_fd(int fd, uint64_t max_uncompressed, rd_feed_cb_t feed_cb, void *userdata);

/* utility: compute sha256 of a file descriptor content (seek restored) */
int rd_sha256_fd(int fd, unsigned char out[32]);

#ifdef __cplusplus
}
#endif

#endif /* RAFAELIA_RAMDISK_H */
