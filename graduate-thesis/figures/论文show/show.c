/* Count the sum of elements in an array */
#include <stdio.h>

int main()
{
	int i = 0;//parameter one
	int data[5]={1,2,3,4,5};//parameter two
	int result = 0;//parameter three
	
	for(;i<5;i++)
	{
		result += data[i];
	}
	printf("%d",result); 
	return 0;
}

