package com.diches.embeddedsystems

import android.content.Context
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import android.widget.Toast
import com.diches.embeddedsystems.geneticAlgorithm.GeneticCycle

class InputHandler(submitter: Button) {
    private lateinit var coefs: List<EditText>
    private lateinit var results: List<TextView>
    private lateinit var populationParameters: Pair<EditText, EditText>
    private lateinit var calcTimeField: TextView
    private lateinit var errorField: TextView
    private lateinit var context: Context

    init {
        submitter.setOnClickListener {
            handleSubmit()
        }
    }

    fun setContext(ctx: Context): InputHandler {
        context = ctx
        return this
    }

    fun setCoefs(fields: List<EditText>): InputHandler {
        coefs = fields
        return this
    }

    fun setResults(fields: List<TextView>): InputHandler {
        results = fields
        return this
    }

    fun setPopulationParams(fields: Pair<EditText, EditText>): InputHandler {
        populationParameters = fields
        return this
    }

    fun setTimeField(field: TextView): InputHandler {
        calcTimeField = field
        return this
    }

    fun setErrorField(field: TextView): InputHandler {
        errorField = field
        return this
    }

    private fun handleSubmit() {
        val (y, pop) = populationParameters
        val coefsNotEmpty = coefs.none { it.text.isEmpty() }
        if (!coefsNotEmpty || y.text.isEmpty() || pop.text.isEmpty()) {
            results.forEach { it.text = "" }
            calcTimeField.text = ""
            errorField.text = "Some of the input arguments aren't specified"
            return
        }

        errorField.text = ""
        val yVal = y.text.toString().toInt()
        val popVal = pop.text.toString().toInt()
        val coefsInt = coefs.map { it.text.toString().toInt() }
        val genCycle = GeneticCycle(yVal, popVal, coefsInt)
        val timeLimit = 3000
        val (elapsedTime, solution) = genCycle.findSolution()
        val outOfTime = timeLimit < elapsedTime
        results.forEachIndexed { index, textView ->
            textView.text = if (outOfTime) "" else "x$index = ${solution[index]}"
        }
        calcTimeField.text = "Time elapsed: $elapsedTime ms."

        if (outOfTime) {
            val msg = "Error: execution time more than 3 sec."
            Toast.makeText(context, msg, Toast.LENGTH_SHORT).show()
            errorField.text = "Solution wasn't found for 3 seconds"
        }
    }
}