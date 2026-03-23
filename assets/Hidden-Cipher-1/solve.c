#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

const char filepath[] = "cipher_flag.txt";
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

    for ( int index_flag = 0; index_flag < len_flag; index_flag += 2 ){
        char byte_str[3];
        int value = 0;
        byte_str[0] = flag[index_flag];
        byte_str[1] = flag[index_flag + 1];
        byte_str[2] = '\0';
        value = strtol(byte_str, NULL, 16);

        char result = value ^ *(index_flag/2 % 6 + secret);
        printf("%c", result);
    }

    fclose(fp);

    return 0;
}
