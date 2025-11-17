#define _GNU_SOURCE
/*
 * native/repack/repack.c
 * Implementation of Repack API (MVP)
 * - parse input header (v1)
 * - extract kernel and ramdisk via unpack_boot_image
 * - optionally apply devpatch (non-destructive marker appended to ramdisk payload)
 * - rebuild header with recalculated sizes and page alignment
 * - produce malloc'd buffer
 */

#include "repack.h"
#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include "../bootimg/bootimg.h"
#include "../magiskboot/unpack.h"

/* Helper: write header into buffer (v1) */
static void write_boot_header_v1(uint8_t *out, const struct boot_img_hdr_v1 *h) {
    memcpy(out, h, sizeof(struct boot_img_hdr_v1));
}

/* Repack implementation (MVP):
   - parse input header (v1)
   - extract kernel and ramdisk via unpack_boot_image
   - optionally apply devpatch (non-destructive marker appended to ramdisk payload in this MVP)
   - rebuild header with recalculated sizes and page alignment
   - produce malloc'd buffer
*/
int repack_boot_image(const uint8_t *in_buf, size_t in_sz, uint8_t **out_buf, size_t *out_sz, int devpatch, int force) {
    (void)force;
    if (!in_buf || in_sz == 0 || !out_buf || !out_sz) return -1;

    /* Sanity: input must have boot magic */
    if (in_sz < sizeof(struct boot_img_hdr_v1)) return -2;
    const struct boot_img_hdr_v1 *hin = (const struct boot_img_hdr_v1*)in_buf;
    if (memcmp(hin->magic, BOOT_MAGIC, BOOT_MAGIC_SIZE) != 0) return -3;

    /* Unpack components */
    uint8_t *kernel = NULL, *ramdisk = NULL;
    size_t ksz = 0, rsz = 0;
    uint32_t page = 0;
    int vendor = 0;
    int rc = unpack_boot_image(in_buf, in_sz, &kernel, &ksz, &ramdisk, &rsz, &page, &vendor);
    if (rc != 0) {
        /* fallback: copy whole buffer as-is */
        uint8_t *copy = malloc(in_sz);
        if (!copy) return -4;
        memcpy(copy, in_buf, in_sz);
        *out_buf = copy;
        *out_sz = in_sz;
        return 0;
    }

    /* Optionally modify ramdisk in a non-destructive way (devpatch): append marker */
    uint8_t *new_ram = NULL;
    size_t new_rsz = rsz;
    if (devpatch) {
        const char *marker = "\n# RAFAELIA_DEV_PATCH\n";
        size_t ml = strlen(marker);
        new_ram = malloc(rsz + ml);
        if (!new_ram) { free(kernel); free(ramdisk); return -5; }
        memcpy(new_ram, ramdisk, rsz);
        memcpy(new_ram + rsz, marker, ml);
        new_rsz = rsz + ml;
    } else {
        new_ram = malloc(rsz);
        if (!new_ram) { free(kernel); free(ramdisk); return -6; }
        memcpy(new_ram, ramdisk, rsz);
    }

    /* Build output header (start from input header and update sizes) */
    struct boot_img_hdr_v1 hout;
    memset(&hout, 0, sizeof(hout));
    memcpy(&hout, hin, sizeof(hout)); /* copy fields; we'll update sizes */
    hout.kernel_size = (uint32_t)ksz;
    hout.ramdisk_size = (uint32_t)new_rsz;
    /* keep same page size */
    if (hout.page_size == 0) hout.page_size = page ? page : 2048;
    uint32_t out_page = hout.page_size;

    /* Compute layout */
    size_t header_size = out_page;
    size_t kernel_offset = header_size;
    size_t kernel_padded = align_to(ksz, out_page);
    size_t ramdisk_offset = kernel_offset + kernel_padded;
    size_t ramdisk_padded = align_to(new_rsz, out_page);
    size_t total_size = ramdisk_offset + ramdisk_padded;

    /* allocate output */
    uint8_t *out = calloc(1, total_size);
    if (!out) { free(kernel); free(ramdisk); free(new_ram); return -7; }

    /* write header into first page (zero padded) */
    memcpy(out, &hout, sizeof(hout));

    /* copy kernel then ramdisk */
    memcpy(out + kernel_offset, kernel, ksz);
    memcpy(out + ramdisk_offset, new_ram, new_rsz);

    /* free temporaries */
    free(kernel); free(ramdisk); free(new_ram);

    *out_buf = out;
    *out_sz = total_size;
    return 0;
}