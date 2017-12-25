#include "defs.h"

int PceListOk(const KASPAROV_BOARD *pos)
{
	int pce = wP;
	int sq;
	int num;
	for (pce = wP; pce <= bK; ++pce)
	{
		if (pos->pceNum[pce] < 0 || pos->pceNum[pce] >= 10)
			return FALSE;
	}

	if (pos->pceNum[wK] != 1 || pos->pceNum[bK] != 1)
		return FALSE;

	for (pce = wP; pce <= bK; ++pce)
	{
		for (num = 0; num < pos->pceNum[pce]; ++num)
		{
			sq = pos->pList[pce][num];
			if (!SqOnBoard(sq)) return FALSE;
		}
	}
	return TRUE;
}

int CheckBoard(const KASPAROV_BOARD *pos)
{
	int t_pceNum[13] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	int t_bigPce[2] = { 0, 0 };
	int t_majPce[2] = { 0, 0 };
	int t_minPce[2] = { 0, 0 };
	int t_material[2] = { 0, 0 };

	int sq64, t_piece, t_pce_num, sq120, colour, pcount;

	U64 t_pawns[3] = { 0ULL, 0ULL, 0ULL };

	t_pawns[WHITE] = pos->pawns[WHITE];
	t_pawns[BLACK] = pos->pawns[BLACK];
	t_pawns[BOTH] = pos->pawns[BOTH];

	// check piece lists
	for (t_piece = wP; t_piece <= bK; ++t_piece)
	{
		for (t_pce_num = 0; t_pce_num < pos->pceNum[t_piece]; ++t_pce_num)
		{
			sq120 = pos->pList[t_piece][t_pce_num];
			ASSERT(pos->pieces[sq120] == t_piece);
		}
	}

	// check piece count and other counters
	for (sq64 = 0; sq64 < 64; ++sq64)
	{
		sq120 = SQ120(sq64);
		t_piece = pos->pieces[sq120];
		t_pceNum[t_piece]++;
		colour = PieceCol[t_piece];
		if (PieceBig[t_piece] == TRUE)
			t_bigPce[colour]++;
		if (PieceMin[t_piece] == TRUE)
			t_minPce[colour]++;
		if (PieceMaj[t_piece] == TRUE)
			t_majPce[colour]++;

		t_material[colour] += PieceVal[t_piece];
	}

	for (t_piece = wP; t_piece <= bK; ++t_piece)
	{
		ASSERT(t_pceNum[t_piece] == pos->pceNum[t_piece]);
	}

	// check bitboards count
	pcount = CNT(t_pawns[WHITE]);
	ASSERT(pcount == pos->pceNum[wP]);
	pcount = CNT(t_pawns[BLACK]);
	ASSERT(pcount == pos->pceNum[bP]);
	pcount = CNT(t_pawns[BOTH]);
	ASSERT(pcount == (pos->pceNum[bP] + pos->pceNum[wP]));

	// check bitboards squares
	while (t_pawns[WHITE])
	{
		sq64 = POP(&t_pawns[WHITE]);
		ASSERT(pos->pieces[SQ120(sq64)] == wP);
	}

	while (t_pawns[BLACK])
	{
		sq64 = POP(&t_pawns[BLACK]);
		ASSERT(pos->pieces[SQ120(sq64)] == bP);
	}

	while (t_pawns[BOTH])
	{
		sq64 = POP(&t_pawns[BOTH]);
		ASSERT((pos->pieces[SQ120(sq64)] == bP) || (pos->pieces[SQ120(sq64)] == wP));
	}

	ASSERT(t_material[WHITE] == pos->material[WHITE] && t_material[BLACK] == pos->material[BLACK]);
	ASSERT(t_minPce[WHITE] == pos->minPce[WHITE] && t_minPce[BLACK] == pos->minPce[BLACK]);
	ASSERT(t_majPce[WHITE] == pos->majPce[WHITE] && t_majPce[BLACK] == pos->majPce[BLACK]);
	ASSERT(t_bigPce[WHITE] == pos->bigPce[WHITE] && t_bigPce[BLACK] == pos->bigPce[BLACK]);

	ASSERT(pos->side == WHITE || pos->side == BLACK);
	ASSERT(GeneratePosKey(pos) == pos->posKey);

	ASSERT(pos->enPas == NO_SQ || (RanksBrd[pos->enPas] == RANK_6 && pos->side == WHITE)
		|| (RanksBrd[pos->enPas] == RANK_3 && pos->side == BLACK));

	ASSERT(pos->pieces[pos->KingSq[WHITE]] == wK);
	ASSERT(pos->pieces[pos->KingSq[BLACK]] == bK);

	ASSERT(pos->castlePerm >= 0 && pos->castlePerm <= 15);

	ASSERT(PceListOk(pos));

	return TRUE;
}

void UpdateListsMaterial(KASPAROV_BOARD *pos)
{
	int piece, sq, index, colour;

	for (index = 0; index < BRD_SQ_NUM; ++index)
	{
		sq = index;
		piece = pos->pieces[index];
		ASSERT(PceValidEmptyOffbrd(piece));
		if (piece != OFFBOARD && piece != EMPTY)
		{
			colour = PieceCol[piece];
			ASSERT(SideValid(colour));

			if (PieceBig[piece] == TRUE)
				pos->bigPce[colour]++;
			if (PieceMin[piece] == TRUE)
				pos->minPce[colour]++;
			if (PieceMaj[piece] == TRUE)
				pos->majPce[colour]++;

			pos->material[colour] += PieceVal[piece];

			ASSERT(pos->pceNum[piece] < 10 && pos->pceNum[piece] >= 0);

			pos->pList[piece][pos->pceNum[piece]] = sq;
			pos->pceNum[piece]++;


			if (piece == wK)
				pos->KingSq[WHITE] = sq;
			if (piece == bK)
				pos->KingSq[BLACK] = sq;

			if (piece == wP)
			{
				SETBIT(pos->pawns[WHITE], SQ64(sq));
				SETBIT(pos->pawns[BOTH], SQ64(sq));
			}
			else if (piece == bP)
			{
				SETBIT(pos->pawns[BLACK], SQ64(sq));
				SETBIT(pos->pawns[BOTH], SQ64(sq));
			}
		}
	}
}

int ParseFen(char *fen, KASPAROV_BOARD *pos)
{
	ASSERT(fen != NULL);
	ASSERT(pos != NULL);

	int  rank = RANK_8;
	int  file = FILE_A;
	int  piece = 0;
	int  count = 0;
	int  sq64 = 0;
	int  sq120 = 0;

	ResetBoard(pos);

	while ((rank >= RANK_1) && *fen)
	{
		count = 1;
		switch (*fen) {
		case 'p': piece = bP; break;
		case 'r': piece = bR; break;
		case 'n': piece = bN; break;
		case 'b': piece = bB; break;
		case 'k': piece = bK; break;
		case 'q': piece = bQ; break;
		case 'P': piece = wP; break;
		case 'R': piece = wR; break;
		case 'N': piece = wN; break;
		case 'B': piece = wB; break;
		case 'K': piece = wK; break;
		case 'Q': piece = wQ; break;

		case '1':
		case '2':
		case '3':
		case '4':
		case '5':
		case '6':
		case '7':
		case '8':
			piece = EMPTY;
			count = *fen - '0';
			break;

		case '/':
		case ' ':
			rank--;
			file = FILE_A;
			fen++;
			continue;

		default:
			printf("FEN error \n");
			return -1;
		}

		for (int i = 0; i < count; i++)
		{
			sq64 = rank * 8 + file;
			sq120 = SQ120(sq64);
			if (piece != EMPTY) {
				pos->pieces[sq120] = piece;
			}
			file++;
		}
		fen++;
	}

	ASSERT(*fen == 'w' || *fen == 'b');

	pos->side = (*fen == 'w') ? WHITE : BLACK;
	fen += 2;

	for (int i = 0; i < 4; i++)
	{
		if (*fen == ' ')
		{
			break;
		}
		switch (*fen)
		{
		case 'K': pos->castlePerm |= WKCA; break;
		case 'Q': pos->castlePerm |= WQCA; break;
		case 'k': pos->castlePerm |= BKCA; break;
		case 'q': pos->castlePerm |= BQCA; break;
		default:	     break;
		}
		fen++;
	}
	fen++;

	ASSERT(pos->castlePerm >= 0 && pos->castlePerm <= 15);

	if (*fen != '-')
	{
		file = fen[0] - 'a';
		rank = fen[1] - '1';

		ASSERT(file >= FILE_A && file <= FILE_H);
		ASSERT(rank >= RANK_1 && rank <= RANK_8);

		pos->enPas = FR2SQ(file, rank);
	}

	fen += 2;
	char tmp1[3];
	for (int i = 0; i < 3; i++)
	{
		if (*fen == ' ')
		{
			tmp1[i]='\0';
			break;
		}
		tmp1[i] = *fen;
		fen++;
	}
	sscanf(tmp1, "%d", &pos->fiftyMove);
	fen++;

	char tmp2[3];
	for (int i = 0; i < 3; i++)
	{
		if (*fen == ' ')
		{
			tmp2[i] = '\0';
			break;
		}
		tmp2[i] = *fen;
		fen++;
	}

	sscanf(tmp2, "%d", &pos->hisPly);

	pos->posKey = GeneratePosKey(pos);

	UpdateListsMaterial(pos);

	return 0;
}

void ResetBoard(KASPAROV_BOARD *pos)
{
	int index = 0;

	for (index = 0; index < BRD_SQ_NUM; ++index)
	{
		pos->pieces[index] = OFFBOARD;
	}

	for (index = 0; index < 64; ++index)
	{
		pos->pieces[SQ120(index)] = EMPTY;
	}

	for (index = 0; index < 2; ++index)
	{
		pos->bigPce[index] = 0;
		pos->majPce[index] = 0;
		pos->minPce[index] = 0;
		pos->material[index] = 0;
	}

	for (index = 0; index < 3; ++index)
	{
		pos->pawns[index] = 0ULL;
	}

	for (index = 0; index < 13; ++index)
	{
		pos->pceNum[index] = 0;
	}

	pos->KingSq[WHITE] = pos->KingSq[BLACK] = NO_SQ;

	pos->side = BOTH;
	pos->enPas = NO_SQ;
	pos->fiftyMove = 0;

	pos->ply = 0;
	pos->hisPly = 0;

	pos->castlePerm = 0;

	pos->posKey = 0ULL;

}

void PrintBoard(const KASPAROV_BOARD *pos)
{
	int sq, file, rank, piece;

	printf("\nGame Board:\n\n");

	for (rank = RANK_8; rank >= RANK_1; rank--)
	{
		printf("%d  ", rank + 1);
		for (file = FILE_A; file <= FILE_H; file++)
		{
			sq = FR2SQ(file, rank);
			piece = pos->pieces[sq];
			printf("%3c", PceChar[piece]);
		}
		printf("\n");
	}

	printf("\n   ");
	for (file = FILE_A; file <= FILE_H; file++)
	{
		printf("%3c", 'a' + file);
	}
	printf("\n");
	printf("side:%c\n", SideChar[pos->side]);
	/*printf("enPas:%d\n",pos->enPas);
	printf("castle:%c%c%c%c\n",
			pos->castlePerm & WKCA ? 'K' : '-',
			pos->castlePerm & WQCA ? 'Q' : '-',
			pos->castlePerm & BKCA ? 'k' : '-',
			pos->castlePerm & BQCA ? 'q' : '-'
			);
	printf("PosKey:%llX\n",pos->posKey);*/
}

int ThreeFoldRep(const KASPAROV_BOARD *pos)
{
	ASSERT(CheckBoard(pos));

	int i = 0, r = 0;
	for (i = 0; i < pos->hisPly; ++i)
	{
		if (pos->history[i].posKey == pos->posKey)
		{
			r++;
		}
	}
	return r;
}

int DrawMaterial(const KASPAROV_BOARD *pos)
{
	ASSERT(CheckBoard(pos));

	if (pos->pceNum[wP] || pos->pceNum[bP])
		return FALSE;
	if (pos->pceNum[wQ] || pos->pceNum[bQ] || pos->pceNum[wR] || pos->pceNum[bR])
		return FALSE;
	if (pos->pceNum[wB] > 1 || pos->pceNum[bB] > 1)
	{
		return FALSE;
	}
	if (pos->pceNum[wN] > 1 || pos->pceNum[bN] > 1)
	{
		return FALSE;
	}
	if (pos->pceNum[wN] && pos->pceNum[wB])
	{
		return FALSE;
	}
	if (pos->pceNum[bN] && pos->pceNum[bB])
	{
		return FALSE;
	}

	return TRUE;
}

U64 GeneratePosKey(const KASPAROV_BOARD *pos)
{
	int sq = 0;
	U64 finalKey = 0;
	int piece = EMPTY;

	// pieces
	for (sq = 0; sq < BRD_SQ_NUM; ++sq)
	{
		piece = pos->pieces[sq];
		if (piece != NO_SQ && piece != EMPTY && piece != OFFBOARD)
		{
			ASSERT(piece >= wP && piece <= bK);
			finalKey ^= PieceKeys[piece][sq];
		}
	}

	if (pos->side == WHITE)
	{
		finalKey ^= SideKey;
	}

	if (pos->enPas != NO_SQ)
	{
		ASSERT(pos->enPas >= 0 && pos->enPas<BRD_SQ_NUM);
		ASSERT(SqOnBoard(pos->enPas));
		ASSERT(RanksBrd[pos->enPas] == RANK_3 || RanksBrd[pos->enPas] == RANK_6);
		finalKey ^= PieceKeys[EMPTY][pos->enPas];
	}

	ASSERT(pos->castlePerm >= 0 && pos->castlePerm <= 15);

	finalKey ^= CastleKeys[pos->castlePerm];

	return finalKey;
}

