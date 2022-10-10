#include <stdio.h> 

int main(){ 
	int int1; 
	int T_1,T_2; 

	label_100: 
	label_101: int1 = 1;
	label_102: if(int1!=4) goto label_104;
	label_103: goto label_107;
	label_104: T_1 = int1+1;
	label_105: int1 = T_1;
	label_106: goto label_102;
	label_107: T_2 = int1-3;
	label_108: int1 = T_2;
	label_109: printf("%d\n", int1); 
	label_110: {}
	
}