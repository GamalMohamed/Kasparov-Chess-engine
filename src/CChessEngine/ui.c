#include "defs.h"

int CheckResult(KASPAROV_BOARD *pos, char** msg)
{
	ASSERT(CheckBoard(pos));

	if (pos->fiftyMove >= 100)
	{
		*msg = "FIFTY MOVE DRAW"; // "50MV"
		return TRUE;
	}

	if (ThreeFoldRep(pos) >= 3)
	{
		*msg = "3-FOLD REPITITION DRAW"; // "3FLD"
		return TRUE;
	}

	if (DrawMaterial(pos) == TRUE)
	{
		*msg = "INSUFFICIENT MATERIAL DRAW"; // "MATD"
		return TRUE;
	}

	S_MOVELIST list[1];
	GenerateAllMoves(pos, list);

	int found = 0;
	for (int MoveNum = 0; MoveNum < list->count; ++MoveNum)
	{

		if (!MakeMove(pos, list->moves[MoveNum].move))
		{
			continue;
		}
		found++;
		TakeMove(pos);
		break;
	}

	if (found != 0)
	{
		*msg = "OK"; // "OK00"
		return FALSE;
	}

	int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
	if (InCheck == TRUE)
	{
		if (pos->side == WHITE)
		{
			*msg = "BLACK MATES"; //"BLKM"
			return TRUE;
		}
		else
		{
			*msg = "WHITE MATES"; //"WHTM"
			return TRUE;
		}
	}
	else
	{
		*msg = "STALEMATE DRAW"; //"STLM"
		return TRUE;
	}
}

char* Game_Loop(KASPAROV_BOARD* pos, SEARCH_INFO* info)
{
	setbuf(stdin, NULL);
	setbuf(stdout, NULL);

	int depth = MAXDEPTH, movetime = 5000;
	int engine = 0;
	int move;
	char* msg = "";
	char inBuf[80], command[80];

	ParseFen(START_FEN, pos);

	while (TRUE)
	{
		fflush(stdout);

		// Agent consultation requested!
		if (engine == 1)
		{
			if (CheckResult(pos, &msg) == FALSE)
			{
				info->starttime = GetTimeMs();
				info->depth = depth;

				if (movetime != 0)
				{
					info->timeset = TRUE;
					info->stoptime = info->starttime + movetime;
				}

				printf("%s   %s\n", SearchPosition(pos, info), msg);
			}
			else
			{
				return msg;
			}
			engine = 0;
		}

		PrintBoard(pos);
		printf("\nEnter > ");

		// Allocate space for user input and wait for it!
		fflush(stdout);
		memset(&inBuf[0], 0, sizeof(inBuf));
		fflush(stdout);
		if (!fgets(inBuf, 80, stdin))
			continue;

		sscanf(inBuf, "%s", command);

		if (!strcmp(command, "consult"))
		{
			engine = 1;
			continue;
		}

		if (!strcmp(command, "setboard"))
		{
			ParseFen(inBuf + 9, pos);
			continue;
		}

		if (!strcmp(command, "quit"))
		{
			info->quit = TRUE;
			break;
		}

		move = ParseMove(inBuf, pos);
		if (move == NOMOVE)
		{
			printf("Command unknown or illegal move: %s\n", inBuf);
			continue;
		}

		MakeMove(pos, move);

		pos->ply = 0;
	}

	return "USER ENDED GAME";
}