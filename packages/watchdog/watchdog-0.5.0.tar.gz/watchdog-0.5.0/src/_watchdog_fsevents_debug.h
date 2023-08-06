/**
 * _watchdog_fsevents_debug.h: debug macros.
 * Copyright (c) 2010 Jonas Haag <jonas@lophus.org>.
 * Copyright (c) 2010 Gora Khargosh <gora.khargosh@gmail.com>
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *   * Redistributions of source code must retain the above copyright
 *     notice, this list of conditions and the following disclaimer.
 *   * Redistributions in binary form must reproduce the above copyright
 *     notice, this list of conditions and the following disclaimer in the
 *     documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef WATCHDOG_FSEVENTS_DEBUG_H_
#define WATCHDOG_FSEVENTS_DEBUG_H_ 1

/**
 * Borrowed from bjoern's source code.
 */
#ifdef DEBUG
    #define DBG_REQ(request, ...) \
        do { \
            printf("[DEBUG Req %ld] ", request->id); \
            DBG(__VA_ARGS__); \
        } while(0)
    #define DBG(...) \
        do { \
            printf(__VA_ARGS__); \
            printf("\n"); \
        } while(0)
#else
    #define DBG(...) do{}while(0)
    #define DBG_REQ(...) DBG(__VA_ARGS__)
#endif

#define DBG_REFCOUNT(obj) \
    DBG(#obj "->obj_refcnt: %d", obj->ob_refcnt)

#define DBG_REFCOUNT_REQ(request, obj) \
    DBG_REQ(request, #obj "->ob_refcnt: %d", obj->ob_refcnt)

#endif /* !WATCHDOG_FSEVENTS_DEBUG_H_ */
