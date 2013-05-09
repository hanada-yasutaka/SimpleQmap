# SimpleQmap

SimpleQmap is python calculator quantum chaotic map for an introduction.

SimpleQmapは与えられたq-表示ユニタリー行列の固有値問題，及び初期値問題を解きます．
量子写像入門としてプログラムは必要最小限のコードしか書いていません．
Note: 計算速度の問題のため，波動関数の伏見表示を求めるルーチンのみC言語で記述．

#### Requirements

You'll need a following package:

1. python2.6 or later
2. numpy
3. gcc (optional)
4. gnuplot(optioal)

#### first setting
To get the Husimi-representaion, type followin code

	cd SimpleQmap/
	bash make.sh

#### Example

	cd samples/
	bash master eigen # solve eigenvalue problem

or 

	bash master evolv # solve initial value probrem