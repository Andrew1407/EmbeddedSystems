package com.diches.embeddedsystems.geneticAlgorithm

import kotlin.math.abs
import kotlin.math.ceil

class Population(private val maxGenValue: Int) {
    private var chroms: List<Chrom> = listOf()

    fun setNewPopulation(newPopulation: List<Chrom>) {
        chroms = newPopulation
    }

    fun generateInitial(populationAmount: Int, gensAmount: Int) {
        val initial = mutableListOf<Chrom>()
        val boundVal = if (maxGenValue == 0) 2 else maxGenValue
        val getRand = { (1..boundVal).random() }
        for (i in 0 until populationAmount) {
            val gens = mutableListOf<Int>()
            for (u in 0 until gensAmount) gens.add(getRand())
            initial.add(i, Chrom(gens = gens))
        }
        chroms = initial.toList()
    }

    fun checkFitness(result: Int, coefs: List<Int>): List<Int>? {
        val deltas = chroms.map {
            it.gens.mapIndexed { i, gen -> gen * coefs[i] }.sum()
        }.map { abs(result - it) }

        val fitsBestIndex = deltas.indexOf(0)
        if (fitsBestIndex != -1) {
            return chroms[fitsBestIndex].gens
        }

        calcProbabilities(deltas)
        return null
    }

    private fun calcProbabilities(deltas: List<Int>) {
        val deltasReversed = deltas.map { 1 / it.toDouble() }
        val reversedSum = deltasReversed.sum()
        deltasReversed.forEachIndexed { i, delta ->
            chroms[i].probability = delta / reversedSum
        }
    }

    fun arrangeTournament(): List<Chrom> = chroms.map { completeTour() }

    private fun completeTour(): Chrom {
        val firstParent = pickParent()
        var secondParent = firstParent
        while (firstParent == secondParent)
            secondParent = pickParent()

        val offspring = produceOffspring(firstParent, secondParent)
        mutate(offspring)
        return offspring
    }

    private fun pickParent(): Int {
        val tournamentSize = (2..chroms.size).random()
        val participants = mutableListOf<Int>()
        var i = tournamentSize
        while (i > 0) {
            val participant = chroms.indices.random()
            if (participants.indexOf(participant) == -1) {
                participants.add(participant)
                i--
            } else {
                continue
            }
        }

        var winner = participants[0]
        for (u in 1 until tournamentSize) {
            val participant =  participants[u]
            if (chroms[participant].probability > chroms[winner].probability)
                winner = participant
        }

        return winner
    }

    private fun produceOffspring(firstIdx: Int, secondIdx: Int): Chrom {
        val firstParent = chroms[firstIdx].gens
        val secondParent = chroms[secondIdx].gens
        val chromSize = firstParent.size
        val crossover = ceil(chromSize.toFloat() / 2).toInt()
        val offspringGens =  firstParent.slice(0 until crossover) +
                secondParent.slice(crossover until chromSize)
        return Chrom(gens = offspringGens.toMutableList())
    }

    private fun mutate(chrom: Chrom) {
        if ((0 until 100).random() > 10) return
        val mutation = listOf(-1, 1).random()
        val gen = (0 until chrom.gens.size).random()
        chrom.gens[gen] += mutation
    }
}