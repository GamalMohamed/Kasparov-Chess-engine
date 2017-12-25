#include "defs.h"

int main(int argc, char *argv[])
{
	AllInit();

	KASPAROV_BOARD pos[1];
	SEARCH_INFO info[1];
	info->quit = FALSE;
	pos->HashTable->pTable = NULL;
	InitHashTable(pos->HashTable, 64);
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	Game_Loop(pos, info);

	free(pos->HashTable->pTable);
	CleanPolyBook();

	return 0;
}








