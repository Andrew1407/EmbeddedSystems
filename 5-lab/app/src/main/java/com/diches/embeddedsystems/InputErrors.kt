package com.diches.embeddedsystems

enum class InputErrors(val msg: String) {
    IS_EMPTY("No value given"),
    NOT_FACTORIZED("The number cannot be factorized"),
    NOT_INT("The input should be integer type (positive)"),
    IS_EVEN("The given number is even (or zero), not odd one"),
    OUT_OF_TIME("Factorization was calculating more than 3 seconds")
}