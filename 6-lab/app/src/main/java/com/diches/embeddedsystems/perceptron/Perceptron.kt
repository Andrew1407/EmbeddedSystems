package com.diches.embeddedsystems.perceptron

class Perceptron(
        private val threshold: Int,
        private val learningRate: Float
) {
    private val dots: Map<Char, Dot> = mapOf(
            'A' to Dot(x = 0.0f, y = 6f),
            'B' to Dot(x = 1f, y = 5f),
            'C' to Dot(x = 3f, y = 3f, greaterThanCheck = false),
            'D' to Dot(x = 2f, y = 4f, greaterThanCheck = false)
    )
    private val weights = mutableListOf(0.0, 0.0)
    private var currentDot = 'A'

    fun calcWeights(iterationsDeadline: Int): WeightsResult {
        return runLearningCycle { i, _ -> i > iterationsDeadline }
    }

    fun calcWeights(timeDeadline: Float): WeightsResult {
        return runLearningCycle { _, time -> time > timeDeadline * 1000L }
    }

    private fun runLearningCycle(checkDeadline: (i: Int, time: Long) -> Boolean): WeightsResult {
        val startTime = System.currentTimeMillis()
        var iterations = 0
        while (true) {
            val iterationTime = System.currentTimeMillis() - startTime
            val deadlineMissed = checkDeadline(iterations, iterationTime)
            val isCorrect = checkResult()
            if (isCorrect || deadlineMissed) {
                currentDot = 'A'
                return WeightsResult(
                        values = weights.toList(),
                        iterations = iterations,
                        timeElapsed = iterationTime
                )
            }

            val dot = dots[currentDot]!!
            val y = dot.x * weights[0] + dot.y * weights[1]
            val delta = threshold - y
            weights[0] += delta * dot.x * learningRate
            weights[1] += delta * dot.y * learningRate
            changeCurrentDot()
            iterations++
        }
    }

    private fun changeCurrentDot() {
        currentDot = if (currentDot == 'D') 'A' else (currentDot.toInt() + 1).toChar()
    }

    private fun checkResult(): Boolean {
        for ((_, values) in dots) {
            val res = weights[0] * values.x + weights[1] * values.y
            val fits = if (values.greaterThanCheck) res > threshold else res < threshold
            if (!fits) return false
        }
        return true
    }

    private data class Dot(
            val x: Float,
            val y: Float,
            val greaterThanCheck: Boolean = true
    )
}
