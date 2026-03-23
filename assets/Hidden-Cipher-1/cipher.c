#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const char filepath[] = "flag.txt";

const char secret[] = "S3Cr3t";

int main(){
    FILE *fp;
    fp = fopen(filepath, "rb");
    if (!fp){
        fprintf(stderr, "Error to open file.");
        return -1;
    }

    long len_flag = 0;
    fseek(fp, 0, SEEK_END);
    len_flag = ftell(fp);
    rewind(fp);

    char *flag = malloc(sizeof(char) * len_flag + 1);
    fread(flag, sizeof(char), len_flag, fp);
    flag[len_flag] = '\0';

    for ( int index_flag = 0; index_flag < len_flag; index_flag++ ){
        //long long result = (((long long)index_flag * 0x2AAAAAABLL) >> 0x20) -  (index_flag >> 0x1F);
        //long long index_secret = index_flag - (result * 4);
        //int value =  flag[index_flag] ^ secret[index_secret];
        //printf("%02x", value);
        int value = *(flag + index_flag) ^ *(index_flag % 6 + secret);
        printf("%02x", value);
    }

    fclose(fp);

    return 0;
}
