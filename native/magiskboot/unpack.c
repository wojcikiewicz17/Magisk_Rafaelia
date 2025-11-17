#define _GNU_SOURCE
/*
 * native/magiskboot/unpack.c
 * Parse a v1 boot image in memory and extract kernel + ramdisk (best-effort).
 * This implementation is conservative and defensive (bounds checks).
 */
#include "unpack.h"
#include "../bootimg/bootimg.h"
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/* Parse a v1 boot image in memory and extract kernel + ramdisk (best-effort).
   This implementation is conservative and defensive (bounds checks).
*/
int unpack_boot_image(const uint8_t *in_buf, size_t in_sz,
                      uint8_t **kernel_buf, size_t *kernel_sz,
                      uint8_t **ramdisk_buf, size_t *ramdisk_sz,
                      uint32_t *page_size, int *has_vendor_boot) {
    if (!in_buf || in_sz < sizeof(struct boot_img_hdr_v1)) return -1;
    const struct boot_img_hdr_v1 *h = (const struct boot_img_hdr_v1*)in_buf;
    if (memcmp(h->magic, BOOT_MAGIC, BOOT_MAGIC_SIZE) != 0) return -2;

    uint32_t page = h->page_size ? h->page_size : 2048;
    if (page == 0) page = 2048;
    if (page_size) *page_size = page;

    size_t offset = page; /* header occupies first page */
    /* kernel */
    uint32_t ksize = h->kernel_size;
    if ((size_t)ksize > in_sz) return -3;
    if (offset + ksize > in_sz) return -3;
    if (kernel_buf) {
        *kernel_buf = malloc(ksize);
        if (!*kernel_buf) return -4;
        memcpy(*kernel_buf, in_buf + offset, ksize);
    }
    if (kernel_sz) *kernel_sz = ksize;
    offset = align_to(offset + ksize, page);

    /* ramdisk */
    uint32_t rsize = h->ramdisk_size;
    if (offset + rsize > in_sz) {
        /* try to be tolerant: cap to available */
        if (offset > in_sz) return -5;
        rsize = (uint32_t)(in_sz - offset);
    }
    if (ramdisk_buf) {
        *ramdisk_buf = malloc(rsize);
        if (!*ramdisk_buf) {
            if (kernel_buf && *kernel_buf) { free(*kernel_buf); *kernel_buf = NULL; }
            return -6;
        }
        memcpy(*ramdisk_buf, in_buf + offset, rsize);
    }
    if (ramdisk_sz) *ramdisk_sz = rsize;
    offset = align_to(offset + rsize, page);

    /* heuristic: vendor_boot if dt_size non-zero or large second_size */
    int vendor = 0;
    if (h->dt_size || h->second_size) vendor = 1;
    if (has_vendor_boot) *has_vendor_boot = vendor;

    return 0;
}