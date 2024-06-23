#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct poll {
    float akp[5][8];
    float chp[5][8];
    float iyi[5][8];
    float dem[5][8];
    float yrp[5][8];
    float zp[5][8];
};

void read_poll_data(FILE *file, struct poll *p, int index) {
    for (size_t i = 0; i < 8; i++) {
        fscanf(file, "%f %f %f %f %f %f", 
            &p->akp[index][i], &p->chp[index][i], &p->iyi[index][i], 
            &p->yrp[index][i], &p->zp[index][i], &p->dem[index][i]);
    }
}

int main() {
    char *cities[5] = {"Ankara", "Antalya", "Bursa", "Istanbul", "Izmir"};
    struct poll tr;

    FILE *fileAnkara = fopen("ankara.txt", "r");
    FILE *fileAntalya = fopen("antalya.txt", "r");
    FILE *fileBursa = fopen("bursa.txt", "r");
    FILE *fileIstanbul = fopen("istanbul.txt", "r");
    FILE *fileIzmir = fopen("izmir.txt", "r");

    if (fileAnkara == NULL || fileAntalya == NULL || fileBursa == NULL || 
        fileIstanbul == NULL || fileIzmir == NULL) {
        printf("Error opening one or more files.\n");
        return 1;
    }

    read_poll_data(fileAnkara, &tr, 0);
    read_poll_data(fileAntalya, &tr, 1);
    read_poll_data(fileBursa, &tr, 2);
    read_poll_data(fileIstanbul, &tr, 3);
    read_poll_data(fileIzmir, &tr, 4);

    fclose(fileAnkara);
    fclose(fileAntalya);
    fclose(fileBursa);
    fclose(fileIstanbul);
    fclose(fileIzmir);

    srand(time(NULL));
    int select;

    printf("1) Istanbul\n2) Ankara\n3) Izmir\n4) Bursa\n5) Antalya\nPlease Select Country: ");
    scanf("%d",&select);
    switch (select){
    case 1:
        printf("%s poll results:\n", cities[3]);
        printf("AKP: %.1f%%, CHP: %.1f%%, IYI: %.1f%%, YRP: %.1f%%, ZP: %.1f%%, DEM: %.1f%%", 
           tr.akp[3][rand() % 8], tr.chp[3][rand() % 8], 
           tr.iyi[3][rand() % 8], tr.yrp[3][rand() % 8], 
           tr.zp[3][rand() % 8], tr.dem[3][rand() % 8]);
        break;
    case 2:
        printf("%s poll results:\n", cities[0]);
        printf("AKP: %.1f%%, CHP: %.1f%%, IYI: %.1f%%, YRP: %.1f%%, ZP: %.1f%%, DEM: %.1f%%", 
           tr.akp[0][rand() % 8], tr.chp[0][rand() % 8], 
           tr.iyi[0][rand() % 8], tr.yrp[0][rand() % 8], 
           tr.zp[0][rand() % 8], tr.dem[0][rand() % 8]);
        break;
    case 3:
        printf("%s poll results:\n", cities[4]);
        printf("AKP: %.1f%%, CHP: %.1f%%, IYI: %.1f%%, YRP: %.1f%%, ZP: %.1f%%, DEM: %.1f%%", 
           tr.akp[4][rand() % 8], tr.chp[4][rand() % 8], 
           tr.iyi[4][rand() % 8], tr.yrp[4][rand() % 8], 
           tr.zp[4][rand() % 8], tr.dem[4][rand() % 8]);
        break;
    case 4:
        printf("%s poll results:\n", cities[2]);
        printf("AKP: %.1f%%, CHP: %.1f%%, IYI: %.1f%%, YRP: %.1f%%, ZP: %.1f%%, DEM: %.1f%%", 
            tr.akp[2][rand() % 8], tr.chp[2][rand() % 8], 
            tr.iyi[2][rand() % 8], tr.yrp[2][rand() % 8], 
            tr.zp[2][rand() % 8], tr.dem[2][rand() % 8]);
        break;
    case 5:
        printf("%s poll results:\n", cities[1]);
        printf("AKP: %.1f%%, CHP: %.1f%%, IYI: %.1f%%, YRP: %.1f%%, ZP: %.1f%%, DEM: %.1f%%", 
           tr.akp[1][rand() % 8], tr.chp[1][rand() % 8], 
           tr.iyi[1][rand() % 8], tr.yrp[1][rand() % 8], 
           tr.zp[1][rand() % 8], tr.dem[1][rand() % 8]);
        break;
    default:
        break;
    }
    return 0;
}