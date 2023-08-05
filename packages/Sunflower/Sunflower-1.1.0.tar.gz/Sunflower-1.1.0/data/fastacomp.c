/* similar to fastacomposition in exonerate but allows piped input */
/* originally by Guy Slater */

#include <stdio.h>
#include <ctype.h>
#include <string.h>

int main(int argc, char **argv) {
    register int i, ch;
    static int comp[256] = {0};
    char *label;

    if (argc > 1) {
      label = argv[1];
    } else {
      label = "<stdin>";
    }

    while((ch = getchar()) != EOF){
        if(ch == '>')
            while((ch = getchar()) != EOF)
                if(ch == '\n')
                    break;
        comp[toupper(ch)]++;
        }

    printf("%s ", label);
    for(i = 0; i < 256; i++)
        if(comp[i] && isprint(i))
            printf("%c %d ", i, comp[i]);
    printf("\n");
    return 0;
}
