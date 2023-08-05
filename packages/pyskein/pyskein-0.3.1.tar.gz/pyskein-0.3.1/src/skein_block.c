/* Implementation of the Skein block functions.

   Based on an implementation by Doug Whiting released to the public domain.
   Modified by Hagen Fuerstenau.
*/

#include <string.h>
#include "skein.h"
#include "threefish.h"


/*****************************  Skein_256 ******************************/
void Skein_256_Process_Block(Skein_256_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt, size_t byteCntAdd)
{
    enum {
        WCNT = SKEIN_256_STATE_WORDS
    };
    u64b_t kw[WCNT+4];     /* key schedule words : chaining vars + tweak */
    u64b_t w[WCNT];        /* local copy of input block */

    Skein_assert(blkCnt != 0);

    ks[0] = ctx->X[0];
    ks[1] = ctx->X[1];
    ks[2] = ctx->X[2];
    ks[3] = ctx->X[3];
    ts[0] = ctx->h.T[0];
    ts[1] = ctx->h.T[1];
    do {
        /* this implementation only supports 2**64 input bytes
           (no carry out here) */
        ts[0] += byteCntAdd;        /* update processed length */
        ts[2] = ts[0] ^ ts[1];

        /* compute the missing key schedule value */
        ks[4] = ks[0] ^ ks[1] ^ ks[2] ^ ks[3] ^ SKEIN_KS_PARITY;

        /* feed block */
        Skein_Get64_LSB_First(w, blkPtr, WCNT);
        Threefish_256_encrypt(kw, w, ks, 1);

        ts[1] &= ~SKEIN_T1_FLAG_FIRST;
        blkPtr += SKEIN_256_BLOCK_BYTES;
    } while (--blkCnt);
    ctx->X[0] = ks[0];
    ctx->X[1] = ks[1];
    ctx->X[2] = ks[2];
    ctx->X[3] = ks[3];
    ctx->h.T[0] = ts[0];
    ctx->h.T[1] = ts[1];
}


/*****************************  Skein_512 ******************************/
void Skein_512_Process_Block(Skein_512_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt, size_t byteCntAdd)
{
    enum {
        WCNT = SKEIN_512_STATE_WORDS
    };

    u64b_t kw[WCNT+4];     /* key schedule words : chaining vars + tweak */
    u64b_t w[WCNT];        /* local copy of input block */

    Skein_assert(blkCnt != 0);

    ks[0] = ctx->X[0];
    ks[1] = ctx->X[1];
    ks[2] = ctx->X[2];
    ks[3] = ctx->X[3];
    ks[4] = ctx->X[4];
    ks[5] = ctx->X[5];
    ks[6] = ctx->X[6];
    ks[7] = ctx->X[7];
    ts[0] = ctx->h.T[0];
    ts[1] = ctx->h.T[1];
    do {
        /* this implementation only supports 2**64 input bytes
           (no carry out here) */
        ts[0] += byteCntAdd;            /* update processed length */
        ts[2] = ts[0] ^ ts[1];

        /* compute the missing key schedule value */
        ks[8] = ks[0] ^ ks[1] ^ ks[2] ^ ks[3] ^
                ks[4] ^ ks[5] ^ ks[6] ^ ks[7] ^ SKEIN_KS_PARITY;

        /* feed block */
        Skein_Get64_LSB_First(w, blkPtr, WCNT);
        Threefish_512_encrypt(kw, w, ks, 1);

        ts[1] &= ~SKEIN_T1_FLAG_FIRST;
        blkPtr += SKEIN_512_BLOCK_BYTES;
    } while (--blkCnt);
    ctx->X[0] = ks[0];
    ctx->X[1] = ks[1];
    ctx->X[2] = ks[2];
    ctx->X[3] = ks[3];
    ctx->X[4] = ks[4];
    ctx->X[5] = ks[5];
    ctx->X[6] = ks[6];
    ctx->X[7] = ks[7];
    ctx->h.T[0] = ts[0];
    ctx->h.T[1] = ts[1];
}


/*****************************  Skein1024 ******************************/
void Skein1024_Process_Block(Skein1024_Ctxt_t *ctx, const u08b_t *blkPtr,
                             size_t blkCnt, size_t byteCntAdd)
{
    enum {
        WCNT = SKEIN1024_STATE_WORDS
    };

    u64b_t kw[WCNT+4];    /* key schedule words : chaining vars + tweak */
    u64b_t w[WCNT];                         /* local copy of input block */

    Skein_assert(blkCnt != 0);

    ks[ 0] = ctx->X[ 0];
    ks[ 1] = ctx->X[ 1];
    ks[ 2] = ctx->X[ 2];
    ks[ 3] = ctx->X[ 3];
    ks[ 4] = ctx->X[ 4];
    ks[ 5] = ctx->X[ 5];
    ks[ 6] = ctx->X[ 6];
    ks[ 7] = ctx->X[ 7];
    ks[ 8] = ctx->X[ 8];
    ks[ 9] = ctx->X[ 9];
    ks[10] = ctx->X[10];
    ks[11] = ctx->X[11];
    ks[12] = ctx->X[12];
    ks[13] = ctx->X[13];
    ks[14] = ctx->X[14];
    ks[15] = ctx->X[15];
    ts[0] = ctx->h.T[0];
    ts[1] = ctx->h.T[1];
    do {
        /* this implementation only supports 2**64 input bytes
           (no carry out here) */
        ts[0] += byteCntAdd;                /* update processed length */
        ts[2]  = ts[0] ^ ts[1];

        /* compute the missing key schedule value */
        ks[16] = ks[ 0] ^ ks[ 1] ^ ks[ 2] ^ ks[ 3] ^
                 ks[ 4] ^ ks[ 5] ^ ks[ 6] ^ ks[ 7] ^
                 ks[ 8] ^ ks[ 9] ^ ks[10] ^ ks[11] ^
                 ks[12] ^ ks[13] ^ ks[14] ^ ks[15] ^ SKEIN_KS_PARITY;

        /* feed block */
        Skein_Get64_LSB_First(w, blkPtr, WCNT);
        Threefish1024_encrypt(kw, w, ks, 1);

        ts[1] &= ~SKEIN_T1_FLAG_FIRST;
        blkPtr += SKEIN1024_BLOCK_BYTES;
    } while (--blkCnt);
    ctx->X[ 0] = ks[ 0];
    ctx->X[ 1] = ks[ 1];
    ctx->X[ 2] = ks[ 2];
    ctx->X[ 3] = ks[ 3];
    ctx->X[ 4] = ks[ 4];
    ctx->X[ 5] = ks[ 5];
    ctx->X[ 6] = ks[ 6];
    ctx->X[ 7] = ks[ 7];
    ctx->X[ 8] = ks[ 8];
    ctx->X[ 9] = ks[ 9];
    ctx->X[10] = ks[10];
    ctx->X[11] = ks[11];
    ctx->X[12] = ks[12];
    ctx->X[13] = ks[13];
    ctx->X[14] = ks[14];
    ctx->X[15] = ks[15];
    ctx->h.T[0] = ts[0];
    ctx->h.T[1] = ts[1];
}
