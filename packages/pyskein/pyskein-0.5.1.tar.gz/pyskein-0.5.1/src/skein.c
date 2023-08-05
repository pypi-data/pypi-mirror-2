/***********************************************************************
**
** Implementation of the Skein hash function.
**
** Original author: Doug Whiting, 2008.
** Modified by: Hagen Fuerstenau, 2009.
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
void Skein1024_Process_Block(Skein1024_Ctxt_t *ctx,const u08b_t *blkPtr,size_t blkCnt,size_t byteCntAdd);


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


#define SKEIN_INIT_DEF(N, M) \
void Skein ## N ## _Init(Skein ## N ## _Ctxt_t *ctx, size_t hashBitLen) \
{ \
    union { \
        u08b_t b[SKEIN ## N ## _STATE_BYTES]; \
        u64b_t w[SKEIN ## N ## _STATE_WORDS]; \
    } cfg; \
\
    ctx->h.hashBitLen = hashBitLen; \
    if (hashBitLen == M) \
        memcpy(ctx->X, SKEIN ## N ## _IV_ ## M, sizeof(ctx->X)); \
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
        Skein ## N ## _Process_Block(ctx, cfg.b, 1, SKEIN_CFG_STR_LEN); \
    } \
\
    Skein_Start_New_Type(ctx, MSG); \
}


#define SKEIN_INITEXT_DEF(N) \
void Skein ## N ## _InitExt(Skein ## N ## _Ctxt_t *ctx, size_t hashBitLen, \
                           const u08b_t *key, size_t keyBytes, \
                           const u08b_t *pers, size_t persBytes, \
                           const u08b_t *nonce, size_t nonceBytes) \
{ \
    union { \
        u08b_t b[SKEIN ## N ## _STATE_BYTES]; \
        u64b_t w[SKEIN ## N ## _STATE_WORDS]; \
    } cfg; \
\
    /* compute the initial chaining values ctx->X[], based on key */ \
    memset(ctx->X, 0, sizeof(ctx->X)); \
    if (key != NULL && keyBytes > 0) { \
        Skein_assert(sizeof(cfg.b) >= sizeof(ctx->X)); \
        /* do a mini-Init right here */ \
        ctx->h.hashBitLen = 8*sizeof(ctx->X); /* state size */ \
        Skein_Start_New_Type(ctx, KEY);       /* T0 = 0; T1 = KEY type */ \
        Skein ## N ## _Update(ctx, key, keyBytes);  /* hash the key */ \
        Skein ## N ## _Final_Pad(ctx, cfg.b); /* put result into cfg.b[] */ \
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
    Skein ## N ## _Process_Block(ctx, cfg.b, 1, SKEIN_CFG_STR_LEN); \
\
    /* personalization string */ \
    if (pers && persBytes) { \
        Skein_Start_New_Type(ctx, PERS); \
        Skein ## N ## _Update(ctx, pers, persBytes); \
        ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;  /* final block */ \
        if (ctx->h.bCnt < SKEIN ## N ## _BLOCK_BYTES) \
            memset(&ctx->b[ctx->h.bCnt], 0, \
                   SKEIN ## N ## _BLOCK_BYTES-ctx->h.bCnt); \
        Skein ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt); \
    } \
\
    /* nonce string */ \
    if (nonce && nonceBytes) { \
        Skein_Start_New_Type(ctx, NONCE); \
        Skein ## N ## _Update(ctx, nonce, nonceBytes); \
        ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;  /* final block */ \
        if (ctx->h.bCnt < SKEIN ## N ## _BLOCK_BYTES) \
            memset(&ctx->b[ctx->h.bCnt], 0, \
                   SKEIN ## N ## _BLOCK_BYTES-ctx->h.bCnt); \
        Skein ## N ## _Process_Block(ctx, ctx->b, 1, ctx->h.bCnt); \
    } \
\
    Skein_Start_New_Type(ctx, MSG); \
}


/*****************************************************************/
/*     256-bit Skein                                             */
/*****************************************************************/

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* init the context for a straight hashing operation  */
SKEIN_INIT_DEF(_256, 256);
SKEIN_INITEXT_DEF(_256);

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* process the input bytes */
int Skein_256_Update(Skein_256_Ctxt_t *ctx, const u08b_t *msg, size_t msgByteCnt)
    {
    size_t n;

    Skein_Assert(ctx->h.bCnt <= SKEIN_256_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* process full blocks, if any */
    if (msgByteCnt + ctx->h.bCnt > SKEIN_256_BLOCK_BYTES)
        {
        if (ctx->h.bCnt)                              /* finish up any buffered message data */
            {
            n = SKEIN_256_BLOCK_BYTES - ctx->h.bCnt;  /* # bytes free in buffer b[] */
            if (n)
                {
                Skein_assert(n < msgByteCnt);         /* check on our logic here */
                memcpy(&ctx->b[ctx->h.bCnt],msg,n);
                msgByteCnt  -= n;
                msg         += n;
                ctx->h.bCnt += n;
                }
            Skein_assert(ctx->h.bCnt == SKEIN_256_BLOCK_BYTES);
            Skein_256_Process_Block(ctx,ctx->b,1,SKEIN_256_BLOCK_BYTES);
            ctx->h.bCnt = 0;
            }
        /* now process any remaining full blocks, directly from input message data */
        if (msgByteCnt > SKEIN_256_BLOCK_BYTES)
            {
            n = (msgByteCnt-1) / SKEIN_256_BLOCK_BYTES;   /* number of full blocks to process */
            Skein_256_Process_Block(ctx,msg,n,SKEIN_256_BLOCK_BYTES);
            msgByteCnt -= n * SKEIN_256_BLOCK_BYTES;
            msg        += n * SKEIN_256_BLOCK_BYTES;
            }
        Skein_assert(ctx->h.bCnt == 0);
        }

    /* copy any remaining source message data bytes into b[] */
    if (msgByteCnt)
        {
        Skein_assert(msgByteCnt + ctx->h.bCnt <= SKEIN_256_BLOCK_BYTES);
        memcpy(&ctx->b[ctx->h.bCnt],msg,msgByteCnt);
        ctx->h.bCnt += msgByteCnt;
        }

    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the result */
int Skein_256_Final(Skein_256_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN_256_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN_256_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;                 /* tag as the final block */
    if (ctx->h.bCnt < SKEIN_256_BLOCK_BYTES)            /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN_256_BLOCK_BYTES - ctx->h.bCnt);

    Skein_256_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);  /* process the final block */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;             /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN_256_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein_256_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN_256_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN_256_BLOCK_BYTES)
            n  = SKEIN_256_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN_256_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(256,&ctx->h,n,hashVal+i*SKEIN_256_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }

#if defined(SKEIN_CODE_SIZE) || defined(SKEIN_PERF)
size_t Skein_256_API_CodeSize(void)
    {
    return ((u08b_t *) Skein_256_API_CodeSize) -
           ((u08b_t *) Skein_256_Init);
    }
#endif

/*****************************************************************/
/*     512-bit Skein                                             */
/*****************************************************************/

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* init the context for a straight hashing operation  */
SKEIN_INIT_DEF(_512, 512);
SKEIN_INITEXT_DEF(_512);


/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* process the input bytes */
int Skein_512_Update(Skein_512_Ctxt_t *ctx, const u08b_t *msg, size_t msgByteCnt)
    {
    size_t n;

    Skein_Assert(ctx->h.bCnt <= SKEIN_512_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* process full blocks, if any */
    if (msgByteCnt + ctx->h.bCnt > SKEIN_512_BLOCK_BYTES)
        {
        if (ctx->h.bCnt)                              /* finish up any buffered message data */
            {
            n = SKEIN_512_BLOCK_BYTES - ctx->h.bCnt;  /* # bytes free in buffer b[] */
            if (n)
                {
                Skein_assert(n < msgByteCnt);         /* check on our logic here */
                memcpy(&ctx->b[ctx->h.bCnt],msg,n);
                msgByteCnt  -= n;
                msg         += n;
                ctx->h.bCnt += n;
                }
            Skein_assert(ctx->h.bCnt == SKEIN_512_BLOCK_BYTES);
            Skein_512_Process_Block(ctx,ctx->b,1,SKEIN_512_BLOCK_BYTES);
            ctx->h.bCnt = 0;
            }
        /* now process any remaining full blocks, directly from input message data */
        if (msgByteCnt > SKEIN_512_BLOCK_BYTES)
            {
            n = (msgByteCnt-1) / SKEIN_512_BLOCK_BYTES;   /* number of full blocks to process */
            Skein_512_Process_Block(ctx,msg,n,SKEIN_512_BLOCK_BYTES);
            msgByteCnt -= n * SKEIN_512_BLOCK_BYTES;
            msg        += n * SKEIN_512_BLOCK_BYTES;
            }
        Skein_assert(ctx->h.bCnt == 0);
        }

    /* copy any remaining source message data bytes into b[] */
    if (msgByteCnt)
        {
        Skein_assert(msgByteCnt + ctx->h.bCnt <= SKEIN_512_BLOCK_BYTES);
        memcpy(&ctx->b[ctx->h.bCnt],msg,msgByteCnt);
        ctx->h.bCnt += msgByteCnt;
        }

    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the result */
int Skein_512_Final(Skein_512_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN_512_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN_512_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;                 /* tag as the final block */
    if (ctx->h.bCnt < SKEIN_512_BLOCK_BYTES)            /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN_512_BLOCK_BYTES - ctx->h.bCnt);

    Skein_512_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);  /* process the final block */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;             /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN_512_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein_512_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN_512_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN_512_BLOCK_BYTES)
            n  = SKEIN_512_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN_512_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(512,&ctx->h,n,hashVal+i*SKEIN_512_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }

#if defined(SKEIN_CODE_SIZE) || defined(SKEIN_PERF)
size_t Skein_512_API_CodeSize(void)
    {
    return ((u08b_t *) Skein_512_API_CodeSize) -
           ((u08b_t *) Skein_512_Init);
    }
#endif

/*****************************************************************/
/*    1024-bit Skein                                             */
/*****************************************************************/

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* init the context for a straight hashing operation  */
SKEIN_INIT_DEF(1024, 1024);
SKEIN_INITEXT_DEF(1024);

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* process the input bytes */
int Skein1024_Update(Skein1024_Ctxt_t *ctx, const u08b_t *msg, size_t msgByteCnt)
    {
    size_t n;

    Skein_Assert(ctx->h.bCnt <= SKEIN1024_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* process full blocks, if any */
    if (msgByteCnt + ctx->h.bCnt > SKEIN1024_BLOCK_BYTES)
        {
        if (ctx->h.bCnt)                              /* finish up any buffered message data */
            {
            n = SKEIN1024_BLOCK_BYTES - ctx->h.bCnt;  /* # bytes free in buffer b[] */
            if (n)
                {
                Skein_assert(n < msgByteCnt);         /* check on our logic here */
                memcpy(&ctx->b[ctx->h.bCnt],msg,n);
                msgByteCnt  -= n;
                msg         += n;
                ctx->h.bCnt += n;
                }
            Skein_assert(ctx->h.bCnt == SKEIN1024_BLOCK_BYTES);
            Skein1024_Process_Block(ctx,ctx->b,1,SKEIN1024_BLOCK_BYTES);
            ctx->h.bCnt = 0;
            }
        /* now process any remaining full blocks, directly from input message data */
        if (msgByteCnt > SKEIN1024_BLOCK_BYTES)
            {
            n = (msgByteCnt-1) / SKEIN1024_BLOCK_BYTES;   /* number of full blocks to process */
            Skein1024_Process_Block(ctx,msg,n,SKEIN1024_BLOCK_BYTES);
            msgByteCnt -= n * SKEIN1024_BLOCK_BYTES;
            msg        += n * SKEIN1024_BLOCK_BYTES;
            }
        Skein_assert(ctx->h.bCnt == 0);
        }

    /* copy any remaining source message data bytes into b[] */
    if (msgByteCnt)
        {
        Skein_assert(msgByteCnt + ctx->h.bCnt <= SKEIN1024_BLOCK_BYTES);
        memcpy(&ctx->b[ctx->h.bCnt],msg,msgByteCnt);
        ctx->h.bCnt += msgByteCnt;
        }

    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the result */
int Skein1024_Final(Skein1024_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN1024_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN1024_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;                 /* tag as the final block */
    if (ctx->h.bCnt < SKEIN1024_BLOCK_BYTES)            /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN1024_BLOCK_BYTES - ctx->h.bCnt);

    Skein1024_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);  /* process the final block */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;             /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN1024_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein1024_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN1024_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN1024_BLOCK_BYTES)
            n  = SKEIN1024_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN1024_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(1024,&ctx->h,n,hashVal+i*SKEIN1024_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }

#if defined(SKEIN_CODE_SIZE) || defined(SKEIN_PERF)
size_t Skein1024_API_CodeSize(void)
    {
    return ((u08b_t *) Skein1024_API_CodeSize) -
           ((u08b_t *) Skein1024_Init);
    }
#endif

/**************** Functions to support MAC/tree hashing ***************/
/*   (this code is identical for Optimized and Reference versions)    */

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the block, no OUTPUT stage */
int Skein_256_Final_Pad(Skein_256_Ctxt_t *ctx, u08b_t *hashVal)
    {
    Skein_Assert(ctx->h.bCnt <= SKEIN_256_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;        /* tag as the final block */
    if (ctx->h.bCnt < SKEIN_256_BLOCK_BYTES)   /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN_256_BLOCK_BYTES - ctx->h.bCnt);
    Skein_256_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);    /* process the final block */

    Skein_Put64_LSB_First(hashVal,ctx->X,SKEIN_256_BLOCK_BYTES);   /* "output" the state bytes */

    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the block, no OUTPUT stage */
int Skein_512_Final_Pad(Skein_512_Ctxt_t *ctx, u08b_t *hashVal)
    {
    Skein_Assert(ctx->h.bCnt <= SKEIN_512_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;        /* tag as the final block */
    if (ctx->h.bCnt < SKEIN_512_BLOCK_BYTES)   /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN_512_BLOCK_BYTES - ctx->h.bCnt);
    Skein_512_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);    /* process the final block */

    Skein_Put64_LSB_First(hashVal,ctx->X,SKEIN_512_BLOCK_BYTES);   /* "output" the state bytes */

    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* finalize the hash computation and output the block, no OUTPUT stage */
int Skein1024_Final_Pad(Skein1024_Ctxt_t *ctx, u08b_t *hashVal)
    {
    Skein_Assert(ctx->h.bCnt <= SKEIN1024_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    ctx->h.T[1] |= SKEIN_T1_FLAG_FINAL;        /* tag as the final block */
    if (ctx->h.bCnt < SKEIN1024_BLOCK_BYTES)   /* zero pad b[] if necessary */
        memset(&ctx->b[ctx->h.bCnt],0,SKEIN1024_BLOCK_BYTES - ctx->h.bCnt);
    Skein1024_Process_Block(ctx,ctx->b,1,ctx->h.bCnt);    /* process the final block */

    Skein_Put64_LSB_First(hashVal,ctx->X,SKEIN1024_BLOCK_BYTES);   /* "output" the state bytes */

    return SKEIN_SUCCESS;
    }

#if SKEIN_TREE_HASH
/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* just do the OUTPUT stage                                       */
int Skein_256_Output(Skein_256_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN_256_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN_256_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;    /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN_256_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein_256_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN_256_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN_256_BLOCK_BYTES)
            n  = SKEIN_256_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN_256_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(256,&ctx->h,n,hashVal+i*SKEIN_256_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* just do the OUTPUT stage                                       */
int Skein_512_Output(Skein_512_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN_512_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN_512_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;    /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN_512_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein_512_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN_512_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN_512_BLOCK_BYTES)
            n  = SKEIN_512_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN_512_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(256,&ctx->h,n,hashVal+i*SKEIN_512_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }

/*++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++*/
/* just do the OUTPUT stage                                       */
int Skein1024_Output(Skein1024_Ctxt_t *ctx, u08b_t *hashVal)
    {
    size_t i,n,byteCnt;
    u64b_t X[SKEIN1024_STATE_WORDS];
    Skein_Assert(ctx->h.bCnt <= SKEIN1024_BLOCK_BYTES,SKEIN_FAIL);    /* catch uninitialized context */

    /* now output the result */
    byteCnt = (ctx->h.hashBitLen + 7) >> 3;    /* total number of output bytes */

    /* run Threefish in "counter mode" to generate output */
    memset(ctx->b,0,sizeof(ctx->b));  /* zero out b[], so it can hold the counter */
    memcpy(X,ctx->X,sizeof(X));       /* keep a local copy of counter mode "key" */
    for (i=0;i*SKEIN1024_BLOCK_BYTES < byteCnt;i++)
        {
        ((u64b_t *)ctx->b)[0]= Skein_Swap64((u64b_t) i); /* build the counter block */
        Skein_Start_New_Type(ctx,OUT_FINAL);
        Skein1024_Process_Block(ctx,ctx->b,1,sizeof(u64b_t)); /* run "counter mode" */
        n = byteCnt - i*SKEIN1024_BLOCK_BYTES;   /* number of output bytes left to go */
        if (n >= SKEIN1024_BLOCK_BYTES)
            n  = SKEIN1024_BLOCK_BYTES;
        Skein_Put64_LSB_First(hashVal+i*SKEIN1024_BLOCK_BYTES,ctx->X,n);   /* "output" the ctr mode bytes */
        Skein_Show_Final(256,&ctx->h,n,hashVal+i*SKEIN1024_BLOCK_BYTES);
        memcpy(ctx->X,X,sizeof(X));   /* restore the counter mode key for next time */
        }
    return SKEIN_SUCCESS;
    }
#endif
