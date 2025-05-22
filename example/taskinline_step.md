lesson_id: 1771198

## TASKINLINE Сложение двух чисел

Some condition text

CONFIG  
score: 7  
visible_tests: 1  
checker: text  
additional_params: param1

TEST  
1 2  
----  
3  
====

CODE  
int add(int a, int b) { return a + b; }

HEADER  
#include <stdio.h>

FOOTER  
return 0;