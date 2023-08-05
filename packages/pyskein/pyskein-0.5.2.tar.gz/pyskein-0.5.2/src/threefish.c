/* Implementation of the Threefish block cipher.
   Written by Hagen Fuerstenau, 2008, 2009, 2010.

   Based on an implementation of the Skein hashing algorithm by Doug Whiting,
   which was released to the public domain.
*/

#include <string.h>
#include "skein.h"
#include "threefish.h"

void Threefish_256_encrypt(u64b_t *kw, const u64b_t *w, u64b_t *out, int feed)
{
    u64b_t X0,X1,X2,X3;    /* local copy of context vars, for speed */

    X0 = w[0] + ks[0];
    X1 = w[1] + ks[1] + ts[0];
    X2 = w[2] + ks[2] + ts[1];
    X3 = w[3] + ks[3];

    R256_8_rounds(0);
    R256_8_rounds(1);
    R256_8_rounds(2);
    R256_8_rounds(3);
    R256_8_rounds(4);
    R256_8_rounds(5);
    R256_8_rounds(6);
    R256_8_rounds(7);
    R256_8_rounds(8);

    if (feed) {
        out[0] = X0^w[0]; out[1] = X1^w[1]; out[2] = X2^w[2]; out[3] = X3^w[3];
    }
    else {
        out[0] = X0; out[1] = X1; out[2] = X2; out[3] = X3;
    }
}

void Threefish_256_decrypt(u64b_t *kw, const u64b_t *w, u64b_t *out)
{
    u64b_t X0,X1,X2,X3;

    X0 = w[0]; X1 = w[1]; X2 = w[2]; X3 = w[3];

    INV_R256_8_rounds(8);
    INV_R256_8_rounds(7);
    INV_R256_8_rounds(6);
    INV_R256_8_rounds(5);
    INV_R256_8_rounds(4);
    INV_R256_8_rounds(3);
    INV_R256_8_rounds(2);
    INV_R256_8_rounds(1);
    INV_R256_8_rounds(0);

    out[0] = X0 - ks[0];
    out[1] = X1 - ks[1] - ts[0];
    out[2] = X2 - ks[2] - ts[1];
    out[3] = X3 - ks[3];
}


void Threefish_512_encrypt(u64b_t *kw, const u64b_t *w, u64b_t *out, int feed)
{
    u64b_t X0,X1,X2,X3,X4,X5,X6,X7;   /* local copy of vars, for speed */

    X0 = w[0] + ks[0];
    X1 = w[1] + ks[1];
    X2 = w[2] + ks[2];
    X3 = w[3] + ks[3];
    X4 = w[4] + ks[4];
    X5 = w[5] + ks[5] + ts[0];
    X6 = w[6] + ks[6] + ts[1];
    X7 = w[7] + ks[7];

    R512_8_rounds(0);
    R512_8_rounds(1);
    R512_8_rounds(2);
    R512_8_rounds(3);
    R512_8_rounds(4);
    R512_8_rounds(5);
    R512_8_rounds(6);
    R512_8_rounds(7);
    R512_8_rounds(8);

    if (feed) {
        out[0] = X0^w[0]; out[1] = X1^w[1]; out[2] = X2^w[2]; out[3] = X3^w[3];
        out[4] = X4^w[4]; out[5] = X5^w[5]; out[6] = X6^w[6]; out[7] = X7^w[7];
    }
    else {
        out[0] = X0; out[1] = X1; out[2] = X2; out[3] = X3;
        out[4] = X4; out[5] = X5; out[6] = X6; out[7] = X7;
    }
}

void Threefish_512_decrypt(u64b_t *kw, const u64b_t *w, u64b_t *out)
{
    u64b_t X0,X1,X2,X3,X4,X5,X6,X7;

    X0 = w[0]; X1 = w[1]; X2 = w[2]; X3 = w[3];
    X4 = w[4]; X5 = w[5]; X6 = w[6]; X7 = w[7];

    INV_R512_8_rounds(8);
    INV_R512_8_rounds(7);
    INV_R512_8_rounds(6);
    INV_R512_8_rounds(5);
    INV_R512_8_rounds(4);
    INV_R512_8_rounds(3);
    INV_R512_8_rounds(2);
    INV_R512_8_rounds(1);
    INV_R512_8_rounds(0);

    out[0] = X0 - ks[0];
    out[1] = X1 - ks[1];
    out[2] = X2 - ks[2];
    out[3] = X3 - ks[3];
    out[4] = X4 - ks[4];
    out[5] = X5 - ks[5] - ts[0];
    out[6] = X6 - ks[6] - ts[1];
    out[7] = X7 - ks[7];
}


void Threefish_1024_encrypt(u64b_t *kw, const u64b_t *w, u64b_t *out, int feed)
{
    u64b_t X00,X01,X02,X03,X04,X05,X06,X07, /* local copy of vars, for speed */
           X08,X09,X10,X11,X12,X13,X14,X15;

    X00 = w[ 0] + ks[ 0];
    X01 = w[ 1] + ks[ 1];
    X02 = w[ 2] + ks[ 2];
    X03 = w[ 3] + ks[ 3];
    X04 = w[ 4] + ks[ 4];
    X05 = w[ 5] + ks[ 5];
    X06 = w[ 6] + ks[ 6];
    X07 = w[ 7] + ks[ 7];
    X08 = w[ 8] + ks[ 8];
    X09 = w[ 9] + ks[ 9];
    X10 = w[10] + ks[10];
    X11 = w[11] + ks[11];
    X12 = w[12] + ks[12];
    X13 = w[13] + ks[13] + ts[0];
    X14 = w[14] + ks[14] + ts[1];
    X15 = w[15] + ks[15];

    R1024_8_rounds(0);
    R1024_8_rounds(1);
    R1024_8_rounds(2);
    R1024_8_rounds(3);
    R1024_8_rounds(4);
    R1024_8_rounds(5);
    R1024_8_rounds(6);
    R1024_8_rounds(7);
    R1024_8_rounds(8);
    R1024_8_rounds(9);

    if (feed) {
        out[ 0] = X00^w[ 0]; out[ 1] = X01^w[ 1]; out[ 2] = X02^w[ 2];
        out[ 3] = X03^w[ 3]; out[ 4] = X04^w[ 4]; out[ 5] = X05^w[ 5];
        out[ 6] = X06^w[ 6]; out[ 7] = X07^w[ 7]; out[ 8] = X08^w[ 8];
        out[ 9] = X09^w[ 9]; out[10] = X10^w[10]; out[11] = X11^w[11];
        out[12] = X12^w[12]; out[13] = X13^w[13]; out[14] = X14^w[14];
        out[15] = X15^w[15];
    }
    else {
        out[ 0] = X00; out[ 1] = X01; out[ 2] = X02; out[ 3] = X03;
        out[ 4] = X04; out[ 5] = X05; out[ 6] = X06; out[ 7] = X07;
        out[ 8] = X08; out[ 9] = X09; out[10] = X10; out[11] = X11;
        out[12] = X12; out[13] = X13; out[14] = X14; out[15] = X15;
    }
}

void Threefish_1024_decrypt(u64b_t *kw, const u64b_t *w, u64b_t *out)
{
    u64b_t X00,X01,X02,X03,X04,X05,X06,X07,
           X08,X09,X10,X11,X12,X13,X14,X15;

    X00 = w[ 0]; X01 = w[ 1]; X02 = w[ 2]; X03 = w[ 3];
    X04 = w[ 4]; X05 = w[ 5]; X06 = w[ 6]; X07 = w[ 7];
    X08 = w[ 8]; X09 = w[ 9]; X10 = w[10]; X11 = w[11];
    X12 = w[12]; X13 = w[13]; X14 = w[14]; X15 = w[15];

    INV_R1024_8_rounds(9);
    INV_R1024_8_rounds(8);
    INV_R1024_8_rounds(7);
    INV_R1024_8_rounds(6);
    INV_R1024_8_rounds(5);
    INV_R1024_8_rounds(4);
    INV_R1024_8_rounds(3);
    INV_R1024_8_rounds(2);
    INV_R1024_8_rounds(1);
    INV_R1024_8_rounds(0);

    out[ 0] = X00 - ks[ 0];
    out[ 1] = X01 - ks[ 1];
    out[ 2] = X02 - ks[ 2];
    out[ 3] = X03 - ks[ 3];
    out[ 4] = X04 - ks[ 4];
    out[ 5] = X05 - ks[ 5];
    out[ 6] = X06 - ks[ 6];
    out[ 7] = X07 - ks[ 7];
    out[ 8] = X08 - ks[ 8];
    out[ 9] = X09 - ks[ 9];
    out[10] = X10 - ks[10];
    out[11] = X11 - ks[11];
    out[12] = X12 - ks[12];
    out[13] = X13 - ks[13] - ts[0];
    out[14] = X14 - ks[14] - ts[1];
    out[15] = X15 - ks[15];
}
