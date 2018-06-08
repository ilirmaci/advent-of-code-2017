#!/usr/bin/env scala

// setup inputs
val inputA = 679
val inputB = 771

val testA = 65
val testB = 8921

// constructor of iteration step for a generator
def get_next(factor: Int)(x: BigInt): BigInt = (x * factor) % 2147483647

// costruct iterator for both generators
def nextA(x: BigInt):BigInt = get_next(16807)(x)
def nextB(x: BigInt):BigInt = get_next(48271)(x)

// test iterator
nextA(1092455)       // expected 1181022009
nextB(1233683848)    // expected 1431495498

// stream constructor
def gen(next: BigInt => BigInt, start:BigInt): Stream[BigInt] = {
    val first_value = next(start)
    first_value #:: gen(next, first_value)
}

// comparison function, return one if there's a match
val last16bits = math.pow(2, 16).toInt
def judge_equal(tpl:(BigInt, BigInt)):Int = if ((tpl._1 % last16bits) == (tpl._2 % last16bits)) 1 else 0

// build generators
val genAtest = gen(nextA, testA)
val genBtest = gen(nextB, testB)

// count equals over 40m pairs, expected 588
// crashes with OOM error 
val num_pairs = 4e7.toInt
(genAtest zip genBtest) take(num_pairs) map(judge_equal) reduceLeft (_ + _)


/*******************
**  First puzzle  **
*******************/

// build generators
val genA = gen(nextA, inputA)
val genB = gen(nextB, inputB)

val first_solution = ((genA zip genB)
                        .take(num_pairs)
                        .map(judge_equal)
                        .sum)
             
print("The soluton to the first puzzle is " + first_solution.toString)


/********************
**  Second puzzle  **
********************/

// build test generators with filter
val genAtest = gen(nextA, testA) filter (_ % 4 == 0)
val genBtest = gen(nextB, testB) filter (_ % 8 == 0)
(genAtest zip genBtest) take 5 foreach println

// build generators
val genAfilter = gen(nextA, inputA) filter (_ % 4 == 0)
val genBfilter = gen(nextB, inputB) filter (_ % 8 == 0)

// this one also crashes with OOM error
val num_pairs = 5e6.toInt
val second_solution = ((genAfilter zip genBfilter)
                        .take(num_pairs)
                        .map(judge_equal)
                        .sum)
                        
print("The soluton to the second puzzle is " + second_solution.toString)


