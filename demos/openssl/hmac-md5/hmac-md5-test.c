/*
 * Copyright (c) 2008 The DragonFly Project.  All rights reserved.
 *
 * This code is derived from software contributed to The DragonFly Project
 * by Matthias Schmidt <matthias@dragonflybsd.org>, University of Marburg,
 * Germany.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 *
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in
 *    the documentation and/or other materials provided with the
 *    distribution.
 * 3. Neither the name of The DragonFly Project nor the names of its
 *    contributors may be used to endorse or promote products derived
 *    from this software without specific, prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 * ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 * LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 * FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE
 * COPYRIGHT HOLDERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 * INCIDENTAL, SPECIAL, EXEMPLARY OR CONSEQUENTIAL DAMAGES (INCLUDING,
 * BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 * LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
 * AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
 * OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
 * SUCH DAMAGE.
 */

#include <openssl/opensslv.h>
#if (OPENSSL_VERSION_NUMBER >= 0x300000L)
#define	IS_OPENSSL3	1
#endif

#include <openssl/x509.h>
#include <openssl/md5.h>
#include <openssl/ssl.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/rand.h>

#include <assert.h>
#include <stdio.h>
#include <string.h>

/*
 * hmac_md5() taken out of RFC 2104.  This RFC was written by H. Krawczyk,
 * M. Bellare and R. Canetti.
 *
 * text      pointer to data stream
 * text_len  length of data stream
 * key       pointer to authentication key
 * key_len   length of authentication key
 * digest    caller digest to be filled int
 */
void
hmac_md5(unsigned char *text, int text_len, unsigned char *key, int key_len,
    unsigned char* digest)
{
#ifdef	IS_OPENSSL3
	const EVP_MD	*md;
	EVP_MD_CTX	*context;
#else
	MD5_CTX		context;
#endif
        unsigned char k_ipad[65];    /* inner padding -
                                      * key XORd with ipad
                                      */
        unsigned char k_opad[65];    /* outer padding -
                                      * key XORd with opad
                                      */
        unsigned char tk[16];
        int i;

#ifdef	IS_OPENSSL3
	context = EVP_MD_CTX_new();
	assert(context != NULL);

	md = EVP_md5();
	assert(md != NULL);
#endif

        /* if key is longer than 64 bytes reset it to key=MD5(key) */
        if (key_len > 64) {
#ifdef	IS_OPENSSL3
		EVP_DigestInit_ex(context, md, NULL);
		EVP_DigestUpdate(context, key, key_len);
		EVP_DigestFinal_ex(context, tk, NULL);
#else
                MD5_Init(&context);
                MD5_Update(&context, key, key_len);
                MD5_Final(tk, &context);
#endif
                key = tk;
                key_len = 16;
        }

        /*
         * the HMAC_MD5 transform looks like:
         *
         * MD5(K XOR opad, MD5(K XOR ipad, text))
         *
         * where K is an n byte key
         * ipad is the byte 0x36 repeated 64 times
	 *
         * opad is the byte 0x5c repeated 64 times
         * and text is the data being protected
         */

        /* start out by storing key in pads */
        bzero( k_ipad, sizeof k_ipad);
        bzero( k_opad, sizeof k_opad);
        bcopy( key, k_ipad, key_len);
        bcopy( key, k_opad, key_len);

        /* XOR key with ipad and opad values */
        for (i=0; i<64; i++) {
                k_ipad[i] ^= 0x36;
                k_opad[i] ^= 0x5c;
        }

#ifdef	IS_OPENSSL3
        /**
         * Perform inner MD5.
         */

	/* Init context for first pass. */
	EVP_DigestInit_ex(context, md, NULL);
	/* Start with inner pad. */
	EVP_DigestUpdate(context, k_ipad, 64);
	/* Update with text of datagram. */
	EVP_DigestUpdate(context, text, text_len);
	/* Finish up first pass. */
	EVP_DigestFinal_ex(context, digest, NULL);

	/**
         * Perform outer MD5.
         */

	/* Re-init context for second pass. */
	EVP_DigestInit_ex(context, md, NULL);
	/* Start with outer pad. */
	EVP_DigestUpdate(context, k_opad, 64);
	/* Update with results of first hash. */
	EVP_DigestUpdate(context, digest, 16);
	/* Finish up second pass. */
	EVP_DigestFinal_ex(context, digest, NULL);

	EVP_MD_CTX_free(context);
#else
        /*
         * perform inner MD5
         */
        MD5_Init(&context);                   /* init context for 1st
                                              * pass */
        MD5_Update(&context, k_ipad, 64);     /* start with inner pad */
        MD5_Update(&context, text, text_len); /* then text of datagram */

	MD5_Final(digest, &context);          /* finish up 1st pass */
        /*
         * perform outer MD5
         */
        MD5_Init(&context);                   /* init context for 2nd
                                              * pass */
        MD5_Update(&context, k_opad, 64);     /* start with outer pad */
        MD5_Update(&context, digest, 16);     /* then results of 1st
                                              * hash */
        MD5_Final(digest, &context);          /* finish up 2nd pass */
#endif
}

const char *SHORT_AUTH_KEY =	"this is a passcode";
const char *LONG_AUTH_KEY =	"this is a SUPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPER LONG passcode";

int
main(int argc, const char *argv[])
{
	const char *auth_key = (argc == 0 || strcmp(argv[1], "--short") == 0) ?
	    SHORT_AUTH_KEY : LONG_AUTH_KEY;

	char *text = "abcdefghijklmnop";
	unsigned char digest[8192] = {0};

	hmac_md5(
	    (unsigned char*)text, strlen(text),
	    (unsigned char*)auth_key, strlen(auth_key),
	    digest);

	printf("key: %s\n", auth_key);
	printf("text: %s\n", text);
	printf("digest: ");

	for (int i = 0; digest[i] != '\0'; i++)
		printf("%02x", digest[i]);
	printf("\n");

	return 0;
}
