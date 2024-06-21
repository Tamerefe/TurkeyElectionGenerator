#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct trky {
    float akp[10];
    float chp[10];
    float iyi[10];
    float hdp[10];
    float mhp[10];
    float sp[10];
    float erdogan[10];
    float ince[10];
    float aksener[10];
    float demirtas[10];
    float karamolla[10];
    float perin[10];
};

int main() {
    struct trky tr;
    FILE *file;
    file = fopen("polls.txt", "r");
    FILE *file2;
    file2 = fopen("candidates.txt", "r");

    srand(time(NULL));

    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.akp[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.chp[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.iyi[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.hdp[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.mhp[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file, "%f", &tr.sp[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.erdogan[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.ince[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.aksener[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.demirtas[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.karamolla[i]);
    }
    for (int i = 0; i < 10; i++) {
        fscanf(file2, "%f", &tr.perin[i]);
    }

    fclose(file);

    float other = 100, akp = tr.akp[rand() % 11], chp = tr.chp[rand() % 11], iyi = tr.iyi[rand() % 11], \
    hdp = tr.hdp[rand() % 11], mhp = tr.mhp[rand() % 11], sp = tr.sp[rand() % 11];

    if(akp + chp + iyi + hdp + mhp + sp > 100){
        akp *= 95/(akp + chp + iyi + hdp + mhp + sp);
        chp *= 95/(akp + chp + iyi + hdp + mhp + sp);
        iyi *= 95/(akp + chp + iyi + hdp + mhp + sp);
        hdp *= 95/(akp + chp + iyi + hdp + mhp + sp);
        mhp *= 95/(akp + chp + iyi + hdp + mhp + sp);
        sp *= 95/(akp + chp + iyi + hdp + mhp + sp);
        other -= akp + chp + iyi + hdp + mhp + sp;
    }else{
        other -= akp + chp + iyi + hdp + mhp + sp;
    }

    float erdogan = tr.erdogan[rand() % 11], ince = tr.ince[rand() % 11], aksener = tr.aksener[rand() % 11], \
    demirtas = tr.demirtas[rand() % 11],karamolla = tr.karamolla[rand() % 11], perin = tr.perin[rand() % 11];

    erdogan *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);
    ince *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);
    aksener *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);
    demirtas *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);
    karamolla *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);
    perin *= 100/(erdogan + ince + aksener + demirtas + karamolla + perin);

    printf("AKP: %%%.2f\t",akp);
    printf("CHP: %%%.2f\t",chp);
    printf("IYI: %%%.2f\t",iyi);
    printf("HDP: %%%.2f\t",hdp);
    printf("MHP: %%%.2f\t",mhp);
    printf("SP: %%%.2f\t",sp);    
    printf("Diger: %%%.2f\n",other);

    printf("Cumhur Ittifaki: %%%.2f\t\t",(akp + mhp));
    printf("Millet Ittifaki: %%%.2f\n",(chp + iyi + sp));

    printf("Erdogan: %%%.2f\t",erdogan);
    printf("Ince: %%%.2f\t",ince);
    printf("Aksener: %%%.2f\t",aksener);
    printf("Demirtas: %%%.2f\t",demirtas);
    printf("Karamollaoglu: %%%.2f\t",karamolla);
    printf("Perincek: %%%.2f\n",perin);

    return 0;
}
