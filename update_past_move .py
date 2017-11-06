{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 74,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "12\n",
      "0000000000000000000000000000000000000000000000000000000000000001\n"
     ]
    }
   ],
   "source": [
    "\n",
    "\n",
    "pastMoves=[]\n",
    "\n",
    "#_____________________________________________________________________________#\n",
    "#Update the pastMoves list by adding the current move to be done [to account for Fifty-Move Rule]\n",
    "#Update board , BlackBitBoard , WhiteBitBoard [to account for Threefold repetition draw rule]\n",
    "from bitstring import BitArray\n",
    "def updatePastMoves(move,WhiteBitBoard,blackbitboard,currentcolor): #(Sara) and (Safa)\n",
    "    pastMoves.append(move)\n",
    "    prev=int(move[0:2])\n",
    "    new=int(move[2:4])\n",
    "    \n",
    "    board[new]=board[prev]\n",
    "    board[prev]=-1\n",
    "    prev_p=(1<<abs(prev))\n",
    "    new_p=(prev_p<<abs(new-prev))\n",
    "    notprev_p=~prev_p\n",
    "    if(currentcolor=='w'):\n",
    "        WhiteBitBoard=new_p|WhiteBitBoard\n",
    "        WhiteBitBoard=notprev_p&WhiteBitBoard\n",
    "    else:\n",
    "        blackbitboard=new_p|blackbitboard\n",
    "        blackbitboard=notprev_p&blackbitboard\n",
    "   \n",
    "    print(WhiteBitBoard)\n",
    "\n",
    "updatePastMoves(\"0103\",6,'w') \n",
    "\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collecting bitstring\n",
      "  Downloading bitstring-3.1.5.zip (624kB)\n",
      "\u001b[K    100% |████████████████████████████████| 624kB 102kB/s ta 0:00:01\n",
      "\u001b[?25hBuilding wheels for collected packages: bitstring\n",
      "  Running setup.py bdist_wheel for bitstring ... \u001b[?25ldone\n",
      "\u001b[?25h  Stored in directory: /home/safaa/.cache/pip/wheels/e9/16/2c/89c3bc78c99908c74f8de29eaf8e75915dfd91b2323cef862a\n",
      "Successfully built bitstring\n",
      "Installing collected packages: bitstring\n",
      "Successfully installed bitstring-3.1.5\n"
     ]
    }
   ],
   "source": [
    "!pip install bitstring\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {
    "collapsed": true
   },
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.1"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
