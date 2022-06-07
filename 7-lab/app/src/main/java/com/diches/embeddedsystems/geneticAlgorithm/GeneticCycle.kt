package com.diches.embeddedsystems.geneticAlgorithm

import kotlin.math.floor

class GeneticCycle(
        private val result: Int,
        populationAmount: Int,
        private val coefs: List<Int>
) {
    private val population: Population

    init {
        val maxGenVal = floor(result.toFloat() / 2).toInt()
        population = Population(maxGenVal)
        population.generateInitial(populationAmount, coefs.size)
    }

    fun findSolution(): Pair<Long, List<Int>> {
        val startTime = System.currentTimeMillis()
        val timeLimit = 3000
        while (true) {
            val res = population.checkFitness(result, coefs)
            if (res != null)
                return Pair(System.currentTimeMillis() - startTime, res)
            val newPopulation = population.arrangeTournament()
            population.setNewPopulation(newPopulation)
            val endTime = System.currentTimeMillis() - startTime
            if (endTime > timeLimit)
                return Pair(endTime, List(coefs.size) { 0 })
        }
    }
}