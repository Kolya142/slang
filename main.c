
#include <stdio.h>
int main() {
unsigned char *msg="Hello, world!";
int value=0;
for (;;) {
if (value==5) {
break;
}
printf("%s",msg);
value++;
}
exit(0);
}