/***********************************************************************
**
** Implementation of the Skein hash function.
**
** Original author: Doug Whiting, 2008.
** Modified by: Hagen Fuerstenau, 2009, 2010.
**
** This algorithm and source code is released to the public domain.
**
************************************************************************/

#define  SKEIN_PORT_CODE /* instantiate any code in skein_port.h */

#include <string.h>      /* get the memcpy/memset functions */
#include "skein.h"       /* get the Skein API definitions   */
#include "skein_iv.h"    /* get precomputed IVs */

/*****************************************************************/
/* External function to process blkCnt (nonzero) full block(s) of data. */
void Skein_256_Process_Block(Skein_256_Ctxt_t *ctx,const u08b_t *blkPtr,size_t blkCnt,size_t byteCntAdd);
void Skein_512_Process_Block(Skein_512_Ctxt_t *ctx,const u08b_t *blkPtr,size_t blkCnt,size_t byteCntAdd);
void Skein_1024_Process_Block(Skein_1024_Ctxt_t *ctx,const u08b_t *blkPtr,size_t blkCnt,size_t byteCntAdd);


#if SKEIN_NEED_SWAP
    #define INITEXT_SWAP(N) \
        { \
        uint_t i; \
        for (i=0; i<SKEIN ## N ## _STATE_WORDS; i++) \
            /* key bytes to context words */ \
            ctx->X[i] = Skein_Swap64(ctx->X[i]); \
        }
#else
    #define INITEXT_SWAP(X)
#endif


#define SKEIN_INIT_DEF(N) \
void Skein_ ## N ## _Init(Skein_ ## N ## _Ctxt_t *ctx, size_t hashBitLen) \
{ \
    union { \
        u08b_t b[SKEIN_ ## N ## _STATE_BYTES]; \
        u64b_t w[SKEIN_ ## N ## _STATE_WORDS]; \
    } cfg; \
\
    ctx->h.hashBitLen = hashBitLen; \
    if (hashBitLen == N) \
        memcpy(ctx->X, SKEIN_ ## N ## _IV_ ## N, sizeof(ctx->X)); \
    else { \
        /* set tweaks: T0=0; T1=CFG | FINAL */ \
        Skein_Start_New_Type(ctx, CFG_FINAL); \
        cfg.w[0] = Skein_Swap64(SKEIN_SCHEMA_VER); \
        cfg.w[1] = Skein_Swap64(hashBitLen); \
        cfg.w[2] = Skein_Swap64(SKEIN_CFG_TREE_INFO_SEQUENTIAL); \
        memset(&cfg.w[3], 0, sizeof(cfg) - 3*sizeof(cfg.w[0])); \
\
        /* compute the initial chaining values from config block */ \
        memset(ctx->X, 0, sizeof(ctx->X)); \
        Skein_ ## N ## _Process_Block(ctx, cfg.b, 1, SKEIN_CFG_STR_LEN); \
    } \
\
    Skein_Start_New_Type(ctx, MSG); \
}


#define SKEIN_INITEXT_DEF(N) \
void Skein_ ## N ## _InitExt(Skein_ ## N ## _Ctxt_t *ctx, size_t hashBitLen, \
                             const u08b_t *key, size_t keyBytes, \
                             const u08b_t *pers, size_t persBytes, \
                             const u08b_t *nonce, size_t nonceBytes) \
{ \
    union { \
        u08b_t b[SKEIN_ ## N ## _STATE_BYTES]; \
        u64b_t w[SKEIN_ ## N ## _STATE_WORDS]; \
    } cfg; \
\
    /* compute the initial chaining values ctx->X[], based on key */ \
    memset(ctx->X, 0, sizeof(ctx->X)); \
    if (key != NULL && keyBytes > 0) { \
        Skein_assert(sizeof(cfg.b) >= sizeof(ctx->X)); \
        /* do a mini-Init right here */ \
        ctx->h.hashBitLen = 8*sizeof(ctx->X); /* state size */ \
        Skein_Start_New_Type(ctx, KEY);       /* T0 = 0; T1 = KEY type */ \
        Skein_ ## N ## _Update(ctx, key, keyBytes);  /* hash the key */ \
        Skein_ ## N ## _Final_Pad(ctx, cfg.b); /* put result into cfg.b[] */ \
        memcpy(ctx->X, cfg.b, sizeof(cfg.b)); /* copy over into ctx->X[] */ \
        INITEXT_SWAP(N); \
    } \
\
    /* config block */ \
    ctx->h.hashBitLen = hashBitLen;          /* output hash bit count */ \
    Skein_Start_New_Type(ctx, CFG_FINAL); \
    memset(&cfg.w, 0, sizeof(cfg.w));        /* pre-pad cfg.w[] with zeroes */\
    cfg.w[0] = Skein_Swap64(SKEIN_SCHEMA_VER); \
    cfg.w[1] = Skein_Swap64(hashBitLen);     /* hash result length in bits */ \
    Skein_ ## N ## _Process_Block(ctx, cfg.b, 1, SKEIN_CFG_STR_LEN); \
\
    /* personalization string */ \
    if (pers && persBytes) { \
        Skein_Start_New_Type(ctx, PERS); \
        Skein_ ## N ## _Update(ctx, pers, persBytes); \
        ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;  /* final block */ \
        if (ctx->h.bCnt < SKEIN_ ## N ## _BLOCK_BYTES) \
            memset(&ctx->b[ctx->h.bCnt], 0, \
                   SKEIN_ ## N ## _BLOCK_BYTES-ctx->h.bCnt); \
        Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt); \
    } \
\
    /* nonce string */ \
    if (nonce && nonceBytes) { \
        Skein_Start_New_Type(ctx, NONCE); \
        Skein_ ## N ## _Update(ctx, nonce, nonceBytes); \
        ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;  /* final block */ \
        if (ctx->h.bCnt < SKEIN_ ## N ## _BLOCK_BYTES) \
            memset(&ctx->b[ctx->h.bCnt], 0, \
                   SKEIN_ ## N ## _BLOCK_BYTES-ctx->h.bCnt); \
        Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt); \
    } \
\
    Skein_Start_New_Type(ctx, MSG); \
}


#define SKEIN_UPDATE_DEF(N) \
void Skein_ ## N ## _Update(Skein_ ## N ## _Ctxt_t *ctx, \
                            const u08b_t *msg, \
                            size_t msgByteCnt) \
{ \
    size_t n; \
\
    /* process full blocks, if any */ \
    if (msgByteCnt + ctx->h.bCnt > SKEIN_ ## N ## _BLOCK_BYTES) { \
        if (ctx->h.bCnt) {       /* finish up any buffered message data */ \
            n = SKEIN_ ## N ## _BLOCK_BYTES - ctx->h.bCnt;  /* # bytes free in buffer b[] */ \
            if (n) { \
                memcpy(&ctx->b[ctx->h.bCnt], msg, n); \
                msgByteCnt  -= n; \
                msg         += n; \
                ctx->h.bCnt += n; \
            } \
            Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, \
                                          SKEIN_ ## N ## _BLOCK_BYTES); \
            ctx->h.bCnt = 0; \
        } \
        /* now process any remaining full blocks, directly from input message data */ \
        if (msgByteCnt > SKEIN_ ## N ## _BLOCK_BYTES) { \
            n = (msgByteCnt-1) / SKEIN_ ## N ## _BLOCK_BYTES;   /* number of full blocks to process */ \
            Skein_ ## N ## _Process_Block(ctx, msg, n, \
                                          SKEIN_ ## N ## _BLOCK_BYTES); \
            msgByteCnt -= n * SKEIN_ ## N ## _BLOCK_BYTES; \
            msg        += n * SKEIN_ ## N ## _BLOCK_BYTES; \
        } \
    } \
\
    /* copy any remaining source message data bytes into b[] */ \
    if (msgByteCnt) { \
        memcpy(&ctx->b[ctx->h.bCnt], msg, msgByteCnt); \
        ctx->h.bCnt += msgByteCnt; \
    } \
}


#define SKEIN_FINAL_DEF(N) \
void Skein_ ## N ## _Final(Skein_ ## N ## _Ctxt_t *ctx, u08b_t *hashVal) \
{ \
    size_t i, n, byteCnt; \
    u64b_t X[SKEIN_ ## N ## _STATE_WORDS]; \
    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;     /* tag as the final block */ \
    if (ctx->h.bCnt < SKEIN_ ## N ## _BLOCK_BYTES)  /* zero pad b[] if necessary */ \
        memset(&ctx->b[ctx->h.bCnt], 0, \
               SKEIN_ ## N ## _BLOCK_BYTES - ctx->h.bCnt); \
    Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt);  /* process the final block */ \
    /* now output the result */ \
    byteCnt = (ctx->h.hashBitLen + 7) >> 3; /* total number of output bytes */ \
    /* run Threefish in "counter mode" to generate output */ \
    memset(ctx->b, 0, sizeof(ctx->b));  /* zero out b[], so it can hold the counter */ \
    memcpy(X, ctx->X, sizeof(X)); /* keep a local copy of counter mode "key" */ \
    for (i=0; i*SKEIN_ ## N ## _BLOCK_BYTES < byteCnt; i++) { \
        ((u64b_t *)ctx->b)[0] = Skein_Swap64((u64b_t) i); /* build the counter block */ \
        Skein_Start_New_Type(ctx, OUT_FINAL); \
        Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, sizeof(u64b_t)); /* run "counter mode" */ \
        n = byteCnt - i*SKEIN_ ## N ## _BLOCK_BYTES; /* number of output bytes left to go */ \
        if (n >= SKEIN_ ## N ## _BLOCK_BYTES) \
            n  = SKEIN_ ## N ## _BLOCK_BYTES; \
        Skein_Put64_LSB_First(hashVal+i*SKEIN_ ## N ## _BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */ \
        memcpy(ctx->X, X, sizeof(X)); /* restore the counter mode key for next time */ \
    } \
}


/* finalize the hash computation and output the block, no OUTPUT stage */
#define SKEIN_FINAL_PAD_DEF(N) \
void Skein_ ## N ## _Final_Pad(Skein_ ## N ## _Ctxt_t *ctx, u08b_t *hashVal) \
{ \
    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL; /* tag as the final block */ \
    if (ctx->h.bCnt < SKEIN_ ## N ## _BLOCK_BYTES) /* zero pad b[] if necessary */ \
        memset(&ctx->b[ctx->h.bCnt], 0, \
               SKEIN_ ## N ## _BLOCK_BYTES - ctx->h.bCnt); \
    Skein_ ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt); /* process the final block */ \
    Skein_Put64_LSB_First(hashVal, ctx->X, SKEIN_ ## N ## _BLOCK_BYTES); /* "output" the state bytes */ \
}


/*****************************************************************/
/*     256-bit Skein                                             */
/*****************************************************************/
SKEIN_INIT_DEF(256);
SKEIN_INITEXT_DEF(256);
SKEIN_UPDATE_DEF(256);
SKEIN_FINAL_DEF(256);
SKEIN_FINAL_PAD_DEF(256);


/*****************************************************************/
/*     512-bit Skein                                             */
/*****************************************************************/
SKEIN_INIT_DEF(512);
SKEIN_INITEXT_DEF(512);
SKEIN_UPDATE_DEF(512);
SKEIN_FINAL_DEF(512);
SKEIN_FINAL_PAD_DEF(512);


/*****************************************************************/
/*    1024-bit Skein                                             */
/*****************************************************************/
SKEIN_INIT_DEF(1024);
SKEIN_INITEXT_DEF(1024);
SKEIN_UPDATE_DEF(1024);
SKEIN_FINAL_DEF(1024);
SKEIN_FINAL_PAD_DEF(1024);


/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* just do the OUTPUT stage                                       */
#if (0)
void Skein_256_Output(Skein_256_Ctxt_t *ctx, u08b_t *hashVal)
{
    size_t i, n, byteCnt;
    u64b_t X[SKEIN_256_STATE_WORDS];
    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3; /* total number of output bytes */
    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b, 0, sizeof(ctx->b)); /* zero out b[], so it can hold the counter */
    memcpy(X, ctx->X, sizeof(X)); /* keep a local copy of counter mode "key" */
    for (i=0; i*SKEIN_256_BLOCK_BYTES < byteCnt; i++) {
        ((u64b_t *)ctx->b)[0] = Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein_256_Process_Block(ctx, ctx->b, 1, sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN_256_BLOCK_BYTES; /* number of output bytes left to go */
        if (n >= SKEIN_256_BLOCK_BYTES)
            n  = SKEIN_256_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN_256_BLOCK_BYTES, ctx->X, n); /* "output" the ctr mode bytes */
        memcpy(ctx->X, X, sizeof(X)); /* restore the counter mode key for next time */
    }
}
#endif
