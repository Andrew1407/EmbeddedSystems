package com.diches.embeddedsystems

import kotlin.math.ceil
import kotlin.math.pow
import kotlin.math.sqrt

fun FermaFunction(num: Long): Pair<Long, Pair<Long, Long>> {
    val startTime = System.currentTimeMillis()
    if (num % 2 == 0L) return Pair(System.currentTimeMillis() - startTime, Pair(0L, 0L))
    var x = ceil(sqrt(num.toDouble()))
    while (x.pow(2) > num) {
        val checkTime = System.currentTimeMillis() - startTime
        if (checkTime > 3000) return Pair(checkTime, Pair(-2, -2))
        val y = sqrt(x.pow(2) - num)
        if (y == y.toInt().toDouble()) {
            val a = (x + y).toLong()
            val b = (x - y).toLong()
            val resTime = System.currentTimeMillis() - startTime
            val resValues = if (a == 1L || b == 1L) Pair(-1L, -1L) else Pair(a, b)
            return Pair(resTime, resValues)
        }
        x++
    }

    return Pair(System.currentTimeMillis() - startTime, Pair(-1L, -1L))
}