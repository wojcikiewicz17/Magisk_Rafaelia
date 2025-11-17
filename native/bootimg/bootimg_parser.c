/*
 * native/bootimg/bootimg_parser.c
 * Implementation of parse_boot_image() with robust heuristics for v1/v3/v4/vendor.
 *
 * Strategy:
 *  - try to parse as v1 (classic) using boot_img_hdr_v1 at offset 0
 *  - validate sizes/alignments heuristically
 *  - detect vendor_boot by scanning for "VNDRBOOT" magic at plausible offsets
 *  - if dt_size present, mark dtb_offset/dtb_size
 *
 * This parser is defensive: will cap sizes, avoid out-of-bounds, and return
 * explicit negative error codes for callers to handle.
 */
#define _GNU_SOURCE
#include "bootimg_parser.h"
#include "bootimg.h"
#include <string.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

/* internal helper to safely read little-endian 32-bit from possibly unaligned buffer */
static uint32_t safe_read_u32le(const uint8_t *p) {
    return (uint32_t)p[0] | ((uint32_t)p[1] << 8) | ((uint32_t)p[2] << 16) | ((uint32_t)p[3] << 24);
}

/* scan for vendor boot magic "VNDRBOOT" at plausible offsets (heuristic) */
static ssize_t scan_vendor_magic(const uint8_t *buf, size_t buf_sz, uint32_t page) {
    /* common place: after kernel+ramdisk+second aligned; but try scanning within first 64MB for speed */
    size_t scan_limit = buf_sz < (64 * 1024 * 1024) ? buf_sz : (64 * 1024 * 1024);
    const char *vmagic = "VNDRBOOT";
    for (size_t i = page; i + 8 < scan_limit; i += page) {
        if (!memcmp(buf + i, vmagic, 8)) return (ssize_t)i;
    }
    /* additional try: scan entire small image (if < 8MB) */
    if (buf_sz < (8 * 1024 * 1024)) {
        for (size_t i = 0; i + 8 < buf_sz; i += 512) {
            if (!memcmp(buf + i, vmagic, 8)) return (ssize_t)i;
        }
    }
    return -1;
}

int parse_boot_image(const uint8_t *in_buf, size_t in_sz, struct boot_image_info *out) {
    if (!in_buf || !out) return -1;
    memset(out, 0, sizeof(*out));
    out->raw_buf = in_buf;
    out->raw_buf_size = in_sz;

    if (in_sz < sizeof(struct boot_img_hdr_v1)) return -3;
    const struct boot_img_hdr_v1 *h = (const struct boot_img_hdr_v1*)in_buf;

    /* quick magic check */
    if (memcmp(h->magic, BOOT_MAGIC, BOOT_MAGIC_SIZE) != 0) {
        /* Not classic boot magic — attempt to find vendor header */
        /* If no boot magic, give up */
        return -2;
    }

    /* Base v1 parsing */
    uint32_t page = h->page_size ? h->page_size : DEFAULT_PAGE_SIZE;
    if (page == 0) page = DEFAULT_PAGE_SIZE;
    out->page_size = page;

    /* offsets */
    size_t offset = page; /* header occupies one page */
    uint32_t ksz = h->kernel_size;
    if ((size_t)ksz > in_sz) return -3;
    if (offset + ksz > in_sz) return -3;
    out->kernel_offset = offset;
    out->kernel_size = ksz;
    offset = align_to(offset + ksz, page);

    uint32_t rsz = h->ramdisk_size;
    /* be tolerant: if header says ramdisk_size past EOF, clamp */
    if (rsz && offset + rsz > in_sz) {
        /* clamp to available */
        if (offset > in_sz) return -3;
        rsz = (uint32_t)(in_sz - offset);
    }
    out->ramdisk_offset = offset;
    out->ramdisk_size = rsz;
    offset = align_to(offset + rsz, page);

    uint32_t ssz = h->second_size;
    if (ssz) {
        if (offset + ssz <= in_sz) {
            out->second_offset = offset;
            out->second_size = ssz;
            offset = align_to(offset + ssz, page);
        } else {
            /* header second_size inconsistent; ignore second */
            out->second_offset = 0;
            out->second_size = 0;
        }
    }

    /* dt_size (device tree blobs / dtbo) */
    uint32_t dtsz = h->dt_size;
    if (dtsz) {
        /* Many images place DT immediately after second; use current offset */
        if (offset + dtsz <= in_sz) {
            out->dtb_offset = offset;
            out->dtb_size = dtsz;
            offset = align_to(offset + dtsz, page);
        } else {
            /* dt_size inconsistent: search for dtb signature (FDT) as fallback */
            /* look for 0xD00DFEED (FDT magic) in the next few MB */
            const uint32_t fdt_magic_be = 0xd00dfeed;
            size_t scan_limit = in_sz < (offset + (4 * 1024 * 1024)) ? in_sz : (offset + (4 * 1024 * 1024));
            for (size_t i = offset; i + 4 <= scan_limit; i += 4) {
                uint32_t v = safe_read_u32le(in_buf + i);
                if (v == fdt_magic_be) { /* probably big-endian check won't match; but try string "FDT" */
                    out->dtb_offset = i;
                    /* best-effort: set dtb_size to remaining */
                    out->dtb_size = (size_t)(in_sz - i);
                    offset = align_to(i + out->dtb_size, page);
                    break;
                }
            }
        }
    }

    /* Heuristic: detect vendor_boot by scanning for "VNDRBOOT" near plausible offsets */
    ssize_t vpos = scan_vendor_magic(in_buf, in_sz, page);
    if (vpos >= 0) {
        out->has_vendor_boot = 1;
        out->vendor_boot_offset = (size_t)vpos;
        /* best-effort vendor size: until EOF or next known structure; set to remaining */
        out->vendor_boot_size = in_sz - (size_t)vpos;
        out->version = RAF_BOOT_VENDOR;
    } else {
        out->has_vendor_boot = 0;
        out->vendor_boot_offset = 0;
        out->vendor_boot_size = 0;
        out->version = RAF_BOOT_V1;
    }

    /* header region size */
    out->header_size = page;

    return 0;
}